#!/usr/bin/python3
import random
def vyberMenu(name, menuArr):
    print(f"{name}:")
    valid = False
    while not valid:
        for i in range(len(menuArr)):
            print(f"{i+1} {menuArr[i].split(';')[0]}")
        try:
            volba = int(input("Volím: "))
            valid = True
        except Exception as e:
            print(e)
    return menuArr[volba-1] 

def najdiOpravu(soubor, char):
    opravy = {}
    objekty = []
    with open(soubor, "r") as f:
        data = f.readlines()
        keys = data[0].replace("#","").strip().split(";")
        for i in data:
            if i[0]!="#" and i!="":
                objekty.append(i.strip()) 

    for i in objekty:
        if i.split(";")[0].lower() == char["rasa"]:
            objekt = i.split(";")

    for i, j in zip(keys, objekt):
        opravy[i] = j

    return opravy 

def vyberZeSouboru(soubor):
    char = {}
    objekty = []
    with open(soubor, "r") as f:
        data = f.readlines()
        keys = data[0].replace("#","").strip().split(";")
        for i in data:
            if i[0]!="#" and i!="":
                objekty.append(i.strip()) 

    objekt = vyberMenu(keys[0],objekty)
    objekt = objekt.split(";")
    for i, j in zip(keys, objekt):
        char[i] = j

    return char

def nahradNedostatky(char, rasa):
    nahraditelne = ["sila","obratnost","odolnost","inteligence","charisma"]
    for i in nahraditelne:
        if char[i] == "x":
            char[i] = rasa[i]
    for i in rasa:
        if i not in nahraditelne:
            char[i] = rasa[i]

def vypisCharakteru(char):
    print(f"""Jméno: {char["jmeno"]}
Povolání: {char["povolani"]}
Rasa: {char["rasa"]}
Třída Velikosti: {char["tridavel"]}
Síla: {char["sila"]}
Inteligence: {char["inteligence"]}
Odolnost: {char["odolnost"]}
Obratnost: {char["obratnost"]}
Charisma: {char["charisma"]}""")

def vygenerujStaty(char):
    switcher = {5: 1, 10: 2, 15: 3}
    staty = ["sila","obratnost","odolnost","inteligence","charisma"]
    opravy = najdiOpravu("tabOprav", char)
    for i in staty:
        meze = char[i].split("-")
        pocetHodu = int(meze[1]) - int(meze[0])
        pocetHodu = switcher[pocetHodu]
        bonus = int(meze[0]) - pocetHodu 
        hod = 0

        for j in range(pocetHodu):
            hod += random.randint(1,6)
            print(f"Hodil si {hod} pro {i}")

        char[i] = hod + bonus
        print(f"Rasová oprava pro {i}: {char[i]} + {opravy[i]}")
        char[i] = char[i] + int(opravy[i])

if __name__ == "__main__":        
    char = vyberZeSouboru("povolani")
    rasa = vyberZeSouboru("rasy")
    nahradNedostatky(char, rasa)

    with open("jmena", "r") as f:
        char["jmeno"] = random.choice(f.readlines()).strip()

    print("Základ\n===")
    vypisCharakteru(char)
    print("===")

    vygenerujStaty(char)
    print("===\nVypočtené staty\n===")
    vypisCharakteru(char)


