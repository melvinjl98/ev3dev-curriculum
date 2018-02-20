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
        self.running = True


class Pokemon(object):
    def __init__(self):
        self.type = None
        self.hp = 50
        self.attack = 37.5
        self.defense = 25


def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("                            Pokemon Red: Remastered Edition")

    party = tkinter.Toplevel()

    walk_speed = 500

    charmander = Pokemon()
    charmander.type = "Fire"
    squirtle = Pokemon()
    squirtle.type = "Water"
    bulbasaur = Pokemon()
    bulbasaur.type = "Grass"

    current_pokemon = bulbasaur

    start_window(root)
    movement(party, mqtt_client, walk_speed)
    party_window(party, mqtt_client, charmander, squirtle, bulbasaur, current_pokemon)

    root.mainloop()


def start_window(root):
    """Creates a window for the start scen image"""
    start_frame = ttk.Frame(root, padding=0)
    start_frame.grid()

    start_screen = tkinter.PhotoImage(file="red_start.gif")

    press_start = ttk.Button(start_frame, image=start_screen)
    press_start.image = start_screen
    press_start.grid()


def movement(party, mqtt_client, walk_speed):
    """Attaches movement controls to ."""

    party.bind('<Up>', lambda event: forward_callback(mqtt_client, walk_speed, walk_speed))
    party.bind('<Down>', lambda event: back_callback(mqtt_client, walk_speed, walk_speed))
    party.bind('<Left>', lambda event: left_callback(mqtt_client, walk_speed, walk_speed))
    party.bind('<Right>', lambda event: right_callback(mqtt_client, walk_speed, walk_speed))
    party.bind('<space>', lambda event: stop_callback(mqtt_client))
    party.bind('<u>', lambda event: send_up(mqtt_client))
    party.bind('<j>', lambda event: send_down(mqtt_client))


def party_window(party, mqtt_client, charmander, squirtle, bulbasaur, current_pokemon):
    """Create a window that displays your Pokemon party."""

    party_frame = ttk.Frame(party, padding=10)
    party_frame.grid()

    charmander_i = tkinter.PhotoImage(file="Charmander.gif")
    squirtle_i = tkinter.PhotoImage(file="Squirtle.gif")
    bulbasaur_i = tkinter.PhotoImage(file="Bulbasaur.gif")

    charmander_b = ttk.Button(party_frame, image=charmander_i)
    charmander_b.image = charmander_i
    charmander_b.grid(row=0, column=0)
    charmander_b['command'] = (lambda: set_current_pokemon(charmander, "Charmander"))

    squirtle_b = ttk.Button(party_frame, image=squirtle_i)
    squirtle_b.image = squirtle_i
    squirtle_b.grid(row=0, column=1)
    squirtle_b['command'] = (lambda: set_current_pokemon(squirtle, "Squirtle"))

    bulbasaur_b = ttk.Button(party_frame, image=bulbasaur_i)
    bulbasaur_b.image = bulbasaur_i
    bulbasaur_b.grid(row=1, column=0)
    bulbasaur_b['command'] = (lambda: set_current_pokemon(bulbasaur, "Bulbasaur"))

    heal_button = ttk.Button(party_frame, text="Heal")
    heal_button.grid(row=4, column=0)
    heal_button['command'] = (lambda: poke_center(mqtt_client, charmander, squirtle, bulbasaur))

    grass_button = ttk.Button(party_frame, text="Search Grass")
    grass_button.grid(row=4, column=1)
    grass_button['command'] = (lambda: grass_walk(current_pokemon))

    q_button = ttk.Button(party_frame, text="Quit")
    q_button.grid(row=4, column=1)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(party_frame, text="Exit")
    e_button.grid(row=4, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    menubar = tkinter.Menu(party)
    party['menu'] = menubar

    music_menu = tkinter.Menu(menubar)
    menubar.add_cascade(menu=music_menu, label='Music')
    music_menu.add_command(label='Opening', command=lambda: mqtt_client.send_message('play_music', [1]))
    music_menu.add_command(label='Battle', command=lambda: mqtt_client.send_message('play_music', [2]))
    music_menu.add_command(label='Champion', command=lambda: mqtt_client.send_message('play_music', [3]))

    wild_menu = tkinter.Menu(menubar)
    menubar.add_cascade(menu=wild_menu, label='Wild')
    wild_menu.add_command(label='Grass', command=lambda: grass_walk(current_pokemon))
    wild_menu.add_command(label='Water', command=lambda: surf(current_pokemon))


def set_current_pokemon(pokemon, string):
    print("Current Pokemon is {}".format(string))
    return pokemon


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


def grass_walk(current_pokemon):
    """Robot is searching grass Pokemon"""
    print("You have entered tall grass.")
    gloom = Pokemon()
    gloom.type = "Grass"
    time.sleep(5)
    battle(current_pokemon, gloom)


def surf(current_pokemon):
    """Robot is searching for water Pokemon"""
    print("Squirtle use Surf.")
    magikarp = Pokemon()
    magikarp.type = "Water"
    time.sleep(5)
    battle(current_pokemon, magikarp)


def battle(current_pokemon, wild_pokemon):
    """Your currently selected pokemon battles against the wild Pokemon."""
    if current_pokemon.type == "Fire" and wild_pokemon.type == "Grass":
        current_pokemon.hp = current_pokemon.hp + current_pokemon.defense - wild_pokemon.attack
        wild_pokemon.hp = wild_pokemon.hp + wild_pokemon.defense - (current_pokemon.attack * 2)
        print(wild_pokemon.hp, current_pokemon.hp)

    if current_pokemon.type == "Fire" and wild_pokemon.type == "Water":
        wild_pokemon.hp = wild_pokemon.hp + wild_pokemon.defense - (.5 * current_pokemon.attack)
        current_pokemon.hp = current_pokemon.hp + current_pokemon.defense - (2 * wild_pokemon.attack)
        print(wild_pokemon.hp, current_pokemon.hp)

    if current_pokemon.type == "Water" and wild_pokemon.type == "Grass":
        current_pokemon.hp = current_pokemon.hp + current_pokemon.defense - (2 * wild_pokemon.attack)
        wild_pokemon.hp = wild_pokemon.hp + wild_pokemon.defense - current_pokemon.attack
        print(wild_pokemon.hp, current_pokemon.hp)

    if current_pokemon.type == "Water" and wild_pokemon.type == "Water":
        wild_pokemon.hp = wild_pokemon.hp + wild_pokemon.defense - current_pokemon.attack
        current_pokemon.hp = current_pokemon.hp + current_pokemon.defense - wild_pokemon.attack
        print(wild_pokemon.hp, current_pokemon.hp)

    if current_pokemon.type == "Grass" and wild_pokemon.type == "Grass":
        current_pokemon.hp = current_pokemon.hp + current_pokemon.defense - wild_pokemon.attack
        wild_pokemon.hp = wild_pokemon.hp + wild_pokemon.defense - current_pokemon.attack
        print(wild_pokemon.hp, current_pokemon.hp)

    if current_pokemon.type == "Grass" and wild_pokemon.type == "Water":
        wild_pokemon.hp = wild_pokemon.hp + wild_pokemon.defense - (2 * current_pokemon.attack)
        current_pokemon.hp = current_pokemon.hp + current_pokemon.defense - wild_pokemon.attack
        print(wild_pokemon.hp, current_pokemon.hp)

    if current_pokemon.hp == 0:
        print("Trainer whited out.")
        return

    elif wild_pokemon.hp == 0:
        print("You are victorious.")
        return

    else:
        print("You got away safely.")
        return


def poke_center(mqtt_client, charmander, squirtle, bulbasaur):
    """send message to robot to look for the PokeCenter beacon"""
    mqtt_client.send_message("seek_beacon_pokemon")
    hp = 50
    charmander.hp = hp
    bulbasaur.hp = hp
    squirtle.hp = hp
    print("c.hp={}, s.hp={}, b.hp={}".format(charmander.hp, squirtle.hp, bulbasaur.hp))


main()
