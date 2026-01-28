import time
import numpy as np
import hello_helpers.hello_misc as hm

node = hm.HelloNode.quick_create('lab1_ros2_motion')

node.move_to_pose({'rotate_mobile_base': np.radians(180)}, blocking=True)
