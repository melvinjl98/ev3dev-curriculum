#   Author: Josh Melvin
import time
import random

import tkinter
from tkinter import ttk

import mqtt_remote_method_calls as com


class MyDelegate(object):
    def __init__(self):
        self.running=True


class Pokemon(object):
    def __init__(self):
        self.type=None
        self.hp=50
        self.attack=37.5
        self.defense=25


class WindowsAndNumber(object):
    def __init__(self):
        self.number = None
        self.label = None
        self.windows = []

def main():

    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()

    windows_and_number = WindowsAndNumber()

    root = tkinter.Tk()

    party_frame = ttk.Frame(root, padding=0, relief='raised')
    party_frame.grid()

    start_window(root, windows_and_number)

    photo = tkinter.PhotoImage(file="red_start.gif")

    press_start = ttk.Button(main_frame, image=photo)
    press_start.image = photo
    press_start.grid()
    press_start['command'] = lambda: start.destroy()
    start.mainloop()

    walk_speed = 300

    movement = tkinter.Tk()
    movement.bind('<Up>', lambda event: forward_callback(mqtt_client, walk_speed, walk_speed))
    movement.bind('<Left>', lambda event: left_callback(mqtt_client, walk_speed, walk_speed))
    movement.bind('<space>', lambda event: stop_callback(mqtt_client))
    movement.bind('<Right>', lambda event: right_callback(mqtt_client, walk_speed, walk_speed))
    movement.bind('<Down>', lambda event: back_callback(mqtt_client, walk_speed, walk_speed))
    movement.bind('<u>', lambda event: send_up(mqtt_client))
    movement.bind('<j>', lambda event: send_down(mqtt_client))

    Charmander = Pokemon()
    Charmander.type = "Fire"
    Squirtle = Pokemon()
    Squirtle.type = "Water"
    Bulbasaur = Pokemon()
    Bulbasaur.type = "Grass"
    party = [Charmander, Squirtle, Bulbasaur]

    charmander = tkinter.PhotoImage(file="Charmander.gif")
    squirtle = tkinter.PhotoImage(file="Squirtle.gif")
    bulbasaur = tkinter.PhotoImage(file="Bulbasaur.gif")

    Charmander = ttk.Button(party_frame, image=charmander)
    Charmander.image = charmander
    Charmander.grid(row=0, column=0)

    Squirtle = ttk.Button(party_frame, image=squirtle)
    Squirtle.image = squirtle
    Squirtle.grid(row=0, column=1)

    Bulbasaur = ttk.Button(party_frame, image=bulbasaur)
    Bulbasaur.image = bulbasaur
    Bulbasaur.grid(row=1, column=0)

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=4, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=5, column=2)
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

def start_window(root, windows):
    """ Puts Buttons on the main window. """
    root.title("                            Pokemon Red: Remastered Edition")

    start_frame = ttk.Frame(root, padding=0, relief='raised')
    start_frame.grid()

    press_start = ttk.Button(start_frame, image=tkinter.PhotoImage(file="red_start.gif"))
    press_start.image = tkinter.PhotoImage(file="red_start.gif")
    press_start.grid()
    press_start['command'] = lambda: change_number(windows, 1)
"""
    destroy_button = ttk.Button(window1_frame,
                                text='Destroy some windows')
    destroy_button.grid()
    destroy_button['command'] = lambda: destroy_windows(windows)
"""

def put_stuff_on_window2(windows_and_number):
    """ Puts Buttons on a secondary window. """
    root2 = tkinter.Toplevel()  # Note Toplevel, NOT Tk.

    window2_frame = ttk.Frame(root2, padding=20)
    window2_frame.grid()

    decrease_button = ttk.Button(window2_frame,
                                 text='Decrease the number')
    decrease_button.grid()
    decrease_button['command'] = lambda: change_number(windows_and_number, -1)

    button_text = 'Pop up a new window with the number'
    pop_up_button = ttk.Button(window2_frame, text=button_text)
    pop_up_button.grid()
    pop_up_button['command'] = lambda: pop_up(windows_and_number)


def put_stuff_on_window3(windows_and_number):
    """ Puts a Label on a secondary window. """
    root3 = tkinter.Toplevel()  # Note Toplevel, NOT Tk.

    window3_frame = ttk.Frame(root3, padding=20)
    window3_frame.grid()

    number_label = ttk.Label(window3_frame, text='The number is: 0')
    number_label.grid()

    windows_and_number.number = 0
    windows_and_number.label = number_label


def change_number(windows_and_number, delta):
    """
    Changes the number in the data by the given delta,
    then displays the changed value in its Label.
    """
    windows_and_number.number = windows_and_number.number + delta
    msg = 'The number is: {}'.format(windows_and_number.number)
    windows_and_number.label['text'] = msg


def pop_up(windows_and_number):
    """ Pops up a window, with a Label that shows some info. """
    window = tkinter.Toplevel()  # Note Toplevel, NOT Tk.
    msg = 'The number is: \n {}'.format(windows_and_number.number)
    label = ttk.Label(window, text=msg)
    label.grid()

    windows_and_number.windows.append(window)


def destroy_windows(data):
    """ Destroys all the windows stored in the given Data object. """
    for k in range(len(data.windows)):
        data.windows[k].destroy()


main()

