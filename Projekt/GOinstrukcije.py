import requests
import re


class Instruktor:
    def __init__(self,ime, predmet, kraj, reference, razpolozljivost, stUcencev, ure, slika):
        self.ime = ime
        self.predmet = predmet
        self.kraj = kraj
        self.reference = reference
        self.razpolozljivost = razpolozljivost
        self.stUcencev = stUcencev
        self.ure = ure
        self.slika = slika

class SeznamInst:
    def __init__(self, seznam=[]):
        self.sez = seznam
    def dodaj(self, instruktor):
        self.sez.append(instruktor)

seznam = SeznamInst()

page = requests.get('https://www.go-tel.si/instrukcije/instruktorji.php').text
tabela = re.split(r'<div class="cleared"></div>', page)[2]
instruktorji = re.split(r'<div class="instruktor_area insOkvir"', tabela)

for s in instruktorji:
    #vrstica = re.findall(r'class="nondecor">\w+\s*</a>', s)
    #if len(vrstica) == 0: continue
    #ime = re.match(r'class="nondecor">(\w+)\s*</a>', vrstica[0]).group(1)
    podatki = re.search(r'.*razpolozljivost="(\d+)".*cena="(\d+)".*', s, re.S)
    if podatki is None: continue
    razpolozljivost = podatki.group(1)
    cena = podatki.group(2)
    print(razpolozljivost, cena)
##    # razdrobi niz na podatke
#inst = Instruktor(ime)
#seznam.dodaj(inst)
