"""
Author: Mason McKeen
csse120 Final Project
"""

import time

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class MyDelegate(object):
    def __init__(self):
        self.running = True

def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    title = 'Super Fast Vroom Cars'

    normal_speed = 400

    gui(root)
    driving(root, mqtt_client, normal_speed)


def driving(root, mqtt_client, current_speed):
    root.bind('<Up>', lambda event: forward_callback(mqtt_client, current_speed, current_speed))
    root.bind('<Down>', lambda event: back_callback(mqtt_client))
    root.bind('<Left>', lambda event: left_callback(mqtt_client, current_speed, current_speed))
    root.bind('<Right>', lambda event: right_callback(mqtt_client, current_speed, current_speed))
    root.bind('<space>', lambda event: boost_callback(mqtt_client))


def forward_callback(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message("drive", [left_speed, right_speed])


def left_callback(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message("turn_left", [left_speed, right_speed])


def stop_callback(mqtt_client):
    mqtt_client.send_message("stop_bot")


def right_callback(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message("turn_right", [left_speed, right_speed])


def back_callback(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message("back", [left_speed, right_speed])


def boost_callback(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message("boost", [left_speed, right_speed])


def gui(root):
    start_frame = ttk.Frame(root, padding=0)
    start_frame.grid()