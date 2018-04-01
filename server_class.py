# server_class code for Raft
from threading import Timer
import random
import boto3

sqs = boto3.resource('sqs')

class Server:
    running = False
    name = 0

    timer = False
    
    # role: 0 - follower (initialized), 1 = candidate, 2 = leader, or otherwise error
    role = 0
    
    # persitent state
    curTerm = 0
    votedFor = 5 # 5 indicates a null value
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
        print("node " + str(self.name) + " timer started")
        self.timer = True
        t = Timer(random.uniform(0.15, 0.3), self.out_of_time)
        t.start()

    def out_of_time(self):
        print("node " + str(self.name) + " timer ended")
        self.timer = False

    def checkTerm(self, T):
        print("term check")
        if T > self.curTerm:
            self.curTerm = T
            self.role = 0

    def sendAppendEntries(self, term, leaderId, prevLogIndex, prevLogTerm, entries, leaderCommit):
        self.checkTerm(term)
        print("send append entry message")
        for i in range(0, 5):
            if i != self.name:
                sqs.get_queue_by_name(QueueName='node' + str(i)).send_message(MessageBody="append," + str(term) + "," + str(leaderId))

    def receiveAppendEntries(self):
        #self.checkTerm(term)
        print("receive append entry message")
        self.role = 0
        self.start_timer()

    def sendRequestVote(self, term, candidateId, lastLogIndex, lastLogTerm):
        self.checkTerm(term)
        print("send request vote message")
        for i in range(0, 5):
            sqs.get_queue_by_name(QueueName='node' + str(i)).send_message(MessageBody="voteR," + str(term) + "," + str(candidateId))

    def receiveRequestVote(self, v):
        print("receive request vote message")
        msg = v.split(",")
        if self.votedFor == "5" or self.votedFor == msg[2]:
            sqs.get_queue_by_name(QueueName='node' + str(self.name)).send_message(MessageBody="vote," + str(msg[1]) + "," + str(msg[2]))
            self.votedFor = int(msg[2]);
            self.start_timer()
        self.checkTerm(int(msg[1]))

    def processVotes(self):
        print("processing votes")
        votes = 0
        queue = sqs.get_queue_by_name(QueueName='node' + str(self.name))
        messages = queue.receive_messages()
        for message in messages:
            m_list = message.body.split(",")
            print(m_list)
            if m_list[0] == "vote" and m_list[2] == self.name:
                votes = votes + 1

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

    def fail(self):
        print("node " + str(self.name) + " failed")

    def recover(self):
        print("node " + str(self.name) + " is recovering")

    def timeout(self):
        print("coordinator timeout")
