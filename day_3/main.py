
class wirepaths(object):

    def __init__(self):
        self.prev_coord = None
        self.current_coord = None
        self.wire_directions = None
        self.wire_trace = None
        self.paths_crossed = None

    def read(self, path):
        self.wire_directions = {}
        with open(path, "r") as f:
            for i, line in enumerate(f):
                self.wire_directions[i] = line.split(",")
    
    def move(self, instruction, wirenum):
        if "\n" in instruction:
            instruction = instruction.split("\n")[0]
        if instruction[0] == "R":
            self.move_right(int(instruction[1:]), wirenum)
        if instruction[0] == "L":
            self.move_left(int(instruction[1:]), wirenum)
        if instruction[0] == "U":
            self.move_up(int(instruction[1:]), wirenum)
        if instruction[0] == "D":
            self.move_down(int(instruction[1:]), wirenum)
    
    def move_right(self, amount, wirenum):
        self.wire_trace[wirenum] = [[i, self.prev_coord[wirenum][1]] for i in range(self.prev_coord[wirenum][0], amount)]
        self.current_coord[wirenum][0] += amount
        self.prev_coord[wirenum] = self.current_coord[wirenum]

    def move_left(self, amount, wirenum):
        self.wire_trace[wirenum] = [[i, self.prev_coord[wirenum][1]] for i in range(self.prev_coord[wirenum][0]- amount, self.prev_coord[wirenum][0])]
        #print(self.wire_trace[0])
        self.current_coord[wirenum][0] -= amount
        self.prev_coord[wirenum] = self.current_coord[wirenum]

    def move_up(self, amount, wirenum):
        self.wire_trace[wirenum] = [[self.prev_coord[wirenum][0], j] for j in range(self.prev_coord[wirenum][1], amount)]
        self.current_coord[wirenum][1] += amount
        self.prev_coord[wirenum] = self.current_coord[wirenum]

    def move_down(self, amount, wirenum):
        self.wire_trace[wirenum] = [[self.prev_coord[wirenum][0], j] for j in range(self.prev_coord[wirenum][1] - amount, self.current_coord[wirenum][1])]
        self.current_coord[wirenum][1] += amount
        self.prev_coord[wirenum] = self.current_coord[wirenum]

    def check_crossing(self):
        print(self.wire_trace)
        for trace0 in self.wire_trace[0]:
            for trace1 in self.wire_trace[1]:
                if trace0[0] == trace1[0]:
                    if trace0[1] == trace1[1]:
                        print(trace0)
                        self.paths_crossed.append(trace0)
    
    def run(self):
        self.wire_trace = {}
        self.wire_trace[0] = []
        self.wire_trace[1] = []
        self.paths_crossed = []
        self.prev_coord = {}
        self.current_coord = {}
        self.prev_coord[0] = [0, 0]
        self.prev_coord[1] = [0, 0]
        self.current_coord[0] = [0, 0]
        self.current_coord[1] = [0, 0]
        for i in range(len(self.wire_directions[0])):
            self.move(self.wire_directions[0][i], 0)
            self.move(self.wire_directions[1][i], 1)
        print(self.paths_crossed)


wp = wirepaths()
wp.read("data2.dat")
wp.run()