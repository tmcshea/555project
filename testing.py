import unittest
import familyTreeParser

class Testing(unittest.TestCase):

# US01: checks if all dates are before the current date
	# tests for datesBeforeCurrentDate function
# 	def test_date_before_current(self):
# 		self.assertEqual(familyTreeParser.datesBeforeCurrentDate('random'), [True, True])
# 		self.assertEqual(familyTreeParser.datesBeforeCurrentDate('@I3@'), [True, False])
# 		self.assertEqual(familyTreeParser.datesBeforeCurrentDate('@I6@'), [False, True])
# 		self.assertEqual(familyTreeParser.datesBeforeCurrentDate(''), [True, True])
# 		self.assertEqual(familyTreeParser.datesBeforeCurrentDate('@I2@'), [True, True])
# 		self.assertEqual(familyTreeParser.datesBeforeCurrentDate('@F3@'), [False, True])
# 		self.assertEqual(familyTreeParser.datesBeforeCurrentDate('@F2@'), [True, True])

# # US02: checks if births occur before they are married
# 	def test_birth_before_marriage(self):
# 		self.assertEqual(familyTreeParser.bornBeforeMarriage('random'), [])
# 		self.assertEqual(familyTreeParser.bornBeforeMarriage('@F2@'), [False, True])
# 		self.assertEqual(familyTreeParser.bornBeforeMarriage('@F3@'), [False, True])
# 		self.assertEqual(familyTreeParser.bornBeforeMarriage(''), [])
# 		self.assertEqual(familyTreeParser.bornBeforeMarriage('@F1@'), [True, True])
# 		self.assertEqual(familyTreeParser.bornBeforeMarriage('@I2@'), [])

# # US03: checks to see if birth occurs before death
# 	# tests for birthBeforeDeath function
# 	def test_birth_before_death(self):
# 		self.assertEqual(familyTreeParser.birthBeforeDeath('random'), False)
# 		self.assertEqual(familyTreeParser.birthBeforeDeath('@I1@'), True)
# 		self.assertEqual(familyTreeParser.birthBeforeDeath('@I4@'), False)
# 		self.assertEqual(familyTreeParser.birthBeforeDeath('@I2@'), False)
# 		self.assertEqual(familyTreeParser.birthBeforeDeath(''), False)
# 		self.assertEqual(familyTreeParser.birthBeforeDeath(32), False)

# # US04: checks to see if marriage is before divorce
# 	# tests for marriageBeforeDivorce function
# 	def test_marriage_before_divorce(self):
# 		self.assertEqual(familyTreeParser.marriageBeforeDivorce('random'), False)
# 		self.assertEqual(familyTreeParser.marriageBeforeDivorce(32), False)
# 		self.assertEqual(familyTreeParser.marriageBeforeDivorce(''), False)
# 		self.assertEqual(familyTreeParser.marriageBeforeDivorce('@F2@'), True)
# 		self.assertEqual(familyTreeParser.marriageBeforeDivorce('@F3@'), False)

# # US05: Checks to see if marriage occured before death of either spouse
# 	# tests for marraigeBeforeDeath function
# 	def test_marraige_before_death(self):
# 		self.assertEqual(familyTreeParser.marriageBeforeDeath('random'), [])
# 		self.assertEqual(familyTreeParser.marriageBeforeDeath(5), [])
# 		self.assertEqual(familyTreeParser.marriageBeforeDeath(''), [])

# # US06: Checks to see if divorce occured before death of either spouse
# 	# tests for divorceBeforeDeath function
# 	def test_divorce_before_death(self):
# 		self.assertEqual(familyTreeParser.divorceBeforeDeath('random'), [None, None])
# 		self.assertEqual(familyTreeParser.divorceBeforeDeath(5), [None, None])
# 		self.assertEqual(familyTreeParser.divorceBeforeDeath(''), [None, None])

# # US07: test (less than 150 years old)
# 	def test_less_than_150_years(self):
# 		self.assertEqual(familyTreeParser.lessThan150('random'), False)
# 		self.assertEqual(familyTreeParser.lessThan150(32), False)
# 		self.assertEqual(familyTreeParser.lessThan150(''), False)
# 		self.assertEqual(familyTreeParser.lessThan150('@I2@'), True)
# 		self.assertEqual(familyTreeParser.lessThan150('@I3@'), True)
# 		self.assertEqual(familyTreeParser.lessThan150('@I1@'), False)
# 		self.assertEqual(familyTreeParser.lessThan150('@I7@'), False)

# # US08: checks if marriage happens before child's birth
# 	def test_birth_before_marriage_divroce(self):
# 		self.assertEqual(familyTreeParser.marriageBeforeBirth('random'), False)
# 		self.assertEqual(familyTreeParser.marriageBeforeBirth(''), False)
# 		self.assertEqual(familyTreeParser.marriageBeforeBirth('@I5@'), True)
# 		self.assertEqual(familyTreeParser.marriageBeforeBirth('@I1@'), False)
# 		self.assertEqual(familyTreeParser.marriageBeforeBirth('@I7@'), True)
# 		self.assertEqual(familyTreeParser.marriageBeforeBirth('@F2@'), False)

# # US08.5: checks if marriage happens before child's birth (CHECKS DIVORCES)
# 		self.assertEqual(familyTreeParser.divorceAfterBirth('random'), False)
# 		self.assertEqual(familyTreeParser.divorceAfterBirth(''), False)
# 		self.assertEqual(familyTreeParser.divorceAfterBirth('@I3@'), False)
# 		self.assertEqual(familyTreeParser.divorceAfterBirth('@I5@'), True)
# 		self.assertEqual(familyTreeParser.divorceAfterBirth('@I1@'), True)
# 		self.assertEqual(familyTreeParser.divorceAfterBirth('@I7@'), True)
# 		self.assertEqual(familyTreeParser.divorceAfterBirth('@F3@'), False)

# # US09: checks if individuals are born BEFORE parents' deaths || out: [wife, husb]
# 	def test_us09_bornBeforeParentDeath(self):
# 		self.assertEqual(familyTreeParser.bornBeforeParentDeath('asdfdasf'), 'INDVIDERROR')
# 		self.assertEqual(familyTreeParser.bornBeforeParentDeath(''), 'INDVIDERROR')
# 		self.assertEqual(familyTreeParser.bornBeforeParentDeath('@I1'), [True, True])
# 		self.assertEqual(familyTreeParser.bornBeforeParentDeath('@I2'), [True, False])

# # US10: checks if everyone got married after 14 years of age || out: [wife, husb]
# 	def test_us10_marriageAfter14(self):
# 		self.assertEqual(familyTreeParser.bornBeforeParentDeath('asdfdasf'), False)
# 		self.assertEqual(familyTreeParser.bornBeforeParentDeath(''), False)
# 		self.assertEqual(familyTreeParser.bornBeforeParentDeath('@F1'), [True, True])
# 		self.assertEqual(familyTreeParser.bornBeforeParentDeath('@F2'), [False, False])

# 	def test_no_bigamy(self):
# 		self.assertEqual(familyTreeParser.noBigamy('random'), False)
# 		self.assertEqual(familyTreeParser.noBigamy(''), False)
# 		self.assertEqual(familyTreeParser.noBigamy('@I7@'), True)
# 		self.assertEqual(familyTreeParser.noBigamy('@I2@'), False)
# 		self.assertEqual(familyTreeParser.noBigamy('@I5@'), True)

# 	def test_no_parents_too_old(self):
# 		self.assertEqual(familyTreeParser.parentsNotTooOld('random'), False)
# 		self.assertEqual(familyTreeParser.parentsNotTooOld(''), False)
# 		self.assertEqual(familyTreeParser.parentsNotTooOld('@F1@'), True)
# 		self.assertEqual(familyTreeParser.parentsNotTooOld('@F33@'), False)
# 		self.assertEqual(familyTreeParser.parentsNotTooOld('@F3'), False)

# 	def test_sibling_spacing(self):
# 		self.assertEqual(familyTreeParser.siblingSpacing('random'), False)
# 		self.assertEqual(familyTreeParser.siblingSpacing(''), False)
# 		self.assertEqual(familyTreeParser.siblingSpacing('@I3@'), False)
# 		self.assertEqual(familyTreeParser.siblingSpacing('@F2@'), True)
# 		self.assertEqual(familyTreeParser.siblingSpacing('@F1@'), True)

# 	def test_sibling_same_birth(self):
# 		self.assertEqual(familyTreeParser.siblingSameBirth('random'), False)
# 		self.assertEqual(familyTreeParser.siblingSameBirth(''), False)
# 		self.assertEqual(familyTreeParser.siblingSameBirth('@I3@'), False)
# 		self.assertEqual(familyTreeParser.siblingSameBirth('@F2@'), True)
# 		self.assertEqual(familyTreeParser.siblingSameBirth('@F1@'), True)

# 	def test_less_than_15_siblings(self):
# 		self.assertEqual(familyTreeParser.less15Siblings('random'), False)
# 		self.assertEqual(familyTreeParser.less15Siblings(''), False)
# 		self.assertEqual(familyTreeParser.less15Siblings('@I3@'), False)
# 		self.assertEqual(familyTreeParser.less15Siblings('@F2@'), True)
# 		self.assertEqual(familyTreeParser.less15Siblings('@F1@'), True)
# # US15: checks to see that a family has less then 15 siblings

# # US16: checks to see that a family has less then 15 siblings
# 	def test_male_last_name(self):
# 		self.assertEqual(familyTreeParser.maleLastName('random'), False)
# 		self.assertEqual(familyTreeParser.maleLastName(''), False)
# 		self.assertEqual(familyTreeParser.maleLastName('@I2@'), True)
# 		self.assertEqual(familyTreeParser.maleLastName('@I3@'), False)
# 		self.assertEqual(familyTreeParser.maleLastName('@I1@'), True)

# sprint3
# # US17: checks for parent + children marriage
# 	def test_us17_noChildrenMarriage(self):
# 		self.assertEqual(familyTreeParser.noChildrenMarriage('badid'), True)
# 		self.assertEqual(familyTreeParser.noChildrenMarriage('@F6@'), False)
# 		self.assertEqual(familyTreeParser.noChildrenMarriage('@F7@'), True)
# 		self.assertEqual(familyTreeParser.noChildrenMarriage('@I7@'), True)
# 		self.assertEqual(familyTreeParser.noChildrenMarriage('@F10@'), True)

# # US18: checks for sibling marriage
# 	def test_us18_noSiblingMarriage(self):
# 		self.assertEqual(familyTreeParser.noSiblingMarriage('badid'), True)
# 		self.assertEqual(familyTreeParser.noSiblingMarriage('@F7@'), False)
# 		self.assertEqual(familyTreeParser.noSiblingMarriage('@F8@'), False)
# 		self.assertEqual(familyTreeParser.noChildrenMarriage('@I7@'), True)
# 		self.assertEqual(familyTreeParser.noChildrenMarriage('@F10@'), True)

# # US19: checks for cousin marraige
# 	def test_us19_noCousinMarraige(self):
# 		self.assertEqual(familyTreeParser.noCousinMarraige('random'), True)
# 		self.assertEqual(familyTreeParser.noCousinMarraige(''), True)
# 		self.assertEqual(familyTreeParser.noCousinMarraige('@F6@'), True)
# 		self.assertEqual(familyTreeParser.noCousinMarraige('@F11@'), False)
# 		self.assertEqual(familyTreeParser.noCousinMarraige('@I3@'), True)

# # US20: check for marraige between uncle/aunt and neice/nephew
# 	def test_us20_noAuntUncle(self):
# 		self.assertEqual(familyTreeParser.noAuntsAndUncles('random'), False)
# 		self.assertEqual(familyTreeParser.noAuntsAndUncles(''), False)
# 		self.assertEqual(familyTreeParser.noAuntsAndUncles('@F9@'), False)
# 		self.assertEqual(familyTreeParser.noAuntsAndUncles('@F4@'), True)
# 		self.assertEqual(familyTreeParser.noAuntsAndUncles('@F12@'), False)
# 		self.assertEqual(familyTreeParser.noAuntsAndUncles('@I1@'), False)

# # US21: checks for sibling marriage
# 	def test_us21_checkGenderRole(self):
# 		self.assertEqual(familyTreeParser.checkGenderRole(''), False)
# 		self.assertEqual(familyTreeParser.checkGenderRole('random'), False)
# 		self.assertEqual(familyTreeParser.checkGenderRole('@F10@'), False)
# 		self.assertEqual(familyTreeParser.checkGenderRole('@F11@'), False)
# 		self.assertEqual(familyTreeParser.checkGenderRole('@F12@'), True)
# 		self.assertEqual(familyTreeParser.checkGenderRole('@F1@'), True)

# # US22: check to make sure every ID is unique
# 	def test_us22_uniqueIDs(self):
# 		self.assertEqual(familyTreeParser.uniqueIDs(), True)

# # US23: check for unique name
# 	def test_us23_uniqueName(self):
# 		self.assertEqual(familyTreeParser.uniqueName('random'), [[],False])
# 		self.assertEqual(familyTreeParser.uniqueName(''), [[],False])
# 		self.assertEqual(familyTreeParser.uniqueName('@I1@'), [['@I35@'],True])
# 		self.assertEqual(familyTreeParser.uniqueName('@I7@'), [['@I27@'],True])
# 		self.assertEqual(familyTreeParser.uniqueName('@I3@'), [[],False])
# 		self.assertEqual(familyTreeParser.uniqueName('@F3@'), [[],False])

# 	# US24: check for unique family spouse
# 	def test_us24_uniqueFamilySpouse(self):
# 		self.assertEqual(familyTreeParser.uniqueFamilySpouse('random'), [[],False])
# 		self.assertEqual(familyTreeParser.uniqueFamilySpouse(''), [[],False])
# 		self.assertEqual(familyTreeParser.uniqueFamilySpouse('@F12@'), [['@F14@'],True])
# 		self.assertEqual(familyTreeParser.uniqueFamilySpouse('@F14@'), [['@F12@'],True])
# 		self.assertEqual(familyTreeParser.uniqueFamilySpouse('@I3@'), [[],False])
# 		self.assertEqual(familyTreeParser.uniqueFamilySpouse('@F3@'), [[],False])

# sprint4
	# US25: check for duplicate children first name entries
	def test_us25_uniqueFirstName(self):
		self.assertEqual(familyTreeParser.uniqueFirstName('dsaf'), False)
		self.assertEqual(familyTreeParser.uniqueFirstName(''), False)
		self.assertEqual(familyTreeParser.uniqueFirstName('@F1@'), True)
		self.assertEqual(familyTreeParser.uniqueFirstName('@F7@'), True)

	# US26: check for consistent records between individuals and families
	def test_us26_correspondingEntries_individual(self):
		self.assertEqual(familyTreeParser.correspondingEntries_individual('51fds'), False)
		self.assertEqual(familyTreeParser.correspondingEntries_individual(''), False)
		self.assertEqual(familyTreeParser.correspondingEntries_individual('@I1@'), True)

	def test_us26_correspondingEntries_family(self):
		self.assertEqual(familyTreeParser.correspondingEntries_family('51fds'), False)
		self.assertEqual(familyTreeParser.correspondingEntries_family(''), False)
		self.assertEqual(familyTreeParser.correspondingEntries_family('@F3@'), True)

	# US27: check for getting the persons age
	def test_us27_getPersonName(self):
		self.assertEqual(familyTreeParser.getPersonAge('random'), False)
		self.assertEqual(familyTreeParser.getPersonAge(''), False)
		self.assertEqual(familyTreeParser.getPersonAge('@I7@'), 827)
		self.assertEqual(familyTreeParser.getPersonAge('@I4@'), -1)
		self.assertEqual(familyTreeParser.getPersonAge('@I16@'), 22)

	#US28: check for order children
	def test_us28_orderChildren(self):
		self.assertEqual(familyTreeParser.orderChildren('@F6@'), ['@I3@'])
		self.assertEqual(familyTreeParser.orderChildren('@F8@'), ['@I10@', '@I33@'])
		self.assertEqual(familyTreeParser.orderChildren('@F7@'), ['@I17@', '@I23@', '@I26@', '@I19@', '@I25@', '@I11@', '@I12@', '@I13@', '@I14@', '@I15@', '@I16@', '@I18@', '@I20@', '@I22@', '@I24@', '@I21@'])


if __name__ == "__main__":
	unittest.main()
