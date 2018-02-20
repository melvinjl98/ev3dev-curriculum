#   Author: Josh Melvin

import ev3dev.ev3 as ev3
import time

import robot_controller as robo
import mqtt_remote_method_calls as com


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

    beacon_seeker = ev3.BeaconSeeker(channel=1)
    current_distance = beacon_seeker.distance

    grass = 17
    water = 12

    if robot.color_sensor.reflected_light_intensity == grass:
        print("Entering Tall Grass")
        mqtt_client.send_message("grass_walk")

    if robot.color_sensor.reflected_light_intensity == water:
        print("Squirtle use Surf.")
        mqtt_client.send_message("surf")

    if current_distance == 0:
        robot.stop_bot()
        robot.drive_inches(2.75, 300)
        robot.arm_up()
        if robot.touch_sensor.is_pressed:
            ev3.Sound.play("/home/robot/csse120/projects/melvinjl/recovery.wav")
            print("Thank you! Your Pokémon are fighting fit! We hope to see you again!")
            robot.arm_down()

    robot.loop_forever()


main()
