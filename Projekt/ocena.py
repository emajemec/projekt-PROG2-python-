def utezi(self, kraj, reference, razpolozljivost, stUcencev, ure):
    ''' Na podlagi ocene uporabnika, program izpiše inštruktorja, ki je
    za uporabnika najbolj primeren.'''

    TvojKraj = input()
    UtezRef = input()
    UtezRaz = input()
    UtezUcenci = input()
    UtezUre = input()

    
    prejsnjaOcena = 0
    for instr in seznam:
        if kraj == TvojKraj:
            Ocena = UtezRef*reference + UtezRaz*razpolozljivost +
                UtezUcenci*stUcencev + UtezUre*ure
        else: continue
        if Ocena > prejsnjaOcena:
            najInstruktor = instr
            prejsnjaOcena = Ocena

    return najInstruktor, slika
