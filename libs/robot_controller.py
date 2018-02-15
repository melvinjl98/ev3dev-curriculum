"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import time
import math


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        """Creats a Snatch3r object"""
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        self.MAX_SPEED = 900
        self.running = True
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.touch_sensor.connected
        assert self.color_sensor
        assert self.ir_sensor
        assert self.pixy

    def drive_inches(self, inches_target, speed_deg_per_second):
        """"Drives to a given relative position with a given speed"""
        self.left_motor.run_to_rel_pos(speed_sp=speed_deg_per_second, position_sp=inches_target*90)
        self.right_motor.run_to_rel_pos(speed_sp=speed_deg_per_second, position_sp=inches_target*90)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        """turn a given degrees at a given speed"""
        self.left_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=-degrees_to_turn*4.95)
        self.right_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=degrees_to_turn*4.95)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()

    def arm_calibration(self):
        """Calibrate the arm motor position"""
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while True:
            time.sleep(0.01)
            if self.touch_sensor.is_pressed:
                break
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range, speed_sp=self.MAX_SPEED)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()
        self.arm_motor.position = 0

    def arm_up(self):
        """Move the arm up"""
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while True:
            time.sleep(0.01)
            if self.touch_sensor.is_pressed:
                break
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep().wait()

    def arm_down(self):
        """Move the arm down"""
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=self.MAX_SPEED)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running
        ev3.Sound.beep().wait()

    def shutdown(self):
        """Turn off all motors turn LEDs green, and stop all other code"""
        self.left_motor.stop(stop_action="brake")
        self.right_motor.stop(stop_action="brake")
        self.arm_motor.stop(stop_action="brake")
        self.running = False
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        print('Goodbye')
        ev3.Sound.speak('Goodbye').wait()

    def loop_forever(self):
        """Creates a never ending loop"""
        while self.running:
            time.sleep(0.1)

    def drive(self, left_speed, right_speed):
        """Turns motors on at given speeds"""
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def turn_right(self, left_speed, right_speed):
        """Turn Motors on to turn right"""
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def turn_left(self, left_speed, right_speed):
        """Turn Motors on to turn left"""
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def back(self, left_speed, right_speed):
        """Turn Motors on to drive backwards"""
        self.left_motor.run_forever(speed_sp=-left_speed)
        self.right_motor.run_forever(speed_sp=-right_speed)

    def stop_bot(self):
        """Stops both motors"""
        self.left_motor.stop(stop_action="brake")
        self.right_motor.stop(stop_action="brake")

    def seek_beacon(self):
        """Look for the IR beacon"""
        beacon_seeker = ev3.BeaconSeeker(channel=1)
        forward_speed = 300
        turn_speed = 100

        while not self.touch_sensor.is_pressed:
            current_heading = beacon_seeker.heading
            current_distance = beacon_seeker.distance
            if current_distance == -128:
                print("IR Remote not found. Distance is -128")
                self.drive(turn_speed, -turn_speed)
            else:
                if math.fabs(current_heading) < math.fabs(2):
                    print("On the right heading. Distance: ", current_distance)
                    if current_distance == 0:
                        self.stop_bot()
                        self.drive_inches(2.75, forward_speed)
                        return True
                    else:
                        self.drive(forward_speed, forward_speed)

                elif math.fabs(current_heading) < 10:
                    print("Adjusting heading: ", current_heading)
                    if current_heading < 0:
                        self.drive(-turn_speed, turn_speed)
                    else:
                        self.drive(turn_speed, -turn_speed)

                else:
                    self.drive(turn_speed, -turn_speed)

            time.sleep(0.2)

        print("Abandon ship!")
        self.stop_bot()
        return False


#   melvinjl
class Pokemon(object):
    def __init__(self):
        self.type=None
        self.hp=50
        self.attack=37.5
        self.defense=25

    def battle(self, wild_pokemon):
        ev3.Sound.play("/home/robot/csse120/projects/melvinjl/battle.wav")

#   mckeenms

#   makinewg
