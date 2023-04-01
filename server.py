"""


"""

import threading
import rpyc

import binaryninja

from .helpers import (
    info,
    err,
    dbg,
)

from .constants import (
    HOST,
    PORT,
)


__service_thread = None
__server = None
__bv = None


class BinjaRpycService(rpyc.Service):
    ALIASES = ["binja", ]

    def __init__(self, bv):
        self.bv = bv
        return

    def on_connect(self, conn):
        info("connect open: {}".format(conn,))
        return

    def on_disconnect(self, conn):
        info("connection closed: {}".format(conn,))
        return

    exposed_binaryninja = binaryninja

    def exposed_bv(self):
        return self.bv

    def exposed_eval(self, cmd):
        return eval(cmd)


def is_service_started(view):
    global __service_thread
    return __service_thread is not None


def start_service(host, port, bv):
    """Starting the RPyC server"""
    global __server, __bv
    __server = None
    __bv = bv

    for i in range(1):
        p = port + i
        try:
            service = rpyc.utils.helpers.classpartial(BinjaRpycService, bv)

            __server = rpyc.utils.server.ThreadedServer(
                service(),
                hostname=host,
                port=p,
                protocol_config={'allow_public_attrs': True, }
            )
            break
        except OSError as e:
            err("OSError: {}".format(e))
            __server = None

    if not __server:
        err("failed to start server...")
        return

    info("server successfully started")
    __server.start()
    return


def rpyc_start(bv):
    global __service_thread
    dbg("Starting background service...")
    __service_thread = threading.Thread(
        target=start_service, args=(HOST, PORT, bv))
    __service_thread.daemon = True
    __service_thread.start()
    binaryninja.show_message_box(
        "Binja-RPyC",
        "Service successfully started, you can use any RPyC client to connect to this instance of Binary Ninja",
        binaryninja.MessageBoxButtonSet.OKButtonSet,
        binaryninja.MessageBoxIcon.InformationIcon
    )
    return


def shutdown_service():
    try:
        info("shutting down service")
        __server.close()
    except Exception as e:
        err("Exception: {}".format(e))
        return False
    return True


def stop_service():
    """ Stopping the service """
    global __service_thread
    dbg("Trying to stop service thread")
    shutdown_service()
    __service_thread.join()
    __service_thread = None
    info("Server stopped")
    return True


def rpyc_stop(bv):
    "Stopping background service... "
    if stop_service():
        binaryninja.show_message_box(
            "Binja-RPyC",
            "Service successfully stopped",
            binaryninja.MessageBoxButtonSet.OKButtonSet,
            binaryninja.MessageBoxIcon.InformationIcon
        )
    return
