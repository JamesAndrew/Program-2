# server code for Raft
from threading import Timer
import random
import boto3

import server_class

def checkClientMessages():
    queue = sqs.get_queue_by_name(QueueName='p0')

# create server object
s = server_class.Server()
s.start_timer()
sqs = boto3.resource('sqs')

# main loop of Server
loop = True
while loop:
    # code for all servers
    if s.commitIndex > s.lastApplied:
            s.lastApplied = s.lastApplied + 1
            s.state = s.log[lastApplied]
            
    # code for followers
    if s.role == 0:
        s.processMessages()
        if s.getTimer() == False:
            s.role = 1
            print("I am becoming a candidate")
            s.curTerm = s.curTerm + 1
            s.votedFor = s.name
            s.start_timer()
            s.sendRequestVote(s.curTerm,s.getName(),1,1)
        
    # code for candidates
    elif s.role == 1:
        s.processMessages()
        print("I am a candidate")
        if s.processVotes():
            s.role = 2
            print("I am becoming a leader")
            s.sendAppendEntries(s.curTerm, s.getName(),1,1,1,1)

    # code for leaders
    elif s.role == 2:
        print("I am a leader");
        s.sendAppendEntries(s.curTerm, s.getName(),1,1,1,1)
        s.running = False
        sqs.get_queue_by_name(QueueName='node1').send_message(MessageBody="end")

    # error
    else:
        print("role " + str(s.role) + " does not exist");

    if s.running == False:
        loop = False
        
