import re
import threading
import time
class INSTRUCTION:
    def __init__(self, NAME, REQUIRES_VALUE, INSTRUCTION_CODE):
        self.NAME = NAME
        self.REQUIRES_VALUE = REQUIRES_VALUE
        self.INSTRUCTION_CODE = INSTRUCTION_CODE
    def __str__(self):
        return f'INSTRUCTION: {self.NAME}'

class COMPILED_INSTRUCTION:
    def __init__(self, INSTRUCTION_NUMBER, INSTRUCTION, VALUE=None):
        self.INSTRUCTION_NUMBER = INSTRUCTION_NUMBER
        self.INSTRUCTION_CODE = INSTRUCTION.INSTRUCTION_CODE
        self.VALUE = VALUE
    def __str__(self):
        if self.VALUE:
            return f'{self.INSTRUCTION_NUMBER} ' + bin(self.INSTRUCTION_CODE)[2:].zfill(4) + ' ' + bin(self.VALUE)[2:].zfill(4)
        else:
            return f'{self.INSTRUCTION_NUMBER} ' + bin(self.INSTRUCTION_CODE)[2:].zfill(4)

class Program:
    def __init__(self):
       self.CODE = []
       self.COMPILED = []
       self.INSTRUCTIONS = [
           INSTRUCTION('NOP', False, 0),
           INSTRUCTION('MOV', True, 1),
           INSTRUCTION('ADD', True,  2),
           INSTRUCTION('SUB', True,  3),
           INSTRUCTION('OUT', False, 4),
           INSTRUCTION('HLT', False, 5),
           INSTRUCTION('JMP', True, 6),
           INSTRUCTION('JPC', True, 7),
           INSTRUCTION('JPZ', True, 8),
           INSTRUCTION('STR', True, 9),
           INSTRUCTION('GET', True, 10),
       ]

    def __call__(self, ASSEMBLY_CODE):
        self.CODE.append(ASSEMBLY_CODE)

    def COMPILE(self):
        print('Compiling program...')
        for ASSEMBLY_CODE in self.CODE:
            ASSEMBLY_CODE = ASSEMBLY_CODE.strip()
            ASSEMBLY_CODE = re.sub(' +', ' ', ASSEMBLY_CODE)
            ASSEMBLY_CODE = ASSEMBLY_CODE.split(' ')
            if not self.__CHECK_VALID(ASSEMBLY_CODE):
                return False
        print('Compiling successful')
        return True


    def __GET_INSTRUCTION(self, INSTRUCTION_NAME):
        for INSTRUCTION in self.INSTRUCTIONS:
            if INSTRUCTION.NAME == INSTRUCTION_NAME:
                return INSTRUCTION
        return None

    def __CHECK_VALID(self, ASSEMBLY_CODE):
        INSTRUCTION_NAME = ASSEMBLY_CODE[0]
        INSTRUCTION = self.__GET_INSTRUCTION(INSTRUCTION_NAME)
        if INSTRUCTION == None:
            print(f'COMPILE ERROR: UNKNOWN COMMAND "{INSTRUCTION_NAME}"')
            return False
        if INSTRUCTION.REQUIRES_VALUE:
            if len(ASSEMBLY_CODE) > 1:
                INSTRUCTION_VALUE = int(ASSEMBLY_CODE[1])
            else:
                print(f'COMPILE ERROR: INSTRUCTION "{INSTRUCTION_NAME}" REQUIRES A VALUE BUT DID NOT RECEIVE ONE')
                return False
        else:
            INSTRUCTION_VALUE = None
        self.COMPILED.append(COMPILED_INSTRUCTION(len(self.COMPILED), INSTRUCTION, INSTRUCTION_VALUE))
        return True

class PYComputer:
    def __init__(self):
        self.REGISTER_SIZE = 0x10 # Register fits 16 instructions and values
        self.REGISTER = [0 for i in range(self.REGISTER_SIZE)]
        self.REGISTER_A = 0xff
        self.PROGRAM_COUNTER = 0
        self.FLAGS = {
            'Z': False, # Flag for value of register A is 0
            'C': False, # Flag for bit overflow
        }
        self.OPERATIONS = [
            self.__NOP,
            self.__MOV,
            self.__ADD,
            self.__SUB,
            self.__OUT,
            self.__HLT,
            self.__JMP,
            self.__JPC,
            self.__JPZ,
            self.__STR,
            self.__GET
        ]
    def run_program(self, program: Program):
        if not program.COMPILE():
            print('EXECUTION ERROR: FAILED TO COMPILE PROGRAM, EXITING')
            return
        i = 0
        for code in program.COMPILED:
            if not self.__ADD_TO_REG(code, i):
                return
            i += 1
        print(f'Program loaded successfully')
        thread = threading.Thread(target=self.__EXECUTE(), args=())
        thread.start()
        thread.join()
        
    def __EXECUTE(self):
        self.PROGRAM_COUNTER = 0
        while self.PROGRAM_COUNTER < len(self.REGISTER):
            INSTRUCTION = self.REGISTER[self.PROGRAM_COUNTER]
            if isinstance(INSTRUCTION, COMPILED_INSTRUCTION):
                idx, val = INSTRUCTION.INSTRUCTION_CODE, INSTRUCTION.VALUE
                self.OPERATIONS[idx](val)
            self.PROGRAM_COUNTER += 1
            time.sleep(0.1)
        
    def __ADD_TO_REG(self, ADD, POSITION):
        if POSITION >= self.REGISTER_SIZE:
            print(f'EXECUTION ERROR: ERROR REGISTER OUT OF MEMORY')
            return False
        self.REGISTER[POSITION] = ADD
        return True

    def __NOP(self, *args):
        pass

    def __MOV(self, *args):
        self.REGISTER_A = args[0]
        
    # Adds register at address to register A
    def __ADD(self, *args):
        self.REGISTER_A = self.REGISTER_A + self.REGISTER[args[0]]
        self.__CHECK_FLAGS()

    def __SUB(self, *args):
        self.REGISTER_A = self.REGISTER_A - self.REGISTER[args[0]]
        self.__CHECK_FLAGS()

    # Prints Register A's value
    def __OUT(self, *args):
        print(self.REGISTER_A)

    # Halts current program by setting program counter to the length of register
    # TODO: Fix this sheit, improve
    def __HLT(self, *args):
        self.PROGRAM_COUNTER = len(self.REGISTER)
        
    def __JMP(self, *args):
        self.PROGRAM_COUNTER = args[0]

    # Jump if carry
    def __JPC(self, *args):
        if self.FLAGS['C']:
            self.PROGRAM_COUNTER = args[0]
            print('JPC')

    # Jump if Zero
    def __JPZ(self, *args):
        if self.FLAGS['Z']:
            self.PROGRAM_COUNTER = args[0]

    # Store Register A at register address
    def __STR(self, *args):
        self.REGISTER[args[0]] = self.REGISTER_A

    def __GET(self, *args):
        self.REGISTER_A = self.REGISTER[args[0]]
        self.__CHECK_FLAGS()

    def __CHECK_FLAGS(self):
        self.FLAGS['Z'] = self.REGISTER_A == 0
        if self.REGISTER_A > 0xff or self.REGISTER_A < 0:
            self.REGISTER_A %= 0x100
            self.FLAGS['C'] = True
        else:
            self.FLAGS['C'] = False