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
import sys
from io import BytesIO
from mutagen.id3 import ID3


pygame.mixer.init()
############            root           #############
root = tk.Tk()

container = ttk.Frame(root)
canvas = tk.Canvas(container, height=350, width=640)
scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion = canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window = scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)
container.pack()
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")


###############            images/icons           ################
imgstop=ImageTk.PhotoImage(Image.open('./icons/pa.png'))
imgplay=ImageTk.PhotoImage(Image.open('./icons/p2.png'))
imgnext=ImageTk.PhotoImage(Image.open('./icons/next.png'))
imgback=ImageTk.PhotoImage(Image.open('./icons/back.png'))
imgpl=ImageTk.PhotoImage(Image.open('./icons/pl.png'))
imgpla=ImageTk.PhotoImage(Image.open('./icons/pla.png'))
imgplus=ImageTk.PhotoImage(Image.open('./icons/plus.png'))
imgfol=ImageTk.PhotoImage(Image.open('./icons/fol.png'))
imgsl=ImageTk.PhotoImage(Image.open('./icons/select.png'))
imgit=ImageTk.PhotoImage(Image.open('./icons/itunes.png'))
imgsn=ImageTk.PhotoImage(Image.open('./icons/skip_next.png'))
imgsb=ImageTk.PhotoImage(Image.open('./icons/skip_back.png'))
imgrp=ImageTk.PhotoImage(Image.open('./icons/rp.png'))
imgitm=ImageTk.PhotoImage(Image.open('./icons/itb.png').resize((40,40), Image.ANTIALIAS))
imgitm2=ImageTk.PhotoImage(Image.open('./icons/itm.png').resize((200,200), Image.ANTIALIAS))
imgitb=ImageTk.PhotoImage(Image.open('./icons/itb.png').resize((150,150), Image.ANTIALIAS))
imgpm=ImageTk.PhotoImage(Image.open('./icons/pm.png').resize((40,40), Image.ANTIALIAS))
imgon=ImageTk.PhotoImage(Image.open('./icons/toggleon.png').resize((40,40), Image.ANTIALIAS))
imgimn=ImageTk.PhotoImage(Image.open('./icons/togglein.png').resize((40,40), Image.ANTIALIAS))
imgoff=ImageTk.PhotoImage(Image.open('./icons/toggleoff.png').resize((40,40), Image.ANTIALIAS))
######################## var #########################
music_directory = os.path.expanduser("~") + "/Music/"
songs=[]
everysongs = []
songs_shuffle = []
playlistsong = []
button = list()
i2 = 0
c2 = 0
c = 0  #----->> cont how many play/pause button pressed
i = 0  #thats important int! this var save the music number
time = 0  ##------------------>> this var save the duration of music
ij = 0
ss = 0
bimage = []   ##---------->> bimage is (B)utton-(I)mage ((small images for music buttons!)) saver    -->--|
bimageb = []  ##---------->>bimageb is (B)utton-(I)mage-(B)ig saver for big label who show the image -->--|
sample_rate = 0  ##------->> this is save the rate of music for play beter music :)                       |
a1 = 0                                     #                                                              |
bc = 0     ##------------->> bc is (B)ackground-(C)hanger of the musics button                            |
tt = 0     ##------------->> thats so fucking important!! this var save how many of music played          |
st = ""    ##                                                                                             |
bigimagedict={}                                                     #                            ---<---|
minimagedict={} #                                         ---<---|
################################################## get songs and their info from directory
print(music_directory)
for file in os.walk(music_directory):
        for f in file:
            for f2 in f:
                if f2.endswith(".mp3"):
                    print("__________________________________________________________")
                    print(f2)
                    f2 = str(f2)
                    if f2[:-4] != "":
                        s=music_directory+f2
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
                            bimage.append(im)
                            bimageb.append(im2)

songs2=[]
songsfile=open("./songs.txt","r+")
for line in songsfile:
        songs2.append(line[:-1])
##########################################################################################################
#---->>ti() calculate how many of music listened
def ti():
    global tt, c
    if c%2 == 1:
        tt = tt + 1
    root.after(1000,ti)
#-----------------------------------------------------------------------------------------------
v2 = StringVar()
Label(root, textvariable = v2).place(x = 138, y = 373)##---->>how many of music listened
v2.set("00:00")
#-----------------------------------------------------------------------------------------------
v3 = StringVar()
Label(root, textvariable = v3).place(x = 480, y = 373)##---->>duratiom of music
v3.set("00:00")
#-----------------------------------------------------------------------------------------------
v5 = StringVar()
Label(root, textvariable = v5).pack()##---->>for make distance between progressbar and scrollable_frame
v5.set("     ")
#-----------------------------------------------------------------------------------------------
v4 = StringVar()
Label(root, textvariable = v4).place(x = 0, y = 148)
v4.set("None")
###---------------------->> klik() can know witch songbutton in s() clicked!!
def klik(n):
    global i, c
    i = n
    c = 0
    playsong()
###---------------->> s() make songs button from their information like image, name, duration etc.
def s(son):
    global st,button,bimage, songs
    button = []
    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    d = tk.Label(scrollable_frame, text = "                     ", font = ("Courier", 10), compound = "left").grid(column = 0)

    d2 = tk.Label(scrollable_frame, text = "name", font = ("Courier", 10), compound = "left").place(x = 230,y = 0)

    d3 = tk.Label(scrollable_frame, text = "time", font = ("Courier", 10), compound = "left").place(x = 600, y = 0)
    for i in range(0,len(son)):

        song = str(son[i])
        ss2 = MP3(song)
        time22 = float(ss2.info.length)
        mn22 = int(time22/60)
        sc22 = int(time22-(mn22*60))
        if sc22 < 10:
            lt22 = str(mn22)+":0"+str(sc22)

        else:
            lt22 = str(mn22) + ":" + str(sc22)

        st = (song.split('/')[-1][:-4])
        if len(st)>15:
            st = st[:15]+"..."
        st = st + (46 - len(st))*" " + lt22
        songs = son
        button.append(tk.Button(scrollable_frame,bg = "gray93", image = minimagedict[song], text = st, font = ("Courier", 10), compound = "left", bd = '0', command = partial(klik, i)))
        button[-1].grid(column = 1, sticky = "nw")

s(everysongs)

###############################################  Important Function!!!   ##############################
def playsong():
    global c, sample_rate, everysongs, tt, a1, button, bc, i, ss, time, l, bimageb, songs
    if i >= (len(songs)):
        i = i - len(songs)
    if c != 0:
        if c%2 == 1:
            pygame.mixer_music.pause()
            playsong1.config(text = 'play', image = imgplay)
            c = c + 1

        else:
            pygame.mixer_music.unpause()
            playsong1.config(text = 'pause',image = imgstop)
            c = c + 1

    else:
        pygame.mixer.quit()
        sample_rate = MP3(songs[i%(len(songs))]).info.sample_rate
        pygame.mixer.init(sample_rate)

        pygame.mixer_music.load(songs[i%(len(songs))])

        ss = MP3(str(songs[i%(len(songs))]))
        time = float(ss.info.length)
        mn2 = int(time/60)
        sc2 = int(time-(mn2*60))
        if sc2 < 10:
            lt2 = str(mn2) + ":0" + str(sc2)
            v3.set(str(lt2))
        else:
            lt2 = str(mn2) + ":" + str(sc2)
            v3.set(str(lt2))


        s = songs[i%(len(songs))]
        st = (s.split('/')[-1][:-4])
        if len(st) > 20:
            st = st[:20] + "..."

        v4.set(st)
        #notif="notify-send deMusic "+(song.split('/')[-1][:-4])+" -i "+"/home/parsa/icons/mu.png"
        #os.system(notif)
        button[bc].config(bg = "gray93")
        button[i].config(bg = "cyan2")
        bc = i
        ibc.config(image = bigimagedict[songs[i]])
        i = i + 1
        print("songs: ", i)
        pygame.mixer_music.play()
        playsong1.config(text = 'pause', image = imgstop)
        pygame.mixer_music.queue(songs[i%(len(songs))])
        c = c + 1
        tt = 0

    if a1 == 0:
        a1 = a1 + 1
        ti()
        que()
###################################################################################################################
def previous():
    global c,tt
    global i
    c = 0
    if tt > 10:
        i = i - 1
        playsong()

    else:
        i = i - 2
        playsong()
####################
def nextf():
    global i
    global c
    c = 0
    playsong()
#####################
def rp():
    global ij
    if ij == 0:
        print("replay is on")
        ij = 1

    else:
        print("replay is off")
        ij = 0
#---------------------------------
# que() do some functions when the music end & repeat in 1s & configur progressbar
def que():
    global i, c, t2, time, tt, ij
    pos = pygame.mixer.music.get_pos()
    if int(pos) == -1:
        c = 0
        tt = 0
        if ij == 1:
            i -= 1
        print(i)
        playsong()
        v['value'] = 0

    else:
        #<<##### progresbar cionfiguring!! #####>>
        if c%2 == 1:
            v['value'] = (tt*100) / time
            mn = int(tt/60)
            sc = tt - (mn*60)
            if sc < 10:
                lt = str(mn) + ":0" + str(int(sc))
                v2.set(str(lt))
            else:
                lt = str(mn) + ":" + str(int(sc))
                v2.set(str(lt))

    root.after(1000,que)
####################### Progres bar #####################################
def pc(event):
    #pc() is (P)rogressbar (C)onfiguring when the mous want to chnge the music time for playing
    global time, tt
    tt = ((event.x)*time) / 300
    pygame.mixer_music.set_pos(tt)
    v['value'] = (tt*100) / time
    mn = int(tt/60)
    sc = tt - (mn*60)
    if sc < 10:
        lt = str(mn) + ":0" + str(int(sc))
        v2.set(str(lt))

    else:
        lt = str(mn) + ":" + str(int(sc))
        v2.set(str(lt))
def cch22(event):
        root.config(cursor = "target")

def cursorchange(event):
        root.config(cursor = "arrow")

v = ttk.Progressbar(root, orient = HORIZONTAL,length = 300)
v.pack()
v.bind('<Button-1>',pc)
v.bind('<B1-Motion>',pc)
v.bind('<Enter>',cch22)
v.bind('<Leave>',cursorchange)
#-----------------------------------------------------------------------------------------------
ibc=tk.Label(root,image=imgitb,compound="t")
ibc.place(x=-1,y=-1)
ibc2=tk.Label(root,text="_____________________")
ibc2.place(x=0,y=165)
playsong1=tk.Button(root, text="play",image=imgplay, padx=0,pady=0,fg="white",bd='0', command=lambda: playsong())
playsong1.pack()
nextkey=tk.Button(root, text=">",image=imgnext, padx=10,pady=5,fg="white",bd='0',command=nextf).place(x=353,y=400)
previouskey=tk.Button(root, text="<",image=imgback, padx=10,pady=5,fg="white",bd='0',command=previous).place(x=267,y=400)
################################## Enter to playlists ####################################################
plba=0
def plb():
        global plba, bc, i, c, tt
        i=0
        bc=0
        if plba%2 == 0:
                s(songs2)
                plb.config(text="  every songs")
        else:
                s(everysongs)
                plb.config(text="    play list ")
        c=0
        tt=0
        playsong()
        plba+=1
plb=tk.Button(root,text="    play list",image=imgpla,bd='0',compound="left",command=plb)
plb.place(x=0,y=200)
######### events
def e1(event):
    playsong()
root.bind('<space>',e1)
#______________________________________
def e2(event):
    nextf()
root.bind('<Right>',e2)
#______________________________________
def e3(event):
    previous()
root.bind('<Left>',e3)
#########################################################################
lon=tk.Label(root,image=imgoff)
lon.place(x=600,y=370)
aon=1
def ca():
      global aon
      rp()

      if aon%2 == 0:
          cab.config(image=imgoff)
      else:
          cab.config(image=imgon)
      aon += 1
#___________________________________________________________________
cab=tk.Button(root,image=imgoff,bd='0',command=ca)
cab.place(x=600,y=370)
######################### Old Widget! ##########################################################
'''
def find():
    filename1=filedialog.askopenfilename(initialdir="/home/parsa",title="Select File")
    playlistsong.append(filename1)
    print(filename1)
    for song in songs:
        label=tk.Label(root2,text=song,bg="gray")
        label.pack()
def song():
    global songs
    filename=filedialog.askopenfilename(initialdir="/home",title="Select File")
    if filename!=():
        if filename not in songs:
            print(filename)
            songs.append(filename)

    for widget in scrollable_frame.winfo_children():
        widget.destroy()
    for i in range(0,len(songs)):
        song=str(songs[i])

        button.append(tk.Button(scrollable_frame,bg="cyan2",image=imgitm,text =(song.split('/')[-1][:-4])+(80-len(song[18:-4]))*" ",font=("Courier", 10),compound="left", command=partial(klik, i)))
        button[-1].grid(column=0,sticky="nw")

####################
def sn():
    global tt
    tt=tt+15
    pygame.mixer_music.set_pos(tt)
#####################
def sb():
    global tt
    if (tt-15)>0:
        tt=tt-15
        pygame.mixer_music.set_pos(tt)
    else:
        tt=0
        pygame.mixer_music.set_pos(tt)
snkey=tk.Button(root, text=">",image=imgsn,command=sn,bd='0',fg="white").place(x=407,y=400)
sbkey=tk.Button(root, text="<",image=imgsb,command=sb,bd='0',fg="white").place(x=212,y=400)
rpb=Button(root,image=imgrp,command=rp,bg='gray').place(x=500,y=400)
file.add_command(label='add song',command=song,image=imgsl,compound="left")
file.add_cascade(menu=playlist,label='playlist',image=imgpl,compound="left")

pla.add_command(label='play lists',image=imgpla,compound="left")
pla.add_command(label='new playlist',command=playlist_f,image=imgplus,compound="left")

playlist.add_command(label='play lists',image=imgpla,compound="left")
playlist.add_command(label='new playlist',command=playlist_f,image=imgplus,compound="left")'''
##################################################################################################
root.resizable(0, 0)
root.title('music player')
root.iconphoto(False, tk.PhotoImage(file='/home/parsa/icons/mu.png'))
root.mainloop()
