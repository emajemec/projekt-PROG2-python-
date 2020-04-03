import requests
import re
import urllib3
import matplotlib.pyplot as plt
import matplotlib.image as img
from math import *


class Instruktor:
    def __init__(self, ime, predmet, kraj, reference, razpolozljivost, stUcencev, ure, slika):
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
    #slika = requests.get('https://www.go-tel.si/instrukcije/'+urlslika).text

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
    predmetipod = re.search(r'.*content=.+predmetov\:(.+)Individualno.*', instr)
    predmetipod1 = predmetipod.group(1)
    predmeti = []
    
    if 'v krajih' in predmetipod1:
        pred, _ = predmetipod1.split('v krajih')
    else:
        pred = predmetipod1
    pred = pred.strip()

    predmeti = pred.split(', ')


    print(predmeti)

    print(ime, razpolozljivost, cena, reference, kraj, starost, ure, ucenci, urlslika)
    nek_instruktor = Instruktor(ime, predmeti, kraj, reference, razpolozljivost, ucenci, ure, urlslika)
    seznam = SeznamInst()
    seznam.dodaj(nek_instruktor)


##    # razdrobi niz na podatke
#inst = Instruktor(ime)
#seznam.dodaj(inst)

'''Ocena instruktorjev glede na uteži uporabnika in izpiše inštrukcije, ki je za uporabnika najbolj primeren.'''


TvojKraj = input('Vnesi kraj: ')
Predmet = input('Vnesi predmet: ')
UtezRef = int(input('Referenca: '))
UtezRaz = int(input('Razpoložljivost: '))
UtezUcenci = int(input('Ucenci: '))
UtezUre = int(input('Ure: '))

    
prejsnjaOcena = 0
for instr in seznam.sez:
    if instr.kraj == TvojKraj and Predmet in instr.predmet:
        Ocena = UtezRef*int(instr.reference) + UtezRaz*int(instr.razpolozljivost) + UtezUcenci*int(instr.stUcencev) + UtezUre*int(instr.ure)
    else:
        Ocena = 0
    if Ocena >= prejsnjaOcena:
        najInstruktor = instr
        prejsnjaOcena = Ocena
    else:continue
slika = img.imread('https://www.go-tel.si/instrukcije/'+najInstruktor.slika)
narisi = plt.imshow(slika)
plt.show()
print(najInstruktor.ime)

'''Na zemljevid Slovenije vriše kraje v katerih delujejo instruktorji,
    velikost kroga ponazarja število instrukotorjev, ki delujejo v tistem kraju,
    barva kroga pa označuje različne predmeta, ki ga v tistem kraju poučuje
    največ inštruktorjev.'''

annotations = {'Ljubljana':(46.056946, 14.505751), 'Maribor':(46.55472, 15.64667), 'Kranj':
               (46.23887, 14.35561), 'Koper':(45.54694, 13.72944), 'Novo mesto':(45.80397, 15.16886),
               'Domžale':(46.1394296, 14.5944553), 'Kamnik':(46.22833, 14.61917), 'Postojna':(45.77582438,14.2117877),
               'Ptuj':(46.419351,15.8709841), 'Tržič':(46.3636679,14.3095397),'Gorišnica':(46.4134821,16.0126903),
               'Solkan':(45.972742,13.649443),'Borovica':(48.600833,18.952778),'Ljutomer':(46.5187046,16.1967404),
               'Medvode':(46.1402476,14.413671),'Celje':(46.2309234,15.2659932),'Ivančna Gorica':(45.9385838,14.8042412),
               'Lenart':(46.5760851,15.8312836),'Miklavž na Dravskem polju':(46.5074,15.6974),'Izola':(45.5398936,13.65939),
               'Dolenjske Toplice':(45.7570315, 15.0590532),'Škofja Loka':(46.165274,14.3067474),'Ribnica':(45.321075,14.7321075),
               'Žirovnica':(46.4046083,14.1353229),'Brezovica pri Ljubljani':(45.9480324,14.4180336),
               'Šentjanž pri Dravogradu':(46.5611,15.0389),'Naklo':(46.2727024,14.3163742)}

SlovarKrajev = dict()
for instr in seznam.sez:   #Posamezen instruktor iz seznama vseh
    if Predmet not in instr.predmet:continue
    if instr.kraj not in SlovarKrajev:
        SlovarKrajev[instr.kraj] = 1
    else:
        SlovarKrajev[instr.kraj] += 1     #Število inštruktorjev v posameznem kraju

longitudes = []
latitudes = []
sizes = []   #Seznam št. inštruktorjev v posameznem kraju
for kraj in SlovarKrajev:
        if kraj in annotations:
            longitudes.append(annotations[kraj][1])
            latitudes.append(annotations[kraj][0])
            sizes.append(SlovarKrajev[kraj])

fig = plt.figure()
#plt.scatter(longitudes, latitudes, marker = 'o', s = [s*10 for s in sizes], cmap = 'Paired')

    
img = plt.imread("SLOVENIA_.png")
fig, ax = plt.subplots()
ax.imshow(img, extent=[12.837371, 16.837371, 44.619316, 48.119316-0.5])
ax.scatter(longitudes, latitudes, marker = 'o', s = [s*10 for s in sizes], cmap = 'Paired')

for annotation in annotations:
    ax.annotate(annotation,(annotations[annotation][1],annotations[annotation][0]))
    
plt.xlabel('City longitude')
plt.ylabel('City latitude')
plt.title('Inštruktorji po Sloveniji', fontweight = 'bold')
plt.show()

