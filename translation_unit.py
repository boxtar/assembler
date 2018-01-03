"""Translates Hack Symbolic Commands into Binary Instructions"""

import sys
import re

DESTINATION_INSTRUCTIONS = {
    '': '000', 'M': '001', 'D': '010', 'MD': '011',
    'A': '100', 'AM': '101', 'AD': '110', 'AMD': '111'}

COMPUTATION_INSTRUCTIONS = {
    '0': '0101010', '1': '0111111', '-1': '0111010', 'D': '0001100',
    'A': '0110000', '!D': '0001101', '!A': '0110001', '-D': '0001111',
    '-A': '0110011', 'D+1': '0011111', 'A+1': '0110111', 'D-1': '0001110',
    'A-1': '0110010', 'D+A': '0000010', 'D-A': '0010011', 'A-D': '0000111',
    'D&A': '0000000', 'D|A': '0010101', '': 'xxxxxxx', 'M': '1110000',
    '!M': '1110001', '-M': '1110011', 'M+1': '1110111', 'M-1': '1110010',
    'D+M': '1000010', 'D-M': '1010011', 'M-D': '1000111', 'D&M': '1000000',
    'D|M': '1010101'}

JUMP_INSTRUCTIONS = {
    '': '000', 'JGT': '001', 'JEQ': '101', 'JGE': '011',
    'JLT': '100', 'JNE': '101', 'JLE': '110', 'JMP': '111'}

def translate(source_commands):
    binary_commands = []
    for command in source_commands:
        if is_a_instruction(command):
            _value = a_instruction_stack.pop()
            _value = '0' + _get_bits(_value).zfill(15)
            binary_commands.append(_value)
        elif is_c_instruction(command):
            _value = c_instruction_stack.pop()
            _value = '111' + COMPUTATION_INSTRUCTIONS[_value[1]] + \
                DESTINATION_INSTRUCTIONS[_value[0]] + \
                JUMP_INSTRUCTIONS[_value[2]]
            binary_commands.append(_value)
        else:
            print("Syntax Error: ", command)
            sys.exit()
    return binary_commands



a_instruction_stack = []
a_instruction_regex = re.compile(r'^@([0-9]+)$')
def is_a_instruction(command):
    match = a_instruction_regex.findall(command)
    if match:
        a_instruction_stack.append(match[0])
        return True
    return False



c_instruction_stack = []
c_instruction_regex = re.compile(
    r'^(M=|D=|MD=|A=|AM=|AD=|AMD=)?(0|1|-1|D|A|M|!D|!A|!M|-D|-A|-M|D\+1|A\+1|M\+1|D-1|A-1|M-1|D\+A|D\+M|D-A|D-M|A-D|M-D|D&A|D&M|D\|A|D\|M){1}(;JGT|;JEQ|;JGE|;JLT|;JNE|;JLE|;JMP)?$')
def is_c_instruction(command):
    matches = c_instruction_regex.match(command)
    if matches:
        _dest = matches.group(1)[0:-1] if matches.group(1) else ''
        _comp = matches.group(2)
        _jump = matches.group(3)[1:] if matches.group(3) else ''
        c_instruction_stack.append([_dest, _comp, _jump])
        return True
    else:
        return False


def _get_bits(number):
    # Returns exact amount of bits for given decimal number
    return bin(int(number))[2:]
