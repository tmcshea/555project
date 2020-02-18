import unittest
import parser

class Testing(unittest.TestCase):

    # tests for birthBeforeDeath function
    def test_birth_before_death(self):
        self.assertEqual(parser.birthBeforeDeath('random'), False)
        self.assertEqual(parser.birthBeforeDeath('@I7@'), True)
        self.assertEqual(parser.birthBeforeDeath('@I9@'), True)
        self.assertEqual(parser.birthBeforeDeath('@I6@'), False)
        self.assertEqual(parser.birthBeforeDeath(''), False)
        self.assertEqual(parser.birthBeforeDeath(32), False)
    
    # tests for marraigeBeforeDivorce function
    def test_marraige_before_divorce(self):
        self.assertEqual(parser.marraigeBeforeDivorce('random'), False)
        self.assertEqual(parser.marraigeBeforeDivorce(32), False)
        self.assertEqual(parser.marraigeBeforeDivorce(''), False)
        self.assertEqual(parser.marraigeBeforeDivorce('@F1@'), True)
        self.assertEqual(parser.marraigeBeforeDivorce('@F5@'), False)
    
if __name__ == "__main__":
    unittest.main()