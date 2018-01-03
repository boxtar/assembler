// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// set the last screen memory location
// KBD immediately follows the SCREEN
@KBD
D=A-1
@screen_max
M=D

(MAIN)
    @SCREEN
    D=A
    // first screen memory location
    @screen_ptr
    M=D

    (FILL_SCREEN)
        // fetch keyboard status
        @KBD
        D=M

        // color white if no key pressed        
        @COLOR_WHITE
        D;JEQ

        // else color black
        (COLOR_BLACK) 
            @screen_ptr
            A=M
            M=-1

        @CHECK_SCREEN_POSITION
        0;JMP

        (COLOR_WHITE)
            @screen_ptr
            A=M
            M=0

        (CHECK_SCREEN_POSITION)
            // if reached end of screen, reset screen pointer
            @screen_ptr
            D=M
            @screen_max
            D=D-M
            @MAIN
            D;JGT

            // else increment screen pointer and continue filling
            @screen_ptr 
            M=M+1
            @FILL_SCREEN
            0;JMP
