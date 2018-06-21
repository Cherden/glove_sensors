from . import serial_dispatcher
from . import constants

GYRO_OFFSET = 512
GYRO_SCALE = 102.3


class Glove:
    def __init__(self):
        self.dispatcher = None
        self.serial_thread = None

        self.cb_touch = None
        self.cb_gyro = None

    def initialize(self):
        self.dispatcher = serial_dispatcher.SerialDispatcher()

        if self.cb_touch:
            self.dispatcher.append_callback(constants.SerialHeader.TOUCH, self.cb_touch)

        if self.cb_gyro:
            self.dispatcher.append_callback(constants.SerialHeader.GYRO, self.cb_gyro)

        serial_port = serial_dispatcher.get_serial_port()

        if (serial_port == False or
            self.dispatcher.initialize(serial_port, constants.SERIAL_BAUDRATE) == False):
            print("Failed to find serial port")
            return

        self.serial_thread = serial_dispatcher.SerialThread(self.dispatcher)
        self.serial_thread.start()

    def add_touch_callback(self, func):
        self.cb_touch = func

    def add_gyro_callback(self, func):
        self.cb_gyro = func

    @staticmethod
    def scale_gyro_values(values):
        ret = []
        for v in values:
            ret.append((v - GYRO_OFFSET) / GYRO_SCALE)

        return ret
