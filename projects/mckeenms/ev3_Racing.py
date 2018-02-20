"""
Author: Mason McKeen
"""

import ev3dev.ev3 as ev3

import time

import robot_controller as robo

import mqtt_remote_method_calls as mqtt

def main():
    while not robot.touch_sensor.is_pressed:
        robot = robo.Snatch3r()
        mqtt_client = mqtt.MqttClient(robot)
        mqtt_client.connect_to_pc()

        #finish_line = 17
        boost = 13
        oil = 11

        if robot.color_sensor.reflected_light_intensity == boost:
            if boost < 3:
                print('Gained Boost')
                boost = boost + 1

        if robot.color_sensor.reflected_light_intensity == oil:
            robot.drive_inches(2, 400)
            robot.turn_degrees(720, 400)
            robot.drive_inches(-3, 400)

    ev3.Sound.speak("Ending").wait()
    print('Pressed')


main()