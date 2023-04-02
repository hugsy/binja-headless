"""


"""

import threading
import typing
import rpyc
import rpyc.utils.helpers
import rpyc.utils.server

import binaryninja

from .helpers import (
    info,
    err,
    dbg,
    warn,
)

from .constants import (
    HOST,
    PORT,
    SERVICE_NAME,
)

if typing.TYPE_CHECKING:
    import rpyc.core.protocol


g_ServiceThread = None
g_Server = None
__bv = None


class BinjaRpycService(rpyc.Service):
    ALIASES = ["binja", ]

    def __init__(self, bv):
        self.bv = bv
        return

    def on_connect(self, conn: rpyc.core.protocol.Connection):
        info("connect open: {}".format(conn,))
        return

    def on_disconnect(self, conn: rpyc.core.protocol.Connection):
        info("connection closed: {}".format(conn,))
        return

    exposed_binaryninja = binaryninja

    def exposed_bv(self):
        return self.bv

    def exposed_eval(self, cmd):
        return eval(cmd)


def is_service_started(view):
    global g_ServiceThread
    return g_ServiceThread is not None


def start_service(host: str, port: int, bv: binaryninja.BinaryView):
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
                protocol_config={'allow_public_attrs': True, }
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


def rpyc_start(bv):
    global g_ServiceThread
    dbg("Starting background service...")
    g_ServiceThread = threading.Thread(
        target=start_service, args=(HOST, PORT, bv))
    g_ServiceThread.daemon = True
    g_ServiceThread.start()
    binaryninja.show_message_box(
        SERVICE_NAME,
        "Service successfully started, you can use any RPyC client to connect to this instance of Binary Ninja",
        binaryninja.MessageBoxButtonSet.OKButtonSet,
        binaryninja.MessageBoxIcon.InformationIcon
    )
    return


def shutdown_service() -> bool:
    if not g_Server:
        warn("Service not started")
        return False
    try:
        dbg("Shutting down service")
        g_Server.close()
    except Exception as e:
        err(f"Exception: {str(e)}")
        return False
    return True


def stop_service() -> bool:
    """ Stopping the service """
    global g_ServiceThread
    if not g_ServiceThread:
        return False

    dbg("Stopping service thread")
    if shutdown_service():
        g_ServiceThread.join()
        g_ServiceThread = None
        info("Service thread stopped")
    return True


def rpyc_stop(bv: binaryninja.BinaryView):
    "Stopping background service... "
    if stop_service():
        binaryninja.show_message_box(
            SERVICE_NAME,
            "Service successfully stopped",
            binaryninja.MessageBoxButtonSet.OKButtonSet,
            binaryninja.MessageBoxIcon.InformationIcon
        )
    else:
        binaryninja.show_message_box(
            SERVICE_NAME,
            "An error occured while stopping the service, check logs",
            binaryninja.MessageBoxButtonSet.OKButtonSet,
            binaryninja.MessageBoxIcon.ErrorIcon
        )

    return
