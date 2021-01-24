# Pyssembler
Programmable computer written in Python

The computer's Registry size can be easily changed, nothing special there. The basic functionallity of the language is that it matches
assembler a lot. There are two example programs, one that generates the fibonacci numbers up to 255 and one that prints all even
numbers up to 255. 

The available functions are:

* NOP             - Does nothing
* MOV [Address]   - Moves content from registry at address to REGISTRY_A
* ADD [Address]   - Adds value from Registry add address to REGISTRY_A
* SUB [Address]   - Subtracts value from Registry at address to REGISTRY_A
* MUL [Address]   - Subtracts value from Registry at address to REGISTRY_A
* DIV [Address]   - Divides REGISTRY_A by value in register at address
* MOD [Address]   - Multiplies REGISTRY_A by value in register at address
* OUT             - Prints out content in REGISTRY_A
* HLT             - Stops the program entirely
* JMP [LINE]      - Jumps to instruction line
* JPC [LINE]      - Jumps to instruction line if and only if there was an overflow-carry in last mathematical operation (ADD, SUB, MUL, DIV, MOD)
* JPZ [LINE]      - Jumps to instruction line if and only if the result of last methematical operation (ADD, SUB, MUL, DIV, MOD) was equal to 0
* STR [Address]   - Stores content of REGISTRY_A in register at address
* GET [Address]   - Puts content of registry at address into REGISTRY_A
