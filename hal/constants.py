from enum import Enum

SERIAL_VERSION = 1
SERIAL_BAUDRATE = 38400


class SerialHeader(Enum):
    DEBUG = 0
    TOUCH = 1
    GYRO = 2


class SerialDispatchError(Enum):
    NO_TERMINATION_BYTE = 1
    CHECKSUM_ERROR = 2
    VERSION_ERROR = 3
    CALLBACK_FUNCTION_NOT_EXISTENT = 4
