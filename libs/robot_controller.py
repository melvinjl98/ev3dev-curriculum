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
        assert self.color_sensor.connected
        assert self.ir_sensor.connected
        assert self.pixy.connected

    def drive_inches(self, inches_target, speed_deg_per_second):
        """"Drives to a given relative position with a given speed"""
        self.left_motor.run_to_rel_pos(speed_sp=speed_deg_per_second, position_sp=inches_target*90)
        self.right_motor.run_to_rel_pos(speed_sp=speed_deg_per_second, position_sp=inches_target*90)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        # ev3.Sound.beep().wait()

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        """turn a given degrees at a given speed"""
        self.left_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=-degrees_to_turn*4.95)
        self.right_motor.run_to_rel_pos(speed_sp=turn_speed_sp, position_sp=degrees_to_turn*4.95)
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)
        # ev3.Sound.beep().wait()

    def arm_calibration(self):
        """Calibrate the arm motor position"""
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while True:
            time.sleep(0.01)
            if self.touch_sensor.is_pressed:
                break
        self.arm_motor.stop(stop_action="brake")
        # ev3.Sound.beep().wait()

        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range, speed_sp=self.MAX_SPEED)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        # ev3.Sound.beep().wait()
        self.arm_motor.position = 0

    def arm_up(self):
        """Move the arm up"""
        self.arm_motor.run_forever(speed_sp=self.MAX_SPEED)
        while True:
            time.sleep(0.01)
            if self.touch_sensor.is_pressed:
                break
        self.arm_motor.stop(stop_action="brake")
        # ev3.Sound.beep().wait()

    def arm_down(self):
        """Move the arm down"""
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=self.MAX_SPEED)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running
        # ev3.Sound.beep().wait()

    def shutdown(self):
        """Turn off all motors turn LEDs green, and stop all other code"""
        self.left_motor.stop(stop_action="brake")
        self.right_motor.stop(stop_action="brake")
        self.arm_motor.stop(stop_action="brake")
        self.running = False
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)
        print('Goodbye')
        ev3.Sound.play("/home/robot/csse120/assets/sounds/awesome_pcm.wav").wait()

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

    def boost(self, left_speed, right_speed):
        """Doubles speed for 5 seconds"""
        self.left_motor.run_forever(speed_sp=2 * left_speed)
        self.right_motor.run_forever(speed_sp=2 * right_speed)

        self.left_motor.wait(5000)
        self.right_motor.wait(5000)

        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def firetruck(self):

        while not self.touch_sensor.is_pressed:
            ev3.Sound.play("/home/robot/csse120/assets/sounds/Siren.wav").wait()
            ev3.Sound.play("/home/robot/csse120/assets/sounds/horn.wav").wait()
            ev3.Sound.play("/home/robot/csse120/assets/sounds/Siren.wav").wait()

    def follow_a_line(self):

        while not self.touch_sensor.is_pressed:
            if self.color_sensor.reflected_light_intensity < 80:
                self.turn_degrees(-10, 400)
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
            if self.color_sensor.reflected_light_intensity < 70 & self.color_sensor.reflected_light_intensity > 60:
                self.drive(0, 0)
                self.arm_calibration()
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)
                break
            else:
                self.drive(600, 600)
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)

    def follow_the_line(self):

        while not self.touch_sensor.is_pressed:
            if self.color_sensor.reflected_light_intensity < 80:
                self.turn_degrees(-10, 400)
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.YELLOW)
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.RED)
            if self.color_sensor.reflected_light_intensity < 70 & self.color_sensor.reflected_light_intensity > 60:
                self.drive(0, 0)
                self.arm_up()
                time.sleep(2)
                self.arm_down()
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)
                break
            else:
                self.drive(600, 600)
                ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.RED)
                ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.YELLOW)

        self.seek_beacon()

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
    def play_music(self, music_number):
        if music_number == 1:
            ev3.Sound.play("/home/robot/csse120/projects/melvinjl/opening.wav")
        if music_number == 2:
            ev3.Sound.play("/home/robot/csse120/projects/melvinjl/battle.wav")
        if music_number == 3:
            ev3.Sound.play("/home/robot/csse120/projects/melvinjl/champion.wav")

    def seek_beacon_pokemon(self):
        """Creates a specialized beacon seeking function to find the beacon and heal the pokemon party."""
        beacon_seeker = ev3.BeaconSeeker(channel=1)
        forward_speed = 500
        turn_speed = 300

        while True:
            current_heading = beacon_seeker.heading
            current_distance = beacon_seeker.distance
            if current_distance == -128:
                self.drive(turn_speed, -turn_speed)
            else:
                if math.fabs(current_heading) < math.fabs(2):
                    if current_distance == 0:
                        self.stop_bot()
                        time.sleep(.25)
                        self.drive_inches(2.75, forward_speed)
                        time.sleep(.25)
                        self.arm_up()
                        if self.touch_sensor.is_pressed:
                            ev3.Sound.play("/home/robot/csse120/projects/melvinjl/recovery.wav")
                            print("Thank you! Your Pokemon are fighting fit! We hope to see you again!")
                            self.arm_down()
                            break
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


#   mckeenms

#   makinewg
