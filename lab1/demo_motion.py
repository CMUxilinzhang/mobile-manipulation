#!/usr/bin/env python3
import time
import numpy as np
import stretch_body.robot

robot = stretch_body.robot.Robot()
robot.startup()

# Extend arm lift
robot.arm.move_to(0.5)
robot.lift.move_to(1.1)
robot.push_command()

robot.arm.wait_until_at_setpoint(timeout=20.0)
robot.lift.wait_until_at_setpoint(timeout=20.0)

# Move wrist motors one at a time
d = np.radians(30)

robot.end_of_arm.move_by('wrist_yaw', d)
robot.push_command()
robot.end_of_arm.wait_until_at_setpoint()

robot.end_of_arm.move_by('wrist_pitch', d)
robot.push_command()
robot.end_of_arm.wait_until_at_setpoint()

robot.end_of_arm.move_by('wrist_roll', d)
robot.push_command()
robot.end_of_arm.wait_until_at_setpoint()

# Open and close the gripper
robot.end_of_arm.move_to('stretch_gripper', 50)
robot.push_command()
robot.end_of_arm.wait_until_at_setpoint()

time.sleep(1.0)

robot.end_of_arm.move_to('stretch_gripper', 0)
robot.push_command()
robot.end_of_arm.wait_until_at_setpoint()

# Rotate RealSense head motors
robot.head.move_by('head_pan', d)
robot.push_command()
robot.head.wait_until_at_setpoint()

robot.head.move_by('head_tilt', d)
robot.push_command()
robot.head.wait_until_at_setpoint()

# Return to stow position


robot.stow()

#robot.push_command()

robot.arm.wait_until_at_setpoint(timeout=20.0)
robot.lift.wait_until_at_setpoint(timeout=20.0)
# 6. Base motion: forward 0.5m, rotate 180deg, forward 0.5m
robot.base.translate_by(0.5)
robot.push_command()
time.sleep(4.0)

robot.base.rotate_by(np.radians(180))
robot.push_command()
time.sleep(5.0)

robot.base.translate_by(0.5)
robot.push_command()
time.sleep(4.0)

robot.stop()

