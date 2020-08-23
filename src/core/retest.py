import re
import sys

deciPattern = r"^[0-9]+$"
hexaPattern = r"^0[x|X][0-9a-fA-F]+$"
doublePattern = r"^[0-9]+.[0-9]*([e|E][+|-]?[0-9]+)?$"
strPattern = r"^\"[^\"\n]*\"$"
user_input = sys.argv[1]
with open(user_input, "r") as myFile:
    data = myFile.read()

if(re.search(strPattern, data)):
    print("correct")
else:
    print("incorrect")
