# server code for Raft
from threading import Timer
import random
import boto3

class Server:
    name = 0

    timer = False
    
    # role: 0 - follower (initialized), 1 = candidate, 2 = leader, or otherwise error
    role = 0
    
    # persitent state
    curTerm = 0
    votedFor = 0
    log = []

    # volatile state
    commitIndex = 0
    lastApplied = 0

    # volatile state for leaders
    nextIndex = []
    matchIndex = []

    def __init__(self):
        self.name = input("server name: ")
        print("new server " + str(self.name) + " added")

    def getName(self):
        return self.name

    def getTimer(self):
        return self.timer

    def start_timer(self):
        print("node " + str(self.name) + " timer started")
        self.timer = True
        t = Timer(random.uniform(0.15, 0.3), self.out_of_time)
        t.start()

    def out_of_time(self):
        print("node " + str(self.name) + " timer ended")
        self.timer = False

    def sendAppendEntries(self, term, leaderId, prevLogIndex, prevLogTerm, entries, leaderCommit):
        print("send append entry message")

    def receiveAppendEntries(self):
        print("receive append entry message")

    def sendRequestVote(self, term, candidateId, lastLogIndex, lastLogTerm):
        print("send request vote message")
        queue = sqs.get_queue_by_name(QueueName='node0')
        queue.send_message(MessageBody= str(term) + "," + str(candidateId))

    def processMessages(self):
        queue = sqs.get_queue_by_name(QueueName='node' + str(self.name))
        messages = queue.receive_messages()
        for message in messages:
            print("msg= " + message.body)
            m_list = message.body.split(",")
            #if int(m_list[0]) < self.curTerm:
            sqs.get_queue_by_name(QueueName='node0').send_message(MessageBody="notvoting")
            message.delete()        

    def receiveRequestVote(self):
        print("receive request vote message")

    def fail(self):
        print("node " + str(self.name) + " failed")

    def recover(self):
        print("node " + str(self.name) + " is recovering")

    def timeout(self):
        print("coordinator timeout")

# create server object
s = Server()
s.start_timer()
sqs = boto3.resource('sqs')

# main loop of Server
loop = True
turn = 5
while loop:
    if turn == 0:
        loop = False
    # code for all servers
    if s.commitIndex > s.lastApplied:
            s.lastApplied = s.lastApplied + 1
            
    # code for followers
    if s.role == 0:
        s.processMessages()
        if s.getTimer() == False:
            s.role = 1
        
    # code for candidates
    
    elif s.role == 1:
        
        print("I am a candidate")
        s.curTerm = s.curTerm + 1
        s.votedFor = s.name
        s.start_timer()
        s.sendRequestVote(s.curTerm,s.getName(),1,1)
        queue = sqs.get_queue_by_name(QueueName='node0')
        messages = queue.receive_messages()
        for message in messages:
            print("msg= " + message.body)
            message.delete()

    # code for leaders
    elif s.role == 2:
        print("I am a leader");

    # error
    else:
        print("role " + str(s.role) + " does not exist");

    turn = turn - 1
