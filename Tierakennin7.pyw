from math import *
from tkinter import *
from sys import platform
from time import sleep, time
from datetime import datetime
import turtle
import sympy

# HUOMIO: Ohjelma ei toimi, jos ei ole määritellyt tiettyjä tiedostopolkuja (esim. self.karttatiedosto).

class Ohjelma():
    def __init__(self):
        self.fontti = ("Courier", 24, "bold")
        self.fontti2 = ("Courier", 24, "italic")
        self.fontti3 = ("Courier", 14, "italic")

        self.komento1 = "setblock ~{} ~1 ~{} minecraft:red_wool\n"
        self.komento2 = "setblock ~{} ~1 ~{} minecraft:blue_wool\n"

        maan_nimi = ""
        kuvan_nimi = ""

        if platform == "linux" or platform == "linux2":
            self.tiedostosijainti = r"".format(maan_nimi)
            self.karttatiedosto = r"".format(kuvan_nimi)
        elif platform == "win32":
            self.tiedostosijainti = r""
            #self.tiedostosijainti = r"".format(maan_nimi)
            self.karttatiedosto = r"{}".format(kuvan_nimi)

        if platform == "linux" or platform == "linux2":
            self.varmuuskopio = r""
        elif platform == "win32":
            self.varmuuskopio = r""

        self.skaalaus = 3.4

        self.eka_kerta = True
        self.onko_klikattu = False
        self.piirtäjät = []
        self.kilpparit = []
        self.kilpparit5 = []
        self.viimeisin_x_lista5 = []
        self.kaaren_pistelista = []
        self.klikkaus_nro = 0

        if platform == "linux" or platform == "linux2": # self.interpolaatio:ta varten
            laajuus = 20
        elif platform == "win32":
            laajuus = 21

        self.ikkuna = Tk()
        if platform == "linux" or platform == "linux2":
            self.ikkuna.geometry('1658x850')
        elif platform == "win32":
            self.ikkuna.geometry("1654x909")
        self.ikkuna.configure(bg="#B7AAA7")
        self.ikkuna.title("Automaattinen tieverkoston rakentajatyökalu (ATR)")

        self.kehys1 = Frame(self.ikkuna, bg="#B7AAA7", borderwidth=10)
        self.kehys2 = Frame(self.ikkuna, bg="#B7AAA7", borderwidth=10)
        self.kehys3 = Frame(self.ikkuna, bg="#B7AAA7", borderwidth=10)

        self.aloitusviesti = Label(text="Syöte on muotoa:                "
                                        "\n +käyrä -käyrä +käänteis -käänteis"
                                        "\nx-min x-max y-min y-max paksuus ", master=self.ikkuna, font=("Courier", 14, "bold"), bg="#B7AAA7")

        self.x_akseli = Entry()
        self.y_akseli = Entry()
        self.skaalaaminen = Entry()

        self.suora = Button(text="Suora", master=self.kehys1, command=self.Suora, font=self.fontti, width=10, borderwidth=3, bg="gray")
        self.kaari = Button(text="Kaari", master=self.kehys1, command=self.Kaari, font=self.fontti, width=10, borderwidth=3, bg="gray")
        self.suorita = Button(text="Suorita", master=self.kehys1, command=self.TietojenKerääminen, font=self.fontti, width=10, borderwidth=3, foreground="lightgreen", bg="gray")
        self.kartta = Button(text="Kartta", master=self.kehys1, command=self.Kartta, font=self.fontti, width=10, borderwidth=3, foreground="blue", bg="gray")
        self.asetukset = Button(text="Asetukset", master=self.kehys1, command=self.Asetuksia, font=self.fontti, width=10, borderwidth=3, bg="gray")
        self.interpolaatio = Button(text="Interpolaatiopolynomi", master=self.kehys3, command=self.Interpolaatiopolynomi, font=self.fontti, width=laajuus, borderwidth=3, bg="gray")
        self.päivitä_kartta = Button(text="Päivitä kartta", master=self.kehys3, command=self.PäivitäKartta, font=self.fontti, width=15, borderwidth=3, foreground="orange", bg="gray")

        self.tekstikenttä = Text(self.kehys2, font=self.fontti3, wrap="none", width=148, height=33, borderwidth=3) #86

        self.tekstikentän_vierityspalkki = Scrollbar(self.kehys2, orient="horizontal")

        self.tekstikenttä.config(xscrollcommand=self.tekstikentän_vierityspalkki.set)
        self.tekstikentän_vierityspalkki.config(command=self.tekstikenttä.xview)

        self.Aloitus()

    def Aloitus(self):
        self.aloitusviesti.grid(row=0, column=0, padx=5, pady=5, sticky="NW")
        self.kehys1.grid(row=0, column=1, sticky="NE")
        self.asetukset.grid(row=0, column=1, sticky="E")
        self.suora.grid(row=0, column=2, padx=10, sticky="E")
        self.kaari.grid(row=0, column=3, sticky="E")
        self.kartta.grid(row=0, column=4, padx=10, sticky="E")
        self.suorita.grid(row=0, column=5, sticky="E")

        self.kehys2.grid(row=1, column=0, columnspan=2, sticky="NE")

        self.tekstikenttä.pack(side="top", fill="both", expand=True)
        self.tekstikentän_vierityspalkki.pack(side="bottom", fill="x")

        self.kehys3.grid(row=3, column=0, columnspan=2, sticky="NE")
        self.interpolaatio.grid(row=0, column=1, sticky="E")
        self.päivitä_kartta.grid(row=0, column=0, padx=10, sticky="E")

        self.ikkuna.mainloop()

    def Asetuksia(self):
        self.ikkuna4 = Tk()
        self.ikkuna4.configure(bg="#B7AAA7")
        self.ikkuna4.title("Asetukset")
        self.ikkuna4.resizable(False, False)

        #print(self.ikkuna.winfo_width(), self.ikkuna.winfo_height())

        self.ohjeet1 = Label(text="Käyrän peilaus", master=self.ikkuna4, font=self.fontti, bg="#B7AAA7")
        self.x_akseli_teksti = Label(text="x-akseli (\u2192)", master=self.ikkuna4, font=self.fontti, bg="#B7AAA7")
        self.y_akseli_teksti = Label(text="y-akseli (\u2191)", master=self.ikkuna4, font=self.fontti, bg="#B7AAA7")
        self.ohjeet2 = Label(text="Kartan skaalaus", master=self.ikkuna4, font=self.fontti, bg="#B7AAA7")

        self.x_akseli = Entry(self.ikkuna4, font=self.fontti2, width=10, borderwidth=3)
        self.y_akseli = Entry(self.ikkuna4, font=self.fontti2, width=10, borderwidth=3)
        self.skaalaaminen = Entry(self.ikkuna4, font=self.fontti2, width=10, borderwidth=3)

        self.ohjeet1.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.x_akseli_teksti.grid(row=1, column=0, padx=5, sticky="E")
        self.x_akseli.grid(row=1, column=1, padx=5, sticky="W")
        self.y_akseli_teksti.grid(row=2, pady=5, padx=5, column=0, sticky="E")
        self.y_akseli.grid(row=2, column=1, padx=5, sticky="W")
        self.ohjeet2.grid(row=3, column=0, columnspan=2, padx=5)
        self.skaalaaminen.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def TietojenKerääminen(self):
        with open(self.tiedostosijainti,"w") as f:
            f.write(r'tellraw @a ["",{"text":"' + f"{datetime.now()}"[:-7] + r'","color":"dark_red"}]'+'\n')
            f.write(r'tellraw @a ["",{"text":"Komennon suoritus onnistui seuraavilla asetuksilla:","color":"gold"}]'+'\n')
        tieto = self.tekstikenttä.get("1.0", "end-1c").split("\n")

        sisältö = []
        self.sijoitettava = ""

        lista2 = self.komento2.split()
        tarkistuskomento = lista2[0] + " {} " + lista2[4]

        for käyrä in tieto:
            self.kirjasto_plus = {}
            self.kirjasto_miinus = {}

            self.paksuus_plus_x = []
            self.paksuus_plus_y = []
            self.paksuus_miinus_x = []
            self.paksuus_miinus_y = []

            komponentit = käyrä.split()

            self.käyrä_plus = komponentit[0]
            self.käyrä_miinus = komponentit[1]
            self.käänteis_plus = komponentit[2]
            self.käänteis_miinus = komponentit[3]
            self.alaraja_x = komponentit[4]
            self.yläraja_x = komponentit[5]
            self.alaraja_y = komponentit[6]
            self.yläraja_y = komponentit[7]
            self.paksuus = int(komponentit[8])
            #self.ylös_peruskorkeudelta = int(komponentit[9])
            #self.alas_peruskorkeudelta = int(komponentit[10])

            if self.käyrä_plus != "-":
                self.PistelistanMuodostus(self.käyrä_plus, 1, 1)
            elif self.käyrä_miinus != "-":
                self.PistelistanMuodostus(self.käyrä_miinus, -1, 1)
            elif self.käänteis_plus != "-":
                self.PistelistanMuodostus(self.käänteis_plus, 1, -1)
            #if self.käänteis_miinus != "-":
            else:
                self.PistelistanMuodostus(self.käänteis_miinus, -1, -1)

            self.x_peilaus = self.x_akseli.get()
            self.y_peilaus = self.y_akseli.get()

            #with open(self.tiedostosijainti, "a") as f:
            def SijoitaTiedostoon():
                lista1 = self.komento.split()
                koordinaattiosio = lista1[1] + " " + lista1[2] + " " + lista1[3]

                if tarkistuskomento.format(koordinaattiosio) in sisältö:
                    pass
                elif self.komento in sisältö:
                    pass
                else:
                    #f.write(self.komento)
                    self.sijoitettava += self.komento + "\n"
                    sisältö.append(self.komento)

            for indeksi in range(len(self.paksuus_plus_x)):
                self.KomennonMuodostus(self.paksuus_plus_x[indeksi], self.paksuus_plus_y[indeksi], self.komento1)

                SijoitaTiedostoon()

            for indeksi in range(len(self.paksuus_miinus_x)):
                self.KomennonMuodostus(self.paksuus_miinus_x[indeksi], self.paksuus_miinus_y[indeksi], self.komento1)

                SijoitaTiedostoon()

            for x in self.kirjasto_plus:
                self.KomennonMuodostus(x, self.kirjasto_plus[x], self.komento2)

                SijoitaTiedostoon()

            for x in self.kirjasto_miinus:
                self.KomennonMuodostus(x, self.kirjasto_miinus[x], self.komento2)

                SijoitaTiedostoon()

            #f.write(r'tellraw @a {"text":"'+käyrä+r'","italic":true,"color":"dark_green"}'+'\n')
            self.sijoitettava += r'tellraw @a {"text":"'+käyrä+r'","italic":true,"color":"dark_green"}' + '\n'

        with open(self.tiedostosijainti, "a") as f:
            f.write(self.sijoitettava)

    def KomennonMuodostus(self, lista_x_indeksi, lista_y_indeksi, komento_pohja):
        if (self.x_peilaus == "" and self.y_peilaus == "") or (self.x_peilaus == "x" and self.y_peilaus == "z"):
            self.komento = komento_pohja.format(int(round(lista_x_indeksi, 0)), int(round(lista_y_indeksi, 0)))
        elif self.x_peilaus == "x" and self.y_peilaus == "-z":
            self.komento = komento_pohja.format(int(round(lista_x_indeksi, 0)), -int(round(lista_y_indeksi, 0)))
        elif self.x_peilaus == "-x" and self.y_peilaus == "z":
            self.komento = komento_pohja.format(-int(round(lista_x_indeksi, 0)), int(round(lista_y_indeksi, 0)))
        elif self.x_peilaus == "-x" and self.y_peilaus == "-z":
            self.komento = komento_pohja.format(-int(round(lista_x_indeksi, 0)), -int(round(lista_y_indeksi, 0)))
        elif self.x_peilaus == "z" and self.y_peilaus == "x":
            self.komento = komento_pohja.format(int(round(lista_y_indeksi, 0)), int(round(lista_x_indeksi, 0)))
        elif self.x_peilaus == "z" and self.y_peilaus == "-x":
            self.komento = komento_pohja.format(int(round(lista_y_indeksi, 0)), -int(round(lista_x_indeksi, 0)))
        elif self.x_peilaus == "-z" and self.y_peilaus == "x":
            self.komento = komento_pohja.format(-int(round(lista_y_indeksi, 0)), int(round(lista_x_indeksi, 0)))
        #if self.x_peilaus == "-z" and self.y_peilaus == "-x":
        else:
            self.komento = komento_pohja.format(-int(round(lista_y_indeksi, 0)), -int(round(lista_x_indeksi, 0)))

    def PistelistanMuodostus(self, ratkaisu, kirjasto, tila): # Muodostaa lopullisen pistelistan komentojen muodostamista varten
        if tila == 1: # x --> y(x), "normaali" funktio
            for x in range(int(self.alaraja_x), int(self.yläraja_x) + 1, 1):
                try:
                    y = eval(ratkaisu)
                except:
                    continue

                säde = int(self.paksuus / 2)

                if self.yläraja_y != "-" and self.alaraja_y != "-":
                    if y > int(self.yläraja_y) or y < int(self.alaraja_y):
                        pass
                    else:
                        self.KirjastonPäivitys(x, y, kirjasto)
                        self.PaksuudenMuodostus(x, y, säde)
                else:
                    self.KirjastonPäivitys(x, y, kirjasto)
                    self.PaksuudenMuodostus(x, y, säde)

        else: # y --> x(y), käänteisfunktio
            for y in range(int(self.alaraja_y), int(self.yläraja_y) + 1, 1):
                try:
                    x = eval(ratkaisu)
                except:
                    continue

                säde = int(self.paksuus / 2)

                if self.yläraja_x != "-" and self.alaraja_x != "-":
                    if x > int(self.yläraja_x) or x < int(self.alaraja_x):
                        pass
                    else:
                        self.KirjastonPäivitys(x, y, kirjasto)
                        self.PaksuudenMuodostus(x, y, säde)
                else:
                    self.KirjastonPäivitys(x, y, kirjasto)
                    self.PaksuudenMuodostus(x, y, säde)

    def PaksuudenMuodostus(self, x, y, säde):
        for _x in range(10*int(x-säde), 10*int(x+säde)+1, 1):
            try:
                _x = _x / 10
                _y1 = y + sqrt(säde**2 - (_x - x) * (_x - x))
                _y2 = y - sqrt(säde**2 - (_x - x) * (_x - x))

                self.KirjastonPäivitys(_x, _y1, 2)
                self.KirjastonPäivitys(_x, _y2, -2)
            except:
                None

    def KirjastonPäivitys(self, x, y, kirjasto): #Tai listan päivitys
        if kirjasto == 1:
            self.kirjasto_plus.update({x : y})
        if kirjasto == -1:
            self.kirjasto_miinus.update({x : y})
        if kirjasto == 2:
            self.paksuus_plus_x.append(x)
            self.paksuus_plus_y.append(y)
        if kirjasto == -2:
            self.paksuus_miinus_x.append(x)
            self.paksuus_miinus_y.append(y)

    def Suora(self):
        self.ikkuna3 = Tk()
        #self.ikkuna3.geometry('479x562')
        self.ikkuna3.resizable(False, False)
        self.ikkuna3.title("Suora")
        self.ikkuna3.configure(bg="#B7AAA7")

        self.kehys2 = Frame(self.ikkuna3, bg="#BC9186", width=24, borderwidth=10)

        self.klikkaa_pisteitä3 = Button(self.ikkuna3, text="Lisää pisteitä", command=lambda: self.Suora2(1), font=self.fontti, width=24, borderwidth=3, bg="gray")
        self.valmiit_klikkaukset3 = Button(self.ikkuna3, text="Lopeta lisäys", command=lambda: self.Suora2(2), font=self.fontti, width=24, borderwidth=3, bg="gray")
        self.suora_valmis = Button(self.ikkuna3, text="Valmis", command=lambda: self.Suora2(3), font=self.fontti, width=24, borderwidth=3, bg="gray", foreground="blue")
        self.suora_poista = Button(self.ikkuna3, text="Poista", command=lambda: self.Suora2(4), font=self.fontti, width=24, borderwidth=3, bg="gray", foreground="red")

        self.teksti_piste1 = Label(self.ikkuna3, text="Piste 1 (x y)", font=self.fontti, width=13, borderwidth=3, bg="#B7AAA7")
        self.teksti_piste2 = Label(self.ikkuna3, text="Piste 2 (x y)", font=self.fontti, width=13, borderwidth=3, bg="#B7AAA7")
        self.teksti_paksuus = Label(self.ikkuna3, text="   Paksuus r", font=self.fontti, width=13, borderwidth=3, bg="#B7AAA7")
        self.teksti_yhdensuuntainen = Label(self.kehys2, text="Yhdensuuntainen", font=self.fontti, width=22, borderwidth=3, bg="#BC9186")
        self.teksti_yhdensuuntainen_etäisyys = Label(self.kehys2, text="Etäisyys ja +/-", font=self.fontti, width=22, borderwidth=3, bg="#BC9186")
        self.teksti_kohtisuorassa = Label(self.kehys2, text="Kohtisuorassa", font=self.fontti, width=22, borderwidth=3, bg="#BC9186")

        self.piste1 = Entry(self.ikkuna3, font=self.fontti2, width=10, borderwidth=3)
        self.piste2 = Entry(self.ikkuna3, font=self.fontti2, width=10, borderwidth=3)
        self.suora_paksuus = Entry(self.ikkuna3, font=self.fontti2, width=10, borderwidth=3)
        self.yhdensuuntainen = Entry(self.kehys2, font=self.fontti2, width=22, borderwidth=3)
        self.yhdensuuntainen_etäisyys = Entry(self.kehys2, font=self.fontti2, width=22, borderwidth=3)
        self.kohtisuorassa = Entry(self.kehys2, font=self.fontti2, width=22, borderwidth=3)

        self.suora_valmis.grid(row=0, column=0, columnspan=2, pady=5, padx=5, sticky="N")
        self.klikkaa_pisteitä3.grid(row=1, column=0, columnspan=2, padx=5, sticky="N")
        self.suora_poista.grid(row=2, column=0, columnspan=2, pady=5, padx=5, sticky="N")
        self.teksti_piste1.grid(row=3, column=0, sticky="N")
        self.piste1.grid(row=3, column=1, sticky="N")
        self.teksti_piste2.grid(row=4, column=0, sticky="N")
        self.piste2.grid(row=4, column=1, sticky="N")
        self.teksti_paksuus.grid(row=5, column=0, sticky="N")
        self.suora_paksuus.grid(row=5, column=1, sticky="N")

        self.kehys2.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="NWE")
        self.teksti_yhdensuuntainen.grid(row=0, column=0, padx=5, sticky="N")
        self.yhdensuuntainen.grid(row=1, column=0, padx=5, pady=5, sticky="N")
        self.teksti_yhdensuuntainen_etäisyys.grid(row=2, column=0, padx=5, sticky="N")
        self.yhdensuuntainen_etäisyys.grid(row=3, column=0, padx=5, pady=5, sticky="N")
        self.teksti_kohtisuorassa.grid(row=4, column=0, padx=5, sticky="N")
        self.kohtisuorassa.grid(row=5, column=0, padx=5, sticky="N")

    def Suora2(self, tila):
        if tila == 1: # lisää pisteitä
            try:
                self.klikkaa_pisteitä3.grid_forget()
                self.valmiit_klikkaukset3.grid(row=1, column=0, columnspan=2, padx=5, sticky="N")
            except:
                None

            self.kilppari1 = turtle.Turtle()
            self.kilppari2 = turtle.Turtle()

            self.kilppari1.hideturtle()
            self.kilppari2.hideturtle()

            self.kilpparit.append(self.kilppari1)
            self.kilpparit.append(self.kilppari2)

            def klikkaus1(x, y):
                self.kilppari1.showturtle()
                self.kilppari1.penup()
                self.kilppari1.goto(x , y)
                self.kilppari1.shape("triangle")
                self.kilppari1.color("lightgreen")
                self.kilppari1.pendown()
                self.piste1_arvo = f"{int(round(int(x)/self.skaalaus, 0))} {int(round(int(y)/self.skaalaus, 0))}"
                self.karttaikkuna.update()

            def klikkaus2(x, y):
                self.kilppari2.showturtle()
                self.kilppari2.penup()
                self.kilppari2.goto(x , y)
                self.kilppari2.shape("triangle")
                self.kilppari2.color("blue")
                self.kilppari2.pendown()
                self.piste2_arvo = f"{int(round(int(x)/self.skaalaus, 0))} {int(round(int(y)/self.skaalaus, 0))}"
                self.karttaikkuna.update()

            self.karttaikkuna.onclick(klikkaus1, 1)
            self.karttaikkuna.onclick(klikkaus2, 3)

        if tila == 2: # lopeta lisäys
            self.onko_klikattu = True

            self.karttaikkuna.onclick(None, 1)
            self.karttaikkuna.onclick(None, 3)

            self.piste1.insert(0, self.piste1_arvo)

            self.x_1 = int(self.piste1_arvo.split()[0])
            self.y_1 = int(self.piste1_arvo.split()[1])

            self.x_2 = int(self.piste2_arvo.split()[0])

            if self.yhdensuuntainen.get() != "":
                yhdensuuntainen_suora = int(self.yhdensuuntainen.get())
                tekstilista = self.tekstikenttä.get(f"{yhdensuuntainen_suora}.0", f"{yhdensuuntainen_suora}.end")

                self.y_2 = int(self.piste2_arvo.split()[1])

                yhtälö = tekstilista.split()[0]
                suoran_yhtälö_kk = yhtälö.split("*")[0]

                k = float(eval(suoran_yhtälö_kk))

                self.x_2 = int(round((k**2 * self.x_1 - k * self.y_1 + k * self.y_2 + self.x_2) / (k**2 + 1), 0))
                self.y_2 = int(round(k * (self.x_2 - self.x_1) + self.y_1, 0))

                self.piste2.insert(0, f"{self.x_2} {self.y_2}")

            elif self.kohtisuorassa.get() != "":
                kohtisuora_suora = int(self.kohtisuorassa.get())
                tekstilista = self.tekstikenttä.get(f"{int(kohtisuora_suora)}.0", f"{int(kohtisuora_suora)}.end")

                self.y_2 = int(self.piste2_arvo.split()[1])

                yhtälö = tekstilista.split()[0]
                suoran_yhtälö_kk = yhtälö.split("*")[0]

                k = float(eval(suoran_yhtälö_kk))

                self.x_2 = int(round((k**2 * self.x_2 + k * self.y_1 - k * self.y_2 + self.x_1) / (k**2 + 1), 0))
                self.y_2 = int(round(-1 / k * (self.x_2 - self.x_1) + self.y_1, 0))

                self.piste2.insert(0, f"{self.x_2} {self.y_2}")

            else:
                self.piste2.insert(0, self.piste2_arvo)
                self.y_2 = int(self.piste2_arvo.split()[1])

            alaraja_x = min(self.x_1, self.x_2)
            yläraja_x = max(self.x_1, self.x_2)

            alaraja_y = min(self.y_1, self.y_2)
            yläraja_y = max(self.y_1, self.y_2)

            käyrä_plus = f"({self.y_1}-{self.y_2})/({self.x_1}-{self.x_2})*x+({self.x_1}*{self.y_2}-{self.x_2}*{self.y_1})/({self.x_1}-{self.x_2})"

            suoran_pistelista = self.KartanPistelistanMuodostus(käyrä_plus, alaraja_x, yläraja_x, alaraja_y, yläraja_y)
            self.KartanPiirtäjä(pistelista=suoran_pistelista)

            self.karttaikkuna.update()

            self.valmiit_klikkaukset3.grid_forget()
            self.klikkaa_pisteitä3.grid(row=1, column=0, columnspan=2, padx=5, sticky="N")

        if tila == 3: # valmis
            for n in self.kilpparit:
                n.hideturtle()

            for i in range(len(self.kilpparit)-1):
                del self.kilpparit[i]

            self.karttaikkuna.update()

            if self.yhdensuuntainen_etäisyys.get() != "":
                if self.piste1.get() != "" or self.piste2.get() != "":
                    raise ValueError("Poista kaikki pisteissä olevat arvot!")
                elif self.yhdensuuntainen.get() == "":
                    raise ValueError("Minkä suoran kanssa yhdensuuntainen?")
                else:
                    yhdensuuntainen_suora = int(self.yhdensuuntainen.get())
                    käyttäjän_syöte = self.yhdensuuntainen_etäisyys.get()

                    try:
                        suorien_välinen_etäisyys = int(käyttäjän_syöte.split()[0])
                        ylä_vai_alapuolella = käyttäjän_syöte.split()[1]
                    except:
                        raise ValueError("Kerro, onko yhdensuuntainen suora olemassaolevan suoran ylä- vai alapuolella (+/-). Tai korvaa arvot.")

                    if ylä_vai_alapuolella != "+":
                        if ylä_vai_alapuolella != "-":
                            raise ValueError("Kerro, onko yhdensuuntainen suora olemassaolevan suoran ylä- vai alapuolella, käyttämällä merkintöjä (+/-).")

                    tekstilista = self.tekstikenttä.get(f"{int(yhdensuuntainen_suora)}.0", f"{int(yhdensuuntainen_suora)}.end")

                    yhtälö = tekstilista.split()[0]
                    suoran_yhtälö_kk = float(eval(yhtälö.split("*")[0]))

                    x_min = int(tekstilista.split()[4])
                    x_max = int(tekstilista.split()[5])

                    y_min = eval(yhtälö.replace("x", f"{x_min}"))
                    y_max = eval(yhtälö.replace("x", f"{x_max}"))

                    normaali_min_kk = -1 / suoran_yhtälö_kk
                    normaali_min_suuntakulma = atan(normaali_min_kk)

                    delta_x = suorien_välinen_etäisyys * cos(normaali_min_suuntakulma)
                    delta_y = suorien_välinen_etäisyys * sin(abs(normaali_min_suuntakulma))

                    if normaali_min_kk < 0:
                        if ylä_vai_alapuolella == "+":
                            uusi_x_min = x_min - delta_x
                            uusi_x_max = x_max - delta_x
                            uusi_y_min = y_min + delta_y
                            uusi_y_max = y_max + delta_y
                        elif ylä_vai_alapuolella == "-":
                            uusi_x_min = x_min + delta_x
                            uusi_x_max = x_max + delta_x
                            uusi_y_min = y_min - delta_y
                            uusi_y_max = y_max - delta_y

                    elif normaali_min_kk > 0:
                        if ylä_vai_alapuolella == "+":
                            uusi_x_min = x_min + delta_x
                            uusi_x_max = x_max + delta_x
                            uusi_y_min = y_min + delta_y
                            uusi_y_max = y_max + delta_y
                        elif ylä_vai_alapuolella == "-":
                            uusi_x_min = x_min - delta_x
                            uusi_x_max = x_max - delta_x
                            uusi_y_min = y_min - delta_y
                            uusi_y_max = y_max - delta_y

                    uusi_x_min = int(round(uusi_x_min, 0))
                    uusi_x_max = int(round(uusi_x_max, 0))
                    uusi_y_min = int(round(uusi_y_min, 0))
                    uusi_y_max = int(round(uusi_y_max, 0))

                    self.piste1.insert(0, f"{uusi_x_min} {uusi_y_min}")
                    self.piste2.insert(0, f"{uusi_x_max} {uusi_y_max}")

            self.x_1 = int(self.piste1.get().split()[0])
            self.y_1 = int(self.piste1.get().split()[1])

            self.x_2 = int(self.piste2.get().split()[0])
            self.y_2 = int(self.piste2.get().split()[1])


            if self.onko_klikattu:
                self.onko_klikattu = False

            yhtälö = f"({self.y_1}-{self.y_2})/({self.x_1}-{self.x_2})*x+({self.x_1}*{self.y_2}-{self.x_2}*{self.y_1})/({self.x_1}-{self.x_2}) - ({self.x_1}-{self.x_2})/({self.y_1}-{self.y_2})*y-({self.x_1}*{self.y_2}-{self.x_2}*{self.y_1})/({self.y_1}-{self.y_2}) -"
            paksuus = self.suora_paksuus.get()

            if self.x_2 >= self.x_1:
                if self.y_2 >= self.y_1:
                    self.tekstikenttä.insert(END, f"{yhtälö} {self.x_1} {self.x_2} {self.y_1} {self.y_2} {paksuus}\n")
                else:
                    self.tekstikenttä.insert(END, f"{yhtälö} {self.x_1} {self.x_2} {self.y_2} {self.y_1} {paksuus}\n")
            else:
                if self.y_2 >= self.y_1:
                    self.tekstikenttä.insert(END, f"{yhtälö} {self.x_2} {self.x_1} {self.y_1} {self.y_2} {paksuus}\n")
                else:
                    self.tekstikenttä.insert(END, f"{yhtälö} {self.x_2} {self.x_1} {self.y_2} {self.y_1} {paksuus}\n")

            self.Varmuuskopioi()

        if tila == 4: # poista
            self.piste1.delete(0, END)
            self.piste2.delete(0, END)
            self.suora_paksuus.delete(0, END)

    def Kaari(self):
        self.ikkuna2 = Tk()
        """
        if platform == "linux" or platform == "linux2":
            self.ikkuna2.geometry('386x417')
        elif platform == "win32":
            self.ikkuna2.geometry('365x430')
        """
        self.ikkuna2.resizable(False, False)
        self.ikkuna2.title("Kaari")
        self.ikkuna2.configure(bg="#B7AAA7")

        self.kehys4 = Frame(self.ikkuna2, bg="#BC9186", width=24, borderwidth=10)

        self.teksti_x_0 = Label(self.ikkuna2, text="K.pisteen x", font=self.fontti, width=12, borderwidth=3, bg="#B7AAA7")
        self.teksti_y_0 = Label(self.ikkuna2, text="K.pisteen y", font=self.fontti, width=12, borderwidth=3, bg="#B7AAA7")
        self.teksti_säde = Label(self.ikkuna2, text="Säde\u00B2", font=self.fontti, width=10, borderwidth=3, bg="#B7AAA7")
        self.teksti_x_min = Label(self.ikkuna2, text="x-min", font=self.fontti, width=10, borderwidth=3, bg="#B7AAA7")
        self.teksti_x_maks = Label(self.ikkuna2, text="x-maks", font=self.fontti, width=10, borderwidth=3, bg="#B7AAA7")
        self.teksti_y_min = Label(self.ikkuna2, text="y-min", font=self.fontti, width=10, borderwidth=3, bg="#B7AAA7")
        self.teksti_y_maks = Label(self.ikkuna2, text="y-maks", font=self.fontti, width=10, borderwidth=3, bg="#B7AAA7")
        self.teksti_ympyrä_paksuus = Label(self.ikkuna2, text=" Paksuus r", font=self.fontti, width=10, borderwidth=3, bg="#B7AAA7")
        self.teksti_suora_1 = Label(self.kehys4, text="Suora 1 (i)", font=self.fontti, width=13, borderwidth=3, bg="#BC9186")
        self.teksti_suora_2 = Label(self.kehys4, text="Suora 2 (i)", font=self.fontti, width=13, borderwidth=3, bg="#BC9186")
        self.teksti_piste = Label(self.kehys4, text="Piste (x y)", font=self.fontti, width=13, borderwidth=3, bg="#BC9186")
        self.teksti_ehto_x = Label(self.kehys4, text="Ehto (x-alue)", font=self.fontti, width=13, borderwidth=3, bg="#BC9186")
        self.teksti_ehto_y = Label(self.kehys4, text="Ehto (y-alue)", font=self.fontti, width=13, borderwidth=3, bg="#BC9186")

        self.x_0 = Entry(self.ikkuna2, font=self.fontti2, width=5, borderwidth=3)
        self.y_0 = Entry(self.ikkuna2, font=self.fontti2, width=5, borderwidth=3)
        self.säde = Entry(self.ikkuna2, font=self.fontti2, width=5, borderwidth=3)
        self.x_min = Entry(self.ikkuna2, font=self.fontti2, width=5, borderwidth=3)
        self.x_maks = Entry(self.ikkuna2, font=self.fontti2, width=5, borderwidth=3)
        self.y_min = Entry(self.ikkuna2, font=self.fontti2, width=5, borderwidth=3)
        self.y_maks = Entry(self.ikkuna2, font=self.fontti2, width=5, borderwidth=3)
        self.ympyrä_paksuus = Entry(self.ikkuna2, font=self.fontti2, width=5, borderwidth=3)
        self.suora_1 = Entry(self.kehys4, font=self.fontti2, width=5, borderwidth=3)
        self.suora_2 = Entry(self.kehys4, font=self.fontti2, width=5, borderwidth=3)
        self.piste = Entry(self.kehys4, font=self.fontti2, width=5, borderwidth=3)
        self.ehto_x = Entry(self.kehys4, font=self.fontti2, width=5, borderwidth=3)
        self.ehto_y = Entry(self.kehys4, font=self.fontti2, width=5, borderwidth=3)

        self.valmis = Button(self.ikkuna2, text="Valmis", command=self.Kaari2, font=self.fontti, width=19, borderwidth=3, bg="gray", foreground="blue")
        self.maalaa_alue = Button(self.kehys4, text="Maalaa alue", command=lambda: self.Kaari3(1), font=self.fontti, width=19, borderwidth=3, bg="gray", foreground="green")
        self.maalaa_rajat = Button(self.kehys4, text="Maalaa rajat", command=lambda: self.Kaari3(2), font=self.fontti, width=19, borderwidth=3, bg="gray", foreground="orange")

        self.valmis.grid(row=0, column=0, columnspan=2, pady=5, padx=5, sticky="N")
        self.teksti_x_0.grid(row=1, column=0, sticky="N")
        self.x_0.grid(row=1, column=1, sticky="N")
        self.teksti_y_0.grid(row=2, column=0, sticky="N")
        self.y_0.grid(row=2, column=1, sticky="N")
        self.teksti_säde.grid(row=3, column=0, sticky="N")
        self.säde.grid(row=3, column=1, sticky="N")
        self.teksti_x_min.grid(row=4, column=0, sticky="N")
        self.x_min.grid(row=4, column=1, sticky="N")
        self.teksti_x_maks.grid(row=5, column=0, sticky="N")
        self.x_maks.grid(row=5, column=1, sticky="N")
        self.teksti_y_min.grid(row=6, column=0, sticky="N")
        self.y_min.grid(row=6, column=1, sticky="N")
        self.teksti_y_maks.grid(row=7, column=0, sticky="N")
        self.y_maks.grid(row=7, column=1, sticky="N")
        self.teksti_ympyrä_paksuus.grid(row=8, column=0, sticky="N")
        self.ympyrä_paksuus.grid(row=8, column=1, sticky="N")

        self.kehys4.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky="N")
        self.teksti_suora_1.grid(row=0, column=0, sticky="NW")
        self.suora_1.grid(row=0, column=1, sticky="NE")
        self.teksti_suora_2.grid(row=1, column=0, sticky="NW")
        self.suora_2.grid(row=1, column=1, sticky="NE")
        self.teksti_piste.grid(row=2, column=0, sticky="NW")
        self.piste.grid(row=2, column=1, sticky="NE")
        self.teksti_ehto_x.grid(row=3, column=0, sticky="NW")
        self.ehto_x.grid(row=3, column=1, sticky="NE")
        self.teksti_ehto_y.grid(row=4, column=0, sticky="NW")
        self.ehto_y.grid(row=4, column=1, sticky="NE")
        self.maalaa_alue.grid(row=5, column=0, columnspan=2, pady=5, sticky="N")
        self.maalaa_rajat.grid(row=6, column=0, columnspan=2, sticky="N")

        self.ikkuna2.mainloop()

    def Kaari2(self):
        try: self.maalauksen_piirtäjä.clear()
        except: None

        if self.suora_1.get() != "":
            suora1 = int(self.suora_1.get())
            suora2 = int(self.suora_2.get())
            piste = self.piste.get()
            ehto_x = self.ehto_x.get()
            ehto_y = self.ehto_y.get()

            rivi_suora1 = self.tekstikenttä.get(f"{suora1}.0", f"{suora1}.end")
            rivi_suora2 = self.tekstikenttä.get(f"{suora2}.0", f"{suora2}.end")

            yhtälö_suora1 = rivi_suora1.split()[0]
            yhtälö_suora2 = rivi_suora2.split()[0]

            k_1 = eval(yhtälö_suora1.split("*x+")[0])
            b_1 = eval(yhtälö_suora1.split("*x+")[1])

            k_2 = eval(yhtälö_suora2.split("*x+")[0])
            b_2 = eval(yhtälö_suora2.split("*x+")[1])

            x_min_1 = int(rivi_suora1.split()[4])
            x_max_1 = int(rivi_suora1.split()[5])

            x_min_2 = int(rivi_suora2.split()[4])
            x_max_2 = int(rivi_suora2.split()[5])

            y_min_1 = int(rivi_suora1.split()[6])
            y_max_1 = int(rivi_suora1.split()[7])

            y_min_2 = int(rivi_suora2.split()[6])
            y_max_2 = int(rivi_suora2.split()[7])

            x_1 = int(piste.split()[0])
            y_1 = int(piste.split()[1])

            if k_1*x_1+b_1 == y_1:
                x_0 = x_1 - (k_1 * (k_2 * x_1 + b_2 - y_1)) / (sqrt((1 + (k_2)**2) * (1 + (k_1)**2)) + (1 + k_2 * k_1))
                y_0 = y_1 + (k_2 * x_1 + b_2 - y_1) / (sqrt((1 + (k_2)**2) * (1 + (k_1)**2)) + (1 + k_2 * k_1))
                if not eval(ehto_x.replace("x", f"{x_0}")) or not eval(ehto_y.replace("y", f"{y_0}")):
                    x_0 = x_1 + (k_1 * (k_2 * x_1 + b_2 - y_1)) / (sqrt((1 + (k_2)**2) * (1 + (k_1)**2)) - (1 + k_2 * k_1))
                    y_0 = y_1 - (k_2 * x_1 + b_2 - y_1) / (sqrt((1 + (k_2)**2) * (1 + (k_1)**2)) - (1 + k_2 * k_1))
            else:
                x_0 = x_1 - (k_2 * (k_1 * x_1 + b_1 - y_1)) / (sqrt((1 + (k_1)**2) * (1 + (k_2)**2)) + (1 + k_1 * k_2))
                y_0 = y_1 + (k_1 * x_1 + b_1 - y_1) / (sqrt((1 + (k_1)**2) * (1 + (k_2)**2)) + (1 + k_1 * k_2))
                if not eval(ehto_x.replace("x", f"{x_0}")) or not eval(ehto_y.replace("y", f"{y_0}")):
                    x_0 = x_1 + (k_2 * (k_1 * x_1 + b_1 - y_1)) / (sqrt((1 + (k_1)**2) * (1 + (k_2)**2)) - (1 + k_1 * k_2))
                    y_0 = y_1 - (k_1 * x_1 + b_1 - y_1) / (sqrt((1 + (k_1)**2) * (1 + (k_2)**2)) - (1 + k_1 * k_2))

            x_0 = int(round(x_0, 0))
            y_0 = int(round(y_0, 0))

            säde = round((x_0 - x_1)**2 + (y_0 - y_1)**2, 6)

            eka_piste_x_1, eka_piste_y_1, toka_piste_x_1, toka_piste_y_1 = YlimääräisetFunktiot.SuoranPäätepisteidenMääritys(self, k_1, x_min_1, y_min_1, x_max_1, y_max_1)
            eka_piste_x_2, eka_piste_y_2, toka_piste_x_2, toka_piste_y_2 = YlimääräisetFunktiot.SuoranPäätepisteidenMääritys(self, k_2, x_min_2, y_min_2, x_max_2, y_max_2)

            #if self.x_min.get() == "" or self.y_min.get() == "":
            if k_2*x_1+b_2 == y_1:
                uusi_sijoitettava, x_2 = YlimääräisetFunktiot.UusiSijoitettava(self, x_0, y_0, k_1, b_1, eka_piste_x_1, eka_piste_y_1,
                                                                               toka_piste_x_1, toka_piste_y_1, rivi_suora1)

                self.tekstikenttä.delete(f"{suora1}.0", f"{suora1}.end")
                self.tekstikenttä.insert(f"{suora1}.0", uusi_sijoitettava)
            else:
                uusi_sijoitettava, x_2 = YlimääräisetFunktiot.UusiSijoitettava(self, x_0, y_0, k_2, b_2, eka_piste_x_2, eka_piste_y_2,
                                                                               toka_piste_x_2, toka_piste_y_2, rivi_suora2)

                self.tekstikenttä.delete(f"{suora2}.0", f"{suora2}.end")
                self.tekstikenttä.insert(f"{suora2}.0", uusi_sijoitettava)

                #x_min = min(x_1, x_2)
                #x_maks = max(x_1, x_2)

            #else:
            x_min = int(self.x_min.get())
            x_maks = int(self.x_maks.get())

        elif self.x_0.get() != "":
            x_0 = self.x_0.get()
            y_0 = self.y_0.get()
            säde = self.säde.get()
            x_min = int(self.x_min.get())
            x_maks = int(self.x_maks.get())

        try:
            y_min = int(self.y_min.get())
            y_maks = int(self.y_maks.get())
            paksuus = self.ympyrä_paksuus.get()
        except:
            raise ValueError("Tarkista syötetyt arvot!")

        käyrä_plus = f"{y_0}+sqrt({säde}-(x-{x_0})*(x-{x_0}))"
        käyrä_miinus = f"{y_0}-sqrt({säde}-(x-{x_0})*(x-{x_0}))"
        käänteis_plus = f"{x_0}+sqrt({säde}-(y-{y_0})*(y-{y_0}))"
        käänteis_miinus = f"{x_0}-sqrt({säde}-(y-{y_0})*(y-{y_0}))"

        yhtälö = f"{käyrä_plus} {käyrä_miinus} {käänteis_plus} {käänteis_miinus}"

        self.tekstikenttä.insert(END, f"{yhtälö} {x_min} {x_maks} {y_min} {y_maks} {paksuus}\n")

        self.Varmuuskopioi()

        kaaren_pistelista = []

        kaaren_pistelista = self.KartanPistelistanMuodostus(käyrä_plus, x_min, x_maks, y_min, y_maks)
        self.KartanPiirtäjä(pistelista=kaaren_pistelista)

        kaaren_pistelista = self.KartanPistelistanMuodostus(käyrä_miinus, x_min, x_maks, y_min, y_maks)
        self.KartanPiirtäjä(pistelista=kaaren_pistelista)

    def Kaari3(self, tila):
        try: self.maalauksen_piirtäjä.clear()
        except: None

        self.maalauksen_piirtäjä = turtle.Turtle()
        self.maalauksen_piirtäjä.color("red")
        self.maalauksen_piirtäjä.width(2)
        self.maalauksen_piirtäjä.hideturtle()
        self.maalauksen_piirtäjä.penup()

        def TurtleKoordinaatteihin(x, y):
            korkeus = self.karttaikkuna.window_height()
            leveys = self.karttaikkuna.window_width()
            return x - (leveys / 2), (korkeus / 2) - y

        def Painaminen(x, y):
            global aloitus_x, aloitus_y
            aloitus_x, aloitus_y = x, y
            #aloitus_x, aloitus_y = TurtleKoordinaatteihin(x, y)
            self.maalauksen_piirtäjä.goto(x, y)

        def Siirtäminen(event):
            global x, y
            x, y = TurtleKoordinaatteihin(event.x, event.y)
            self.maalauksen_piirtäjä.clear()
            self.maalauksen_piirtäjä.goto(x, y)
            self.maalauksen_piirtäjä.pendown()
            self.maalauksen_piirtäjä.goto(aloitus_x, y)
            self.maalauksen_piirtäjä.goto(aloitus_x, aloitus_y)
            self.maalauksen_piirtäjä.goto(x, aloitus_y)
            self.maalauksen_piirtäjä.goto(x, y)
            self.karttaikkuna.update()

        def Vapauttaminen(event):
            self.maalauksen_piirtäjä.penup()

            maalaus_yx = int(round(max(x, aloitus_x) / self.skaalaus, 0))
            maalaus_ax = int(round(min(x, aloitus_x) / self.skaalaus, 0))

            maalaus_yy = int(round(max(y, aloitus_y) / self.skaalaus, 0))
            maalaus_ay = int(round(min(y, aloitus_y) / self.skaalaus, 0))

            if tila == 2:
                self.ehto_x.delete(0, END)
                self.ehto_x.insert(0, f"{maalaus_ax}<x<{maalaus_yx}")

                self.ehto_y.delete(0, END)
                self.ehto_y.insert(0, f"{maalaus_ay}<y<{maalaus_yy}")
            else:
                self.x_min.delete(0, END)
                self.x_min.insert(0, maalaus_ax)

                self.x_maks.delete(0, END)
                self.x_maks.insert(0, maalaus_yx)

                self.y_min.delete(0, END)
                self.y_min.insert(0, maalaus_ay)

                self.y_maks.delete(0, END)
                self.y_maks.insert(0, maalaus_yy)

        self.karttaikkuna.onscreenclick(Painaminen)

        kanvas = self.karttaikkuna.getcanvas()
        kanvas.bind("<B1-Motion>", Siirtäminen)
        kanvas.bind("<ButtonRelease-1>", Vapauttaminen)

    def Interpolaatiopolynomi(self):
        self.ikkuna5 = Tk()
        self.ikkuna5.title("Interpolaatiopolynomi")
        self.ikkuna5.configure(bg="#B7AAA7")
        self.ikkuna5.resizable(False, False)

        self.klikkaa_pisteitä5 = Button(self.ikkuna5, text="Lisää pisteitä", command=lambda: self.Interpolaatiopolynomi2(1), font=self.fontti, width=24, borderwidth=3, bg="gray")
        self.valmiit_klikkaukset5 = Button(self.ikkuna5, text="Lopeta lisäys", command=lambda: self.Interpolaatiopolynomi2(2), font=self.fontti, width=24, borderwidth=3, bg="gray")
        self.valmis5 = Button(self.ikkuna5, text="Valmis", command=lambda: self.Interpolaatiopolynomi2(3), font=self.fontti, width=24, borderwidth=3, bg="gray", foreground="blue")
        self.uusi_yritys5 = Button(self.ikkuna5, text="Uusi yritys", command=lambda: self.Interpolaatiopolynomi2(4), font=self.fontti, width=24, borderwidth=3, bg="gray", foreground="red")
        self.vaihda_merkkiä_nappi5 = Button(self.ikkuna5, text="Korjaa", command=lambda: self.Interpolaatiopolynomi2(5), font=self.fontti, width=24, borderwidth=3, bg="gray")

        self.vaihda_merkkiä_ohje5 = Label(self.ikkuna5, text="     Indeksi", font=self.fontti, width=12, borderwidth=3, bg="#B7AAA7")
        self.vaihda_merkkiä_teksti5 = Entry(self.ikkuna5, font=self.fontti2, borderwidth=3)

        self.paksuus_teksti5 = Label(self.ikkuna5, text="  Paksuus (d)", font=self.fontti, width=12, borderwidth=3, bg="#B7AAA7")
        self.paksuus5 = Entry(self.ikkuna5, font=self.fontti2, width=11, borderwidth=3)

        if platform == "linux" or platform == "linux2":
            self.vaihda_merkkiä_teksti5.configure(width=12)
        elif platform == "win32":
            self.vaihda_merkkiä_teksti5.configure(width=11)

        self.valmis5.grid(row=0, column=0, columnspan=2, pady=5, padx=5, sticky="N")
        self.klikkaa_pisteitä5.grid(row=1, column=0, columnspan=2, padx=5, sticky="N")
        self.uusi_yritys5.grid(row=2, column=0, columnspan=2, pady=5, padx=5, sticky="N")
        self.vaihda_merkkiä_ohje5.grid(row=3, column=0, padx=5, sticky="SE")
        self.vaihda_merkkiä_teksti5.grid(row=3, column=1, padx=5, sticky="N")
        self.vaihda_merkkiä_nappi5.grid(row=4, column=0, columnspan=2, pady=5, padx=5, sticky="N")
        self.paksuus_teksti5.grid(row=5, column=0, pady=5, padx=5, sticky="N")
        self.paksuus5.grid(row=5, column=1, columnspan=2, pady=5, padx=5, sticky="N")

        self.ikkuna5.mainloop()

    def Interpolaatiopolynomi2(self, tila):
        if tila == 1: # "Klikkaa pisteitä"
            self.klikkaa_pisteitä5.grid_forget()
            self.valmiit_klikkaukset5.grid(row=1, column=0, columnspan=2, padx=5, sticky="N")

            self.pisteet5 = []

            def klikkaus(x, y):
                self.klikkaus_nro += 1
                kilppari = turtle.Turtle()
                kilppari.penup()
                kilppari.goto(x, y)
                kilppari.shape("triangle")
                kilppari.color("lightgreen")
                kilppari.write(self.klikkaus_nro, font=self.fontti3)
                kilppari.pendown()
                self.kilpparit5.append(kilppari)
                piste_arvo = f"{int(round(int(x) / self.skaalaus, 0))} {int(round(int(y) / self.skaalaus, 0))}"

                self.pisteet5.append(piste_arvo)

                self.karttaikkuna.update()

            self.karttaikkuna.onclick(klikkaus, 1)

        if tila == 2: # "Valmiit klikkaukset"
            self.karttaikkuna.onclick(None, 1)

            self.valmiit_klikkaukset5.grid_forget()
            self.klikkaa_pisteitä5.grid(row=1, column=0, columnspan=2, padx=5, sticky="N")

            self.klikkaus_nro = 0

            self.x_lista = []
            self.y_lista = []

            for piste in self.pisteet5:
                self.x_lista.append(float(piste.split()[0]))
                self.y_lista.append(float(piste.split()[1]))

            self.derivaatat = []

            for indeksi in range(len(self.x_lista)):
                try:
                    if indeksi == 0:
                        derivaatta = (self.y_lista[indeksi] - self.y_lista[indeksi + 1]) / (self.x_lista[indeksi] - self.x_lista[indeksi + 1])
                    elif indeksi == len(self.x_lista)-1:
                        derivaatta = (self.y_lista[indeksi - 1] - self.y_lista[indeksi]) / (self.x_lista[indeksi - 1] - self.x_lista[indeksi])
                    else:
                        derivaatta = (self.y_lista[indeksi - 1] - self.y_lista[indeksi + 1]) / (self.x_lista[indeksi - 1] - self.x_lista[indeksi + 1])
                except ZeroDivisionError:
                    derivaatta = 10**6

                self.derivaatat.append(derivaatta)

            x_min = min(self.x_lista)
            x_max = max(self.x_lista)

            self.hermite_polynomit = []

            for i in range(len(self.x_lista) - 1):
                rikki = False

                x_1 = self.x_lista[i]
                x_2 = self.x_lista[i + 1]

                if x_1 == x_2:
                    x_1 += 1

                y_1 = self.y_lista[i]
                y_2 = self.y_lista[i + 1]

                if y_1 == y_2:
                    y_1 += 1

                d_1 = self.derivaatat[i]
                d_2 = self.derivaatat[i + 1]

                if abs(d_1) <= 1 or abs(d_2) <= 1:
                    tyyppi = 1
                    raja_1, raja_2, raja_arvo_1, raja_arvo_2, raja_derivaatta_1, raja_derivaatta_2 = self.Interpolaatiopolynomi6(x_1, x_2, y_1, y_2, d_1, d_2)

                else:
                    tyyppi = -1

                    try:
                        d_1 = 1 / d_1
                    except ZeroDivisionError:
                        d_1 = 10 ** 6
                    try:
                        d_2 = 1 / d_2
                    except ZeroDivisionError:
                        d_2 = 10 ** 6

                    raja_1, raja_2, raja_arvo_1, raja_arvo_2, raja_derivaatta_1, raja_derivaatta_2 = self.Interpolaatiopolynomi6(y_1, y_2, x_1, x_2, d_1, d_2)

                a, b, c, d = self.Interpolaatiopolynomi3(raja_1, raja_2, raja_arvo_1, raja_arvo_2, raja_derivaatta_1, raja_derivaatta_2)

                toinen_derivaatta = f"6*({a})*M+({b})"

                for muuttuja in range(int(raja_1), int(raja_2)):
                    toisen_derivaatan_arvo = eval(toinen_derivaatta.replace("M", str(muuttuja)))
                    if abs(toisen_derivaatan_arvo) > 4:
                        rikki = True
                        break

                if rikki:
                    polynomi = self.Interpolaatiopolynomi5(tyyppi, i)[0]
                else:
                    if tyyppi == 1:
                        polynomi = f"({a})*x**3+({b})*x**2+({c})*x+({d})"
                    else:
                        polynomi = f"({a})*y**3+({b})*y**2+({c})*y+({d})"

                self.hermite_polynomit.append([polynomi, tyyppi, raja_1, raja_2])

            self.hermite_lausekkeet = []

            self.Interpolaatiopolynomi4()

            self.viimeisin_x_lista5 = self.x_lista

        if tila == 3: # "Valmis"
            paksuus = self.paksuus5.get()

            if paksuus == "":
                raise ValueError("Muista paksuus (d)!")

            for _polynomi in range(len(self.x_lista) - 1):
                raja_1 = int(self.hermite_polynomit[_polynomi][2])
                raja_2 = int(self.hermite_polynomit[_polynomi][3])

                if self.hermite_polynomit[_polynomi][1] == 1:
                    self.hermite_lausekkeet.append(f"{self.hermite_polynomit[_polynomi][0]} - - - {raja_1} {raja_2} - - {paksuus}")
                else:
                    self.hermite_lausekkeet.append(f"- - {self.hermite_polynomit[_polynomi][0]} - - - {raja_1} {raja_2} {paksuus}")

            for lauseke in self.hermite_lausekkeet:
                self.tekstikenttä.insert(END, f"{lauseke}\n")

            for kilppari in self.kilpparit5:
                kilppari.reset()
                kilppari.clear()

            self.kilpparit5 = []

            self.Varmuuskopioi()

        if tila == 4: # "Uusi yritys"
            try:
                for n in range(len(self.viimeisin_x_lista5)):
                    self.kilpparit5[-1].hideturtle()
                    self.kilpparit5[-1].clear()
                    del self.kilpparit5[-1]

                for n in range(len(self.hermite_polynomit)):
                    self.piirtäjät[-1].clear()
                    del self.piirtäjät[-1]

                self.viimeisin_x_lista5 = None
                self.klikkaus_nro = 0
            except:
                raise ValueError("Vain viimeisimmän voi poistaa!")

            self.karttaikkuna.update()

        if tila == 5: # "Korjaa"
            try:
                indeksi = int(self.vaihda_merkkiä_teksti5.get()) - 1
            except:
                raise ValueError("Minkä käyrän kanssa vaihdetaan merkkiä? (polynomi 1, 2 vai 3 jne.)")

            polynomi = self.hermite_polynomit[indeksi][0]
            tyyppi = self.hermite_polynomit[indeksi][1]

            self.hermite_polynomit[indeksi] = self.Interpolaatiopolynomi5(tyyppi, indeksi)

            for n in range(len(self.hermite_polynomit)):
                self.piirtäjät[-1].clear()
                del self.piirtäjät[-1]

            self.Interpolaatiopolynomi4()

    def Interpolaatiopolynomi3(self, raja_1, raja_2, raja_arvo_1, raja_arvo_2, raja_derivaatta_1, raja_derivaatta_2): # Palauttaa polynomin kertoimet
        a, b, c, d = sympy.symbols('a b c d')

        yhtälö1 = sympy.Eq(a * raja_1 ** 3 + b * raja_1 ** 2 + c * raja_1 + d, raja_arvo_1)
        yhtälö2 = sympy.Eq(a * raja_2 ** 3 + b * raja_2 ** 2 + c * raja_2 + d, raja_arvo_2)
        yhtälö3 = sympy.Eq(3 * a * raja_1 ** 2 + 2 * b * raja_1 + c, raja_derivaatta_1)
        yhtälö4 = sympy.Eq(3 * a * raja_2 ** 2 + 2 * b * raja_2 + c, raja_derivaatta_2)

        ratkaisut = sympy.solve((yhtälö1, yhtälö2, yhtälö3, yhtälö4), (a, b, c, d))

        a = ratkaisut[a]
        b = ratkaisut[b]
        c = ratkaisut[c]
        d = ratkaisut[d]

        return a, b, c, d

    def Interpolaatiopolynomi4(self): # Luo pistelistan karttaikkunaan piirtämistä varten
        for polynomi in self.hermite_polynomit:
            lauseke = polynomi[0]
            alaraja = int(polynomi[2])
            yläraja = int(polynomi[3])

            hermite_pistelista = self.KartanPistelistanMuodostus(lauseke, alaraja, yläraja, "-", "-")

            self.KartanPiirtäjä(pistelista=hermite_pistelista)

    def Interpolaatiopolynomi5(self, tyyppi, indeksi): # Korjaa rikkinäisen polynomin paluttamalla korjatun sekä rajat
        x_1 = self.x_lista[indeksi]
        x_2 = self.x_lista[indeksi + 1]

        if x_1 == x_2:
            x_1 += 1

        y_1 = self.y_lista[indeksi]
        y_2 = self.y_lista[indeksi + 1]

        if y_1 == y_2:
            y_1 += 1

        if tyyppi == 1:
            try:
                d_1 = 1 / self.derivaatat[indeksi]
            except ZeroDivisionError:
                d_1 = 10 ** 6
            try:
                d_2 = 1 / self.derivaatat[indeksi + 1]
            except ZeroDivisionError:
                d_2 = 10 ** 6

            raja_1, raja_2, raja_arvo_1, raja_arvo_2, raja_derivaatta_1, raja_derivaatta_2 = self.Interpolaatiopolynomi6(y_1, y_2, x_1, x_2, d_1, d_2)

            a, b, c, d = self.Interpolaatiopolynomi3(raja_1, raja_2, raja_arvo_1, raja_arvo_2, raja_derivaatta_1, raja_derivaatta_2)

            return ([f"({a})*y**3+({b})*y**2+({c})*y+({d})", -1, raja_1, raja_2])

        else:
            d_1 = self.derivaatat[indeksi]
            d_2 = self.derivaatat[indeksi + 1]

            raja_1, raja_2, raja_arvo_1, raja_arvo_2, raja_derivaatta_1, raja_derivaatta_2 = self.Interpolaatiopolynomi6(x_1, x_2, y_1, y_2, d_1, d_2)

            a, b, c, d = self.Interpolaatiopolynomi3(raja_1, raja_2, raja_arvo_1, raja_arvo_2, raja_derivaatta_1, raja_derivaatta_2)

            return ([f"({a})*x**3+({b})*x**2+({c})*x+({d})", 1, raja_1, raja_2])

    def Interpolaatiopolynomi6(self, eka_a, eka_b, toka_a, toka_b, derivaatta_a, derivaatta_b): # Miettii läpi välin päätepisteiden suuruusjärjestyksen
        if eka_b > eka_a:
            raja_1 = eka_a
            raja_2 = eka_b
            raja_arvo_1 = toka_a
            raja_arvo_2 = toka_b
            raja_derivaatta_1 = derivaatta_a
            raja_derivaatta_2 = derivaatta_b
        else:
            raja_1 = eka_b
            raja_2 = eka_a
            raja_arvo_1 = toka_b
            raja_arvo_2 = toka_a
            raja_derivaatta_1 = derivaatta_b
            raja_derivaatta_2 = derivaatta_a

        return raja_1, raja_2, raja_arvo_1, raja_arvo_2, raja_derivaatta_1, raja_derivaatta_2

    def Kartta(self):
        self.karttaikkuna = turtle.Screen()
        self.karttaikkuna.title("Karttaikkuna")
        turtle.TurtleScreen._RUNNING = True
        self.karttaikkuna.setup(width=1280, height=1280)
        self.karttaikkuna.bgpic(self.karttatiedosto)
        self.karttaikkuna.tracer(0)

        try:
            if self.skaalaaminen.get() != "":
                self.skaalaus = float(self.skaalaaminen.get())
        except:
            None

        # x-akseli:
        pää_x_akseli = turtle.Turtle()
        pää_x_akseli.penup()
        pää_x_akseli.width(2)
        pää_x_akseli.goto(x=0, y=-1000)
        pää_x_akseli.pendown()
        pää_x_akseli.goto(x=0, y=1000)

        # Muut x-akselit:
        for muut_x_a in range(-200, 200, 10):
            if muut_x_a == 0:
                continue
            muut_x_akselit = turtle.Turtle()
            muut_x_akselit.penup()
            muut_x_akselit.hideturtle()
            muut_x_akselit.color("gray")
            muut_x_akselit.goto(x=muut_x_a*self.skaalaus*2, y=-1000)
            muut_x_akselit.pendown()
            muut_x_akselit.goto(x=muut_x_a*self.skaalaus*2, y=1000)

        # y-akseli:
        pää_y_akseli = turtle.Turtle()
        pää_y_akseli.penup()
        pää_y_akseli.hideturtle()
        pää_y_akseli.width(2)
        pää_y_akseli.goto(x=-1000, y=0)
        pää_y_akseli.pendown()
        pää_y_akseli.goto(x=1000, y=0)

        # muut y-akselit:
        for muut_y_a in range(-200, 200, 10):
            if muut_y_a == 0:
                continue
            muut_y_akselit = turtle.Turtle()
            muut_y_akselit.penup()
            muut_y_akselit.hideturtle()
            muut_y_akselit.color("gray")
            muut_y_akselit.goto(x=-1000, y=muut_y_a * self.skaalaus*2)
            muut_y_akselit.pendown()
            muut_y_akselit.goto(x=1000, y=muut_y_a * self.skaalaus*2)

        # x-akselin arvot:
        for x_akseli_arvot in range(-400, 400, 40):
            if x_akseli_arvot == 0:
                continue
            x_arvo = turtle.Turtle()
            x_arvo.penup()
            x_arvo.hideturtle()
            x_arvo.goto(x=x_akseli_arvot * self.skaalaus + 3, y=0)
            x_arvo.write(x_akseli_arvot, font=("Courier New", 12, "bold"))

        # y-akselin arvot:
        for y_akseli_arvot in range(-400, 400, 40):
            y_arvo = turtle.Turtle()
            y_arvo.penup()
            y_arvo.hideturtle()
            y_arvo.goto(x=3, y=y_akseli_arvot * self.skaalaus)
            y_arvo.write(y_akseli_arvot, font=("Courier New", 12, "bold"))

        self.karttaikkuna.update()
        self.karttaikkuna.mainloop()

    def KartanPistelistanMuodostus(self, käyrä, muuttuja_ar, muuttuja_yr, arvo_ar, arvo_yr): # "ar" = alaraja, "yr" = yläraja
        pistelista = []

        if "y" in [*käyrä]:
            korvattava = "y"
        else:
            korvattava = "x"

        for muuttuja in range(muuttuja_ar, muuttuja_yr + 1):
            try:
                arvo = eval(käyrä.replace(korvattava, f"({muuttuja})"))
            except ValueError:
                continue

            if arvo_ar != "-" and arvo_yr != "-":
                if arvo > arvo_yr or arvo < arvo_ar:
                    continue
            if korvattava == "x":
                pistelista.append([self.skaalaus * muuttuja, self.skaalaus * arvo])
            else:
                pistelista.append([self.skaalaus * arvo, self.skaalaus * muuttuja])

        return pistelista

    def KartanPiirtäjä(self, pistelista, väri="red"):
        self.suoran_piirtäjä = turtle.Turtle()
        self.suoran_piirtäjä.width(10)
        self.suoran_piirtäjä.hideturtle()
        self.suoran_piirtäjä.color(väri)
        self.suoran_piirtäjä.penup()

        for numero, indeksi in enumerate(pistelista):
            if indeksi == pistelista[0]:
                self.suoran_piirtäjä.goto(pistelista[0])
                self.suoran_piirtäjä.pendown()
            else:
                self.suoran_piirtäjä.goto(indeksi[0], indeksi[1])

        self.karttaikkuna.update()

        self.piirtäjät.append(self.suoran_piirtäjä)

    def PäivitäKartta(self):
        for piirtäjä in self.piirtäjät:
            piirtäjä.clear()

        self.piirtäjät = []

        tieto = self.tekstikenttä.get("1.0", "end-1c").split("\n")

        if tieto[-1] == "":
            del tieto[-1]

        for käyrä in tieto:
            komponentit = käyrä.split()

            käyrä_plus = komponentit[0]
            käyrä_miinus = komponentit[1]
            käänteis_plus = komponentit[2]
            käänteis_miinus = komponentit[3]
            alaraja_x = komponentit[4]
            yläraja_x = komponentit[5]
            alaraja_y = komponentit[6]
            yläraja_y = komponentit[7]

            käyrät_palasina = [*käyrä_plus] + [*käyrä_miinus]

            if "/" in käyrät_palasina: # suora
                suoran_pistelista = self.KartanPistelistanMuodostus(käyrä_plus, int(alaraja_x), int(yläraja_x), int(alaraja_y), int(yläraja_y))
                self.KartanPiirtäjä(pistelista=suoran_pistelista)

            elif "s" in käyrät_palasina: # kaari
                kaaren_pistelista = self.KartanPistelistanMuodostus(käyrä_plus, int(alaraja_x), int(yläraja_x), int(alaraja_y), int(yläraja_y))
                self.KartanPiirtäjä(pistelista=kaaren_pistelista)
                kaaren_pistelista = self.KartanPistelistanMuodostus(käyrä_miinus, int(alaraja_x), int(yläraja_x), int(alaraja_y), int(yläraja_y))
                self.KartanPiirtäjä(pistelista=kaaren_pistelista)

            else: # interpolaatiopolynomi
                #print(käyrät_palasina)
                if käyrä_plus == "-":
                    hermite_pistelista = self.KartanPistelistanMuodostus(käänteis_plus, int(alaraja_y), int(yläraja_y), alaraja_x, yläraja_x)
                    self.KartanPiirtäjä(pistelista=hermite_pistelista)
                else:
                    hermite_pistelista = self.KartanPistelistanMuodostus(käyrä_plus, int(alaraja_x), int(yläraja_x), alaraja_y, yläraja_y)
                    self.KartanPiirtäjä(pistelista=hermite_pistelista)

    def Varmuuskopioi(self):
        varmuuskopio_tieto = self.tekstikenttä.get("1.0", "end-1c")
        with open(self.varmuuskopio, "w") as f:
            f.write(varmuuskopio_tieto)

class YlimääräisetFunktiot():
    def SuoranPäätepisteidenMääritys(self, k, x_min, y_min, x_max, y_max):
        if k > 0:
            eka_piste_x = x_min
            eka_piste_y = y_min
            toka_piste_x = x_max
            toka_piste_y = y_max
        else:
            eka_piste_x = x_min
            eka_piste_y = y_max
            toka_piste_x = x_max
            toka_piste_y = y_min

        return eka_piste_x, eka_piste_y, toka_piste_x, toka_piste_y

    def UusiSijoitettava(self, x_0, y_0, k, b, eka_piste_x_1, eka_piste_y_1, toka_piste_x_1, toka_piste_y_1, rivi_suora):

        x_2 = int(round((x_0 - k * (b - y_0)) / (k ** 2 + 1), 0))
        y_2 = int(round(k * x_2 + b, 0))

        etäisyys_ekaan_pisteeseen = dist((x_2, y_2), (eka_piste_x_1, eka_piste_y_1))
        etäisyys_tokaan_pisteeseen = dist((x_2, y_2), (toka_piste_x_1, toka_piste_y_1))

        rivi = rivi_suora.split()

        pisteen_uusi_x = x_2
        pisteen_uusi_y = y_2

        if etäisyys_ekaan_pisteeseen < etäisyys_tokaan_pisteeseen:
            verrattava_x = toka_piste_x_1
            verrattava_y = toka_piste_y_1
        else:
            verrattava_x = eka_piste_x_1
            verrattava_y = eka_piste_y_1

        rivi[4] = str(min(pisteen_uusi_x, verrattava_x))
        rivi[5] = str(max(pisteen_uusi_x, verrattava_x))
        rivi[6] = str(min(pisteen_uusi_y, verrattava_y))
        rivi[7] = str(max(pisteen_uusi_y, verrattava_y))

        # return "{} {} {} {} {} {} {} {} {}".format(rivi[0], rivi[1], rivi[2], rivi[3], rivi[4], rivi[5], rivi[6], rivi[7], rivi[8]), x_2
        return " ".join(rivi), x_2

Ohjelma()
