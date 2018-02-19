"""
    Author: Josh Melvin
    CSSE 120 Final Project
    Pokemon Red: Remastered Edition
    My project is recreation of the classic Gameboy Color game, Pokemon Red.
    The robot is controlled via keyboard and can drive in all directions as
    well as have its arm move up and down. The pc side of the code handles
    the Tkinter windows and when the robot's color sensor detects green it
    sends a message to the pc to run a battle function to have your Pokemon
    battle a wild Pokemon. Detecting blue will do a similar thing except the
    code will prompt the user if they want to proceed first.
"""
import time

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
    root.title("                            Pokemon Red: Remastered Edition")

    walk_speed = 300

    start_window(root, windows_and_number)
    movement(mqtt_client, walk_speed)
    party_window(mqtt_client, windows_and_number)

    Charmander = Pokemon()
    Charmander.type = "Fire"
    Squirtle = Pokemon()
    Squirtle.type = "Water"
    Bulbasaur = Pokemon()
    Bulbasaur.type = "Grass"

    root.mainloop()


def start_window(root, windows_and_number):
    """ Puts Buttons on the main window. """
    start_frame = ttk.Frame(root, padding=0)
    start_frame.grid()

    press_start = ttk.Button(start_frame, image=tkinter.PhotoImage(file="red_start.gif"))
    press_start.image = tkinter.PhotoImage(file="red_start.gif")
    press_start.grid()
    windows_and_number.windows.append(start_window)
    press_start['command'] = lambda: start_game(windows_and_number)

"""
    destroy_button = ttk.Button(window1_frame,
                                text='Destroy some windows')
    destroy_button.grid()
    destroy_button['command'] = lambda: start_game(windows)
"""


def movement(mqtt_client, walk_speed):
    """Creates an invisible window that binds robot movement to keyboard controls."""
    movement_win = tkinter.Toplevel()

    movement_win.bind('<Up>', lambda event: forward_callback(mqtt_client, walk_speed, walk_speed))
    movement_win.bind('<Down>', lambda event: back_callback(mqtt_client, walk_speed, walk_speed))
    movement_win.bind('<Left>', lambda event: left_callback(mqtt_client, walk_speed, walk_speed))
    movement_win.bind('<Right>', lambda event: right_callback(mqtt_client, walk_speed, walk_speed))
    movement_win.bind('<space>', lambda event: stop_callback(mqtt_client))
    movement_win.bind('<u>', lambda event: send_up(mqtt_client))
    movement_win.bind('<j>', lambda event: send_down(mqtt_client))


def party_window(mqtt_client, windows_and_number):
    """Create a window that displays your Pokemon party."""
    party = tkinter.Toplevel()

    party_frame = ttk.Frame(party, padding=20)
    party_frame.grid()

    charmander_i = tkinter.PhotoImage(file="Charmander.gif")
    squirtle_i = tkinter.PhotoImage(file="Squirtle.gif")
    bulbasaur_i = tkinter.PhotoImage(file="Bulbasaur.gif")

    charmander = ttk.Button(party_frame, image=charmander_i)
    charmander.image = charmander_i
    charmander.grid(row=0, column=0)
    charmander['command'] = (lambda: set_current_pokemon(mqtt_client, False))

    squirtle = ttk.Button(party_frame, image=squirtle_i)
    squirtle.image = squirtle_i
    squirtle.grid(row=0, column=1)
    squirtle['command'] = (lambda: set_current_pokemon(mqtt_client, False))

    bulbasaur = ttk.Button(party_frame, image=bulbasaur_i)
    bulbasaur.image = bulbasaur_i
    bulbasaur.grid(row=1, column=0)
    bulbasaur['command'] = (lambda: set_current_pokemon(mqtt_client, False))

    q_button = ttk.Button(party_frame, text="Quit")
    q_button.grid(row=4, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(party_frame, text="Exit")
    e_button.grid(row=5, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))


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


def start_game(data):
    """ Destroys all the windows stored in the given Data object. """
    for k in range(len(data.windows)):
        data.windows[k].destroy()


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


def send_up(mqtt_client):
    mqtt_client.send_message("arm_up")


def send_down(mqtt_client):
    mqtt_client.send_message("arm_down")


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


"""
def Grass_Walk():
    

def Surf():
"""

main()
