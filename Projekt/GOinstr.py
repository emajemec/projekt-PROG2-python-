import requests
import re
import urllib3
import matplotlib.pyplot as plt
import matplotlib.image as img
from math import *
from PIL import Image
from io import BytesIO



class Instruktor:
    def __init__(self, ime, kraj, predmeti, reference, razpolozljivost, ucenci, ure, slika):
        self.ime = ime
        self.predmeti = predmeti
        self.kraj = kraj
        self.reference = reference
        self.razpolozljivost = razpolozljivost
        self.ucenci = ucenci
        self.ure = ure
        self.slika = slika

class SeznamInst:
    def __init__(self, seznam=[]):
        self.sez = seznam
    def dodaj(self, instruktor):
        self.sez.append(instruktor)

f = open('instruktorji.txt', 'r')
i = 1
for vrstica in f.readlines():
    ime, kraj, predmeti, reference, razpolozljivost, ucenci, ure = vrstica.split('-') 
    slika = 'instruktor'+str(i)+'.png'
    i += 1

    nek_instruktor = Instruktor(ime, kraj, predmeti, reference, razpolozljivost, ucenci, ure, slika)
    seznam = SeznamInst()
    seznam.dodaj(nek_instruktor)


Predmet = input('Vnesi predmet: ')
'''Na zemljevid Slovenije vriše kraje v katerih delujejo instruktorji,
    velikost kroga ponazarja število instrukotorjev, ki delujejo v tistem kraju,
    barva kroga pa označuje različne predmeta, ki ga v tistem kraju poučuje
    največ inštruktorjev.'''

annotations = {'Ljubljana':(46.056946, 14.505751), 'Maribor':(46.55472, 15.64667), 'Kranj':
               (46.23887, 14.35561), 'Koper':(45.54694, 13.72944), 'Novo mesto':(45.80397, 15.16886),
               'Domžale':(46.1394296, 14.5944553), 'Kamnik':(46.22833, 14.61917), 'Postojna':(45.77582438,14.2117877),
               'Ptuj':(46.419351,15.8709841), 'Tržič':(46.3636679,14.3095397),'Gorišnica':(46.4134821,16.0126903),
               'Solkan':(45.972742,13.649443),'Borovnica':(45.917833,14.3641778),'Ljutomer':(46.5187046,16.1967404),
               'Medvode':(46.1402476,14.413671),'Celje':(46.2309234,15.2659932),'Ivančna Gorica':(45.9385838,14.8042412),
               'Lenart':(46.5760851,15.8312836),'Miklavž na Dravskem polju':(46.5074,15.6974),'Izola':(45.5398936,13.65939),
               'Dolenjske Toplice':(45.7570315, 15.0590532),'Škofja Loka':(46.165274,14.3067474),'Ribnica':(45.73883,14.73077),
               'Žirovnica':(46.4046083,14.1353229),'Brezovica pri Ljubljani':(45.9480324,14.4180336),
               'Šentjanž pri Dravogradu':(46.5611,15.0389),'Naklo':(46.2727024,14.3163742)}

SlovarKrajev = dict()
for instr in seznam.sez:   #Posamezen instruktor iz seznama vseh
    if Predmet not in instr.predmeti:continue
    if instr.kraj not in SlovarKrajev:
        SlovarKrajev[instr.kraj] = 1
    else:
        SlovarKrajev[instr.kraj] += 1     #Število inštruktorjev v posameznem kraju

pravilni_kraji = dict()
for instr in seznam.sez:
    if Predmet in instr.predmeti:
        pravilni_kraji[instr.kraj] = annotations[instr.kraj]

longitudes = []
latitudes = []
sizes = []   #Seznam št. inštruktorjev v posameznem kraju
for kraj in pravilni_kraji:
    if kraj in pravilni_kraji:
        longitudes.append(pravilni_kraji[kraj][1])
        latitudes.append(pravilni_kraji[kraj][0])
        sizes.append(SlovarKrajev[kraj])

#fig = plt.figure()
#plt.scatter(longitudes, latitudes, marker = 'o', s = [s*10 for s in sizes], cmap = 'Paired')

    
img = plt.imread("SLOVENIA.jpg")
fig, ax = plt.subplots()
ax.imshow(img, extent=[13.3203, 16.6670, 45.4269, 46.8762])
ax.scatter(longitudes, latitudes, marker = 'o', s = [s*10 for s in sizes], cmap = 'Paired')

for annotation in pravilni_kraji:
    ax.annotate(annotation,(pravilni_kraji[annotation][1],pravilni_kraji[annotation][0]))
    
plt.xlabel('City longitude')
plt.ylabel('City latitude')
plt.title('Inštruktorji za predmet: '+Predmet, fontweight = 'bold')
plt.show()

'''Ocena instruktorjev glede na uteži uporabnika in izpiše inštrukcije, ki je za uporabnika najbolj primeren.'''


TvojKraj = input('Vnesi kraj: ')
i = 0
for instr in seznam.sez:
    if Predmet in instr.predmeti and TvojKraj == instr.kraj:
        i += 1
if i % 100 == 1:
    for instr in seznam.sez:
        if Predmet in instr.predmeti and TvojKraj == instr.kraj:
            print('Zate imamo na voljo '+ instr.ime)
elif i % 100 == 2:
    print('Zate imamo na voljo '+str(i)+' inštruktorja.')
elif (i % 100 == 3) or (i % 100 == 4):
    print('Zate imamo na voljo '+str(i)+' inštruktorje.')
else:
    print('Zate imamo na voljo '+str(i)+' inštruktorjev.')



if i % 100 >= 2:
    print(
        'Oceni, kaj ti je pri instruktorju najbolj pomembno in izvedel bos, kateri instruktor je najbolj primeren zate.')
    UtezRef = int(input('Referenca: '))
    UtezRaz = int(input('Razpoložljivost: '))
    UtezUcenci = int(input('Ucenci: '))
    UtezUre = int(input('Ure: '))

    prejsnjaOcena = 0
    for instr in seznam.sez:
        if instr.kraj == TvojKraj and Predmet in instr.predmeti:
            Ocena = UtezRef*int(instr.reference) + UtezRaz*int(instr.razpolozljivost) + UtezUcenci*int(instr.ucenci) + UtezUre*int(instr.ure)
        else:
            Ocena = 0
        if Ocena >= prejsnjaOcena:
            najInstruktor = instr
            prejsnjaOcena = Ocena
        else:continue

    image = Image.open(najInstruktor.slika)
    image.show()
    print(najInstruktor.ime)
else:
    for instr in seznam.sez:
        if instr.kraj == TvojKraj and Predmet in instr.predmeti:
            pravi_instr = instr
    image = Image.open(pravi_instr.slika)
    image.show()