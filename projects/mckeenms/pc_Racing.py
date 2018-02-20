"""
Author: Mason McKeen
csse120 Final Project
"""

import time

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as mqtt


class MyDelegate(object):
    def __init__(self):
        self.running = True

def main():
    my_delegate = MyDelegate()
    mqtt_client = mqtt.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title = 'Super Fast Vroom Cars'

    normal_speed = 400
    turn_speed = normal_speed / 2
    boost_speed = normal_speed * 2
    current_speed = normal_speed
    drive(mqtt_client, normal_speed)

def drive(mqtt_client, motor_speed):
    drive_window = tkinter.Toplevel()

    drive_window.bind('<Up>', lambda event: forward_callback(mqtt_client, motor_speed, motor_speed))
    drive_window.bind('<Down>', lambda event: brake_callback(mqtt_client))
    drive_window.bind('<Left>', lambda event: left_callback(mqtt_client, motor_speed, motor_speed))
    drive_window.bind('<Right>', lambda event: right_callback(mqtt_client, motor_speed, motor_speed))
    drive_window.bind('<space>', lambda event: boost_callback(mqtt_client))


def forward_callback(mqtt_client, right_speed, left_speed):


def brake_callback(mqtt_client):
    ''

def right_callback(mqtt_client, right_speed, left_speed):
    ''


def left_callback(mqtt_client, right_speed, left_speed):
    ''


def boost_callback(mqtt_client, current_speed):
    ''