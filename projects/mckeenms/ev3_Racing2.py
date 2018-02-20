"""
Author: Mason McKeen
"""

import ev3dev.ev3 as ev3

import time

import robot_controller as robo

import mqtt_remote_method_calls as mqtt

def main():
    robot = robo.Snatch3r()
    mqtt_client = mqtt.MqttClient(robot)
    mqtt_client.connect_to_pc()
    print('running')

    while not robot.touch_sensor.is_pressed:

        print(robot.color_sensor.reflected_light_intensity)
        finish_line = 17
        boost = 13
        oil = 11

        if robot.color_sensor.reflected_light_intensity == finish_line:
            ev3.Sound.speak("Crossed the Finish!")

        if robot.color_sensor.reflected_light_intensity == boost:
                ev3.Sound.speak("Gained Boost").wait()
                give_boost(mqtt_client)

        if robot.color_sensor.reflected_light_intensity == oil:
            ev3.Sound.speak("Oof").wait()
            robot.drive_inches(2, 400)
            robot.turn_degrees(360, 800)
            robot.drive_inches(3, 400)

    ev3.Sound.speak("Ending").wait()
    print('Pressed')

def give_boost(mqtt_client):
    mqtt_client.send_message("boost")

main()