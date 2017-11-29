#!usr/bin/env/ python
# coding: utf-8
"""
MUR - Manjaro User Repository
Thanks : Baba, Fredo, Rhylx, Francky, hRF, Pepito, for AMAR Project.
Date : 29 Nov 2K17,
version :  1.0
gksudo -s python mur.py
"""

import os
import sys
from PIL import Image 
import subprocess
from tkinter import *

if sys.version_info[0] == 3:
    from tkinter import messagebox
else:
    import tkMessageBox as messagebox

if os.getuid() != 0:
    os.system ("gksudo python /usr/bin/mur.py")
    #print("Utiliser le script en tant qu'administrateur, lancer le avec 'gksudo -s python mur.py'")
    sys.exit(1)

pacmanfichier = "/etc/pacman.conf"

try:
    #On suppose d'abord que MUR est désactivé. On met donc etatmur = 0 au départ.
    etatmur = 0
    with open(pacmanfichier, 'r') as searchfile:
        for line in searchfile:
            #Si la chaîne '[MUR]' est écrit quelque part dans pacman.conf, alors le dépôt est activé et on met etatmur = 1.
            if 'mur.conf' in line:
                etatmur = 1
    searchfile.close()
except OSError:
    print("pacman.conf non acessible, donnez le chemin vers votre fichier")
    sys.exit(1)

configmur = "\n#Do not disable MUR manually if you use the app\nInclude = /etc/pacman.d/mur.conf\n"

def pressA():
    A.config(state=DISABLED)
    B.config(state=ACTIVE)
    try:
        with open(pacmanfichier, "a") as ecrire:
            ecrire.write(configmur)
            ecrire.close()
            os.system("sudo pacman -Syy")
            INFO.config(text="Actif", fg="green")  # on active le depot MUR, donc on ecrit sur le fichier.
            etatmur = 1
            ecrire.close()
    except OSError:
        messagebox.showerror("Erreur", "Ficher pacman.conf non accessible en écrture\nVérifier vos droit et relancer"
                                       " le script\nVérifier aussi que vous ne faite une mise à jours en même temps")

 
def pressB():
    A.config(state=ACTIVE)
    B.config(state=DISABLED)
    try:
        with open((pacmanfichier), "r") as f:
            lines = f.readlines()
            lines.remove("#Do not disable MUR manually if you use the app\n")
            lines.remove("Include = /etc/pacman.d/mur.conf\n")
        with open((pacmanfichier), "w") as new_f:
            for line in lines:
                new_f.write(line)
        os.system ("sudo pacman -Syy")
        INFO.config(text="Inactif", fg="red")  # on active le depot MUR, donc on ecrit sur le fichier.
        etatmur = 0
        f.close()
        new_f.close()
    except OSError:
        messagebox.showerror("Erreur", "Ficher pacman.conf non accessible en écrture\nVérifier vos droit et relancer"
                                       " le script\nVérifier aussi que vous ne faite une mise à jours en même temps")


win = Tk()
win.title("MUR - Manjaro User Repository")
win.geometry("620x280")
tux = PhotoImage(file="/usr/share/icons/mur.png")  # lien vers l'icone de la fenetre
win.tk.call('wm', 'iconphoto', win._w, tux)  # application de la fenetre

TEXTE = Label(win, text='MUR', fg="blue")
TEXTE2 = Label(win, text="Le dépôt MUR (Manjaro User Repository) est un dépôt tiers donnant\n"
                           "accès à des logiciels supplémentaires non-accessibles via les dépôts officiels."
                           "\n\nCe dépôt a été créé afin de pouvoir donner accès simplement à des logiciels dont"
                           " l'installation\nvia AUR est problématique ou des logiciels qui ne concernent que"
                           " Manjaro\net qui sont expulsés d'AUR pour cette raison.", fg="purple")
TEXTE.pack(side=TOP, padx=5, pady=3)  # Titre de l'application de texte
TEXTE2.pack(side=TOP, padx=5, pady=10)  # Titre de l'application de texte

A = Button(win, text='ACTIVER', height=2, width=30, command=pressA)
B = Button(win, text='DESACTIVER', height=2, width=30, command=pressB)

INFO = Label(win, text='', fg="black")  # Informations qui changent en fonction du bouton appuyé par l'utilisateur
MESSAGE = Label(win, text='ETAT DU DEPÔT', fg="blue")

INFO.pack(side=BOTTOM)  # on ferme les boutons en décidant de leur amplacement
MESSAGE.pack(side=BOTTOM)

if etatmur:
    A.pack()
    A.config(state=DISABLED)
    B.pack()
    B.config(state=ACTIVE)
else:
    A.pack()
    A.config(state=ACTIVE)
    B.pack()
    B.config(state=DISABLED)

if etatmur == 0:
    INFO.config(text="Inactif", fg="red")  # on active le depot MUR, donc on ecrit sur le fichier.
else:
    INFO.config(text="Actif", fg="green")  # on active le depot MUR, donc on ecrit sur le fichier.
    
win.mainloop()
