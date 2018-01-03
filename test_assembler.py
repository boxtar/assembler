"""Tests operation of assembler suite"""
import unittest
import parser
import translation_unit
from symbol_table import SYMBOL_TABLE

class TestParsingFunctionality(unittest.TestCase):
    """Tests operation of assembler suite"""

    @classmethod
    def setUpClass(cls):
        cls.initial_commands = [
            '// Regular comment\n',
            '@R0\n',
            '\n\n',
            'D=M\n\n',
            '(LABEL_TEST)\n',
            '\t@temp\n',
            '\tD=D-A\n\n',
            '\t// Random comment  \n',
            '@END\n',
            '!D;JMP\n\n',
            '(OR_TEST)\n',
            '\tD=D|M\n\n',
            '(END)\n',
            '@test.12\n',
            '  // The end\n'
        ]
        cls.stripped_commands = [
            '@R0',
            'D=M',
            '(LABEL_TEST)',
            '@temp',
            'D=D-A',
            '@END',
            '!D;JMP',
            '(OR_TEST)',
            'D=D|M',
            '(END)',
            '@test.12'
        ]
        cls.extracted_labels = {
            'LABEL_TEST': 2, 'OR_TEST': 6, 'END': 7
        }
        cls.commands_with_labels_extracted = [
            '@R0',
            'D=M',
            '@temp',
            'D=D-A',
            '@END',
            '!D;JMP',
            'D=D|M',
            '@test.12'
        ]
        cls.extracted_variables = {
            'temp': 16, 'test.12': 17
        }
        cls.commands_with_resolved_labels_and_variables = [
            '@0',
            'D=M',
            '@16',
            'D=D-A',
            '@7',
            '!D;JMP',
            'D=D|M',
            '@17'
        ]
    # End classmethod setUpClass


    def test_strips_whitespace(self):
        self.assertEqual(
            parser.strip_comments_and_whitespace(self.initial_commands), 
            self.stripped_commands)

    
    def test_extracts_user_labels(self):
        labels, commands = parser.extract_user_labels(self.stripped_commands)
        self.assertEqual(labels, self.extracted_labels)
        self.assertEqual(commands, self.commands_with_labels_extracted)

    
    def test_extracts_user_variables(self):
        existing_symbols = SYMBOL_TABLE.copy()
        existing_symbols.update(self.extracted_labels)
        variables, commands = parser.extract_user_variables(self.commands_with_labels_extracted, existing_symbols)
        self.assertEqual(variables, self.extracted_variables)
        self.assertEqual(commands, self.commands_with_resolved_labels_and_variables)
    

    def test_is_a_instruction(self):
        self.assertTrue(translation_unit.is_a_instruction("@01"))
        self.assertTrue(translation_unit.is_a_instruction("@1024"))
        self.assertFalse(translation_unit.is_a_instruction("@SCREEN"))
        self.assertFalse(translation_unit.is_a_instruction("D=M"))


    def test_is_c_instruction(self):
        self.assertTrue(translation_unit.is_c_instruction("D=M"))
        self.assertTrue(translation_unit.is_c_instruction("D=D+1;JGE"))
        self.assertTrue(translation_unit.is_c_instruction("D;JGT"))
        self.assertTrue(translation_unit.is_c_instruction("0;JMP"))
        self.assertFalse(translation_unit.is_c_instruction("@0"))
        self.assertFalse(translation_unit.is_c_instruction("// Comment"))
        self.assertFalse(translation_unit.is_c_instruction("(LABEL)"))

# End class TestParsingFunctionality


if __name__ == '__main__':
    unittest.main()
