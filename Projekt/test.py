import requests
import re

conn = requests.get('https://www.go-tel.si/instrukcije/instruktorji.php?fbclid=IwAR0RndAXFVkwN4yQKtHnKKPA-ItIgvPbkVsWW4Ru-nPju9rn6EvaH07-FvA')

vsi = re.findall('<option value=".*?">', conn.text)

predelani = list()
for vsak in vsi:
    ime = vsak.replace('<option value="', '').replace('">', '')
    print(ime)
    if len(ime) > 3 and ime[3] == '-':
        predelani.append(ime)

