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
turn = 10
while loop:
    if turn == 0:
        loop = False
        
    # code for all servers
    if s.commitIndex > s.lastApplied:
            s.lastApplied = s.lastApplied + 1
            
    # code for followers
    if s.role == 0:
        #s.processMessages()
        if s.getTimer() == False:
            s.role = 1
        
    # code for candidates
    
    elif s.role == 1:
        
        print("I am a candidate")
        s.curTerm = s.curTerm + 1
        s.votedFor = s.name
        s.start_timer()
        s.sendRequestVote(s.curTerm,s.getName(),1,1)
        

    # code for leaders
    elif s.role == 2:
        print("I am a leader");
        s.sendAppendEntries(s.curTerm, s.getName(),1,1,1,1)

    # error
    else:
        print("role " + str(s.role) + " does not exist");

    turn = turn - 1
