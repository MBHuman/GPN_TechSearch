import json
from ut.robot import Robot

def test_robot():
    robot = Robot('')
    robot.load_data_into_elastic()

if __name__ == '__main__':
    test_robot()
