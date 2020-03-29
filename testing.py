import unittest
import familyTreeParser

class Testing(unittest.TestCase):

# US01: checks if all dates are before the current date
	# tests for datesBeforeCurrentDate function
	def test_date_before_current(self):
		self.assertEqual(familyTreeParser.datesBeforeCurrentDate('random'), [True, True])
		self.assertEqual(familyTreeParser.datesBeforeCurrentDate('@I3@'), [True, False])
		self.assertEqual(familyTreeParser.datesBeforeCurrentDate('@I6@'), [False, True])
		self.assertEqual(familyTreeParser.datesBeforeCurrentDate(''), [True, True])
		self.assertEqual(familyTreeParser.datesBeforeCurrentDate('@I2@'), [True, True])
		self.assertEqual(familyTreeParser.datesBeforeCurrentDate('@F3@'), [False, True])
		self.assertEqual(familyTreeParser.datesBeforeCurrentDate('@F2@'), [True, True])

# US02: checks if births occur before they are married
	def test_birth_before_marriage(self):
		self.assertEqual(familyTreeParser.bornBeforeMarriage('random'), [])
		self.assertEqual(familyTreeParser.bornBeforeMarriage('@F2@'), [False, True])
		self.assertEqual(familyTreeParser.bornBeforeMarriage('@F3@'), [False, True])
		self.assertEqual(familyTreeParser.bornBeforeMarriage(''), [])
		self.assertEqual(familyTreeParser.bornBeforeMarriage('@F1@'), [True, True])
		self.assertEqual(familyTreeParser.bornBeforeMarriage('@I2@'), [])

# US03: checks to see if birth occurs before death
	# tests for birthBeforeDeath function
	def test_birth_before_death(self):
		self.assertEqual(familyTreeParser.birthBeforeDeath('random'), False)
		self.assertEqual(familyTreeParser.birthBeforeDeath('@I1@'), True)
		self.assertEqual(familyTreeParser.birthBeforeDeath('@I4@'), False)
		self.assertEqual(familyTreeParser.birthBeforeDeath('@I2@'), False)
		self.assertEqual(familyTreeParser.birthBeforeDeath(''), False)
		self.assertEqual(familyTreeParser.birthBeforeDeath(32), False)

# US04: checks to see if marriage is before divorce
	# tests for marriageBeforeDivorce function
	def test_marriage_before_divorce(self):
		self.assertEqual(familyTreeParser.marriageBeforeDivorce('random'), False)
		self.assertEqual(familyTreeParser.marriageBeforeDivorce(32), False)
		self.assertEqual(familyTreeParser.marriageBeforeDivorce(''), False)
		self.assertEqual(familyTreeParser.marriageBeforeDivorce('@F2@'), True)
		self.assertEqual(familyTreeParser.marriageBeforeDivorce('@F3@'), False)

# US05: Checks to see if marriage occured before death of either spouse
	# tests for marraigeBeforeDeath function
	def test_marraige_before_death(self):
		self.assertEqual(familyTreeParser.marriageBeforeDeath('random'), [])
		self.assertEqual(familyTreeParser.marriageBeforeDeath(5), [])
		self.assertEqual(familyTreeParser.marriageBeforeDeath(''), [])

# US06: Checks to see if divorce occured before death of either spouse
	# tests for divorceBeforeDeath function
	def test_divorce_before_death(self):
		self.assertEqual(familyTreeParser.divorceBeforeDeath('random'), [None, None])
		self.assertEqual(familyTreeParser.divorceBeforeDeath(5), [None, None])
		self.assertEqual(familyTreeParser.divorceBeforeDeath(''), [None, None])

# US07: test (less than 150 years old)
	def test_less_than_150_years(self):
		self.assertEqual(familyTreeParser.lessThan150('random'), False)
		self.assertEqual(familyTreeParser.lessThan150(32), False)
		self.assertEqual(familyTreeParser.lessThan150(''), False)
		self.assertEqual(familyTreeParser.lessThan150('@I2@'), True)
		self.assertEqual(familyTreeParser.lessThan150('@I3@'), True)
		self.assertEqual(familyTreeParser.lessThan150('@I1@'), False)
		self.assertEqual(familyTreeParser.lessThan150('@I7@'), False)

# US08: checks if marriage happens before child's birth
	def test_birth_before_marriage_divroce(self):
		self.assertEqual(familyTreeParser.marriageBeforeBirth('random'), False)
		self.assertEqual(familyTreeParser.marriageBeforeBirth(''), False)
		self.assertEqual(familyTreeParser.marriageBeforeBirth('@I5@'), True)
		self.assertEqual(familyTreeParser.marriageBeforeBirth('@I1@'), False)
		self.assertEqual(familyTreeParser.marriageBeforeBirth('@I7@'), True)
		self.assertEqual(familyTreeParser.marriageBeforeBirth('@F2@'), False)

# US08.5: checks if marriage happens before child's birth (CHECKS DIVORCES)
		self.assertEqual(familyTreeParser.divorceAfterBirth('random'), False)
		self.assertEqual(familyTreeParser.divorceAfterBirth(''), False)
		self.assertEqual(familyTreeParser.divorceAfterBirth('@I3@'), False)
		self.assertEqual(familyTreeParser.divorceAfterBirth('@I5@'), True)
		self.assertEqual(familyTreeParser.divorceAfterBirth('@I1@'), True)
		self.assertEqual(familyTreeParser.divorceAfterBirth('@I7@'), True)
		self.assertEqual(familyTreeParser.divorceAfterBirth('@F3@'), False)

# US09: checks if individuals are born BEFORE parents' deaths || out: [wife, husb]
	def test_us09_bornBeforeParentDeath(self):
		self.assertEqual(familyTreeParser.bornBeforeParentDeath('asdfdasf'), 'INDVIDERROR')
		self.assertEqual(familyTreeParser.bornBeforeParentDeath(''), 'INDVIDERROR')
		self.assertEqual(familyTreeParser.bornBeforeParentDeath('@I1'), [True, True])
		self.assertEqual(familyTreeParser.bornBeforeParentDeath('@I2'), [True, False])

# US10: checks if everyone got married after 14 years of age || out: [wife, husb]
	def test_us10_marriageAfter14(self):
		self.assertEqual(familyTreeParser.bornBeforeParentDeath('asdfdasf'), False)
		self.assertEqual(familyTreeParser.bornBeforeParentDeath(''), False)
		self.assertEqual(familyTreeParser.bornBeforeParentDeath('@F1'), [True, True])
		self.assertEqual(familyTreeParser.bornBeforeParentDeath('@F2'), [False, False])

	def test_no_bigamy(self):
		self.assertEqual(familyTreeParser.noBigamy('random'), False)
		self.assertEqual(familyTreeParser.noBigamy(''), False)
		self.assertEqual(familyTreeParser.noBigamy('@I7@'), True)
		self.assertEqual(familyTreeParser.noBigamy('@I2@'), False)
		self.assertEqual(familyTreeParser.noBigamy('@I5@'), True)

	def test_no_parents_too_old(self):
		self.assertEqual(familyTreeParser.parentsNotTooOld('random'), False)
		self.assertEqual(familyTreeParser.parentsNotTooOld(''), False)
		self.assertEqual(familyTreeParser.parentsNotTooOld('@F1@'), True)
		self.assertEqual(familyTreeParser.parentsNotTooOld('@F33@'), False)
		self.assertEqual(familyTreeParser.parentsNotTooOld('@F3'), False)

	def test_sibling_spacing(self):
		self.assertEqual(familyTreeParser.siblingSpacing('random'), False)
		self.assertEqual(familyTreeParser.siblingSpacing(''), False)
		self.assertEqual(familyTreeParser.siblingSpacing('@I3@'), False)
		self.assertEqual(familyTreeParser.siblingSpacing('@F2@'), True)
		self.assertEqual(familyTreeParser.siblingSpacing('@F1@'), True)

	def test_sibling_same_birth(self):
		self.assertEqual(familyTreeParser.siblingSameBirth('random'), False)
		self.assertEqual(familyTreeParser.siblingSameBirth(''), False)
		self.assertEqual(familyTreeParser.siblingSameBirth('@I3@'), False)
		self.assertEqual(familyTreeParser.siblingSameBirth('@F2@'), True)
		self.assertEqual(familyTreeParser.siblingSameBirth('@F1@'), True)

	def test_less_than_15_siblings(self):
		self.assertEqual(familyTreeParser.less15Siblings('random'), False)
		self.assertEqual(familyTreeParser.less15Siblings(''), False)
		self.assertEqual(familyTreeParser.less15Siblings('@I3@'), False)
		self.assertEqual(familyTreeParser.less15Siblings('@F2@'), True)
		self.assertEqual(familyTreeParser.less15Siblings('@F1@'), True)
# US15: checks to see that a family has less then 15 siblings

# US16: checks to see that a family has less then 15 siblings
	def test_male_last_name(self):
		self.assertEqual(familyTreeParser.maleLastName('random'), False)
		self.assertEqual(familyTreeParser.maleLastName(''), False)
		self.assertEqual(familyTreeParser.maleLastName('@I2@'), True)
		self.assertEqual(familyTreeParser.maleLastName('@I3@'), False)
		self.assertEqual(familyTreeParser.maleLastName('@I1@'), True)

# sprint3
# US17: checks for parent + children marriage
	def test_us17_noChildrenMarriage(self):
		self.assertEqual(familyTreeParser.noChildrenMarriage('badid'), False)
		self.assertEqual(familyTreeParser.noChildrenMarriage(), False)
		self.assertEqual(familyTreeParser.noChildrenMarriage(), True)

# US18: checks for sibling marriage
	def test_us18_noSiblingMarriage(self):
		self.assertEqual(familyTreeParser.noChildrenMarriage(), False)
		self.assertEqual(familyTreeParser.noChildrenMarriage(), False)
		self.assertEqual(familyTreeParser.noChildrenMarriage(), False)

# US21: checks for correct gender for family role
	def test_us21_checkGenderRole(self):
		self.assertEqual(familyTreeParser.checkGenderRole(''), False)
		self.assertEqual(familyTreeParser.checkGenderRole('@I2@'), True)
		self.assertEqual(familyTreeParser.checkGenderRole('@I3@'), True)
		self.assertEqual(familyTreeParser.checkGenderRole('@I4@'), True)

# US22: checks for unique IDs for family and individual
	def test_us22_uniqueIDs(self):
		self.assertEqual(familyTreeParser.uniqueIDs(), True)

if __name__ == "__main__":
	unittest.main()
