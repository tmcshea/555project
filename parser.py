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
from datetime import datetime

#Global Dictionary for individual and families info
individual = {}
families = {}
csv_file = open('output.csv', mode='w')
noneLastName = []
#parser function, need file input to run
def parser(file):
    #Allows access to global variables
    global individual, families

    #Arrays of valid tags
    zeroLevel = ["NOTE", "HEAD", "TRLR"]
    zeroExcep = ["INDI", "FAM"]
    oneLevel = ["NAME", "SEX", "FAMC", "FAMS", "HUSB",
                    "WIFE", "CHIL"]
    oneDate = ["BIRT", "DEAT", "MARR", "DIV"]


    #Varibales
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
                    individual[id][dateType] =  ' '.join(inputs[2:])
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
                    individual[id][inputs[1]] = ' '.join(inputs[2:])
                elif(list == "families"):
                    if inputs[1] in families[id]:
                        families[id][inputs[1]].append(' '.join(inputs[2:]))
                    else:
                        families[id][inputs[1]] =  [' '.join(inputs[2:])]
            elif(inputs[1] in oneDate):
                dateNext = True
                dateType = inputs[1]

#Function to display individual and families information and creates a csv file
# with this information.
def display():
	# individuals informatio

    x = PrettyTable()
    x.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]

    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"])
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
        x.add_row([ids, individual[ids]["NAME"], individual[ids]["SEX"], individual[ids]["BIRT"], age, alive, death, child, spouse])
        writer.writerow([ids, individual[ids]["NAME"], individual[ids]["SEX"], individual[ids]["BIRT"], age, alive, death, child, spouse])

    # family/marriage information
    y = PrettyTable()
    y.field_names = ["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"]
    writer.writerow([])
    writer.writerow(["ID", "Married", "Divorced", "Husband ID", "Husband Name", "Wife ID", "Wife Name", "Children"])
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
        writer.writerow([ids, married, divorced, HUSB, husName, WIFE, wifName, child])
    csv_file.write("\n")
    print(x)
    print(y)

# function to put date in comparable format
def parseDate(date):
    formattedDate = (str(datetime.strptime(date, '%d %b %Y')).split(' ')[0])
    return formattedDate

# function that find the age of person given a date
def age(date):
    today = datetime.today()

    if(int(today.month) - int(date[5:7]) > 0):
        return (int(today.year) - int(date[:4]))
    elif(int(today.month) - int(date[5:7]) == 0 and int(today.day) - int(date[8:]) >=0):
        return (int(today.year) - int(date[:4]))
    else:
        return (int(today.year) - int(date[:4])) - 1

# US01: checks if all dates are before the current date
# Input: none, uses global vars created in main parser method: individual and families
# ************** NOT TESTED YET
def datesBeforeCurrentDate(id):
    now = datetime.today()	# today's date
    results = [True, True]
    if id in individual:	# individual dates: BIRT and DEAT
        if 'BIRT' in individual[id]:
            birth = parseDate(individual[id]['BIRT'])
            if birth > str(now):
                results[0] = False
        if 'DEAT' in individual[id]:
            death = parseDate(individual[id]['DEAT'])
            if death > str(now):
                results[1] = False
    if id in families:	# families dates: MARR and DIV
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
# Input: none, uses global vars created in main parser method: individual and families
# ************** NOT TESTED YET
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

# US08: checks if divorce is after child's birth
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

# US015: checks to see that a family has less then 15 siblings
# Input: famID tag from families Dictionary
def less15Siblings(famId):
    if(famID not in families):
        return False
    if("CHIL" not in families[famID]):
        return True

    children = families[famID]["CHIL"]

    if(len(children) >= 15):
        return False
    else:
        return True

# US016: checks to see that a family has less then 15 siblings
# Input: famID tag from families Dictionary
# def maleLastName(id):
#     if(id not in individual):
#         return False
#     if('FAMS' not in individual[id]):
#         return True

def Sprint1():
    for id in individual:

        #US01 error check
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

        #US03 error check
        if (birthBeforeDeath(id) == False):
            print("ERROR: INDIVIDUAL: US03: " + id + ": Died " + individual[id]['DEAT'] + " before born "
                        + individual[id]['BIRT'])
            csv_file.write("ERROR: INDIVIDUAL: US03: " + id + ": Died " + individual[id]['DEAT'] + " before born "
                        + individual[id]['BIRT'])
            csv_file.write("\n")
        #US07 error check
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
        #US08 error check
        if (marriageBeforeBirth(id) == False):
            famID = individual[id]['FAMC']
            print("ANOMALY: FAMILY: US08: " + famID + ": Child " + id + " born "
                        + individual[id]['BIRT'] + " before marriage on " + families[famID]["MARR"])
            csv_file.write("ANOMALY: FAMILY: US08: " + famID + ": Child " + id + " born "
                        + individual[id]['BIRT'] + " before marriage on " + families[famID]["MARR"])
            csv_file.write("\n")
        #US08 error check
        if (divorceAfterBirth(id) == False):
            famID = individual[id]['FAMC']
            print("ANOMALY: FAMILY: US08: " + famID + ": Child " + id + " born "
                        + individual[id]['BIRT'] + " after divorce on " + families[famID]["DIV"])
            csv_file.write("ANOMALY: FAMILY: US08: " + famID + ": Child " + id + " born "
                        + individual[id]['BIRT'] + " after divorce on " + families[famID]["DIV"])
            csv_file.write("\n")


    for famID in families:

        #US01 error check
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
        #US02 error check
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
        #US04 error check
        if(marriageBeforeDivorce(famID) == False):
            print("ERROR: FAMILY: US04: " + famID + ": Divorced " + families[famID]["DIV"] + " before married "
                        + families[famID]["MARR"])
            csv_file.write("ERROR: FAMILY: US04: " + famID + ": Divorced " + families[famID]["DIV"] + " before married "
                        + families[famID]["MARR"])
            csv_file.write("\n")

# added a default file for testing purposes
if(len(sys.argv) >= 2):
    gedFile = str(sys.argv[1])
else:
    gedFile = 'test_error_family.ged'

parser(gedFile)
display()
Sprint1()
