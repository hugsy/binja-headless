from binaryninja import (
    PluginCommand,
)

from .constants import SERVICE_NAME


from .server import (
    rpyc_start,
    rpyc_stop,
    is_service_started,
)


PluginCommand.register(
    f"{SERVICE_NAME}\\Start service",
    "Start the RPyC server",
    rpyc_start,
    is_valid=lambda view: not is_service_started(view)
)


PluginCommand.register(
    f"{SERVICE_NAME}\\Stop service",
    "Stop the RPyC server",
    rpyc_stop,
    is_valid=lambda view: is_service_started(view)
)
