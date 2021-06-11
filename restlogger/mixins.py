from typing import Dict


class ExtraLogMixin:

    extra_log_info: Dict[dict, dict] = {}

    def add_extra_log_info(self, data: dict):
        self.extra_log_info.update(data)
