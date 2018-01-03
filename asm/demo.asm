// Set arrays base address to start of screen space
@SCREEN
D=A
@arr
M=D

// The number of times to repeat loop set by user
@R0
D=M
@length
M=D

// Setup counter
@i
M=0

(ARRAY_FILL)
// if ( i == length ) goto END
@i
D=M
@length
D=D-M
@END
D;JEQ

// Set arr[i] = -1
// In other words: RAM[arr+i] = -1
// In other other words: SCREEN[i*32] = -1
@arr
A=M
M=-1

// arr += 32 (32 registers per 1 row so this moves us to next row on screen)
@32
D=A
@arr
M=M+D

// i++
@i
M=M+1

// Back to start of loop
@ARRAY_FILL
0;JMP

(END)
@END
0;JMP

