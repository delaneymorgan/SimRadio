#!/usr/bin/env python
# coding=utf-8

import argparse
import json
import signal
import sys

from web_service import WebService
from sim_radio import SimRadio
from model import Model

__version__ = "20241122-1"

g_running_flag = True

def signal_handler(raised_signal, frame):
    """
    handle SIGINT or other "quit" signals
    :param raised_signal: the raised signal
    :param frame: ???
    :return: Nothing
    """
    global g_running_flag
    _ = frame
    if raised_signal == signal.SIGINT:
        g_running_flag = False
        sys.exit(0)
    return


def arg_parser():
    """
    parse arguments
    :return: the parsed arguments
    """
    parser = argparse.ArgumentParser(description='SimRadio - Simple AECM Radio Simulator via SNMP.')
    parser.add_argument("-v", "--verbose", help="verbose mode", action="store_true")
    parser.add_argument("-d", "--debug", help="debug mode (includes verbose mode)", action="store_true")
    parser.add_argument("-p", "--port", help="port#", type=int, default=12345)
    parser.add_argument("--version", action="version", version='%(prog)s {version}'.format(version=__version__))
    args = parser.parse_args()
    return args


def main():
    args = arg_parser()
    signal.signal(signal.SIGINT, signal_handler)
    model = Model(args)
    service = WebService("SimRadio", model)
    sim_radio = SimRadio(args, model)
    sim_radio.run()
    return


if __name__ == "__main__":
    main()
