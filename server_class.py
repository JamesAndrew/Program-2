# server_class code for Raft
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
        for i in range(0, 5):
            if i != self.name:
                sqs.get_queue_by_name(QueueName='node' + i).send_message(MessageBody="append," + str(term) + "," + str(leaderId))

    def receiveAppendEntries(self):
        print("receive append entry message")

    def sendRequestVote(self, term, candidateId, lastLogIndex, lastLogTerm):
        print("send request vote message")
        for i in range(0, 5):
            if i != self.name:
                sqs.get_queue_by_name(QueueName='node' + i).send_message(MessageBody="vote," + str(term) + "," + str(candidateId))

    def processVotes(self):
        votes = 0
        queue = sqs.get_queue_by_name(QueueName='node' + str(self.name))
        messages = queue.receive_messages()
        for message in messages:
            print("msg= " + message.body)
            m_list = message.body.split(",")
            if int(m_list[1]) < self.curTerm:
                pass
            if self.votedFor == 5 or self.votedFor == m_list[2]:
                votes = votes + 1
            message.delete()

        return votes

    def receiveRequestVote(self):
        print("receive request vote message")

    def fail(self):
        print("node " + str(self.name) + " failed")

    def recover(self):
        print("node " + str(self.name) + " is recovering")

    def timeout(self):
        print("coordinator timeout")
