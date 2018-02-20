"""
Author: Mason McKeen
"""

import ev3dev.ev3 as ev3
import time
import robot_controller as robo
import mqtt_remote_method_calls as mqtt

lap = 0

def main(lap):
    robot = robo.Snatch3r()
    mqtt_client = mqtt.MqttClient(robot)
    mqtt_client.connect_to_pc()

    finish_line = 17
    boost = 12
    oil = 3

    if robot.color_sensor.reflected_light_intensity == finish_line:
        lap = lap + 1
        if lap == 3:
            lap = 0
            print('Finish')
            ev3.Sound.speak('Crossing the finish!').wait()
        else:
            print('Lap Number', lap)

    if robot.color_sensor.reflected_light_intensity == boost:
        'thing'

    if robot.color_sensor.reflected_light_intensity == oil:
        robot.drive_inches(2, 400)
        robot.turn_degrees(540, 400)
        robot.drive_inches(-3, 400)

    robot.loop_forever()

main()