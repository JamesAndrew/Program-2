# load robot class
import robot
import boto3

# load AWS s3 for and sqs
s3 = boto3.resource('s3')
sqs = boto3.resource('sqs')

# create player
r0 = robot.Robot()

# main loop of game
loop = True
while loop:
    option = input("action: ")
    if option == "0":
        loop = False
    elif option == "t":
        print "test"
    elif option == "q":
        r0.punch_with_left()
    elif option == "w":
        r0.punch_with_right()
    elif option == "a":
        r0.block_with_left()
    elif option == "s":
        r0.block_with_right()
    else:
        print("invalid command")

print("Thank you for playing, goodbye!")
