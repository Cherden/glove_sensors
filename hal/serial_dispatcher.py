import serial
import time
import os
import threading

from . import crc16
from . import constants

SERIAL_READ_START = 0xAF
SERIAL_READ_END = 0xFE
SERIAL_SEND_START = 0xDE
SERIAL_SEND_END = 0xED


def get_serial_port():
    output = os.popen("""ls /dev/ | egrep 'wchusbserial|ttyUSB'""").read()

    output_lines = output.splitlines()

    output_lines.sort()

    if len(output_lines) > 0:
        return "/dev/" + output_lines[-1]
    else:
        return False


class SerialThread(threading.Thread):
    def __init__(self, serial):
        threading.Thread.__init__(self)
        self.daemon = True

        self.ser_dispatcher = serial

    def run(self):
        while True:
            self.ser_dispatcher.dispatch()


class SerialDispatcher():
    def __init__(self):
        self.callback_list = {}
        self.interval_list = {}
        self.initialized = False
        self.ser_con = None

    def initialize(self, port, baudrate):
        self.ser_con = serial.Serial()

        self.ser_con.port = port
        self.ser_con.baudrate = baudrate
        self.ser_con.timeout = None

        try:
            self.ser_con.open()
        except serial.SerialException:
            return False

        self.ser_con.flushOutput()
        self.ser_con.flushInput()

        time.sleep(2)

        self.initialized = True

        return True

    def append_callback(self, idx, cb):
        if self.initialized:
            print("Can not append callback function when already initialized")
            return False
        else:
            self.callback_list[idx.value] = cb

            return True

    def __read_byte(self):
        return ord(self.ser_con.read())

    def dispatch(self):
        # Read until start sequence occurs
        while self.__read_byte() != SERIAL_READ_START:
            time.sleep(0.01)

        buffer = []
        # Version
        buffer.append(self.__read_byte())
        # Type
        buffer.append(self.__read_byte())
        # Length
        buffer.append(self.__read_byte())

        # Payload
        for i in range(buffer[2]):
            buffer.append(self.__read_byte())

        # CRC Checksum
        crc1 = self.__read_byte()
        crc2 = self.__read_byte()
        crc = (crc2 << 8) | crc1

        last_byte = self.__read_byte()
        if last_byte != SERIAL_READ_END:
            return constants.SerialDispatchError.NO_TERMINATION_BYTE

        crc_t = crc16.crc16_ccitt(buffer, buffer[2] + 3)
        if crc != crc_t:
            return constants.SerialDispatchError.CHECKSUM_ERROR

        if buffer[0] != constants.SERIAL_VERSION:
            return constants.SerialDispatchError.VERSION_ERROR

        payload = []
        for i in range(3, len(buffer), 2):
            payload.append((buffer[i + 1] << 8) | buffer[i])

        if buffer[1] in self.callback_list:
            self.callback_list[buffer[1]](payload)
