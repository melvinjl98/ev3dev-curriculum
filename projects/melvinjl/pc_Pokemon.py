#   Author: Josh Melvin
import time
import random

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Pokemon Red: Remastered Edition")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    walk_speed = 300
    run_speed = 600

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    forward_button['command'] = lambda: forward_callback(mqtt_client, walk_speed, walk_speed)
    root.bind('<Up>', lambda event: forward_callback(mqtt_client, walk_speed, walk_speed))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    left_button['command'] = lambda: left_callback(mqtt_client, walk_speed, walk_speed)
    root.bind('<Left>', lambda event: left_callback(mqtt_client, walk_speed, walk_speed))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    stop_button['command'] = lambda: stop_callback(mqtt_client)
    root.bind('<space>', lambda event: stop_callback(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    right_button['command'] = lambda: right_callback(mqtt_client, walk_speed, walk_speed)
    root.bind('<Right>', lambda event: right_callback(mqtt_client, walk_speed, walk_speed))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    back_button['command'] = lambda: back_callback(mqtt_client, walk_speed, walk_speed)
    root.bind('<Down>', lambda event: back_callback(mqtt_client, walk_speed, walk_speed))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    root.mainloop()

    def forward_callback(mqtt_client, left_speed, right_speed):
        print("drive")
        mqtt_client.send_message("drive", [left_speed, right_speed])

    def left_callback(mqtt_client, left_speed, right_speed):
        print("turn left")
        mqtt_client.send_message("turn_left", [left_speed, right_speed])

    def stop_callback(mqtt_client):
        print("stop")
        mqtt_client.send_message("stop_bot")

    def right_callback(mqtt_client, left_speed, right_speed):
        print("turn right")
        mqtt_client.send_message("turn_right", [left_speed, right_speed])

    def back_callback(mqtt_client, left_speed, right_speed):
        print("back up")
        mqtt_client.send_message("back", [left_speed, right_speed])

    def send_up(mqtt_client):
        print("arm_up")
        mqtt_client.send_message("arm_up")

    def send_down(mqtt_client):
        print("arm_down")
        mqtt_client.send_message("arm_down")

    def quit_program(mqtt_client, shutdown_ev3):
        if shutdown_ev3:
            print("shutdown")
            mqtt_client.send_message("shutdown")
        mqtt_client.close()
        exit()


main()
