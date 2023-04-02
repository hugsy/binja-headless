from binaryninja import (
    log_info,
    log_debug,
    log_warn,
    log_error,
    BackgroundTaskThread,
)

from .constants import (
    DEBUG,
    SERVICE_NAME,
)


def expose(f):
    "Decorator to set exposed flag on a function."
    f.exposed = True
    return f


def is_exposed(f):
    "Test whether another function should be publicly exposed."
    return getattr(f, 'exposed', False)


def ishex(s):
    return s.lower().startswith("0x") and map(lambda c: c in "0123456789abcdef", s[2:].lower())


def info(x: str) -> None:
    log_info(f"[{SERVICE_NAME}] {x}")


def warn(x: str) -> None:
    log_warn(f"[{SERVICE_NAME}] {x}")


def err(x: str) -> None:
    log_error(f"[{SERVICE_NAME}] {x}")


def dbg(x: str) -> None:
    if DEBUG:
        log_debug(f"[{SERVICE_NAME}] {x}")


class RunInBackground(BackgroundTaskThread):
    def __init__(self, target, cancel_cb=None, *args, **kwargs):
        BackgroundTaskThread.__init__(self, '', cancel_cb is not None)
        self.target = target
        self.args = args
        self.kwargs = kwargs
        self.cancel_cb = cancel_cb
        return

    def run(self):
        self.target(self, *self.args, **self.kwargs)
        return

    def cancel(self):
        if self.cancel_cb:
            self.cancel_cb()
        return
