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

def main():
    computer = PYComputer()

    program = get_fibonacci()
    computer.run_program(program)

if __name__ == '__main__':
    main()