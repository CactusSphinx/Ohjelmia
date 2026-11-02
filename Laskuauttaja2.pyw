from tkinter import *

#luku = int(input("luku --> "))
#luku -= 2

class Ohjelma:
    def __init__(self):
        self.fontti = ("Courier", 24, "bold")
        self.päälle = True
        self.lista_kirjasto = {}

        self.laajuus_maksimi = 6
        self.väli_maksimi = 10

        self.ikkuna = Tk()
        self.ikkuna.geometry('638x760')
        self.ikkuna.title("Minecraft-laskuapuri")
        self.ikkuna.rowconfigure(0, weight=1, minsize=200)
        self.ikkuna.columnconfigure(0, weight=1, minsize=200)

        self.runko1 = Frame(self.ikkuna, bg="#B7AAA7", borderwidth=10)
        self.runko1_1 = Frame(self.runko1, bg="#B7AAA7")
        self.runko1_2 = Frame(self.runko1, bg="#BC9186", borderwidth=10)

        self.aloitusviesti = Label(text="Kuutioiden määrä", master=self.runko1, font=self.fontti, bg="#B7AAA7")
        self.toimivat_yhdistelmät_teksti = Label(master=self.runko1, font=self.fontti, bg="#E5D6D2")
        self.laajuus_maksimi_teksti = Label(text="Laajuuden maksimi", master=self.runko1_2, font=self.fontti, bg="#BC9186")
        self.väli_maksimi_teksti = Label(text="Välin maksimi", master=self.runko1_2, font=self.fontti, bg="#BC9186")
        self.liikaa_ilmoitus = Label(text="Liikaa toimivia yhdistelmiä!", master=self.runko1, font=("Courier", 24, "bold"), fg="red", bg="#B7AAA7")

        self.kuutiosyöte = Entry(master=self.runko1, font=self.fontti, borderwidth=3, bg="gray")
        self.laajuus_maksimi_syöte = Entry(master=self.runko1_2, font=self.fontti, width=12, borderwidth=3, bg="gray")
        self.väli_maksimi_syöte = Entry(master=self.runko1_2, font=self.fontti, width=12, borderwidth=3, bg="gray")

        self.käynnistys = Button(text="Käynnistä", master=self.runko1, command=self.ToiminnanAloitus, font=self.fontti, width=10, borderwidth=3, bg="gray")
        self.tyhjennys = Button(text="Tyhjennä", master=self.runko1_1, command=self.Tyhjennä, font=self.fontti, width=10, borderwidth=3, foreground="red", bg="gray")
        self.määritys = Button(text="Määritä", master=self.runko1_1, command=self.Määritys, font=self.fontti, width=10, borderwidth=3, bg="gray")

        self.Käynnistys()

    def Käynnistys(self):
        self.runko1.grid(row=0, column=0, sticky="N")
        self.aloitusviesti.grid(row=0, column=0, pady=5)
        self.kuutiosyöte.grid(row=1, column=0)
        self.käynnistys.grid(row=1, column=1, padx=5)
        self.runko1_1.grid(row=2, column=1, sticky="N")
        self.tyhjennys.grid(row=0, column=0, pady=5)
        self.määritys.grid(row=1, column=0)

        self.kuutiosyöte.bind("<Return>", self.ToiminnanAloitus)

        self.ikkuna.mainloop()

    def ToiminnanAloitus(self, event=None):
        self.toimivat_yhdistelmät = []
        try:
            self.liikaa_ilmoitus.grid_forget()
            self.toimivat_yhdistelmät_teksti.grid_forget()
            self.toimivat_yhdistelmät_teksti["text"] = ""
        except:
            None

        self.luku = int(self.kuutiosyöte.get()) - 2

        for laajuus in range(1, self.laajuus_maksimi+1):
            for väli in range(1, self.väli_maksimi+1):
                self.Toiminta(laajuus, väli)

        toimivat = ""

        for toimii in self.toimivat_yhdistelmät:
            toimivat += f"\n{toimii}"
            if len(toimivat.split("\n")) > 15:
                self.liikaa_ilmoitus.grid(row=3, column=0, pady=5, columnspan=2)
                break

        self.toimivat_yhdistelmät_teksti["text"] = f"Seuraavat toimivat: {toimivat}"
        self.toimivat_yhdistelmät_teksti.grid(row=2, column=0)

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

    def Määritys(self):
        if self.päälle:
            self.päälle = False
            self.laajuus_maksimi_teksti.grid(row=0, padx=5, column=0)
            self.laajuus_maksimi_syöte.grid(row=0, column=1)

            self.väli_maksimi_teksti.grid(row=1, column=0, padx=5, sticky="E")
            self.väli_maksimi_syöte.grid(row=1, column=1, sticky="E")

            self.runko1_2.grid(row=4, column=0, columnspan=2, pady=8, sticky="NW")

        else:
            self.päälle = True

            try:
                self.laajuus_maksimi = int(self.laajuus_maksimi_syöte.get())
                self.väli_maksimi = int(self.väli_maksimi_syöte.get())
            except:
                None

            self.runko1_2.grid_forget()
            self.kuutiosyöte.focus_set()

    def Tyhjennä(self):
        self.liikaa_ilmoitus.grid_forget()
        self.toimivat_yhdistelmät_teksti.grid_forget()

Ohjelma()