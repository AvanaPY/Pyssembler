from Computer import PYComputer, Program

def get_program(file_path):
    with open(file_path, 'r') as f:
        program = Program()
        line = f.readline()
        while line:
            program(line)
            line = f.readline()
        f.close()
    return program

def main():
    computer = PYComputer()

    program = get_program('program.pys')
    computer.run_program(program)

if __name__ == '__main__':
    main()