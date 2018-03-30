class Robot:
    name = 0
    blocking_with_left = False
    blocking_with_right = False

    def __init__(self):
        print("new robot")

    def punch_with_left(self):
        print("robot " + str(self.name) + "punched with left fist")

    def punch_with_right(self):
        print("robot " + str(self.name) + "punched with right fist")

    def block_with_left(self):
        print("robot " +str(self.name) + "blocked with left")

    def block_with_right(self):
        print("robot " +str(self.name) + "blocked with right")
