from math import *
from time import sleep

# Tässä ohjelmassa koordinaattiakseleiden suuntaus vastaa standardia matematiikassa käytettyä suuntausta, ei Minecraftin suuntausta
# (eli tässä ohjelmassa z-akseli on pystyakseli, eikä y niin kuin Minessä).

rajat_z = [-200, 100]
rajat_x = [0, 62]
rajat_y = [0, 54]

ratkaistu_z = input("z:")
ratkaistu_x = input("x:")
ratkaistu_y = input("y:")

tiedostosijainti = r"C:\Users\User\AppData\Roaming\.minecraft\forge 1.12.2\saves\Tehdenson City - 5.8.2026\data\functions\digi\funktio.mcfunction"

open(tiedostosijainti, 'w').close()

with open(tiedostosijainti, "a") as f:
    for x in range(rajat_x[0], rajat_x[1]):
        for y in range(rajat_y[0], rajat_y[1]):
            for indeksi in ratkaistu_z.split():
                muokattu = str(indeksi.replace("x", str(x)).replace("y", str(y)))
                try:
                    z = int(round(float(eval(muokattu)), 0))
                except:
                    continue

                if rajat_z[0] <= z <= rajat_z[1]:
                    komento = "setblock ~{} ~{} ~{} wool 14\n".format(x, z, y)
                    f.write(komento)

    print("osio z tehty")

    for y in range(rajat_y[0], rajat_y[1]):
        for z in range(rajat_z[0], rajat_z[1]):
            for indeksi in ratkaistu_x.split():
                muokattu = str(indeksi.replace("y", str(y)).replace("z", str(z)))
                try:
                    x = int(round(float(eval(muokattu)), 0))
                except:
                    continue

                if rajat_x[0] <= x <= rajat_x[1]:
                    komento = "setblock ~{} ~{} ~{} wool 14\n".format(x, z, y)
                    f.write(komento)


    print("osio x tehty")

    for x in range(rajat_x[0], rajat_x[1]):
        for z in range(rajat_z[0], rajat_z[1]):
            for indeksi in ratkaistu_y.split():
                muokattu = str(indeksi.replace("x", str(x)).replace("z", str(z)))
                try:
                    y = int(round(eval(muokattu), 0))
                except:
                    continue

                if rajat_y[0] <= y <= rajat_y[1]:
                    komento = "setblock ~{} ~{} ~{} wool 14\n".format(x, z, y)
                    f.write(komento)


    print("osio y tehty")

            #((200*((x)/(40))*((y)/(40)))/(2.71828**(((((x)/(40)))**(2)+(((y)/(40)))**(2)))))
