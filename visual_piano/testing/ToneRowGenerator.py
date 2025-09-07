import random


def generateToneRow():
    toneRowGenerate = True
    row = []
    while toneRowGenerate:
        
        tone = random.randint(1,12)
        if tone not in row:
            row.append(tone)
        if len(row) == 12:
            toneRowGenerate = False

    for i in row:
        print(i, end = " ")
    print("")
        
for i in range(20):
    generateToneRow()
        

