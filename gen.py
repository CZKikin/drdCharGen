#!/usr/bin/python3
import random
def vyberZeSouboru(soubor):
    char = {}
    objekty = []
    with open(soubor, "r") as f:
        data = f.readlines()
        keys = data[0].replace("#","").strip().split(";")
        for i in data:
            if i[0]!="#" and i!="":
                objekty.append(i.strip()) 

    objekt = random.choice(objekty)
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

char = vyberZeSouboru("classes")
rasa = vyberZeSouboru("races")
nahradNedostatky(char, rasa)

with open("names", "r") as f:
    char["jmeno"] = random.choice(f.readlines()).strip()
vypisCharakteru(char)
