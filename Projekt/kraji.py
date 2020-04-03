import matplotlib.pyplot as plt
from math import *

def kraji():
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
        

