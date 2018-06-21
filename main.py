from hal import glove 
import time


def touch_callback(data):
    print('Touch Data: ' + str(data))


def gyro_callback(data):
    scaled_data = glove.Glove.scale_gyro_values(data)
    print('Gyro Data: ' + str(scaled_data))


def __main():
    g = glove.Glove()
    g.add_touch_callback(touch_callback)
    g.add_gyro_callback(gyro_callback)

    g.initialize()

    time.sleep(100)


if __name__ == "__main__":
    __main()
