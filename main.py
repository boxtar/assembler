"""Drives the translation process from Hack ASM to Hack Binary Instructions"""
# Johnpaul McMahon
# November 2017

import sys
import parser
import translation_unit
from symbol_table import SYMBOL_TABLE


# Check for file name
if len(sys.argv) != 2:
    print("Usage: Main.py file.asm")
    sys.exit()

# If we got here then we have a file name to work with
IN_FILE = sys.argv[1]

# Check input file's extension
if not IN_FILE.endswith('.asm'):
    print("Input file must end in '.asm'")
    sys.exit()

# Set output file name
OUT_FILE = IN_FILE[0:-4] + '.hack'

# Will eventually hold the binary translation
COMMANDS = []

# Strip comments and blanks
with open(IN_FILE) as filename:
    COMMANDS = parser.strip_comments_and_whitespace(filename.readlines())

# Extract User defined Labels from commands. Also returns commands with User labels stripped out
LABELS, COMMANDS = parser.extract_user_labels(COMMANDS)
SYMBOL_TABLE.update(LABELS)

VARIABLES, COMMANDS = parser.extract_user_variables(COMMANDS, SYMBOL_TABLE)
SYMBOL_TABLE.update(VARIABLES)

COMMANDS = translation_unit.translate(COMMANDS)

with open(OUT_FILE, 'w') as output_file:
    for command in COMMANDS:
        output_file.write(command + '\n')
