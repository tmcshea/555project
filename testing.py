import unittest
import parser

class Testing(unittest.TestCase):

    # tests for datesBeforeCurrentDate function
    def test_date_before_current(self):
        self.assertEqual(parser.datesBeforeCurrentDate('random'), None)
        self.assertEqual(parser.datesBeforeCurrentDate('@I3@'),
                            "ERROR: INDIVIDUAL: US01: @I3@: Death 12 APR 2050 occurs in the future")
        self.assertEqual(parser.datesBeforeCurrentDate('@I6@'),
                            "ERROR: INDIVIDUAL: US01: @I6@: Birthday 13 SEP 2030 occurs in the future")
        self.assertEqual(parser.datesBeforeCurrentDate(''), None)
        self.assertEqual(parser.datesBeforeCurrentDate('@I2@'), None)
        self.assertEqual(parser.datesBeforeCurrentDate('@F3@'),
                            "ERROR: FAMILY: US01: @F3@: Marriage 18 SEP 2020 occurs in the future")
        self.assertEqual(parser.datesBeforeCurrentDate('@F2@'), None)

    def test_birth_before_marriage(self):
        self.assertEqual(parser.bornBeforeMarriage())

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
