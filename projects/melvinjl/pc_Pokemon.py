#   Author: Josh Melvin
import time
import random

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com




def main():

#    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    start = tkinter.Tk()
    start.title("                            Pokemon Red: Remastered Edition")

    main_frame = ttk.Frame(start, padding=0, relief='raised')
    main_frame.grid()

    photo = tkinter.PhotoImage(file="red_start.gif")

    button1 = ttk.Button(main_frame, image=photo)
    button1.image = photo
    button1.grid()
    button1['command'] = lambda: start.destroy()
    start.mainloop()

    walk_speed = 300
    run_speed = 600

    movement = tkinter.Tk()
    movement.bind('<Up>', lambda event: forward_callback(mqtt_client, walk_speed, walk_speed))
    movement.bind('<Left>', lambda event: left_callback(mqtt_client, walk_speed, walk_speed))
    movement.bind('<space>', lambda event: stop_callback(mqtt_client))
    movement.bind('<Right>', lambda event: right_callback(mqtt_client, walk_speed, walk_speed))
    movement.bind('<Down>', lambda event: back_callback(mqtt_client, walk_speed, walk_speed))
    movement.bind('<u>', lambda event: send_up(mqtt_client))
    movement.bind('<j>', lambda event: send_down(mqtt_client))

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

def forward_callback(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message("drive", [left_speed, right_speed])

def left_callback(mqtt_client, left_speed, right_speed):
    mqtt_client.send_message("turn_left", [left_speed, right_speed])

def stop_callback(mqtt_client):
    mqtt_client.send_message("stop_bot")

def right_callback(mqtt_client, left_speed, right_speed):
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

"""
Charmander = robo.Pokemon()
Charmander.type = "Fire"
Squirtle = robo.Pokemon()
Squirtle.type = "Water"
Bulbasaur = robo.Pokemon()
Bulbasaur.type = "Grass"
party = [Charmander, Squirtle, Bulbasaur]
"""

main()
