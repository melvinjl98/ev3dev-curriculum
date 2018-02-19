#   Author: Josh Melvin

import ev3dev.ev3 as ev3
import time

import robot_controller as robo
import mqtt_remote_method_calls as com


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

    if robot.color_sensor.color == ev3.ColorSensor.COLOR_GREEN:
        mqtt_client.send_message("Grass_Walk")

    if robot.color_sensor.color == ev3.ColorSensor.COLOR_BLUE:
        mqtt_client.send_message("Surf")

    robot.loop_forever()


main()
