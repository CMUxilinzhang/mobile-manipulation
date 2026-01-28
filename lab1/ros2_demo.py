#!/usr/bin/env python3
import time
import numpy as np
import rclpy
import hello_helpers.hello_misc as hm

def jpos(node, joint_name: str) -> float:
    """Read current joint position from /joint_states (rad for revolute, m for prismatic)."""
    i = node.joint_state.name.index(joint_name)
    return node.joint_state.position[i]

def main():
    rclpy.init()
    node = hm.HelloNode.quick_create('lab1_ros2_motion')

    # ---------- 0) stow ----------
    node.stow_the_robot()  # PDF says this is the ROS2 equivalent of robot.stow() :contentReference[oaicite:2]{index=2}

    # ---------- 1) arm full out + lift full up (same time) ----------
    # Use one move_to_pose call so ROS plans them together.
    node.move_to_pose({
        'joint_arm': 0.5,     # meters (telescoping arm) — same as API demo
        'joint_lift': 1.1     # meters (lift)
    }, blocking=True)

    # ---------- 2) wrist motors one at a time ----------
    d = np.radians(30)

    node.move_to_pose({'joint_wrist_yaw': jpos(node, 'joint_wrist_yaw') + d}, blocking=True)
    node.move_to_pose({'joint_wrist_pitch': jpos(node, 'joint_wrist_pitch') + d}, blocking=True)
    node.move_to_pose({'joint_wrist_roll': jpos(node, 'joint_wrist_roll') + d}, blocking=True)

    # ---------- 3) gripper open then close ----------
    # Joint name can be left or right finger (PDF lists both). We'll use left.
    # Gripper units for this joint are typically meters/radians depending on driver;
    # empirically: small positive opens, 0 closes. If your robot behaves reversed, flip signs.
    node.move_to_pose({'joint_gripper_finger_left': 0.04}, blocking=True)  # open (tune if needed)
    time.sleep(0.5)
    node.move_to_pose({'joint_gripper_finger_left': 0.0}, blocking=True)   # close

    # ---------- 4) head (RealSense) pan + tilt ----------
    node.move_to_pose({'joint_head_pan':  jpos(node, 'joint_head_pan') + d}, blocking=True)
    node.move_to_pose({'joint_head_tilt': jpos(node, 'joint_head_tilt') + d}, blocking=True)

    # ---------- 5) back to stow ----------
    node.stow_the_robot()

    # ---------- 6) base: forward 0.5m, rotate 180deg, forward 0.5m ----------
    node.move_to_pose({'translate_mobile_base': 0.5}, blocking=True)
    node.move_to_pose({'rotate_mobile_base': np.radians(180)}, blocking=True)
    node
