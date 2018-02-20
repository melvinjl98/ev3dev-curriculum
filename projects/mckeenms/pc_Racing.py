"""
Author: Mason McKeen
csse120 Final Project
For this project, I decided to go with an arcade-style
racer. the goal is to collect boost, dodge oil slicks
and to cross the finish line. Boosts obviously make you
faster but oil will spin you out and take away your speed.
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
    root.title = 'Super Fast Vroom Cars'

    normal_speed = 400

    driving(root, mqtt_client, normal_speed)

    root.mainloop()

def driving(root, mqtt_client, current_speed):
    root.bind('<Up>', lambda event: forward_callback(mqtt_client, current_speed, current_speed))
    root.bind('<Down>', lambda event: stop_callback(mqtt_client))
    root.bind('<Left>', lambda event: left_callback(mqtt_client, current_speed, current_speed))
    root.bind('<Right>', lambda event: right_callback(mqtt_client, current_speed, current_speed))
    #root.bind('<space>', lambda event: boost_callback(mqtt_client, current_speed, current_speed))


def forward_callback(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message("drive", [left_speed, right_speed])


def left_callback(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message("turn_left", [left_speed, right_speed])


def stop_callback(mqtt_client):
    mqtt_client.send_message("stop_bot")


def right_callback(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message("turn_right", [left_speed, right_speed])


#def boost_callback(mqtt_client, left_speed, right_speed):
#    mqtt_client.send_message("boost", [left_speed, right_speed])

main()