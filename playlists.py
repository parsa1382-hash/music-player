import os
import time
import pickle
import pygame
import tkinter as tk
from tkinter import filedialog, Text, ttk
from tkinter import*
from PIL import Image, ImageTk
from PIL import*
from functools import partial
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
import sys
from io import BytesIO

############            root           #############
root=tk.Tk()

container = ttk.Frame(root)
canvas = tk.Canvas(container, height=350, width=400)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
container.pack()
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")
##########################################  images  ############################################
imgdone=ImageTk.PhotoImage(Image.open('/home/parsa/icons/done.png'))
imgitm=ImageTk.PhotoImage(Image.open('/home/parsa/icons/itm.png').resize((40,40), Image.ANTIALIAS))
imgitm2=ImageTk.PhotoImage(Image.open('/home/parsa/icons/itm.png').resize((200,200), Image.ANTIALIAS))
imgitb=ImageTk.PhotoImage(Image.open('/home/parsa/icons/itb.png').resize((150,150), Image.ANTIALIAS))
imgpm=ImageTk.PhotoImage(Image.open('/home/parsa/icons/pm.png').resize((40,40), Image.ANTIALIAS))




everysongs=[]
button = list()

playlistmaker=[]

ss=0
bimage=[]
bimageb=[]

st=""
bigimagedict={}
minimagedict={}

buttonc=[]

##################################################
for file in os.walk("/home/parsa/Music"):
        for f in file:
            for f2 in f:
                if f2.endswith(".mp3"):
                    print("__________________________________________________________")
                    print(f2)
                    f2=str(f2)
                    if f2[:-4]!="":
                        s="/home/parsa/Music/"+f2
                        everysongs.append(s)
                        if ID3:
                            tags=ID3(s)
                            if (tags.get("APIC:"))!=None:
                                print(".........image add")
                                im=ImageTk.PhotoImage(Image.open(BytesIO(tags.get("APIC:").data)).resize((40,40), Image.ANTIALIAS))
                                im2=ImageTk.PhotoImage(Image.open(BytesIO(tags.get("APIC:").data)).resize((150,150), Image.ANTIALIAS))
                            else:
                                im=imgitm
                                im2=imgitb

                            bigimagedict[s]=im2
                            minimagedict[s]=im
                            buttonc.append(0)
                            bimage.append(im)
                            bimageb.append(im2)


###############################################################################################################


def klik(n):
        global buttonc, everysongs, playlistmaker
        if buttonc[n]==0:
                buttonc[n]=1
                playlistmaker.append(everysongs[n])
                button[n].config(bg='orange')
                print(everysongs[n]," appended")
        else:
                buttonc[n]=0
                playlistmaker.remove(everysongs[n])
                button[n].config(bg='cyan2')
                print(everysongs[n]," deleted")





def s(son):
    global st,button,bimage, songs
    button=[]
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    
    for i in range(0,len(son)):
        song=str(son[i])
        ss2=MP3(song)
        time22=float(ss2.info.length)
        mn22=int(time22/60)
        sc22=int(time22-(mn22*60))
        if sc22<10:
            lt22=str(mn22)+":0"+str(sc22)
        else:
            lt22=str(mn22)+":"+str(sc22)
        
        st=(song.split('/')[-1][:-4])
        if len(st)>15:
            st=st[:15]+"..."
        st=st+(46-len(st))*" "
        songs=son
        button.append(tk.Button(scrollable_frame,bg="cyan2"
                                ,image=minimagedict[song]
                                ,text=st,font=("Courier", 10)
                                ,compound="left",bd='0'
                                ,command=partial(klik, i)))
        button[-1].grid(column=0,sticky="nw")

s(everysongs)
##########################################
def find():
    filename1=filedialog.askopenfilename(initialdir="/home/parsa",title="Select File")
    playlistsong.append(filename1)
    print(filename1)
    for song in playlistsong:
        label=tk.Label(scrollable_frame2,text=song,bg="gray")
        label.pack()

######################################################################################
en=StringVar()
def done():
        global en, playlistmaker
        f=open((en.get()+".txt"),"w+")
        for i in playlistmaker:
                f.write(i+"\n")
        f.close()
        print(en.get())
sl2=tk.Button(root, text="done", padx=10,pady=5,image=imgdone, command=done)
sl2.pack(side="right")
name=tk.Label(text='name:').pack(side='left')

e=tk.Entry(root,textvariable=en,bg='gray95').pack(side='left')






root.mainloop()
