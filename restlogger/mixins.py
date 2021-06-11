class ExtraLogMixin:

    extra_log_info = {}

    def add_extra_log_info(self, data: dict):
        self.extra_log_info.update(data)
