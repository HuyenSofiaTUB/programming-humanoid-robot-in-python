'''In this file you need to implement remote procedure call (RPC) server

* There are different RPC libraries for python, such as xmlrpclib, json-rpc. You are free to choose.
* The following functions have to be implemented and exported:
 * get_angle
 * set_angle
 * get_posture
 * execute_keyframes
 * get_transform
 * set_transform
* You can test RPC server with ipython before implementing agent_client.py
'''

# add PYTHONPATH
import os
import sys
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'kinematics'))

from inverse_kinematics import InverseKinematicsAgent

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import logging
import threading
import time
import numpy as np

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)
    
class ServerAgent(InverseKinematicsAgent):
    '''ServerAgent provides RPC service
    '''
    # YOUR CODE HERE
    def __init__(self):
        super(ServerAgent, self).__init__()
        
        logging.basicConfig(level=logging.DEBUG)
        server = SimpleXMLRPCServer(('localhost', 9999), logRequests=True)
        print("Listening on localhost:9999")
        server.register_instance(self)
        server.register_introspection_functions()
        server.register_multicall_functions()
        #server.serve_forever()
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        print("Server thread started")
    
    def get_angle(self, joint_name):
        '''get sensor value of given joint'''
        # YOUR CODE HERE
        return self.perception.joint[joint_name]
    
    def set_angle(self, joint_name, angle):
        '''set target angle of joint for PID controller
        '''
        # YOUR CODE HERE
        self.target_joints[joint_name] = angle

    def get_posture(self):
        '''return current posture of robot'''
        # YOUR CODE HERE
        self.posture = self.recognize_posture(self.perception)
        print(self.posture)
        return self.posture

    def execute_keyframes(self, keyframes):
        '''excute keyframes, note this function is blocking call,
        e.g. return until keyframes are executed
        '''
        # YOUR CODE HERE
        self.keyframes = keyframes
        self.angle_interpolation(keyframes, self.perception)
        sum_times = keyframes[1]
        time_now = time.time()
        start_time = time.time()
        #blocking call
        finished = False
        while not finished:
             time_now = time.time()
             finished = True
             for i in range(len(sum_times)):
                 if (time_now - start_time < sum_times[i][-1]):
                     finished = False
        return True

    def get_transform(self, name):
        '''get transform with given name
        '''
        # YOUR CODE HERE
        trns = self.transforms[name].toList()
        for i in range(len(trns)):
            for j in range(len(trns[i][j])):
                trns[i][j] = float(trns[i][j])
        return trns

    def set_transform(self, effector_name, transform):
        '''solve the inverse kinematics and control joints use the results
        '''
        # YOUR CODE HERE
        self.set_transforms(effector_name, transform)
        return True


if __name__ == '__main__':
    agent = ServerAgent()
    agent.run()

