import serial
import time

arduino = None  # Don't open yet

def connect_to_arduino():
    global arduino
    
    if arduino is None or not arduino.is_open:
        
        arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
        time.sleep(2)  # Give time to reset
    else:
        print("DIDNT WORK")
time.sleep(2)  # Allow time for the Arduino to reset after connection

def get_answer():
    connect_to_arduino()
    arduino.reset_input_buffer()
    arduino.write(b'answer_time\n')
    # Wait for Arduino
    for i in range (0,30):
        time.sleep(0.3)
        # Read response
        if arduino.in_waiting > 0:
            data = arduino.readline().decode().strip()
            return data
    
    return None

def rightAnswer(player):
    connect_to_arduino()
    arduino.reset_input_buffer()
    arduino.write(f'win,{player}\n'.encode())  # Encode properly
    # Wait a little bit for Arduino
    time.sleep(0.2)

def wrongAnswer(player):
    connect_to_arduino()
    arduino.reset_input_buffer()
    arduino.write(f'lose,{player}\n'.encode())  # Encode properly
    time.sleep(0.2)


def close_connection():
    global arduino
    if arduino and arduino.is_open:
        arduino.close()
# For testing, let's try a simple communication test
# print("Sending 'answer_time' command...")
# data = get_answer()
# print(f"Received: {data}")

# # time.sleep(2)
# # print("Sending 'win,0' command...")
# # rightAnswer(data)

# # time.sleep(2)
# # print("Sending 'lose,1' command...")
# # wrongAnswer(data)
# # data = (int(data) + 1) % 2
# # time.sleep(2)
# # print("Sending 'lose,1' command...")
# wrongAnswer(data)