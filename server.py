""" """

import threading
import importlib
import rpyc
import rpyc.utils.helpers
import rpyc.utils.server

from typing import TYPE_CHECKING, Optional

import binaryninja  # type: ignore

from .helpers import (
    info,
    err,
    dbg,
)

from .constants import (
    DEFAULT_HOST_IP,
    DEFAULT_HOST_PORT,
    SERVICE_NAME,
    SETTING_AUTOSTART,
    SETTING_RPYC_HOST,
    SETTING_RPYC_PORT,
)

if TYPE_CHECKING:
    import rpyc.core.protocol


g_ServiceThread: Optional[threading.Thread] = None
g_Server: Optional[rpyc.utils.server.ThreadedServer] = None
__bv: Optional["binaryninja.binaryview.BinaryView"] = None


def register_settings() -> None:
    all_settings: dict[str, str] = {
        SETTING_AUTOSTART: f"""{{ "title" : "Auto Start", "description" : "Automatically start {SERVICE_NAME} when Binary Ninja opens", "type" : "boolean", "default" : false, "ignore" : ["SettingsProjectScope", "SettingsResourceScope"]}}""",
        SETTING_RPYC_HOST: f"""{{ "title" : "TCP Listen Host", "description" : "Interface {SERVICE_NAME} should listen", "type" : "string", "default" : "{DEFAULT_HOST_IP}", "ignore" : ["SettingsProjectScope", "SettingsResourceScope"]}}""",
        SETTING_RPYC_PORT: f"""{{ "title" : "TCP Listen Port", "description" : "TCP port {SERVICE_NAME} should listen", "type" : "number", "minValue": 1, "maxValue": 65535,  "default" : {DEFAULT_HOST_PORT}, "ignore" : ["SettingsProjectScope", "SettingsResourceScope"]}}""",
    }

    settings = binaryninja.Settings()
    if not settings.register_group(SERVICE_NAME, SERVICE_NAME):
        raise RuntimeWarning("Failed to register group setting")

    for name, value in all_settings.items():
        if not settings.register_setting(f"{SERVICE_NAME}.{name}", value):
            raise RuntimeWarning(f"Failed to register setting {name}")


class BinjaRpycService(rpyc.Service):
    ALIASES = [
        "binja",
    ]

    def __init__(self, bv):
        self.bv = bv
        return

    def on_connect(self, conn: rpyc.core.protocol.Connection):
        info(f"connect open: {conn}")
        return

    def on_disconnect(self, conn: rpyc.core.protocol.Connection):
        info(f"connection closed: {conn}")
        return

    exposed_binaryninja = binaryninja

    def exposed_bv(self):
        return self.bv

    def exposed_eval(self, cmd):
        return eval(cmd)
    
    def exposed_import_module(self, mod):
        return importlib.import_module(mod)


def is_service_started():
    global g_ServiceThread
    return g_ServiceThread is not None


def start_service(host: str, port: int, bv: binaryninja.binaryview.BinaryView) -> None:
    """Starting the RPyC server"""
    global g_Server, __bv
    g_Server = None
    __bv = bv

    for i in range(1):
        p: int = port + i
        try:
            service = rpyc.utils.helpers.classpartial(BinjaRpycService, bv)

            g_Server = rpyc.utils.server.ThreadedServer(
                service(),
                hostname=host,
                port=p,
                protocol_config={
                    "allow_public_attrs": True,
                },
            )
            break
        except OSError as e:
            err(f"OSError: {str(e)}")
            g_Server = None

    if not g_Server:
        err("failed to start server...")
        return

    info("server successfully started")
    g_Server.start()
    return


def rpyc_start(bv: Optional[binaryninja.binaryview.BinaryView] = None) -> None:
    global g_ServiceThread
    dbg("Starting background service...")
    settings = binaryninja.Settings()
    host: str = settings.get_string(f"{SERVICE_NAME}.{SETTING_RPYC_HOST}")
    port: int = settings.get_integer(f"{SERVICE_NAME}.{SETTING_RPYC_PORT}")

    g_ServiceThread = threading.Thread(target=start_service, args=(host, port, bv))
    g_ServiceThread.daemon = True
    g_ServiceThread.start()
    info(f"{SERVICE_NAME} successfully started in background")
    # binaryninja.show_message_box(
    #     SERVICE_NAME,
    #     "Service successfully started, you can use any RPyC client to connect to this instance of Binary Ninja",
    #     binaryninja.MessageBoxButtonSet.OKButtonSet,
    #     binaryninja.MessageBoxIcon.InformationIcon,
    # )
    return


def shutdown_service() -> bool:
    if g_Server is None:
        err("Server is not running (Service not started?)")
        return False

    try:
        dbg("Shutting down service")
        g_Server.close()
        info("Service successfully shutdown")
    except Exception as e:
        err(f"Exception: {str(e)}")
        return False
    return True


def stop_service() -> bool:
    """Stopping the service"""
    global g_ServiceThread
    if g_ServiceThread is None:
        err("Thread is None (Service not started?)")
        return False

    dbg("Stopping service thread")
    if shutdown_service():
        g_ServiceThread.join()
        g_ServiceThread = None
        info("Service thread stopped")
    else:
        err("Error while shutting down service")
        return False
    return True


def rpyc_stop(bv: binaryninja.BinaryView):
    "Stopping background service..."
    if not stop_service():
        # binaryninja.show_message_box(
        #     SERVICE_NAME,
        #     "Service successfully stopped",
        #     binaryninja.MessageBoxButtonSet.OKButtonSet,
        #     binaryninja.MessageBoxIcon.InformationIcon,
        # )
        # else:
        binaryninja.show_message_box(
            SERVICE_NAME,
            "An error occured while stopping the service, check logs",
            binaryninja.MessageBoxButtonSet.OKButtonSet,
            binaryninja.MessageBoxIcon.ErrorIcon,
        )

    return
