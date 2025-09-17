'''
Author: pcs3rd
Description: This starts scavresh.
'''
import threading
from sys import path as spath
from os import opath
from pubsub import pub
from datetime import datetime
path = opath.dirname(opath.realpath(__file__)) + '/sysmods'
if not path in spath:
    spath.insert(1, path)
del path


import meshtastic.serial_interface #pip install meshtastic or use launch.sh for venv
import meshtastic.tcp_interface
import meshtastic.ble_interface
import time
import asyncio
import random
import contextlib # for suppressing output on watchdog
import io # for suppressing output on watchdogghrtp[;]

import meshtastic
import meshtastic.serial_interface

from interpret import

db_name = "scav.db"
opath.isfile(db_name)
scavresh_database = dataStore.session("scav.db")
match dataStore.read_setting(scavresh_database, ):
    case "ble":
        pass
    case "serial":
        pass
    case "tcp":
        pass
    

def onReceive(packet, interface): # called when a packet arrives
    print(f"Meshtastic radio recieved packet: {packet}")


    

def onConnection(interface, topic=pub.AUTO_TOPIC): # called when we (re)connect to the radio
    # defaults to broadcast, specify a destination ID if you wish
    interface.sendText("hello mesh")

pub.subscribe(onReceive, "meshtastic.receive")
pub.subscribe(onConnection, "meshtastic.connection.established")
# By default will try to find a meshtastic device, otherwise provide a device path like /dev/ttyUSB0
interface = meshtastic.serial_interface.SerialInterface()