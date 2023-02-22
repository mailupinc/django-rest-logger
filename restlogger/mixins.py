import datetime
from dataclasses import asdict, dataclass, field
from typing import Optional

from django.utils import timezone


@dataclass
class LogStep:
    """DataClass to represent a single Log Step"""

    msg: str
    detail: dict = field(default_factory=dict)

    def __str__(self):
        return self.msg


@dataclass
class TimingStep:
    """DataClass to represent a single Timing Step"""

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
    """
    Mixin to be used both with Django Views or DjangoRestFramework APIViews and their derivates
    It must be placed as the first mixin in the chain, as it overrides the dispatch() method,
    leveraging the MRO.

    Example:

        class MyView(ExecutionLogMixin, GenericAPIView):
            ...

    """

    task_info: dict
    log_steps: list[LogStep]
    timing_steps: dict[str, TimingStep]

    def __init__(self):
        self.task_info = {}
        self.log_steps = []
        self.timing_steps = {}

    def add_task_info(self, task_info: dict):
        """Update the task_info class attribute with the given data"""
        self.task_info.update(task_info)

    def add_log_step(self, msg: str, detail: Optional[dict] = None):
        """Append a LogStep to the log_steps class attribute"""
        if not detail:
            detail = {}
        self.log_steps.append(LogStep(msg, detail))

    def get_log_steps(self) -> list:
        """Return a list of serialized LogSteps stored in the log_steps class attribute"""
        return [asdict(step) for step in self.log_steps]

    def start_timing_step(self, name: str):
        """Starts a timing step with the given name"""
        self.timing_steps[name] = TimingStep()

    def stop_timing_step(self, name: str):
        """Stops a timing step with the given name, if any"""
        if timing_step := self.timing_steps.get(name):
            timing_step.end = timezone.now()

    def get_timing_steps(self) -> dict:
        """Returns all TimingSteps stored in the timing_steps class attribute, except the null ones"""
        return {
            name: timing_step.total.total_seconds()
            for name, timing_step in self.timing_steps.items()
            if timing_step.total
        }

    def get_execution_log_info(self) -> dict:
        """Returns an object with task_info, log_steps and timing_steps stored in class attributes"""
        return {
            "task_info": self.task_info,
            "log_steps": self.get_log_steps(),
            "timing_steps": self.get_timing_steps(),
        }

    def dispatch(self, request, *args, **kwargs):
        """Calls the parent dispatch(), and appends execution_log_info to the request"""
        response = super().dispatch(request, *args, **kwargs)
        request.execution_log_info = self.get_execution_log_info()
        return response
