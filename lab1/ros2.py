#!/usr/bin/env python3
import time
import numpy as np
import hello_helpers.hello_misc as hm

def wait_for_joint_states(node, timeout_s=5.0):
    """Wait until node.joint_state looks valid."""
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        js = getattr(node, "joint_state", None)
        if js is not None and hasattr(js, "name") and js.name is not None and len(js.name) > 0:
            return True
        time.sleep(0.05)
    return False

def jpos(node, joint_name: str, default=0.0) -> float:
    """Get current joint position from node.joint_state; return default if unavailable."""
    js = getattr(node, "joint_state", None)
    if js is None or not hasattr(js, "name") or not hasattr(js, "position"):
        return default
    try:
        i = js.name.index(joint_name)
        return float(js.position[i])
    except Exception:
        return default

def main():
    node = hm.HelloNode.quick_create('lab1_ros2_motion')

    if not wait_for_joint_states(node, timeout_s=5.0):
        print("[WARN] joint_states not ready yet; continuing anyway (jpos may use defaults).")


    node.stow_the_robot()
    time.sleep(0.5)

    # Arm full out and lift
    node.move_to_pose({
        'joint_arm': 0.5,     # meters
        'joint_lift': 1.1   
    }, blocking=True)

    # Wrist motors one at a time 
    d = np.radians(30)

    node.move_to_pose({'joint_wrist_yaw': 0.5}, blocking=True, duration = 2.0)
    node.move_to_pose({'joint_wrist_pitch': -0.5}, blocking=True, duration = 2.0)
    node.move_to_pose({'joint_wrist_roll': 1.0}, blocking=True, duration = 2.0)

    # Gripper open then close 
    open_val = 0.04
    close_val = 0.0
    node.move_to_pose({'gripper_aperture': open_val}, blocking=True, duration=1.5)
    node.move_to_pose({'gripper_aperture': close_val}, blocking=True, duration=1.5)

    # Head (RealSense)
    node.move_to_pose({'joint_head_pan': np.radians(45),
                      'joint_head_tilt': np.radians(45)}, blocking=True,duration = 3)

    # Back to stow 
    node.stow_the_robot()
    time.sleep(0.5)

    # move forward and rotate and move back
    node.move_to_pose({'translate_mobile_base': 0.5}, blocking=True)
    node.move_to_pose({'rotate_mobile_base': np.radians(180)}, blocking=True)
    node.move_to_pose({'translate_mobile_base': 0.5}, blocking=True)

    # stow again at the very end
    node.stow_the_robot()
    time.sleep(0.5)

    node.destroy_node()

if __name__ == '__main__':
    main()

