#   Author: Josh Melvin

import ev3dev.ev3 as ev3
import robot_controller as robo
import mqtt_remote_method_calls as com


def main():
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

    grass = 17
    water = 12

    while robot.color_sensor.reflected_light_intensity >= grass:
        print("Entering Tall Grass")
        mqtt_client.send_message("grass_walk")

    while 8 < robot.color_sensor.reflected_light_intensity <= 15:
        print("Squirtle use Surf.")
        mqtt_client.send_message("surf")

    robot.loop_forever()


main()
