from dataclasses import dataclass


@dataclass
class LogStep:
    msg: str
    detail: dict = {}

    def __str__(self):
        return self.msg


class ExecutionLogMixin:
    task_info: dict = {}
    log_steps: list[LogStep] = []
    timing_steps: dict = {}

    def add_task_info(self, task_info: dict):
        self.task_info.update(task_info)

    def add_log_step(self, msg: str, detail: dict):
        self.log_steps.append(LogStep(msg, detail))

    def add_timing_step(self, data: dict):
        self.timing_steps.update(data)

    def get_execution_log_info(self):
        return {"task_info": self.task_info, "log_steps": self.log_steps, "timing_steps": self.timing_steps}

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        request.execution_log_info = self.get_execution_log_info()
        return response
