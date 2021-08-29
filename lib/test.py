import json
from ut.robot import Robot
from ut.elastic_interaction import Elastic

def test_robot():
    robot = Robot('')
    # robot.load_data_into_elastic()

    print(robot.transform_to_common('name and commandname and command'))

    # elastic = Elastic()
    # print(elastic.get_results('Машиностроение'))


if __name__ == '__main__':
    test_robot()
