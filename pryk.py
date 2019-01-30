from PIL import Image
from imutils import paths
import argparse
import os
import time

# Argumenty potrebne do zrobienia co ma byc zrobione
ap = argparse.ArgumentParser()
ap.add_argument("-w", "--znak", required=True, help="nazwa pliku znaku wodnego")
ap.add_argument("-i", "--skad", required=True, help="nazwa folderu do przerobienia")
ap.add_argument("-o", "--dokad", required=True, help="nazwa folderu przerobionego")
ap.add_argument("-c", "--correct", type=int, default=1, help="flaga do wyswietlania bledow")
args = vars(ap.parse_args())

# definicja ilosci wykonanych petli
loops = 0

# czas na poczatku petli
czas_start = time.time()

# glowna petla
if args["correct"] > 0:
    for imagePath in paths.list_images(args["skad"]):
        # wczytuje obrazek do przerobienia
        base_image = Image.open(imagePath)

        # wczytuje znak wodny
        znakWodny = Image.open(args["znak"])

        # pobiera wymiary obrazka i znaku glownego
        width, height = base_image.size
        wW, wH = znakWodny.size

        # ustala pozycje dla znaku downego -
        position = (int((width / 2) - (wW / 2)), int((height / 2) - (wH / 2)))

        # Robi nowy obraz na ktorym beda wklejone obydwa obrazy
        transparent = Image.new('RGB', (width, height), (0, 0, 0, 0))

        # wkleja zdjecie
        transparent.paste(base_image, (0, 0))

        # wkleja znak wodny
        transparent.paste(znakWodny, position, mask=znakWodny)

        # pobieramy nazwe pliku oryginalnego zdjecia
        filename = imagePath[imagePath.rfind(os.path.sep) + 1:]

        # przerabiamy go na nowa nazwe w nowym folderze
        p = os.path.sep.join((args["dokad"], filename))

        # zapisujemy
        transparent.save(p)

        # Wypisuje aktualnie przerobione zdjecie
        print("Dodano znak do : " + imagePath)

        # dodaje +1 do ilosci
        loops += 1

# czas na koncu petli
czas_koniec = time.time()

# wypis koncowy
print(str(loops) + " zdjec zrobionych w " + str(czas_koniec - czas_start) + " sekund")
