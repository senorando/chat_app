import sys
sys.path.append("..")

import unittest
from bot import chatBot

class unmocked_tests(unittest.TestCase):
    
    def test_about(self):
        bot = chatBot()
        ABOUT_EXP = "Welcome to \"Not Discord\"! My name is BimboBOT and I'm here to help you out with different things. Just type [!!help] to learn more about what I can do!"
        
        self.assertEqual(bot.command('!!about'), bot.command('!! about'), ABOUT_EXP)
        
    def test_help(self):
        bot = chatBot()
        HELP_EXP = "All commands start with !! and are followed by the command with or without a space: !! about: Tells you about me! I'm not very interesting though :(, !! yoda [message] : Translates your message to yoda!"
        
        self.assertEqual(bot.command('!!help'), bot.command('!! help'), HELP_EXP)
    
    def test_upper_about(self):
        bot = chatBot()
        ABOUT_EXP = "Welcome to \"Not Discord\"! My name is BimboBOT and I'm here to help you out with different things. Just type [!!help] to learn more about what I can do!"
        
        self.assertEqual(bot.command('!!ABOUT'), bot.command('!! ABOUT'), ABOUT_EXP)
        
    def test_upper_help(self):
        bot = chatBot()
        HELP_EXP = "All commands start with !! and are followed by the command with or without a space: !! about: Tells you about me! I'm not very interesting though :(, !! yoda [message] : Translates your message to yoda!"
        
        self.assertEqual(bot.command('!!HELP'), bot.command('!! HELP'), HELP_EXP)
    
    def test_bad_command(self):
        bot = chatBot()
        expected = "Command not recognized. Please try one of these: !! [about|help|yoda]"
        
        self.assertEqual(bot.command('!!helps'), bot.command('!!abouts'), expected)
    
    def test_int_input(self):
        bot = chatBot()
        INT_INPUT = [30, -1, 20000000, 0, 1]
        
        for test in INT_INPUT:
            self.assertRaises(AttributeError, bot.command, test)
    
    def test_bool_input(self):
        bot = chatBot()
        BOOL_INPUT = [True, False]
        
        for test in BOOL_INPUT:
            self.assertRaises(AttributeError, bot.command, test)
    
    def test_list_input(self):
        bot = chatBot()
        LIST_INPUT = [['a', 'b', 'c'], ['e', 'f', 'g'], ['h', 'i', 'j']]
        
        for test in LIST_INPUT:
            self.assertRaises(AttributeError, bot.command, test)
    
    def test_dict_input(self):
        bot = chatBot()
        DICT_INPUT = [{'command': '!!help'}, {'command': '!!about'}]
        
        for test in DICT_INPUT:
            self.assertRaises(AttributeError, bot.command, test)
    
    def test_empty_string(self):
        bot = chatBot()
        expected = "Command not recognized. Please try one of these: !! [about|help|yoda]"
        
        self.assertEqual(bot.command(''), expected)
    
if __name__ == '__main__':
    unittest.main()