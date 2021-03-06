# server code for Raft
from threading import Timer
import random
import boto3

import server_class

def checkClientMessages():
    queue = sqs.get_queue_by_name(QueueName='p0')

def election():
    print("election started")
    s.curTerm = int(s.curTerm) + 1
    s.start_timer()
    s.sendRequestVote(s.curTerm,s.getName(),1,1)

# create server object
s = server_class.Server()
s.start_timer()
sqs = boto3.resource('sqs')

if s.name == 0:
    # set timer for node failure
    ti = Timer(5.0, s.fail())

    # set timer for leader timeout
    timeout = Timer(10.0, s.fail())

# main loop of Server
loop = True
count = 30
while loop:
    if s.running == True:
        print("term " + str(s.curTerm))
        # code for all servers
        if s.commitIndex > s.lastApplied:
                s.lastApplied = s.lastApplied + 1
                s.state = s.log[lastApplied]
        s.checkMessages()
                
        # code for followers
        if s.role == 0:
            print("I am a follower")
            s.processMessages()
            if s.getTimer() == False:
                s.role = 1
                print("I am becoming a candidate")
                election()
            
        # code for candidates
        elif s.role == 1:
            print("I am a candidate")
            if s.processVotes():
                s.role = 2
                s.cancel_timer()
                print("I am becoming a leader")
                s.sendAppendEntries(s.curTerm, s.getName(),1,1,1,1)
            elif s.getTimer() == False:
                election()

        # code for leaders
        elif s.role == 2:
            print("I am a leader");
            s.sendAppendEntries(s.curTerm, s.getName(),1,1,1,1)
            sqs.get_queue_by_name(QueueName='node1').send_message(MessageBody="end")

        # error
        else:
            print("role " + str(s.role) + " does not exist");
