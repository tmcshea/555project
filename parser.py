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
    x = PrettyTable()
    x.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]

    with open('output.csv', mode='w') as csv_file:
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
    print(x)
    print(y)

# function to put date in comparable format
def parseDate(date):
    formattedDate = (str(datetime.strptime(date, '%d %b %Y')).split(' ')[0])
    return formattedDate

# checks if a persons birth is before their death
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

# checks if the marraige of a family is before a divorce. If no marraige or divorce, returns true
def marraigeBeforeDivorce(famID):
    if(famID not in families):
        return False
    if('DIV' in families[famID] and 'MARR' in families[famID]):
        marraige = parseDate(families[famID]['MARR'])
        divorce = parseDate(families[famID]['DIV'])
        if (marraige > divorce):
            return False
        else:
            return True
    return True

parser(str(sys.argv[1]))
display()
print(birthBeforeDeath('@I6@'))
print(marraigeBeforeDivorce('@F3@'))
