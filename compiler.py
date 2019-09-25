from Computer import PYComputer, Program

def get_fibonacci():
    fibonacci_program = Program()
    fibonacci_program('MOV 1')   #0
    fibonacci_program('STR 14')  #1  y = 1
    fibonacci_program('MOV 0')   #2  x = 0
    fibonacci_program('OUT')     #3  print
    fibonacci_program('ADD 14')  #4  |+ y
    fibonacci_program('STR 15')  #5  |z = x + y
    fibonacci_program('GET 14')  #6   | 
    fibonacci_program('STR 13')  #7   | x = y
    fibonacci_program('GET 15')  #8  | 
    fibonacci_program('STR 14')  #9  | y = z
    fibonacci_program('GET 13')  #10  | x
    fibonacci_program('JPC 0')   #11
    fibonacci_program('JMP 3')   #12
                                 #13 x
                                 #14 y
                                 #15 z
    return fibonacci_program

def get_even_numbers():
    program = Program()
    program('MOV 1')   #0
    program('STR 15')  #1 Store incremental value at 15
    program('MOV 2')   #2
    program('STR 14')  #3 Store even-check value at 14
    program('GET 13')  #4 Load x
    program('ADD 15')  #5 Add increment
    program('STR 13')  #6 Store value at 13
    program('MOD 14')  #7 Check even
    program('JPZ 10')  #8 
    program('JMP 4')   #9
    program('GET 13')  #10
    program('OUT')     #11
    program('JMP 5')   #12
    
    return program

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