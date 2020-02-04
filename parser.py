"""
parser.py
Provides valid and invalid input to a ged file
Prints results to terminal or console and also output results to a txt file
Takes file input name through argv in the terminal

Author: Tyler McShea
Date: Jan 31, 2020
"""
import sys

def parser(file):
    zeroLevel = ["NOTE", "HEAD", "TRLR"]
    zeroExcep = ["INDI", "FAM"]
    oneLevel = ["NAME", "SEX", "FAMC", "FAMS", "HUSB",
                    "WIFE", "CHIL"]
    oneDate = ["BIRT", "DEAT", "MARR", "DIV"]
    dateNext = False
    print(zeroLevel)
    f = open(file, "r")
    out = open(file[:-4] + "_output.txt", "w")
    for lines in f:
        inputs = lines.split()
        if(dateNext):
            dateNext = False
            if(inputs[0] == "2" and inputs[1] == "DATE"):
                print("-->" + lines, end='')
                out.write("-->" + lines)
                print("<--" + inputs[0].strip() + "|" + inputs[1].strip() + "|Y|" + ' '.join(inputs[2:]))
                out.write("<--" + inputs[0].strip() + "|" + inputs[1].strip() + "|Y|" + ' '.join(inputs[2:])+
                            "\n")
            else:
                print("-->" + lines, end='')
                out.write("-->" + lines)
                print("<--" + inputs[0].strip() + "|" + inputs[1].strip() + "|N|" + ' '.join(inputs[2:]))
                out.write("<--" + inputs[0].strip() + "|" + inputs[1].strip() + "|N|" + ' '.join(inputs[2:])+
                            "\n")
        elif(inputs[0] == "0"):
            if(inputs[1] in zeroLevel):
                print("-->" + lines, end='')
                out.write("-->" + lines)
                print("<--" + inputs[0].strip() + "|" + inputs[1].strip() + "|Y|" + ' '.join(inputs[2:]))
                out.write("<--" + inputs[0].strip() + "|" + inputs[1].strip() + "|Y|" + ' '.join(inputs[2:])+
                            "\n")
            elif(len(inputs) >= 3 and inputs[2] in zeroExcep):
                print("-->" + lines, end='')
                out.write("-->" + lines)
                print("<--" + inputs[0].strip() + "|" + inputs[2].strip() + "|Y|" + inputs[1].strip())
                out.write("<--" + inputs[0].strip() + "|" + inputs[2].strip() + "|Y|" + inputs[1].strip()+
                            "\n")
            else:
                print("-->" + lines, end='')
                out.write("-->" + lines)
                print("<--" + inputs[0].strip() + "|" + inputs[1].strip() + "|N|" + ' '.join(inputs[2:]))
                out.write("<--" + inputs[0].strip() + "|" + inputs[1].strip() + "|N|" + ' '.join(inputs[2:])+
                            "\n")
        elif(inputs[0] == "1"):
            if(inputs[1] in oneLevel):
                print("-->" + lines, end='')
                out.write("-->" + lines)
                print("<--" + inputs[0].strip() + "|" + inputs[1].strip() + "|Y|" + ' '.join(inputs[2:]))
                out.write("<--" + inputs[0].strip() + "|" + inputs[1].strip() + "|Y|" + ' '.join(inputs[2:])+
                            "\n")
            elif(inputs[1] in oneDate):
                dateNext = True
                print("-->" + lines, end='')
                out.write("-->" + lines)
                print("<--" + inputs[0].strip() + "|" + inputs[1].strip() + "|Y|" + ' '.join(inputs[2:]))
                out.write("<--" + inputs[0].strip() + "|" + inputs[1].strip() + "|Y|" + ' '.join(inputs[2:])+
                            "\n")
            else:
                print("-->" + lines, end='')
                out.write("-->" + lines)
                print("<--" + inputs[0].strip() + "|" + inputs[1].strip() + "|N|" + ' '.join(inputs[2:]))
                out.write("<--" + inputs[0].strip() + "|" + inputs[1].strip() + "|N|" + ' '.join(inputs[2:])+
                            "\n")
        else:
            print("-->" + lines, end='')
            out.write("-->" + lines)
            print("<--" + inputs[0].strip() + "|" + inputs[1].strip() + "|N|" + ' '.join(inputs[2:]))
            out.write("<--" + inputs[0].strip() + "|" + inputs[1].strip() + "|N|" + ' '.join(inputs[2:])+
                        "\n")


parser(str(sys.argv[1]))
