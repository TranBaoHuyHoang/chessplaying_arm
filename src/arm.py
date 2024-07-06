#Code for Chess Robot Inverse Kinematics
import serial
from time import sleep
import time


class ChessRobotArm:
    def __init__(self, port='COM5') -> None:
        self.port = port
        self.ser = serial.Serial(port, 9600)
        print(f"Connected to Robot on port {port}")

    def command(self, value: str) -> None:
        time.sleep(2)
        self.ser.write(value.encode('utf-8'))
        print(f"Sent command: {value}")
        time.sleep(2)

    def move(self, value) -> None:
        self.command(value)