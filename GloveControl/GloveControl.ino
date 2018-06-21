#include "crc16.h"

#define VERSION                 1

#define SERIAL_BAUDRATE         38400

#define INDEX_FINGER_PIN        7
#define MIDDLE_FINGER_PIN       4
#define RING_FINGER_PIN         3
#define PINKY_FINGER_PIN        2

#define GYRO_X_PIN              A3
#define GYRO_Y_PIN              A5
#define GYRO_Z_PIN              A4

#define SERIAL_SEND_START       0xAF
#define SERIAL_SEND_END         0xFE

#define SERIAL_READ_START       0xDE
#define SERIAL_READ_END         0xED

#define CRC16MASK               0x8005

enum Header{
    DEBUG,
    TOUCH,
    GYRO,
    HEADER_END
};

enum DebugMessages{
	CONFIG_OK = 1,
	CONFIG_NO_START_SYMBOL,
	CONFIG_NO_END_SYMBOL,
	CONFIG_WRONG_VERSION,
	CONFIG_CRC_ERROR
};


/**
 * Send data over serial interface
 * Protocol:
 *        8            8         8            8        n * 16        16         8
 *    |--0xAF--|--Version--|--Type--|--Length--|--Payload--|--CRC--|--0xFE--|
 *
 * Fields with a length of over 8 bits send their data LSB first
 */
void sendData(Header h, char len, uint16_t* payload){
    char buf[255] = {0};
    int i = 0;
    int j = 0;

    buf[0] = VERSION;
    buf[1] = (char) h;
    buf[2] = len*2;
    for (i = 0, j = 0; i < len; i++, j = j + 2){
        uint16_t temp = payload[i];

        buf[3 + j    ] = (uint8_t) (temp & 0xFF);
        buf[3 + j + 1] = (uint8_t) (temp >> 8);
    }

    uint16_t crc = crc16_ccitt(buf, len*2+3);

#ifndef TEST_MODE
    Serial.write(SERIAL_SEND_START);

    Serial.write(buf, len*2+3);

    Serial.write((char) (crc & 0xFF));
    Serial.write((char) (crc >> 8));

    Serial.write(SERIAL_SEND_END);
#else
    Serial::write(SERIAL_SEND_START);


    Serial::write(buf, len*2+3);

    Serial::write((char) (crc & 0xFF));
    Serial::write((char) (crc >> 8));

    Serial::write(SERIAL_SEND_END);
#endif
}

/***********************************************************
 * Touch Sensor
 ***********************************************************/

void getTouch(uint16_t* touch_out){
#ifdef TEST_MODE
    cout << "\n****In getTouch()" << endl;
#endif

    // Read digital values on pins and encode in char
    touch_out[0] = (uint16_t) digitalRead(INDEX_FINGER_PIN);
    touch_out[1] = (uint16_t) digitalRead(MIDDLE_FINGER_PIN);
    touch_out[2] = (uint16_t) digitalRead(RING_FINGER_PIN);
    touch_out[3] = (uint16_t) digitalRead(PINKY_FINGER_PIN);

#ifdef TEST_MODE
    cout << "****Leaving getTouch()\n" << endl;
#endif
}

/***********************************************************
 * Gyro Sensor
 ***********************************************************/

void getGyro(uint16_t* gyro_out){
#ifdef TEST_MODE
    cout << "\n****In getGyro()" << endl;
#endif

    gyro_out[0] = (uint16_t) analogRead(GYRO_X_PIN);
    gyro_out[1] = (uint16_t) analogRead(GYRO_Y_PIN);
    gyro_out[2] = (uint16_t) analogRead(GYRO_Z_PIN);

#ifdef TEST_MODE
    cout << "****Leaving getGyro()\n" << endl;
#endif
}

/*
 * Arduino Setup
 * Configure serial channel to PI and initialize pins.
 */
void setup(){
#ifdef TEST_MODE
    cout << "\n****In setup()" << endl;
    Serial::begin(SERIAL_BAUDRATE);
#else
    Serial.begin(SERIAL_BAUDRATE);
    while(!Serial);
#endif

    pinMode(INDEX_FINGER_PIN, INPUT);
    pinMode(MIDDLE_FINGER_PIN, INPUT);
    pinMode(RING_FINGER_PIN, INPUT);
    pinMode(PINKY_FINGER_PIN, INPUT);

    pinMode(GYRO_X_PIN, INPUT);
    pinMode(GYRO_Y_PIN, INPUT);
    pinMode(GYRO_Z_PIN, INPUT);

#ifdef TEST_MODE
    cout << "****Leaving setup()\n" << endl;
#endif
}

/*
 * Arduino Loop
 * Read and send sensor values.
 */
void loop(){
    uint16_t touch_values[4] = {0};
    uint16_t gyro_values[3] = {0};
    
    getTouch(touch_values);
    sendData(TOUCH, 4, touch_values);

    getGyro(gyro_values);
    sendData(GYRO, 3, gyro_values);

    delay(100);
}
