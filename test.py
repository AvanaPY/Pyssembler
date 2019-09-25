from Computer import PYComputer, Program

def main():
    computer = PYComputer()

    program = Program()
    program('MOV 14')
    program('ADD 28')
    program('OUT')
    program('HLT')

    computer.run_program(program)

if __name__ == '__main__':
    main()