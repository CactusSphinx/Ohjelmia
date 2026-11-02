from math import *

class Ohjelma():
    def __init__(self):
        self.edellinen = 0
        self.edellinen1 = 0

        self.ToiminnanAloitus()

    def ToiminnanAloitus(self, event=None):
        #print(f"{self.ikkuna.winfo_width()}x{self.ikkuna.winfo_height()}")
        for _ in range(7, 1000):
            self.toimivat_yhdistelmät = []

            self.luku = _

            if self.luku%2 == 0:
                self.laajuus_maksimi = int(self.luku/2 - 1)
            else:
                self.laajuus_maksimi = int(self.luku//2)

            self.väli_maksimi = self.luku - 2

            for laajuus in range(1, self.laajuus_maksimi+1):
                for väli in range(1, self.väli_maksimi+1):
                    self.Toiminta(laajuus, väli)

            toimivat = ""

            for toimii in self.toimivat_yhdistelmät:
                toimivat += f"\n{toimii}"
                if len(toimivat.split("\n")) > 15:
                    break

            summa = 0
            summa1 = 0
            summa2 = 0

            for indeksi in self.toimivat_yhdistelmät:
                w = indeksi.split("+")
                #print(int(w[0]), int(w[1]))
                summa += int(w[0]) + int(w[1])

            for x in self.toimivat_yhdistelmät:
                a = int(x.split("+")[0])
                summa1 += a
                b = int(x.split("+")[1])
                summa2 += b

            #print(self.luku, summa, len(self.toimivat_yhdistelmät), summa-self.edellinen, summa1, summa2)
            print(self.luku, summa2, summa2-self.edellinen1)

            with open(r"C:\Users\User\Documents\luku.txt", "a") as f:
                f.write(str(self.luku)+"\n")
            with open(r"C:\Users\User\Documents\b.txt", "a") as h:
                h.write(str(summa2)+"\n")

            if summa2-self.edellinen1 == 1:
                with open(r"C:\Users\User\Documents\bingo.txt", "a") as g:
                    g.write(str(self.luku-1)+"\n")

            self.edellinen = summa
            self.edellinen1 = summa2

            toimivat = ""

    def Toiminta(self, eka, toka):
        lista = []
        while len(lista) < self.luku:
            for x in range(eka):
                if len(lista) == self.luku:
                    break
                else:
                    lista.append(True)
            for y in range(toka):
                if len(lista) == self.luku:
                    break
                else:
                    lista.append(False)

        self.Tarkistus(lista, eka, toka)


    def Tarkistus(self, lista, eka, toka):
        toimii = True
        for numero, osa in enumerate(lista):
            if osa == lista[-numero-1]:
                pass
            else:
                #print(f"{eka} + {toka} ei toimi")
                #print(f"{eka} + {toka}: {lista}")
                toimii = False
                break

        if toimii:
            for osa in lista:
                if osa == False:
                    toimii = True
                    break
                else:
                    toimii = False

        if toimii:
            self.toimivat_yhdistelmät.append("{} + {}".format(eka, toka))

Ohjelma()