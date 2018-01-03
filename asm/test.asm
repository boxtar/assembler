// Test program for testing Assembler

(_INIT)
    // Save RAM[0] into counter
    @R0
    D=A
    @counter
    M=D

    // Init to 0 temp
    @0
    D=A 
    @temp 
    M=D

(MAIN)
    // temp - 10
    @temp
    D=A
    @10
    D=D-A

    // end program if temp - 10 Equals 0 (i.e temp reached 10)
    @END
    D;JEQ

    @MAIN
    0;JMP

(END)
    @END
    0;JMP

