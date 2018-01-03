// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Initialise iterator
@i
M=0

// Initialise the number to be added
@num_to_add
M=0

// Initialise area of RAM that will hold the result
// If not done then the result will be unreliable as add directly to R2 on each iteration
@R2
M=0

// Figure out which of R0 and R1 is smaller.
// The smaller figure will be used to determine the number of
// repetitions of the loop.
@R0
D=M
@R1
D=D-M

// if first number (R0) is smaller than second (R1) then branch
@FIRST_IS_SMALLER
D;JLT

// else if second number (R1) is smaller than first (R0) then execute below
@R1
D=M
@i
M=D

// The larger number (R0) is saved to @num_to_add for use in THE_LOOP
@R0
D=M
@num_to_add
M=D

// Variables are set - Lets branch to the loop
@THE_LOOP
0;JMP

(FIRST_IS_SMALLER)
// R0 is smaller than R1 so use that as the number of times to loop
// i.e. set @i to @R0. We will decrement @i on each iteration
@R0
D=M
@i
M=D

// The larger number (R1) is saved to @num_to_add for use in THE_LOOP
@R1
D=M
@num_to_add
M=D

(THE_LOOP)
// If i==0 branch to close off function
@i
D=M
@END
D;JEQ

// else add num_to_add to result
@num_to_add
D=M
@R2
M=M+D

// decrement i
@i
M=M-1

// back we go
@THE_LOOP
0;JMP

(END)
@END
0;JMP