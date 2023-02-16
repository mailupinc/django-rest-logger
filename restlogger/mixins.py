import datetime
from dataclasses import asdict, dataclass, field
from typing import Optional

from django.utils import timezone


@dataclass
class LogStep:
    msg: str
    detail: dict = field(default_factory=dict)

    def __str__(self):
        return self.msg


@dataclass
class TimingStep:
    start: Optional[datetime.datetime] = None
    end: Optional[datetime.datetime] = None

    def __post_init__(self):
        self.start = timezone.now()

    @property
    def total(self) -> datetime.timedelta:
        if self.end is not None:
            return self.end - self.start  # type: ignore
        else:
            return datetime.timedelta(0)


class ExecutionLogMixin:
    task_info: dict
    log_steps: list[LogStep]
    timing_steps: dict[str, TimingStep]

    def __init__(self):
        self.task_info = {}
        self.log_steps = []
        self.timing_steps = {}

    def add_task_info(self, task_info: dict):
        self.task_info.update(task_info)

    def add_log_step(self, msg: str, detail: Optional[dict] = None):
        if not detail:
            detail = {}
        self.log_steps.append(LogStep(msg, detail))

    def get_log_steps(self):
        return [asdict(step) for step in self.log_steps]

    def start_timing_step(self, name: str):
        self.timing_steps[name] = TimingStep()

    def stop_timing_step(self, name: str):
        if timing_step := self.timing_steps.get(name):
            timing_step.end = timezone.now()

    def get_timing_steps(self) -> dict:
        return {
            name: timing_step.total.total_seconds()
            for name, timing_step in self.timing_steps.items()
            if timing_step.total
        }

    def get_execution_log_info(self) -> dict:
        return {
            "task_info": self.task_info,
            "log_steps": self.get_log_steps(),
            "timing_steps": self.get_timing_steps(),
        }

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        request.execution_log_info = self.get_execution_log_info()
        return response
