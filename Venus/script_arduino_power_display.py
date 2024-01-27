# ---------- ---------- [Configuration] ---------- ---------- #
serial_port = "/dev/ttyUSB0"
serial_rate = 9600

installation_id = 0
api_token = ""
start_timestamp = 1703980800 #(https://www.epochconverter.com/)
kwh_from_offset = 0
kwh_to_offset = 0
# ---------- ---------- [Configuration] ---------- ---------- #

try:
  import gobject  # Python 2.x
except:
  from gi.repository import GLib as gobject # Python 3.x
from operator import truediv, truth
from pickle import FALSE
import platform
import logging
from re import I
import time
import sys
import json
import os
import subprocess
import shlex
from threading import Thread
import serial,serial.tools.list_ports
import dbus
sys.path.insert(1, os.path.join(os.path.dirname(__file__), '/opt/victronenergy/dbus-modem'))
from vedbus import VeDbusService, VeDbusItemExport, VeDbusItemImport
import random
import requests
import math
from dbusmonitor import DbusMonitor

dbusObjects = {}

class DbusService:
    def __init__(self):
        self.serial = None
        self.kwh_from_grid = None
        self.kwh_to_grid = None
        self.power = None
        self.serial = None

        self.thread_api = Thread(target=self._update_api)

        self.dbusConn = dbus.SystemBus()

        self.serial_connect()
        self._update_api_thread()
        gobject.timeout_add(150000, self._update_api_thread)
        gobject.timeout_add(1000, self._update_display)

    def _update_api_thread(self):
      if (self.thread_api.is_alive() == False):
        self.thread_api = Thread(target=self._update_api)
        self.thread_api.start()
      return True
    
    def serial_connect(self):
        print("Connecting to serial (" + serial_port + "," + str(serial_rate) + ")")
        if self.serial is None:
          try:
            self.serial=serial.Serial(serial_port, serial_rate, timeout=0.01)
            subprocess.call(shlex.split('/opt/victronenergy/serial-starter/stop-tty.sh ' + serial_port)) #tell venusos to not read this serial port
            print("Serial connected")
          except Exception as error:
            print("Serial port doesn't exist" + str(error))

    def _update_api(self):
      headers = {'x-authorization': 'Token ' + api_token}
      data_api = requests.get("https://vrmapi.victronenergy.com/v2/installations/" + str(installation_id) + "/stats?interval=years&start=" + str(start_timestamp), headers=headers, verify=False, timeout=15)
      json_api = json.loads(data_api.text)

      self.kwh_from_grid = float(json_api["totals"]["grid_history_from"]) + kwh_from_offset
      self.kwh_to_grid = float(json_api["totals"]["grid_history_to"]) + kwh_to_offset
      return True

    def _update_display(self):
      if VeDbusItemImport(self.dbusConn, 'com.victronenergy.system', '/Ac/ActiveIn/L1/Power').get_value() == None:
        self.power = 0
      else:
        self.power = float(VeDbusItemImport(self.dbusConn, 'com.victronenergy.system', '/Ac/ActiveIn/L1/Power').get_value())
      if self.kwh_from_grid != None and self.kwh_to_grid != None and self.power != None:
        self.serial.write(bytes(str(round(self.kwh_from_grid, 1)), encoding='utf8') + b";" + bytes(str(round(self.kwh_to_grid, 1)), encoding='utf8') + b";" + bytes(str(math.floor(self.power)), encoding='utf8') + b"W")
        print("------------------------------")
        print("From: " + str(round(self.kwh_from_grid, 1)) + "kWh")
        print("Power: " + str(math.floor(self.power)) + "W" )
        print("To: " + str(round(self.kwh_to_grid, 1)) + "kWh")
        print("------------------------------")
      return True



def main():
  from dbus.mainloop.glib import DBusGMainLoop
  DBusGMainLoop(set_as_default=True)
  DbusService()
    
  mainloop = gobject.MainLoop()
  mainloop.run()



if __name__ == "__main__":
    main()
