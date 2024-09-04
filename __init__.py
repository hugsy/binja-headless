from binaryninja import (  # type: ignore
    PluginCommand,
    Settings,
)

from .constants import SERVICE_NAME, SETTING_AUTOSTART


from .server import (
    register_settings,
    rpyc_start,
    rpyc_stop,
    is_service_started,
)


if not Settings().contains(f"{SERVICE_NAME}.{SETTING_AUTOSTART}"):
    register_settings()

if Settings().get_bool(f"{SERVICE_NAME}.{SETTING_AUTOSTART}"):
    rpyc_start()

PluginCommand.register(
    f"{SERVICE_NAME}\\Start service",
    "Start the RPyC server",
    rpyc_start,
    is_valid=lambda _: not is_service_started(),
)


PluginCommand.register(
    f"{SERVICE_NAME}\\Stop service",
    "Stop the RPyC server",
    rpyc_stop,
    is_valid=lambda _: is_service_started(),
)
