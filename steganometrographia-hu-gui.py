# -*- coding: utf-8 -*-
# Steganometrographia program
# Náday Ádám (nadapapa@gmail.com)

try:
    from tkinter import *
    from tkinter.ttk import *
except:
    from Tkinter import *
    from ttk import *

import random
import pickle
import re
import webbrowser
import copy

class HyperlinkManager:

    def __init__(self, text):

        self.text = text

        self.text.tag_config("hyper", foreground="blue", underline=1)

        self.text.tag_bind("hyper", "<Enter>", self._enter)
        self.text.tag_bind("hyper", "<Leave>", self._leave)
        self.text.tag_bind("hyper", "<Button-1>", self._click)

        self.reset()

    def reset(self):
        self.links = {}

    def add(self, action):
        # add an action to the manager.  returns tags to use in
        # associated text widget
        tag = "hyper-%d" % len(self.links)
        self.links[tag] = action
        return "hyper", tag

    def _enter(self, event):
        self.text.config(cursor="hand2")

    def _leave(self, event):
        self.text.config(cursor="")

    def _click(self, event):
        for tag in self.text.tag_names(CURRENT):
            if tag[:6] == "hyper-":
                self.links[tag]()
                return
            
ablak=Tk()
ablak.geometry("370x550")
ablak.title("Steganometrographia")
ikon = PhotoImage(file='icon2.gif')
#ikon = Image()
#ablak.wm_iconbitmap("icon.ico")
ablak.tk.call('wm', 'iconphoto', ablak._w, ikon)
ablak.resizable(width=FALSE,
                height=FALSE)

# abc és tabellák betöltése fájlból
try:
    with open("tabellak.p", "rb") as f:
        abc,tabellak = pickle.load(f)
except:
    with open("tabellak2.p", "rb") as f:
        abc,tabellak = pickle.load(f) 

def generator():
    var = v.get()
    sor = int(sorok.get())*2
    #epistola.configure(state='normal')
    epistola.delete("1.0", END)
    szamlalo=0
    szamlalo2=0
    uzenet=[]
    eredmeny=[]
    a=0
    try:
        if var == 1: #random generátor
            for i in range(sor):
                uzenet.append(random.choice(abc))

            for tabella in tabellak:
                if szamlalo<(sor):
                    if szamlalo == 0:
                        eredmeny.append(tabella[uzenet[(szamlalo)]])
                    elif szamlalo %2 == 1:
                        eredmeny.append(tabella[uzenet[(szamlalo)]])
                        eredmeny.append("\n")
                        szamlalo2 += 1
                    else:
                    #szamlalo %2 ==0:
                        if szamlalo2 % 2 == 1:
                            eredmeny.append("    ")
                        eredmeny.append(tabella[uzenet[(szamlalo)]])
                    szamlalo += 1
        else: #üzenet átírása
            szoveg = bevitel.get()
            szoveg = re.sub("[^a-zA-Z]+", "", szoveg.upper())
        
            for i in szoveg:
                if szamlalo<44:
                    if szamlalo == 0:
                        eredmeny.append(tabellak[szamlalo][i])
                    elif szamlalo %2 == 1:
                        eredmeny.append(tabellak[szamlalo][i])
                        eredmeny.append("\n")
                        szamlalo2 += 1
                    else:
                        if szamlalo2 % 2 == 1:
                            eredmeny.append("    ")
                        eredmeny.append(tabellak[szamlalo][i])
                    szamlalo += 1            
    except KeyError as e:
        epistola.insert(END, "Sajnos a betűk között nem szerepel {0}.".format(e))
    else:
        epistola.insert(END,"".join(eredmeny))
        #epistola.configure(state="disabled")
        
    szamlalo=0
    a=0
    uzenet=[]
    
def dekodolas():
    bevitel.delete(0, END)
    tabellak2= copy.deepcopy(tabellak)
    szoveg = epistola.get('1.0', END)
    szoveg = re.sub("[^a-zA-Z]+", "", szoveg.upper())
    for tabella in tabellak2:
        for i in tabella:
            tabella[i] = re.sub("[^a-zA-Z]+", "", tabella[i].upper())
            if tabella[i] in szoveg:
                bevitel.insert(END, i)

    
def clipboard():
    # kimásolja a szöveget a vágólapra
    epistola.clipboard_clear()
    text = epistola.get("1.0", END)
    epistola.clipboard_append(text)

def programrol():
    ## új ablak - programról
    menubar.entryconfig(2,state=DISABLED)
   
    programrol_ablak = Toplevel()
    programrol_ablak.title("Erről a programról")
    programrol_ablak.geometry("410x540")
    programrol_ablak.resizable(width=FALSE,
                     height=FALSE)
    programrol_ablak.tk.call('wm', 'iconphoto', programrol_ablak._w, ikon)

    keret = Frame(programrol_ablak)
    keret.pack()
    scroll = Scrollbar(keret,
                       orient= VERTICAL)
    scroll.pack(side=RIGHT,
                fill="y",
                expand=False)
    szoveg = Text(keret,
                  font="Times",
                  wrap=WORD,
                  yscrollcommand=scroll.set,
                  height=25)
    szoveg.pack()

    def kilep():
        programrol_ablak.destroy()
        menubar.entryconfig(2,state=NORMAL)
    button= Button(programrol_ablak,
                   text="Bezár",
                   command=kilep
                   ).pack()
    programrol_ablak.protocol("WM_DELETE_WINDOW", kilep)
    
    kep = PhotoImage(file="cimlap.gif")
    szoveg.image_create(END, image=kep)
    szoveg.kep = kep
#leírás
    szoveg.tag_config("italic", font=('Times', '12', 'italic'))
    szoveg.tag_config("bold", font=('Times', '14', 'bold'))
    szoveg.tag_config("kis", font=('Times', '8'))
    cim="Steganometrographia, sive Artificium novum & inauditum"
    szoveg.insert(END, '''Ez a kis applikáció lényegében egy könyv \
"programosítása".
Melchias Uken ''')
    szoveg.insert(END, cim, 'italic')
    szoveg.insert(END, ''' című 1751-ben megjelent könyve \
alapján készült. A könyv egy steganometrographia nevű rejtjelező \
eljárást ismertet, aminek segítségével rövid üzeneteket lehet latin \
disztichonokba rejteni. Az alapelve, hogy az ABC betűihez félsorokat \
rendel. A könyvben található táblázatok segítségével ki lehet \
keresni az üzenet betűihez tartozó verssordarabokat. A végeredmény egy \
latin nyelvű disztichonos költemény, ami témáját tekintve egy verses levél, \
de közben ott lapul benne a titkos üzenet. A levél címzettje, ha szintén \
rendelkezik a könyvvel, könnyen dekódolhatja az üzenetet.
Ezzel a programmal ezt a folyamatot lehet könnyebben, gyorsabban \
és egyszerűbben elvégezni. A használatáról bővebben a "Használat" menüpont alatt.
''')
    hyperlink = HyperlinkManager(szoveg)
    
    def link1():
        webbrowser.open_new('https://books.google.hu/books?id=16QBAAAAYAAJ')

    def link2():
        webbrowser.open_new('https://archive.org/details/steganometrogra00ukengoog')

    szoveg.insert(END, "\nA teljes könyv letölthető:\n")
    szoveg.insert(END, "google books", hyperlink.add(link1))
    szoveg.insert(END, "\n")
    szoveg.insert(END, "archive.org", hyperlink.add(link2))
    szoveg.insert(END, """\n\n
Készítette: Náday Ádám
nadapapa@gmail.com""", 'kis')
    szoveg.configure(state="disabled")   

def hasznalat():
    ## új ablak - használat
    menubar.entryconfig(1,state=DISABLED)
    
    hasznalat_ablak = Toplevel()
    hasznalat_ablak.title("Használat")
    hasznalat_ablak.geometry("400x240")
    hasznalat_ablak.resizable(width=FALSE,
                        height=FALSE)
    hasznalat_ablak.tk.call('wm', 'iconphoto', hasznalat_ablak._w, ikon)
    
    keret = Frame(hasznalat_ablak)
    keret.pack()
    scroll = Scrollbar(keret,
                       orient= VERTICAL)
    scroll.pack(side=RIGHT,
                fill="y",
                expand=False)
    szoveg = Text(keret,
                  font="Times",
                  wrap=WORD,
                  yscrollcommand=scroll.set,
                  height=10)
    szoveg.pack()
    
    def kilep():
        hasznalat_ablak.destroy()
        menubar.entryconfig(1,state=NORMAL)
    button = Button(hasznalat_ablak,
                   text="Bezár",
                   command=kilep
                   ).pack()
    hasznalat_ablak.protocol("WM_DELETE_WINDOW", kilep)
    ## használat ablak szöveg
    szoveg.tag_config("italic", font=('Times', '12', 'italic'))
    szoveg.tag_config("bold", font=('Times', '14', 'bold'))
    szoveg.insert(END,"""A program használata
""", 'bold')
    szoveg.insert(END,
"""A program háromféleképpen használható:
    - Véletlenszerű versgenerálás
    - Rövid szöveg kódolása versben
    - Kódolt vers dekódolása
""")
    szoveg.insert(END, """
1. Véletlenszerű versgenerálás:""", 'italic')
    szoveg.insert(END, """
  Ahhoz, hogy a program véletlenszerűen generáljon \
egy verset, ki kell jelölni a "random" opciót, majd megnyomni a "Verset!" gombot. \
Az opció melletti legördülő listából kiválasztható a generált vers hossza. Tetszőleges \
szám is beírható, de maximum 22 soros vers generálható.

""")
    szoveg.insert(END, """2. Rövid szöveg kódolása versben:""", 'italic')
    szoveg.insert(END, """
  A könyv eredetileg rövid üzenetek rejtjelezésére íródott. Ezt a programmal is el lehet végezni \
Ilyenkor ki kell jelölni az "üzenet" opciót és a mellette lévő mezőbe írni a kódolandó \
üzenetet, majd megnyomni a "Verset!" gombot. Csak betűket lehet kódolni és maximum 44 betű \
hosszúságú szöveg kódolható.

""")
    szoveg.insert(END, """3. Kódolt vers dekódolása:""", 'italic')
    szoveg.insert(END, """
    Az előző folyamar megforítása. A verset a nagy mezőbe kell bemásolni, majd megnyomni a "Dekódolás" \
  gombot. A kimenet a kis mezőben jelenik meg. A dekódolt üzenetben nincsenek szóközök és \
  teljesen nagybetűs.
  
""")
    szoveg.insert(END, """4. Betűk""", 'italic')
    szoveg.insert(END, """
  Melchias Uken eredetileg a német nyelvterületre szánta a könyvet, ezért az alábbi betűk \
titkosíthatóak:
A, B, C, D, E, F, G, H, I, K, L, M, N, O, P, Q, R, S, T, V, W, X, Z
""")
    
    szoveg.configure(state="disabled")

## Menü 
menubar = Menu(ablak)
menubar.add_command(label="Használat",
                     command=hasznalat)
menubar.add_command(label="A programról",
                     command=programrol)
menubar.add_command(label="Kilép",
                     command=ablak.destroy)

### főablak felépítése
## generálás választás
v = IntVar()
v.set(1)
def valasztas():
    return v

rand = Radiobutton(ablak,
                       text="random",
                       variable=v,
                       value=1,
                       command=valasztas
                       )
rand.grid(row=0, column=0, sticky=W, padx=10, pady=1)
szoveg = Radiobutton(ablak,
                         text="üzenet",
                         variable=v,
                         value=2,
                         command=valasztas
                         )
szoveg.grid(row=1, column=0, sticky=W, padx=10, pady=1)

## random sorok száma
sorok = Combobox(ablak,
                 width="2",
                 exportselection=0,
                 height="11",
                 values=["2","4","6","8","10","12","14","16","18","20","22"])
sorok.set("2")
sorok.grid(row=0, column=1, sticky="w", pady=10)

Label(ablak, text="sor").grid(row=0, column=1, sticky="w", padx=35, pady=1)

## üzenet bevitel
bevitel=Entry(ablak, width="30")
bevitel.grid(row=1, column=1, columnspan=3, sticky="w", pady=1)

## vers kiírás
epistola = Text(ablak,
                height=22,
                width=45,
                font="Times")
##Label(ablak,
##          text=""""""
##          ).grid(row=2, column=1, sticky="w")

## gombok 
button = Button(ablak,
                text='Verset!',
                command=generator
                )
button.grid(row=3, column=0, pady=5)

masolas = Button(ablak,
                 text="Vágólapra másol",
                 command=clipboard
                 )
masolas.grid(row=3, column=1, sticky="w", pady=5, padx=30)

dekod = Button(ablak, text="Dekódolás", command=dekodolas)
dekod.grid(row=3, column=2, pady=5, sticky="w")

## szöveg kimenet 
epistola.grid(row=5, column=0, columnspan=3, sticky="w")

##ablak
ablak.config(menu=menubar)
ablak.mainloop()
