import itertools
import multiprocessing as mp
import time
class Computer(object):
    def __init__(self, program, inputs=()):
        self.program = program
        self.inputs = iter(inputs)
        self.pointer = 0
        self.running = None
        self.MODE_LENGTH = 3
        self.OPCODE_LENGTH = 2
        self.output = None
        self.halted = False

        self.OPCODES = {
            1: self.add,
            2: self.multiply,
            3: self.input_,
            4: self.output_,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equal,
            99: self.end}

        self.NUM_OF_PARAMS = {
            1: 3,
            2: 3, 
            3: 1,
            4: 1,
            5: 2,
            6: 2,
            7: 3,
            8: 3,
            99: 0}

        self.MODE_DICT = {
            0: self.position,
            1: self.immediate}

        self.OPCODES_WITH_JUMP = set((5, 6))

    def parameter_mode(self, location):
        instruction = format(self.program[location], "0" + str(self.MODE_LENGTH + self.OPCODE_LENGTH) + "d")
        OPCODE = int(instruction[-1*self.OPCODE_LENGTH:])
        modes = []
        for i in range(self.MODE_LENGTH):
            modes.append(int(instruction[i]))
        return modes, OPCODE

    def position(self, location):
        return self.program[location]

    def immediate(self, location):
        return location

    def add(self, p1, p2, p3):
        self.program[p3] = self.program[p1] + self.program[p2] 
    
    def multiply(self, p1, p2, p3):
        self.program[p3] = self.program[p1] * self.program[p2]

    def input_(self, p1):
        self.program[p1] = next(self.inputs)

    def output_(self, p1):
        self.output = self.program[p1]
        self.running = False

    def jump_if_true(self, p1, p2):
        if self.program[p1] != 0:
            self.pointer = self.program[p2]
    
    def jump_if_false(self, p1, p2):
        if self.program[p1] == 0:
            self.pointer = self.program[p2]

    def less_than(self, p1, p2, p3):
        if self.program[p1] < self.program[p2]:
            self.program[p3] = 1
        else:
            self.program[p3] = 0

    def equal(self, p1, p2, p3):
        if self.program[p1] == self.program[p2]:
            self.program[p3] = 1
        else:
            self.program[p3] = 0

    def end(self):
        self.running = False
        self.halted = True

    def get_parameters(self, modes, OPCODE):
        parameters = []
        for i in range(1, self.NUM_OF_PARAMS[OPCODE] + 1):
            mode = modes[self.MODE_LENGTH - i]
            parameters.append(self.MODE_DICT[mode](self.pointer + i))
        return parameters

    def check_if_halted(self):
        if self.prev_pointer == self.pointer:
            self.halted = True
            self.running = False

    def update_input(self, new_input):
        self.inputs = iter([new_input])

    def run(self):
        self.running = True
        while self.running:
            modes, OPCODE = self.parameter_mode(self.pointer)
            parameters = self.get_parameters(modes, OPCODE)
            self.prev_pointer = self.pointer
            self.OPCODES[OPCODE](*parameters)
            if OPCODE not in self.OPCODES_WITH_JUMP:
                self.pointer += self.NUM_OF_PARAMS[OPCODE] + 1
            self.check_if_halted()
        return self.output, self.halted


class Amplifier(Computer):
    def __init__(self, phase_setting, input_sequence):
        amp_control_software = [3,8,1001,8,10,8,105,1,0,0,21,42,59,76,85,106,187,268,349,430,99999,3,9,102,3,9,9,1001,9,2,9,1002,9,3,9,1001,9,3,9,4,9,99,3,9,102,3,9,9,101,3,9,9,1002,9,2,9,4,9,99,3,9,102,3,9,9,1001,9,4,9,1002,9,5,9,4,9,99,3,9,102,2,9,9,4,9,99,3,9,101,3,9,9,1002,9,2,9,1001,9,4,9,1002,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,99]
        super(Amplifier, self).__init__(amp_control_software, inputs=(phase_setting, input_sequence))


def amp_chain(phase_settings):
    input_sequence = 0
    for setting in phase_settings:
        amp = Amplifier(setting, input_sequence)
        input_sequence = amp.run()
    return input_sequence


def amp_chain_with_feedback(phase_settings):
    input_sequence = 0
    amps = []
    amp_number = 0
    for setting in phase_settings:
        amps.append(Amplifier(setting, input_sequence))
        input_sequence, halted = amps[-1].run()
    while not halted:
        amps[amp_number].update_input(input_sequence)
        input_sequence, halted = amps[amp_number].run()
        if halted:
            if amp_number == 4:
                return input_sequence
            else:
                halted = False
        if amp_number == 4:
            amp_number = 0
        else:
            amp_number += 1

def get_max_output(feedback=False):
    start = time.time()
    best_max = 0
    if feedback:
        perm = [5, 6, 7, 8, 9]
    else:
        perm = [0, 1, 2, 3, 4]
    for setting in itertools.permutations(perm):
        if feedback:
            result = amp_chain_with_feedback(setting)
        else:
            result = amp_chain(setting)
        if result > best_max:
            best_max = result
    return best_max, time.time() - start
                        
def mp_max_output(feedback=False):
    start = time.time()
    pool = mp.Pool(processes=mp.cpu_count())
    if feedback:
        perm = [5, 6, 7, 8, 9]
        results = [pool.apply(amp_chain_with_feedback, args=(setting, )) for setting in itertools.permutations(perm)]
    else:
        perm = [0, 1, 2, 3, 4]
        results = [pool.apply(amp_chain, args=(setting, )) for setting in itertools.permutations(perm)]
    return max(results), time.time() - start
#print(amp_chain_with_feedback([9,8,7,6,5]))
feedback = True
print(mp_max_output(feedback=feedback))
print(get_max_output(feedback=feedback))
