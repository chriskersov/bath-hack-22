import serial
import time

arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=1)

def get_answer():
    arduino.reset_input_buffer()
    arduino.write(b'answer_time\n')

    # Wait for Arduino
    time.sleep(3)

    # Read response
    if arduino.in_waiting > 0:
        data = arduino.readline().decode().strip()
        return data
    else:
        return "error, no response from Arduino"


def rightAnswer(player):
    arduino.reset_input_buffer()
    arduino.write(f'win,{player}\n')
    # Wait a little bit for Arduino
    time.sleep(0.2)

def wrongAnswer(player):
    player = (player + 1) % 2
    arduino.reset_input_buffer()
    arduino.write(f'lose,{player}\n')
    # Wait a little bit for Arduino
    time.sleep(0.2)