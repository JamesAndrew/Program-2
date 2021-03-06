# server_class code for Raft
from threading import Timer
import random
import boto3

sqs = boto3.resource('sqs')

class Server:
    t = 0
    running = False
    name = 0

    timer = False
    
    # role: 0 - follower (initialized), 1 = candidate, 2 = leader, or otherwise error
    role = 0
    
    # persitent state
    curTerm = 0
    log = []
    state = ""

    # volatile state
    commitIndex = 0
    lastApplied = 0

    # volatile state for leaders
    nextIndex = []
    matchIndex = []

    def __init__(self):
        self.name = input("server name: ")
        print("new server " + str(self.name) + " added")
        self.running = True 

    def getName(self):
        return self.name

    def getTimer(self):
        return self.timer

    def start_timer(self):
        self.timer = True
        rand = random.uniform(0.3, 1.0)
        self.t = Timer(rand, self.out_of_time)
        self.t.start()
        print("node " + str(self.name) + " timer started for " + str(rand) + "s")

    def out_of_time(self):
        print("node " + str(self.name) + " timer ended")
        self.timer = False

    def cancel_timer(self):
        self.t.cancel()

    def checkTerm(self, T):
        print("term check")
        if T > int(self.curTerm):
            self.curTerm = T
            self.role = 0

    def sendAppendEntries(self, term, leaderId, prevLogIndex, prevLogTerm, entries, leaderCommit):
        print("send append entry message")
        self.checkTerm(term)
        for i in range(0, 5):
            if i != self.name:
                sqs.get_queue_by_name(QueueName='node' + str(i)).send_message(MessageBody="append," + str(term) + "," + str(leaderId))

    def receiveAppendEntries(self, a):
        print("receive append entry message")
        print(a)
        msg = a.split(",")
        self.checkTerm(int(msg[1]))        
        self.role = 0
        self.start_timer()
        if msg[1] < curTerm:
            pass

    def sendRequestVote(self, term, candidateId, lastLogIndex, lastLogTerm):
        self.checkTerm(term)
        print("send request vote message")
        for i in range(0, 5):
            if i != self.name:
                sqs.get_queue_by_name(QueueName='node' + str(i)).send_message(MessageBody="voteR," + str(term) + "," + str(candidateId))

    def receiveRequestVote(self, v):
        print("receive request vote message")
        print(v)
        msg = v.split(",")
        self.checkTerm(int(msg[1]))
        if int(msg[1]) < int(self.curTerm):
            pass
        else:
            print("vote, " + str(msg[1]) + "," + str(msg[2]))
            sqs.get_queue_by_name(QueueName='node' + str(self.name)).send_message(MessageBody="vote," + str(msg[1]) + "," + str(msg[2]))
            self.start_timer()

    def processVotes(self):
        print("processing votes")
        votes = 1
        queue = sqs.get_queue_by_name(QueueName='node' + str(self.name))
        messages = queue.receive_messages()
        for message in messages:
            m_list = message.body.split(",")
            print(m_list)
            if m_list[0] == "vote" and int(m_list[2]) == int(self.name):
                votes = votes + 1

        print(str(votes) + " votes received")
        if votes > 1:
            return True
        else:
            return False

    def processMessages(self):
        queue = sqs.get_queue_by_name(QueueName='node' + str(self.name))
        messages = queue.receive_messages()
        for message in messages:
            m_list = message.body.split(",")
            if m_list[0] == "voteR":
                self.receiveRequestVote(message.body)
            elif m_list[0] == "append":
                self.receiveAppendEntries(message.body)
            elif m_list[0] == "end":
                self.running = False

    def checkMessages(self):
        queue = sqs.get_queue_by_name(QueueName='node' + str(self.name))
        messages = queue.receive_messages()
        for message in messages:
            m_list = message.body.split(",")
            if int(m_list[1]) > int(self.curTerm):
                self.curTerm = int(m_list[1])
                self.role = 0
                self.start_timer()
    
    def fail(self):
        print("node " + str(self.name) + " failed")
        self.running = False
        t = Timer(5, self.recover())
        t.start()

    def recover(self):
        print("node " + str(self.name) + " is recovering")
        self.running = True

    def timeout(self):
        print("coordinator timeout")
        self.running = False
        t = Timer(1, self.recover())
        t.start()
