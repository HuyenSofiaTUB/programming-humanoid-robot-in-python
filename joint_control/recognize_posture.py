'''In this exercise you need to use the learned classifier to recognize current posture of robot

* Tasks:
    1. load learned classifier in `PostureRecognitionAgent.__init__`
    2. recognize current posture in `PostureRecognitionAgent.recognize_posture`

* Hints:
    Let the robot execute different keyframes, and recognize these postures.

'''
import numpy as np

from angle_interpolation import AngleInterpolationAgent
from keyframes import hello
import pickle
from os import listdir

ROBOT_POSE_DATA_DIR = 'robot_pose_data'
classes = listdir(ROBOT_POSE_DATA_DIR)
joints = ['LHipYawPitch', 'LHipRoll', 'LHipPitch', 'LKneePitch', 'RHipYawPitch', 'RHipRoll', 'RHipPitch', 'RKneePitch']


class PostureRecognitionAgent(AngleInterpolationAgent):
    def __init__(self, simspark_ip='localhost',
                 simspark_port=3100,
                 teamname='DAInamite',
                 player_id=0,
                 sync_mode=True):
        super(PostureRecognitionAgent, self).__init__(simspark_ip, simspark_port, teamname, player_id, sync_mode)
        self.posture = 'unknown'
        self.posture_classifier = 'robot_pose.pkl'  # LOAD YOUR CLASSIFIER

    def think(self, perception):
        self.posture = self.recognize_posture(perception)
        return super(PostureRecognitionAgent, self).think(perception)

    def recognize_posture(self, perception):
        posture = 'unknown'
        # YOUR CODE HERE
        clf = pickle.load(open(self.posture_classifier, 'rb'))
        all_data = []
        for i in joints:
            all_data.append(perception.joint[i])
        for j in perception.imu:
            all_data.append(j)

        all_data = np.asarray(all_data)
        #all_data = all_data.reshape(-1, 1)

        predicted = clf.predict(all_data)
        posture = classes[predicted]
        return posture


if __name__ == '__main__':
    agent = PostureRecognitionAgent()
    agent.keyframes = hello()  # CHANGE DIFFERENT KEYFRAMES
    agent.run()
