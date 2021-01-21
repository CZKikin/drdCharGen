#!/usr/bin/python3
import random, subprocess
def vypocitejPostihy(char, hlavniStaty):
    switcher = {1: -5, 2: -4, 3: -4, 4: -3, 5: -3, 6: -2, 7: -2, 8: -1, 9: -1,
            10: 0, 11: 0, 12: 0, 13: 1, 14: 1, 15: 2, 16: 2, 17: 3, 18: 3,
            19: 4, 20: 4, 21: 5}
    postihleStaty = ["sila","obratnost","odolnost","inteligence","charisma"]
    for i in postihleStaty:
        if switcher[char[i]] < 0:
            print(f"Postih {i}: {char[i]} {switcher[char[i]]}")
            char[i] = str(char[i]) + f" {str(switcher[char[i]])}"
        else:
            print(f"Postih {i}: {char[i]} +{switcher[char[i]]}")
            char[i] = str(char[i]) + f" +{str(switcher[char[i]])}"

def vypocitejHp(char):
    tabulka = {"valecnik": (10,10,0),
            "hranicar": (8,6,2),
            "alchymista": (7,6,1),
            "kouzelnik": (6,6,0),
            "zlodej": (6,6,0)}
    zaklad, kostka, bonus = tabulka[char["povolani"]]
    hod = random.randint(1,kostka)
    print(f"Hp: {zaklad} + hodil si: {hod} + {bonus}")
    return zaklad + hod + bonus

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
    hlavniStaty = [] 
    for i in nahraditelne:
        if char[i] == "x":
            char[i] = rasa[i]
        else:
            hlavniStaty.append(i)
    for i in rasa:
        if i not in nahraditelne:
            char[i] = rasa[i]
    return hlavniStaty

def vypisCharakteru(char):
    print(f"""Jméno: {char["jmeno"]}
Povolání: {char["povolani"]}
Rasa: {char["rasa"]}
Třída Velikosti: {char["tridavel"]}
Životy: {char["hp"]}
Síla: {char["sila"]}
Inteligence: {char["inteligence"]}
Odolnost: {char["odolnost"]}
Obratnost: {char["obratnost"]}
Charisma: {char["charisma"]}""")

def vygenerujStaty(char, hlavniStaty):
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
        if i in hlavniStaty:
            print(f"Rasová oprava pro {i}: {char[i]} + {opravy[i]}")
            char[i] = char[i] + int(opravy[i])

        if char[i] < 1:
            char[i] = 1

def generateLows(char):
    staty = ["sila","obratnost","odolnost","inteligence","charisma"]
    minima = {}
    for i in staty:
        minima[i] = int(char[i].split("-")[0])
    return minima

def checkForLows(char, minima):
    staty = ["sila","obratnost","odolnost","inteligence","charisma"]
    for i in staty:
        if char[i] < minima[i]:
            char[i] = minima[i]

if __name__ == "__main__":        
    char = vyberZeSouboru("povolani")
    rasa = vyberZeSouboru("rasy")
    hlavniStaty = nahradNedostatky(char, rasa)
    minima = generateLows(char)

    with open("jmena", "r") as f:
        char["jmeno"] = random.choice(f.readlines()).strip()

    vygenerujStaty(char, hlavniStaty)
    checkForLows(char, minima)

    vypocitejPostihy(char, hlavniStaty)
    char["hp"] = vypocitejHp(char)
    print("===\nVypočtené staty\n===")
    vypisCharakteru(char)



