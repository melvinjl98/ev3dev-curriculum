#   Author: Josh Melvin

import ev3dev.ev3 as ev3
import time

import robot_controller as robo
import mqtt_remote_method_calls as com


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

    #grass =
    #water =

    #if robot.color_sensor.reflected_light_intensity = grass:

    #elif robot.color_sensor.reflected_light_intensity = water:

    robot.loop_forever()


main()
