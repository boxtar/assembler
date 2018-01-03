# Parser for Hack Assembly Source
# Johnpaul McMahon November 2017
# TODO: Could group operations up to reduce the amount of loops through the source commands

import re

def strip_comments_and_whitespace(source_commands):
    # Strips out all comments and leading/trailing whitespace/newlines.

    # This List will contain only Assembly commands from the source file
    stripped_commands = []

    for command in source_commands:
        command = command.split('//', 1)[0]
        command = command.strip()
        if not is_comment_or_empty_line(command):
                stripped_commands.append(command)
    return stripped_commands


def is_comment_or_empty_line(string):
    # Returns True if string param is a comment or empty line.
    # Returns False otherwise.
    return string.startswith('//') or string == ''


def extract_user_labels(source_commands):
    # MUST BE CALLED BEFORE extract_user_variables
    # Loops through given list of commands and finds Labels (anything enclosed within parentheses).
    # Returns a Dict with the extracted labels and a List of commands with no labels
    labels = {}
    # Holds commands with all labels extracted
    updated_commands = []
    # Tracks current position in command list. Don't increment on finding a Label
    current_position = 0

    for i in range(len(source_commands)):
        # Cache current command
        current_command = source_commands[i]

        # Check if current command is a label
        match = re.match(r'^\((.+)\)$', current_command)

        if match:
            # If we found a label add it to labels dict (overwriting any previous version of the label)
            labels[match.group(1)] = current_position
        else:
            # If not a label then push onto commands list
            updated_commands.append(current_command)
            # and increment instruction pointer
            current_position += 1

    return labels, updated_commands


def extract_user_variables(source_commands, existing_symbols, var_base_addr=16):
    """MUST BE CALLED AFTER extract_user_labels"""
    variables = {}
    resolved_commands = []

    for command in source_commands:
        match = re.match(r'^@([\w.]+)$', command)
        # If we found an A Instruction
        if match:
            match = match.group(1)
            # If it's not a digit then we need to resolve to an address
            if not match.isdigit():
                if match in existing_symbols:
                    command = "@" + str(existing_symbols[match])
                elif match in variables:
                    command = "@" + str(variables[match])
                else:
                    variables[match] = var_base_addr
                    command = "@" + str(var_base_addr)
                    var_base_addr += 1
                
        # Every command will be added to new resolved commands list
        resolved_commands.append(command)

    return variables, resolved_commands
