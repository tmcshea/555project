"""
parser.py
Provides valid and invalid input to a ged file
Prints results to terminal or console and also output results to a txt file
Takes file input name through argv in the terminal

Author: Tyler McShea, Aaron Jin, Connor Murphy, Nicholas Polich
Date: Feb 9, 2020
"""

import sys
import csv
from prettytable import PrettyTable
from datetime import datetime, date

# Global Dictionary for individual and families info
individual = {}
families = {}
csv_file = open('output.csv', mode='w')
familyLastName = {}
lastNameBool = {}

# parser function
# in: gedcom file


def parser(file):
	# Allows access to global variables
	global individual, families

	# Arrays of valid tags
	zeroLevel = ["NOTE", "HEAD", "TRLR"]
	zeroExcep = ["INDI", "FAM"]
	oneLevel = ["NAME", "SEX", "FAMC", "FAMS", "HUSB",
					"WIFE", "CHIL"]
	oneDate = ["BIRT", "DEAT", "MARR", "DIV"]

	# Varibales
	dateNext = False
	id = ""
	list = ""
	dateType = ""

	f = open(file, "r")
	for lines in f:
		inputs = lines.split()
		if(dateNext):
			dateNext = False
			if(inputs[0] == "2" and inputs[1] == "DATE"):
				if(list == "individual"):
					individual[id][dateType] = ' '.join(inputs[2:])
				elif(list == "families"):
					families[id][dateType] = ' '.join(inputs[2:])
		elif(inputs[0] == "0"):
			if(len(inputs) >= 3 and inputs[2] in zeroExcep):
				if(inputs[2] == zeroExcep[0]):
					individual[inputs[1]] = {}
					id = inputs[1]
					list = "individual"
				else:
					families[inputs[1]] = {}
					id = inputs[1]
					list = "families"
		elif(inputs[0] == "1"):
			if(inputs[1] in oneLevel):
				if(list == "individual"):
					if(inputs[1] == 'FAMS'):
						if inputs[1] in individual[id]:
							individual[id][inputs[1]].append(
								' '.join(inputs[2:]))
						else:
							individual[id][inputs[1]] = [' '.join(inputs[2:])]
					else:
						individual[id][inputs[1]] = ' '.join(inputs[2:])
				elif(list == "families"):
					if inputs[1] in families[id]:
						families[id][inputs[1]].append(' '.join(inputs[2:]))
					else:
						families[id][inputs[1]] = [' '.join(inputs[2:])]
			elif(inputs[1] in oneDate):
				dateNext = True
				dateType = inputs[1]

# Function to display individual and families information and creates a csv file
# with this information.


def display():
	# individuals informatio

	x = PrettyTable()
	x.field_names = ["ID", "Name", "Gender", "Birthday",
		"Age", "Alive", "Death", "Child", "Spouse"]

	writer = csv.writer(csv_file, delimiter=',',
						quotechar='"', quoting=csv.QUOTE_MINIMAL)
	writer.writerow(["ID", "Name", "Gender", "Birthday", "Age",
					"Alive", "Death", "Child", "Spouse"])
	for ids in individual:
		if("DEAT" not in individual[ids]):
			death = "NA"
			alive = "True"
		else:
			death = individual[ids]["DEAT"]
			alive = "False"
		if("FAMC" not in individual[ids]):
			child = "NA"
		else:
			child = individual[ids]["FAMC"]
		if("FAMS" not in individual[ids]):
			spouse = "NA"
		else:
			spouse = individual[ids]["FAMS"]
		age = 2020 - int(individual[ids]["BIRT"][-4:])
		x.add_row([ids, individual[ids]["NAME"], individual[ids]["SEX"],
				  individual[ids]["BIRT"], age, alive, death, child, spouse])
		writer.writerow([ids, individual[ids]["NAME"], individual[ids]["SEX"],
						individual[ids]["BIRT"], age, alive, death, child, spouse])

	# family/marriage information
	y = PrettyTable()
	y.field_names = ["ID", "Married", "Divorced", "Husband ID",
		"Husband Name", "Wife ID", "Wife Name", "Children"]
	writer.writerow([])
	writer.writerow(["ID", "Married", "Divorced", "Husband ID",
					"Husband Name", "Wife ID", "Wife Name", "Children"])
	for ids in families:
		if("MARR" not in families[ids]):
			married = "NA"
		else:
			married = families[ids]["MARR"]
		if("DIV" not in families[ids]):
			divorced = "NA"
		else:
			divorced = families[ids]["DIV"]
		if("HUSB" not in families[ids]):
			HUSB = "NA"
			husName = "NA"
		else:
			HUSB = families[ids]["HUSB"]
			husName = []
			for name in HUSB:
				husName.append(individual[name]["NAME"])
		if("WIFE" not in families[ids]):
			WIFE = "NA"
			wifName = "NA"
		else:
			WIFE = families[ids]["WIFE"]
			wifName = []
			for name in WIFE:
				wifName.append(individual[name]["NAME"])

		if("CHIL" not in families[ids]):
			child = "NA"
		else:
			child = families[ids]["CHIL"]
		y.add_row([ids, married, divorced, HUSB, husName, WIFE, wifName, child])
		writer.writerow([ids, married, divorced, HUSB,
						husName, WIFE, wifName, child])
	csv_file.write("\n")
	print(x)
	print(y)

# date formatter function


def parseDate(date):
	formattedDate = (str(datetime.strptime(date, '%d %b %Y')).split(' ')[0])
	return formattedDate

# function that finds a person's age (does not stop at death)
# input: date passed through parseDate


def age(date):
	today = datetime.today()
	if(int(today.month) - int(date[5:7]) > 0):
		return (int(today.year) - int(date[:4]))
	elif(int(today.month) - int(date[5:7]) == 0 and int(today.day) - int(date[8:]) >= 0):
		return (int(today.year) - int(date[:4]))
	else:
		return (int(today.year) - int(date[:4])) - 1

# helper function for US10: marriage after 14
# input: individual id, family id


def age_during_marriage(birth, marr):
	if(int(marr[5:7]) - int(birth[5:7]) > 0):
		return (int(marr[:4]) - int(birth[:4]))
	elif(int(marr[5:7]) - int(birth[5:7]) == 0 and int(marr[8:]) - int(birth[8:]) >= 0):
		return (int(marr[:4]) - int(birth[:4]))
	else:
		return (int(marr[:4]) - int(birth[:4])) - 1

# ----------------------------
# SPRINT 1
# ----------------------------

# US01: checks if all dates are before the current date
# Input: any ID
# Output: indv:	[birth, death]
# 		  fam:	[marriage, divorce]

def datesBeforeCurrentDate(id):
	now = datetime.today()  # today's date
	results = [True, True]
	if id in individual:  # individual dates: BIRT and DEAT
		if 'BIRT' in individual[id]:
			birth = parseDate(individual[id]['BIRT'])
			if birth > str(now):
				results[0] = False
		if 'DEAT' in individual[id]:
			death = parseDate(individual[id]['DEAT'])
			if death > str(now):
				results[1] = False
	if id in families:  # families dates: MARR and DIV
		if 'MARR' in families[id]:
			marriage = parseDate(families[id]['MARR'])
			if marriage > str(now):
				results[0] = False
		if 'DIV' in families[id]:
			divorce = parseDate(families[id]['DIV'])
			if divorce > str(now):
				results[1] = False
	return results

# US02: checks if births occur before they are married
# Input: family ID
# Output: [husband, wife]

def bornBeforeMarriage(famID):
	results = []
	if(famID in families and "MARR" in families[famID]):
		results = [True, True]
		if("HUSB" in families[famID]):
			husband = families[famID]['HUSB'][0]
			marriage = parseDate(families[famID]['MARR'])
			birth = parseDate(individual[husband]['BIRT'])
			if birth > marriage:
				results[0] = False
		if("WIFE" in families[famID]):
			wife = families[famID]['WIFE'][0]
			marriage = parseDate(families[famID]['MARR'])
			birth = parseDate(individual[wife]['BIRT'])
			if birth > marriage:
				results[1] = False
	return results

# US03: checks to see if birth occurs before death
# Input: id tag from individual Dictionary
def birthBeforeDeath(id):
	if(id not in individual):
		return False
	if('DEAT' in individual[id]):
		birth = parseDate(individual[id]['BIRT'])
		death = parseDate(individual[id]['DEAT'])
		if (birth > death):
			return False
		else:
			return True
	return True

# US04: checks to see if marriage is before divorce
# Input: famID tag from families Dictionary
def marriageBeforeDivorce(famID):
	if(famID not in families):
		return False
	if('DIV' in families[famID] and 'MARR' in families[famID]):
		marriage = parseDate(families[famID]['MARR'])
		divorce = parseDate(families[famID]['DIV'])
		if (marriage > divorce):
			return False
		else:
			return True
	return True

# US05: Checks to see if marriage occured before death of either spouse
# Input: famID tag from families Dictionary
def marriageBeforeDeath(famID):
	results = []
	if(famID in families and 'MARR' in families[famID]):
		results = [True, True]
		marriage = parseDate(families[famID]['MARR'])
		husbID = families[famID]['HUSB'][0]
		wifeID = families[famID]['WIFE'][0]
		if ("DEAT" in individual[husbID]):
			deathHusb = parseDate(individual[husbID]['DEAT'])
			if(marriage > deathHusb):
				results[0] = False
		if ("DEAT" in individual[wifeID]):
			deathWife = parseDate(individual[wifeID]['DEAT'])
			if(marriage > deathWife):
				results[1] = False
	return results

# US06: Checks to see if divorce occured before death of either spouse
# Input: famID tag from families Dictionary
def divorceBeforeDeath(famID):
	results = [None, None]
	if(famID in families and 'DIV' in families[famID]):
		results = [True, True]
		divorce = parseDate(families[famID]['DIV'])
		husbID = families[famID]['HUSB'][0]
		wifeID = families[famID]['WIFE'][0]
		if ("DEAT" in individual[husbID]):
			deathHusb = parseDate(individual[husbID]['DEAT'])
			if(divorce > deathHusb):
				results[0] = False
		if ("DEAT" in individual[wifeID]):
			deathWife = parseDate(individual[wifeID]['DEAT'])
			if(divorce > deathWife):
				results[1] = False
	return results

# US07: checks to make sure person is less thre 150 years old
# Input: id tag from individual Dictionary
def lessThan150(id):
	if(id not in individual):
		return False
	birth = parseDate(individual[id]['BIRT'])
	if(age(birth) >= 150):
		return False
	return True

# US08: checks if marriage happens before child's birth
# Input: id tag from individual Dictionary
def marriageBeforeBirth(id):
	if(id not in individual):
		return False
	if('FAMC' not in individual[id]):
		return True
	birth = parseDate(individual[id]['BIRT'])
	famID = individual[id]['FAMC']

	if(famID not in families):
		return False
	if('MARR' in families[famID]):
		marriage = parseDate(families[famID]['MARR'])
		if (marriage > birth):
			return False
		else:
			return True
	else:
		return False

# US08.5: checks if divorce is after child's birth
# Input: id tag from individual Dictionary
def divorceAfterBirth(id):
	if(id not in individual):
		return False
	if('FAMC' not in individual[id]):
		return True
	birth = parseDate(individual[id]['BIRT'])
	famID = individual[id]['FAMC']

	if(famID not in families):
		return False

	if('DIV' in families[famID]):
		divorce = parseDate(families[famID]['DIV'])
		if(birth > divorce):
			if(birth[:4] == divorce[:4] and int(birth[5:7]) - int(divorce[5:7]) <= 9):
				return True
			else:
				return False
		else:
			return True
	else:
		return True

# ----------------------------
# SPRINT 2
# ----------------------------

# US09: checks if individuals are born BEFORE parents' deaths
# Input: id tag from individual dictionary
# Output: [wife death makes sense, husb "]
# ************** NOT TESTED YET
def bornBeforeParentDeath(id):
	if (id not in individual):
<<<<<<< HEAD
	    return 'INDVIDERROR'
=======
		return 'INDVIDERROR'
>>>>>>> 9682265c52a15ce413525ed773b3f35fc03d8de8

	result = [True, True]
	birth = parseDate(individual[id]['BIRT'])

	if 'FAMC' not in individual[id]:
		return 'NOTACHILD'
	else:
		famID = individual[id]['FAMC']

	if (famID not in families):
		return 'FAMIDERROR'

	wifeID = families[famID]['WIFE'][0]
	husbID = families[famID]['HUSB'][0]

	if ('DEAT' in individual[wifeID]):
		# wife dead rip
		deathDate = individual[wifeID]['DEAT']
		if (birth > deathDate):
			pass
		else:
			result[0] = False

	if ('DEAT' in individual[husbID]):
		# husband dead rip
		deathDate = individual[husbID]['DEAT']
		if (birth > deathDate):
			if (birth[:4] == deathDate[:4] and
				int(birth[5:7] - int(deathDate[5:7]) <= 9)):
				result[1] = False
			else:
				pass
		else:
			result[1] = False

	return result
	# took 20 minutes

# US10: marriage after 14
# Input: id tag from family dictionary
# Output: False if famID invalid
#		[ wife<14?, husb<14? ]
# ************** NOT TESTED YET
def marriageAfter14(famID):
	# base case: is famID valid?
	if (famID not in families):
		return False
	result = [True, True] # result array

	# husb and wife indiv ids
	family = families[famID]
	husbandID = family['HUSB'][0]
	wifeID = family['WIFE'][0]

	# check if husb and wife exist?         ///// wouldn't this have been tested already?

	# check each spouse using age(id)
	husbBirth = parseDate(individual[husbandID]['BIRT'])
	wifeBirth = parseDate(individual[wifeID]['BIRT'])
	marr = parseDate(family['MARR'])
	if age_during_marriage(husbBirth, marr) < 14:
		result[0] = False
	if age_during_marriage(wifeBirth, marr) < 14:
		result[1] = False

	return result
	# took 10 minutes


# Returns the families a person is part of
# Input: id from individual Dictionary
# Output: false if id is not found, empty list if no families, list of families otherwise
def parseFamilies(id):
	if (id not in individual):
		return False
	if ('FAMS' not in individual[id]):
		return []
	return individual[id]['FAMS']

# helper function for noBigamy
# Input: list of family dates in form [startDate, endDate]
def noBigamyHelper(famList):
	for fam in famList:
		for otherFam in famList:
			if (fam == otherFam):
				continue
			if ((fam[0] < otherFam[1]) and (fam[1] > otherFam[0])):
				return False
			if ((fam[1] > otherFam[0]) and (fam[0] < otherFam[1])):
				return False
	return True

# US11: checks to make sure a person is not in two families at once
# Input: id from individuals Dictionary
# NOTE: will also return false if marraige occurs after death
def noBigamy(id):
	MAXDATE = parseDate('31 DEC 9999')
	if (id not in individual):
		return False
	famList = parseFamilies(id)
	if (len(famList) == 1):
		return True
	# if it gets to this point, the person is in multiple families. Need to check they don't overlap
	allDatesList = []
	for family in famList:
		startDate = parseDate(families[family]['MARR'])
		endDate = MAXDATE
		if ('DIV' in families[family]):
			endDate = parseDate(families[family]['DIV'])
		else:
			if ('DEAT' in individual[families[family]['WIFE'][0]]):
				wifeDeath = individual[families[family]['WIFE'][0]]['DEAT']
				endDate = min(endDate, wifeDeath)
			if ('DEAT' in individual[families[family]['HUSB'][0]]):
				husbDeath = individual[families[family]['HUSB'][0]]['DEAT']
				endDate = min(endDate, husbDeath)
		thisFamilylength = [startDate, endDate]
		allDatesList.append(thisFamilylength)
	valid = noBigamyHelper(allDatesList)
	return valid

# US12: checks to make sure parents are correct ages in relation to their kids.
# Input: famID tag from families Dictionary
def parentsNotTooOld(famID):
	if ('HUSB' not in families[famID] or 'WIFE' not in families[famID]):
		return False
	wifeBirth = individual[families[famID]['WIFE'][0]]['BIRT']
	wifeAge = age(parseDate(wifeBirth))
	husbBirth = individual[families[famID]['HUSB'][0]]['BIRT']
	husbAge = age(parseDate(husbBirth))
	children = families[famID]["CHIL"]
	for kid in children:
		kidBirth = individual[kid]['BIRT']
		kidAge = age(parseDate(kidBirth))
		if ((wifeAge - kidAge >= 60) or (husbAge - kidAge >= 80)):
			return False
	return True

# US13: Birth dates of siblings must be more than 8 months apart or
# fewer than 2 days apart
# Input: famID tag from families Dictionary
def siblingSpacing(famID):
	if(famID not in families):
		return False
	if("CHIL" not in families[famID]):
		return True
	children = families[famID]["CHIL"]
	if(len(children) < 2):
		return True
	else:
		birthday_siblings = []
		for child in children:
			birthday_siblings.append(parseDate(individual[child]['BIRT']))
		splitdates = []
		for dates in birthday_siblings:
			newdate = dates.split('-')
			year = int(newdate[0])
			month = int(newdate[1])
			day = int(newdate[2])
			dateformatted = date(year, month, day)
			splitdates.append(dateformatted)
		for d1 in splitdates:
			for d2 in splitdates:
				if((d1.year - d2.year) * 12 + d1.month - d2.month) < 8 or ((d1.year == d2.year) and (d1.month == d2.month) and ((d1.day - d2.day) >= 2)):
					return False
	return True

# US14: No more than 5 sibilings should be born at the same time
# Input: famID tag from families Dictionary
def siblingSameBirth(famID):
	if(famID not in families):
		return False
	if("CHIL" not in families[famID]):
		return True
	children = families[famID]["CHIL"]
	if(len(children) <= 5):
		return True
	else:
		birthday_siblings = {}
		for child in children:
			if(parseDate(individual[child]['BIRT']) in birthday_siblings):
				birthday_siblings[parseDate(individual[child]['BIRT'])] += 1
			else:
				birthday_siblings[parseDate(individual[child]['BIRT'])] = 1
		for i in birthday_siblings:
			if (birthday_siblings[i] >= 5):
				return False
		return True

# US15: checks to see that a family has less then 15 siblings
# Input: famID tag from families Dictionary
def less15Siblings(famID):
	if(famID not in families):
		return False
	if("CHIL" not in families[famID]):
		return True

	children = families[famID]["CHIL"]

	if(len(children) >= 15):
		return False
	else:
		return True

# Helper function that parser the last name of the individual
# Input: id tag from individual Dictionary
def parserLastName(id):
	if (id not in individual or 'NAME' not in individual[id]):
		return ""
	else:
		name = individual[id]['NAME'].split()
		return name[1][1:-1]

<<<<<<< HEAD
# US16: checks to see that a family has less then 15 siblings
# Input: id tag from individual Dictionary
=======
# Helper function for US16
# Input: famID tag from families Dictionary
>>>>>>> 9682265c52a15ce413525ed773b3f35fc03d8de8
def maleLastNameHelper(id):
	if(id not in individual):
		return False
	if('FAMS' in individual[id]):
		famSpouse = individual[id]['FAMS'][0]
	else:
		famSpouse = None
	if('FAMC' in individual[id]):
		famChild = individual[id]['FAMC']
	else:
		famChild = None
	if(famChild == None):
		if (famSpouse == None):
			return True
		else:
			familyLastName[famSpouse] = parserLastName(id)
			return True
	if(famChild in familyLastName):
		if(familyLastName[famChild] == parserLastName(id)):
			familyLastName[famSpouse] = familyLastName[famChild]
			return True
		else:
			familyLastName[famSpouse] = parserLastName(id)
			return False
	else:
		return False

<<<<<<< HEAD
# US016: checks to see that a family has less then 15 siblings
# Input: id tag from individual Dictionary
=======
# US16: checks to see that a family has less then 15 siblings
# Input: famID tag from families Dictionary
>>>>>>> 9682265c52a15ce413525ed773b3f35fc03d8de8
def maleLastName(id):
	if (id not in individual or individual[id]['SEX'] != 'M'):
		return False
	if ('FAMS' not in individual[id]):
		lastNameBool[id] = maleLastNameHelper(id)
	else:
		lastNameBool[id] = maleLastNameHelper(id)
		children = families[individual[id]['FAMS'][0]]['CHIL']
		for chil in children:
			if (individual[chil]['SEX'] == 'M'):
				maleLastName(chil)
	return True

<<<<<<< HEAD
# US23: check to see if there is only one person with the same
# 		name and birthday.
# Input: id tag from individual Dictionary
def uniqueName(id):
	if (id not in individual):
		return [[],False]

	sameName = []
	for people in individual:
		if (people != id and individual[id]['NAME'] == individual[people]['NAME']):
			if (individual[id]['BIRT'] == individual[people]['BIRT']):
				sameName.append(people)

	if (len(sameName) != 0):
		return [sameName, True]
	else:
		return [[], False]

def uniqueFamilySpouse(famid):
	if (famid not in families):
		return [[], False]

	sameFamily = []
	wife = families[famid]['WIFE'][0]
	husband = families[famid]['HUSB'][0]

	for family in families:
		if (famid != family and families[family]['WIFE'][0] == wife and families[famid]['HUSB'][0] == husband):
			if(families[family]['MARR'] == families[famid]['MARR']):
				sameFamily.append(family)

	if (len(sameFamily) != 0):
		return [sameFamily, True]
	else:
		return [[], False]
=======
# US17: checks for parent + children marriage
# Input: famID from families dictionary
# TODO: test US17
def noChildrenMarriage(famID):
	if famID not in families:
		return False
	# save husband and wife id
	family = families[famID]
	parents = [family['HUSB'], family['WIFE']]
	# for every INDI children in list
	for child in family['CHIL']:
		if 'FAMS' not in individual[child]:
			pass
		# check if any of their spouses in FAMS matches the parents
		for fam in individual[child]['FAMS']:
			newfamily = families[fam]
			spouses = [newfamily['HUSB'], newfamily['WIFE']]
			if parents in spouses:
				return False
	return True

# US18: checks for sibling marriage
# Input: famID	# use len()
def noSiblingMarriage(famID):
	if famID not in families:
		return False
	# check if an only child, return true if yes
	family = families[famID]
	childrenList = family['CHIL']
	if len(childrenList) < 2:
		return True
	# go through spouse list in each kid
	for child in childrenList:
		childFamilyList = individual[child]['FAMS']
		# go through every family kid's a spouse of
		for childFam in childFamilyList:
			# find opposite spouse id
			if childFam['HUSB'] != child:
				spouse = childFam['HUSB']
			else:
				spouse = childFam['WIFE']
			# if spouse is sibling, return false
			if spouse in childrenList:
				return False
	return True

>>>>>>> 9682265c52a15ce413525ed773b3f35fc03d8de8
def Sprint1():
	for id in individual:
		# US01 error check
		if (datesBeforeCurrentDate(id)[0] == False):
			print("ERROR: INDIVIDUAL: US01: " + id + ": Birthday " + individual[id]['BIRT']
						+ " occurs in the future")
			csv_file.write("ERROR: INDIVIDUAL: US01: " + id + ": Birthday " + individual[id]['BIRT']
						+ " occurs in the future")
			csv_file.write("\n")
		if (datesBeforeCurrentDate(id)[1] == False):
			print("ERROR: INDIVIDUAL: US01: " + id + ": Death " + individual[id]['DEAT']
						+ " occurs in the future")
			csv_file.write("ERROR: INDIVIDUAL: US01: " + id + ": Death " + individual[id]['DEAT']
						+ " occurs in the future")
			csv_file.write("\n")
		# US03 error check
		if (birthBeforeDeath(id) == False):
			print("ERROR: INDIVIDUAL: US03: " + id + ": Died " + individual[id]['DEAT'] + " before born "
						+ individual[id]['BIRT'])
			csv_file.write("ERROR: INDIVIDUAL: US03: " + id + ": Died " + individual[id]['DEAT'] + " before born "
						+ individual[id]['BIRT'])
			csv_file.write("\n")
		# US07 error check
		if (lessThan150(id) == False):
			if ("DEAT" not in individual[id]):
				death = "NA"
			else:
				death = individual[id]["DEAT"]
			print("ERROR: INDIVIDUAL: US07: " + id + ": More than 150 years old - Birth - "
						+ individual[id]['BIRT'] + " - Death - "
						+ death)
			csv_file.write("ERROR: INDIVIDUAL: US07: " + id + ": More than 150 years old - Birth - "
						+ individual[id]['BIRT'] + " - Death - "
						+ death)
			csv_file.write("\n")
		# US08 error check
		if (marriageBeforeBirth(id) == False):
			famID = individual[id]['FAMC']
			print("ANOMALY: FAMILY: US08: " + famID + ": Child " + id + " born "
						+ individual[id]['BIRT'] + " before marriage on " + families[famID]["MARR"])
			csv_file.write("ANOMALY: FAMILY: US08: " + famID + ": Child " + id + " born "
						+ individual[id]['BIRT'] + " before marriage on " + families[famID]["MARR"])
			csv_file.write("\n")
		# US08 error check
		if (divorceAfterBirth(id) == False):
			famID = individual[id]['FAMC']
			print("ANOMALY: FAMILY: US08: " + famID + ": Child " + id + " born "
						+ individual[id]['BIRT'] + " after divorce on " + families[famID]["DIV"])
			csv_file.write("ANOMALY: FAMILY: US08: " + famID + ": Child " + id + " born "
						+ individual[id]['BIRT'] + " after divorce on " + families[famID]["DIV"])
			csv_file.write("\n")

	for famID in families:
		# US01 error check
		if(datesBeforeCurrentDate(famID)[0] == False):
			print("ERROR: FAMILY: US01: " + famID + ": Marriage " + families[famID]['MARR']
						+ " occurs in the future")
			csv_file.write("ERROR: FAMILY: US01: " + famID + ": Marriage " + families[famID]['MARR']
						+ " occurs in the future")
			csv_file.write("\n")
		if(datesBeforeCurrentDate(famID)[1] == False):
			print("ERROR: FAMILY: US01: " + famID + ": Divorce " + families[famID]['DIV']
						+ " occurs in the future")
			csv_file.write("ERROR: FAMILY: US01: " + famID + ": Divorce " + families[famID]['DIV']
						+ " occurs in the future")
			csv_file.write("\n")
		# US02 error check
		if (bornBeforeMarriage(famID)[0] == False):
			husband = families[famID]['HUSB'][0]
			marriage = parseDate(families[famID]['MARR'])
			birth = parseDate(individual[husband]['BIRT'])
			print("ERROR: FAMILY: US02: " + famID + ": Husband's birth date " + birth
						+ " after marriage date " + marriage)
			csv_file.write("ERROR: FAMILY: US02: " + famID + ": Husband's birth date " + birth
						+ " after marriage date " + marriage)
			csv_file.write("\n")
		if (bornBeforeMarriage(famID)[1] == False):
			wife = families[famID]['WIFE'][0]
			marriage = parseDate(families[famID]['MARR'])
			birth = parseDate(individual[wife]['BIRT'])
			print("ERROR: FAMILY: US02: " + famID + ": Wife's birth date " + birth
						+ " after marriage date " + marriage)
			csv_file.write("ERROR: FAMILY: US02: " + famID + ": Wife's birth date " + birth
						+ " after marriage date " + marriage)
			csv_file.write("\n")
		# US04 error check
		if (marriageBeforeDivorce(famID) == False):
			print("ERROR: FAMILY: US04: " + famID + ": Divorced " + families[famID]["DIV"] + " before married "
						+ families[famID]["MARR"])
			csv_file.write("ERROR: FAMILY: US04: " + famID + ": Divorced " + families[famID]["DIV"] + " before married "
						+ families[famID]["MARR"])
			csv_file.write("\n")
		# US05 error check
		if (marriageBeforeDeath(famID)[0] == False):
			husband = families[famID]['HUSB'][0]
			marriage = parseDate(families[famID]['MARR'])
			death = parseDate(individual[husband]['DEAT'])
			print("ERROR: FAMILY: US05: " + famID + ": Married " + marriage
						+ " after husbands (" + husband +") death on " + death)
			csv_file.write("ERROR: FAMILY: US05: " + famID + ": Married " + marriage
						+ " after husband's (" + husband +") death on " + death)
			csv_file.write("\n")
		if (marriageBeforeDeath(famID)[1] == False):
			wife = families[famID]['WIFE'][0]
			marriage = parseDate(families[famID]['MARR'])
			death = parseDate(individual[wife]['DEAT'])
			print("ERROR: FAMILY: US05: " + famID + ": Married " + marriage
						+ " after wife's (" + wife +") death on " + death)
			csv_file.write("ERROR: FAMILY: US05: " + famID + ": Married " + marriage
						+ " after wife's (" + wife +") death on " + death)
			csv_file.write("\n")
		# US06 error check
		if (divorceBeforeDeath(famID)[0] == False):
			husband = families[famID]['HUSB'][0]
			divorce = parseDate(families[famID]['DIV'])
			death = parseDate(individual[husband]['DEAT'])
			print("ERROR: FAMILY: US06: " + famID + ": Divorced " + divorce
						+ " after husbands (" + husband +") death on " + death)
			csv_file.write("ERROR: FAMILY: US06: " + famID + ": Divorced " + divorce
						+ " after husbands (" + husband +") death on " + death)
			csv_file.write("\n")
		if (divorceBeforeDeath(famID)[1] == False):
			wife = families[famID]['WIFE'][0]
			divorce = parseDate(families[famID]['DIV'])
			death = parseDate(individual[wife]['DEAT'])
			print("ERROR: FAMILY: US06: " + famID + ": Divorced " + divorce
						+ " after wife's (" + wife +") death on " + death)
			csv_file.write("ERROR: FAMILY: US06: " + famID + ": Divorced " + divorce
						+ " after wife's (" + wife +") death on " + death)
			csv_file.write("\n")

def Sprint2():
	for id in individual:
		if (individual[id]['SEX'] == 'M' and 'FAMC' not in individual[id]):
			maleLastName(id)

<<<<<<< HEAD
=======
	for famID in families:
		if (siblingSpacing(famID) == False):
			print("ERROR: FAMILY: US13: " + famID + ": Children are born too close together")
			csv_file.write("ERROR: FAMILY: US13: " + famID + ": Children are born too close together")
			csv_file.write("\n")
		if (siblingSameBirth(famID) == False):
			print("ERROR: FAMILY: US14: " + famID + ": More than 5 siblings have the same birth")
			csv_file.write("ERROR: FAMILY: US15: " + famID + ": More than 5 siblings have the same birth")
			csv_file.write("\n")
		if (less15Siblings(famID) == False):
			print("ERROR: FAMILY: US15: " + famID + ": Family has more than 15 chilren")
			csv_file.write("ERROR: FAMILY: US15: " + famID + ": Family has more than 15 chilren")
			csv_file.write("\n")

	for id in lastNameBool:
		if(lastNameBool[id] == False):
			father = families[individual[id]['FAMC']]['HUSB'][0]
			fatherName = individual[father]['NAME']
			print("ANOMALY: INDIVIDUAL: US16: " + id + ": " + id + ", " + individual[id]['NAME'] +
						 " has different last name then father " + father + ", " + fatherName)
			csv_file.write("ANOMALY: INDIVIDUAL: US16: " + id + ": " + id + ", " + individual[id]['NAME'] +
						 " has different last name then father " + father + ", " + fatherName)
			csv_file.write("\n")
	
	for id in individual:
>>>>>>> 9682265c52a15ce413525ed773b3f35fc03d8de8
		if (noBigamy(id) == False):
			print('ERROR: INDIVIDUAL: US11: ' + id + ' is married to multiple people at the same time')
			csv_file.write('ERROR: INDIVIDUAL: US11: ' + id + ' is married to multiple people at the same time')
			csv_file.write("\n")

		# US09 - bornBeforeParentDeath : [wife death, husb death]
		if (bornBeforeParentDeath(id) == 'INDVIDERROR'):
			print("ERROR: INDIVIDUAL: US09:  " + id +
				": ID is giving an erro")
		if (bornBeforeParentDeath(id) == 'FAMIDERROR'):
			print("ERROR: INDIVIDUAL: US09:  " + id +
				": ID is giving an error")
		if (bornBeforeParentDeath(id) == 'NOTACHILD'):
			pass
		if (bornBeforeParentDeath(id)[0] == False):
			print("ERROR: US09: INDIVIDUAL: " + id +
				": Mother died before birth of " + individual[id]['NAME'] )
		if (not bornBeforeParentDeath(id)[1]):
			print("ERROR: US09: INDIVIDUAL: " + id +
				": Father died 6 months before birth of " + individual[id]['NAME'] )
		# US16 - maleLastName
		if (individual[id]['SEX'] == 'M' and 'FAMC' not in individual[id]):
			maleLastName(id)

	for id in lastNameBool:
		if(lastNameBool[id] == False):
			father = families[individual[id]['FAMC']]['HUSB'][0]
			fatherName = individual[father]['NAME']
			print("ANOMALY: INDIVIDUAL: US16: " + id + ": " + id + ", " + individual[id]['NAME'] +
						 " has different last name then father " + father + ", " + fatherName)
			csv_file.write("ANOMALY: INDIVIDUAL: US16: " + id + ": " + id + ", " + individual[id]['NAME'] +
						 " has different last name then father " + father + ", " + fatherName)
			csv_file.write("\n")

	for famID in families:
		# US13
		if (siblingSpacing(famID) == False):
			print("ERROR: FAMILY: US13: " + famID + ": Children are born too close together")
			csv_file.write("ERROR: FAMILY: US13: " + famID + ": Children are born too close together")
			csv_file.write("\n")

		# US14
		if (siblingSameBirth(famID) == False):
			print("ERROR: FAMILY: US14: " + famID + ": More than 5 siblings have the same birth")
			csv_file.write("ERROR: FAMILY: US15: " + famID + ": More than 5 siblings have the same birth")
			csv_file.write("\n")

		# US15
		if (less15Siblings(famID) == False):
			print("ERROR: FAMILY: US15: " + famID + ": Family has more than 15 chilren")
			csv_file.write("ERROR: FAMILY: US15: " + famID + ": Family has more than 15 chilren")
			csv_file.write("\n")

		# US10 - marriageAfter14 : [ wife, husb ]
		if (not marriageAfter14(famID)[0]):
			print("ERROR: FAMILY: US10:  " + famID +
				": Mother married before 14" )
		if (not marriageAfter14(famID)[1]):
			print("ERROR: FAMILY: US10:  " + famID +
				": Father married before 14" )

		# US15 - less15Siblings
		if (less15Siblings(famID) == False):
			print("ERROR: FAMILY: US15: " + famID + ": Family has more than 15 chilren")
			csv_file.write("ERROR: FAMILY: US15: " + famID + ": Family has more than 15 chilren")
			csv_file.write("\n")

		if (parentsNotTooOld(famID) == False):
			print('ERROR: FAMILY: US12: ' + famID + ': A parent gave birth to a kid while too old')
			csv_file.write('ERROR: FAMILY: US12: ' + famID + ': A parent gave birth to a kid while too old')
			csv_file.write("\n")

def Sprint3():
<<<<<<< HEAD

	for id in individual:
		uniqueResults = uniqueName(id)
		if (uniqueResults[1]):
			print('ERROR: INDIVIDUAL: US23: ' + id + ': Individial has the same name and birthday as ', end = "")
			print(*uniqueResults[0], sep= ", ")
			# csv_file.write('ERROR: INDIVIDUAL: US23: ' + id + ': Individial has the same name and birthday as ' + *uniqueResults[0], sep= ", ")
			# csv_file.write("\n")

	for famID in families:
		uniqueResults = uniqueFamilySpouse(famID)
		if (uniqueResults[1]):
			print('ERROR: FAMILY: US24: ' + famID + ': Family has the same Spouses and marriage date as ', end = "")
			print(*uniqueResults[0], sep= ", ")
			# csv_file.write('ERROR: FAMILY: US24: ' + famID + ': Family has the same Spouses and marriage date as ' + *uniqueResults[0], sep= ", ")
			# csv_file.write("\n")
=======
	return False
>>>>>>> 9682265c52a15ce413525ed773b3f35fc03d8de8

# added a default file for testing purposes
if(len(sys.argv) >= 2):
	gedFile = str(sys.argv[1])
else:
	gedFile = 'test_bigamy_and_parents_age.ged'
	# gedFile = 'test_error_family.ged'

parser(gedFile)
display()
# Sprint1()
# Sprint2()
Sprint3()
<<<<<<< HEAD
=======
# print("\n")
# print(individual)
# print("\n")
# print(families)

# Aaron: added I8 (Cammy Victor) and F18 (James + Cammy) for US17 testing to test_bigamy_and_parents_age.ged
>>>>>>> 9682265c52a15ce413525ed773b3f35fc03d8de8
