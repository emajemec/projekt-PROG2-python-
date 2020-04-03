import matplotlib.pyplot as plt
from math import *

annotations = {'Ljubljana':(46.056946, 14.505751), 'Maribor':(46.55472, 15.64667), 'Kranj':
               (46.23887, 14.35561), 'Koper':(45.54694, 13.72944), 'Novo mesto':(45.80397, 15.16886)}

attributes = None
instances = []

with open('cities.tab', 'r') as file:
    for i, line in enumerate(file):
        if i == 0:
            attributes = [atribute.strip() for attribute in line.split('\t')]
        else:
            instances.append([line[:line.find('\t')]] + [float(value) for value in line.split('\t')[1:]])

longitudes = [instance[2] for instance in instances]
latitudes = [instance[3] for instance in instances]
sizes = [instance[4] for instance in instances]
colors = [instance[1] for instance in instances]

fig = plt.figure()
plt.scatter(longitudes, latitudes, marker = 'o', s = [sqrt(s) for s in sizes],
            c = colors, cmap = 'Paired')
plt.colorbar()

for annotation in annotations:
    plt.scatter(annotations[annotation][1],annotations[annotation][0], marker = '*',
                s = 200, c = [0, 0, 0])
    
plt.xlabel('City longitude')
plt.ylabel('City latitude')
plt.title('Slovenian cities', fontweight = 'bold')
plt.show()



