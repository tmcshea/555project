import unittest
import parser

class Testing(unittest.TestCase):

    # tests for datesBeforeCurrentDate function
    def test_date_before_current(self):
        self.assertEqual(parser.datesBeforeCurrentDate('random'), [True, True])
        self.assertEqual(parser.datesBeforeCurrentDate('@I3@'), [True, False])
        self.assertEqual(parser.datesBeforeCurrentDate('@I6@'), [False, True])
        self.assertEqual(parser.datesBeforeCurrentDate(''), [True, True])
        self.assertEqual(parser.datesBeforeCurrentDate('@I2@'), [True, True])
        self.assertEqual(parser.datesBeforeCurrentDate('@F3@'), [False, True])
        self.assertEqual(parser.datesBeforeCurrentDate('@F2@'), [True, True])

    def test_birth_before_marriage(self):
        self.assertEqual(parser.bornBeforeMarriage('random'), [])
        self.assertEqual(parser.bornBeforeMarriage('@F2@'), [False, True])
        self.assertEqual(parser.bornBeforeMarriage('@F3@'), [False, True])
        self.assertEqual(parser.bornBeforeMarriage(''), [])
        self.assertEqual(parser.bornBeforeMarriage('@F1@'), [True, True])
        self.assertEqual(parser.bornBeforeMarriage('@I2@'), [])

    # tests for birthBeforeDeath function
    def test_birth_before_death(self):
        self.assertEqual(parser.birthBeforeDeath('random'), False)
        self.assertEqual(parser.birthBeforeDeath('@I1@'), True)
        self.assertEqual(parser.birthBeforeDeath('@I4@'), False)
        self.assertEqual(parser.birthBeforeDeath('@I2@'), False)
        self.assertEqual(parser.birthBeforeDeath(''), False)
        self.assertEqual(parser.birthBeforeDeath(32), False)

    # tests for marriageBeforeDivorce function
    def test_marriage_before_divorce(self):
        self.assertEqual(parser.marriageBeforeDivorce('random'), False)
        self.assertEqual(parser.marriageBeforeDivorce(32), False)
        self.assertEqual(parser.marriageBeforeDivorce(''), False)
        self.assertEqual(parser.marriageBeforeDivorce('@F2@'), True)
        self.assertEqual(parser.marriageBeforeDivorce('@F3@'), False)

    def test_less_than_150_years(self):
        self.assertEqual(parser.lessThan150('random'), False)
        self.assertEqual(parser.lessThan150(32), False)
        self.assertEqual(parser.lessThan150(''), False)
        self.assertEqual(parser.lessThan150('@I2@'), True)
        self.assertEqual(parser.lessThan150('@I3@'), True)
        self.assertEqual(parser.lessThan150('@I1@'), False)
        self.assertEqual(parser.lessThan150('@I7@'), False)

    def test_birth_before_marriage_divroce(self):
        self.assertEqual(parser.marriageBeforeBirth('random'), False)
        self.assertEqual(parser.marriageBeforeBirth(''), False)
        self.assertEqual(parser.marriageBeforeBirth('@I5@'), True)
        self.assertEqual(parser.marriageBeforeBirth('@I1@'), False)
        self.assertEqual(parser.marriageBeforeBirth('@I7@'), True)
        self.assertEqual(parser.marriageBeforeBirth('@F2@'), False)


        self.assertEqual(parser.divorceAfterBirth('random'), False)
        self.assertEqual(parser.divorceAfterBirth(''), False)
        self.assertEqual(parser.divorceAfterBirth('@I3@'), False)
        self.assertEqual(parser.divorceAfterBirth('@I5@'), True)
        self.assertEqual(parser.divorceAfterBirth('@I1@'), True)
        self.assertEqual(parser.divorceAfterBirth('@I7@'), True)
        self.assertEqual(parser.divorceAfterBirth('@F3@'), False)

    # tests for marraigeBeforeDeath function
    def test_marraige_before_death(self):
        self.assertEqual(parser.marriageBeforeDeath('random'), [])
        self.assertEqual(parser.marriageBeforeDeath(5), [])
        self.assertEqual(parser.marriageBeforeDeath(''), [])

    # tests for divorceBeforeDeath function
    def test_divorce_before_death(self):
        self.assertEqual(parser.divorceBeforeDeath('random'), [None, None])
        self.assertEqual(parser.divorceBeforeDeath(5), [None, None])
        self.assertEqual(parser.divorceBeforeDeath(''), [None, None])

if __name__ == "__main__":
    unittest.main()
