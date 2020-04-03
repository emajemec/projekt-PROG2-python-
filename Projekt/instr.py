import requests
import re
import urllib3
import matplotlib.pyplot as plt
from math import *

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
    vrstica = re.findall(r'class="nondecor">\w+\s*</a>', s)
    if len(vrstica) == 0: continue
    ime = re.match(r'class="nondecor">(\w+)\s*</a>', vrstica[0]).group(1)
    podatki = re.search(r'.*razpolozljivost="(\d+)".*reference="(\d+)".*razdalja="(\d+)".*starost="(\d+)".*href="(\d+)-(\w+)".*src="images/Instruktor(\w+).(\w+)".*', s, re.S)
    if podatki is None: continue
    razpolozljivost = podatki.group(1)
    reference = podatki.group(2)
    razdalja = podatki.group(3)
    starost = podatki.group(4)
    koda = podatki.group(5)+'-'+podatki.group(6)
    urlslika = 'images/Instruktor'+podatki.group(7)+'.'+podatki.group(8)
    slika = requests.get('https://www.go-tel.si/instrukcije/'+urlslika).text

    '''Za vsazga instruktorja posebi'''
    instr = requests.get('https://www.go-tel.si/instrukcije/'+ koda).text
    cenapod = re.search(r'.*onchange="cena\(\'(\d+)\'\).*', instr)
    cena = cenapod.group(1)
    krajpod = re.search(r'.*naslov=".+, (.+)"', instr)
    kraj = krajpod.group(1)
    urepod = re.search(r'.*<p>(\d+) ur</p>.*', instr)
    ure = urepod.group(1)
    ucencipod = re.search(r'.*<p>(\d+)\+.*', instr)
    ucenci = ucencipod.group(1)
    
    print(ime, razpolozljivost, cena, reference, kraj, starost, ure, ucenci, urlslika)
    
    
##    # razdrobi niz na podatke
#inst = Instruktor(ime)
#seznam.dodaj(inst)


'''Na zemljevid Slovenije vriše kraje v katerih delujejo instruktorji,
    velikost kroga ponazarja število instrukotorjev, ki delujejo v tistem kraju,
    barva kroga pa označuje različne predmeta, ki ga v tistem kraju poučuje
    največ inštruktorjev.'''

annotations = {'Ljubljana':(46.056946, 14.505751), 'Maribor':(46.55472, 15.64667), 'Kranj':
               (46.23887, 14.35561), 'Koper':(45.54694, 13.72944), 'Novo mesto':(45.80397, 15.16886)}


SlovarKrajev = dict()
for instr in seznam.sez:   #Posamezen instruktor iz seznama vseh
    if instr.kraj not in SlovarKrajev:
        SlovarKrajev[instr.kraj] = 1
    else:
        SlovarKrajev[instr.kraj] += 1     #Število inštruktorjev v posameznem kraju

longitudes = []
latitudes = []
sizes = []   #Seznam št. inštruktorjev v posameznem kraju
for kraj in SlovarKrajev:
        if kraj in annotations:
            longitudes.append(annotations[kraj][0])
            latitudes.append(annotations[kraj][1])
            sizes.append(SlovarKrajev[kraj])

fig = plt.figure()
plt.scatter(longitudes, latitudes, marker = 'o', s = [sqrt(s) for s in sizes], cmap = 'Paired')
plt.colorbar()

for annotation in annotations:
    plt.annotate(annotation,(annotations[annotation][1],annotations[annotation][0]))
    

plt.xlabel('City longitude')
plt.ylabel('City latitude')
plt.title('Slovenian cities', fontweight = 'bold')
plt.show()
