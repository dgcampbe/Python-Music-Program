#Main music program

#import random module for some randomness in the music
import random
#import tkinter for GUI
import tkinter as tk
#for file and folder dialogs
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
#for writing some files to a specified folder
import os.path
#Pygame is here!!!
import pygame
from pygame import midi
#import livewires
import time
#Music21 module from MIT (absolutely amazing)
import music21
#A module I made for testing using pygame for playing MIDIs(included)
import bach_aof
import playmodule
from collections import OrderedDict

#some variables that need to be defined
defaultsavepath = "C:/PythonMusic/textfiles/"
globalsavepath = defaultsavepath
Note_list = ["A","B","C","D","E","F","G"]
Octaves = [1,2,3,4,5,6]
Pitches = ["soprano", "mezzo-soprano", "alto", "tenor", "baritone", "bass"]
Pitchdict = {"soprano": "C4-A5", "mezzo-soprano": "A3-F5", "alto": "F3-D5", "tenor": "B2-G4", "baritone": "G2-E4", "bass": "E2-C4"}

class Application(tk.Frame):
    
    #Application class, where the GUI magic happens
    def __init__(self, parent, *args, **kwargs):
        
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.guisongnum = 1
        self.grid()
        self.create_widgets()
        self.guisongdict = OrderedDict()

    def create_widgets(self):

        self.create_text()
        self.create_checks()
        self.create_labels()
        self.create_buttons()
        self.create_menus()

    def create_labels(self):

        self.musiclabel = tk.Label(self, text = "This is a simple music program. Please Enjoy.")
        self.musiclabel.grid(row = 0, column = 0, columnspan = 6, sticky = tk.W)

        self.musiclabel2 = tk.Label(self, text = "Number of notes for the song: ")
        self.musiclabel2.grid(row = 1, column = 0, columnspan = 2, sticky = tk.W)

        self.musiclabel3 = tk.Label(self, text = "Save location:")
        self.musiclabel3.grid(row = 6, column = 0, columnspan = 2, sticky = tk.W)

        self.musiclabel4 = tk.Label(self, text = ".txt")
        self.musiclabel4.grid(row = 6, column = 2, columnspan = 1, sticky = tk.W)

    def create_buttons(self):
                
        self.musicbutton1 = tk.Button(self)
        self.musicbutton1.grid(row = 7, column = 0, columnspan = 1, sticky = tk.W)
        self.musicbutton1.configure(text = "Save to file.")
        
        self.musicbutton2 = tk.Button(self)
        self.musicbutton2.grid(row = 1, column = 6, sticky = tk.W)
        self.musicbutton2.configure(text = "Submit")

        self.musicbutton4 = tk.Button(self)
        self.musicbutton4.grid(row = 7, column = 1, columnspan = 1, sticky = tk.W)
        self.musicbutton4.configure(text = "Play song.")

        self.musicbutton5 = tk.Button(self)
        self.musicbutton5.grid(row = 7, column = 2, sticky = tk.W)
        self.musicbutton5.configure(text = "Do everything.")
          
        #remember to change this value as needed (headache avoided)
        self.musicbutton1.configure(command = self.savetofile1)
        self.musicbutton2.configure(command = self.submit)
        self.musicbutton4.configure(command = self.playguisong)
        self.musicbutton5.configure(command = self.doeverything)
        
    def create_text(self):

        self.firstentry = tk.Entry(self)
        self.firstentry.grid(row = 1, column = 2, columnspan = 2, sticky = tk.W)

        self.savetofile = tk.Entry(self)
        self.savetofile.grid(row = 6, column = 1, columnspan = 1, sticky = tk.W)

        self.guisongspeed = tk.Entry(self)
        self.guisongspeed.grid(row = 1, column = 5, columnspan = 1, sticky = tk.W)

        self.display = tk.Text(self, width = 75, height = 15, wrap = tk.WORD)
        self.display.grid(row = 2, column = 0, columnspan = 7, sticky = tk.W)
        self.puttextinbox("This is where results will go. The console is more verbose for debugging.", "False")

    def create_checks(self):
        
        self.bool1 = tk.BooleanVar()
        self.bool2 = tk.BooleanVar()
        self.bool3 = tk.BooleanVar()
        """ 
        self.check1 = tk.Checkbutton(self)
        self.check1.configure(variable = self.bool1)
        self.check1.configure(command = self.submit)
        self.check1.grid(row = 4, column = 5, sticky = tk.S)
        """

    def create_menus(self):

        self.pitchmenusetting = tk.StringVar()
        self.pitchmenu = tk.OptionMenu(self, self.pitchmenusetting, "soprano", "mezzo-soprano", "alto", "tenor", "baritone", "bass")
        self.pitchmenu.grid(row = 1, column = 4, columnspan = 1, sticky = tk.W)
        self.pitchmenusetting.set("alto")
        
    def submit(self):

        textboxstuff = self.firstentry.get()
        menustuff = self.pitchmenusetting.get()
        speed = self.guisongspeed.get()

        if not speed:

            speed = "60"

        if textboxstuff:

            self.guisongdict[self.guisongnum]  = Song("guisong" + str(self.guisongnum), speed, menustuff, textboxstuff)

            self.guisongdictlist = list(self.guisongdict.items())
            self.guisongdictlist2 = self.guisongdictlist[-1]
            
            self.guisongdictlist2[1].add_notes()
            self.guisongnum += 1

            self.puttextinbox( "length: " + textboxstuff + "\n" + str(self.guisongdictlist2[1].print_songlist()), "False")
            
        else:

            print("No Number provided.")
            self.puttextinbox("No Number provided.", "False")

    def puttextinbox(self, putinbox, append):

        if append == "False":

            self.display.delete(0.0, tk.END)
            self.display.insert(0.0, putinbox)

        else:

            self.display.insert(0.0, putinbox)

    def savetofile1(self):

        savepath = askdirectory()
        filename = self.savetofile.get()
        self.guisongdictlist2[1].savesonglist(filename, savepath)

    def playguisong(self):
   
        playmodule.playsong(self.guisongdictlist2[1], 60)

    def doeverything(self):

        self.submit()
        self.savetofile1()
        self.playguisong()

#I am going to rewrite the program to work with tkinter with pack and pack-forget to hide elements (maybe a complete rewrite in node.js :P)

def GUI():

    #now enter can used to submit stuff
    def entersubmit(event = None):
    
        app.doeverything()
        
    #Creates GUI from the Application class.
    print("GUI started.")
    root = tk.Tk()
    root.title("Python Music Program")
    root.geometry("600x400")
    app = Application(root)
    #bind enter to submit
    root.bind('<Return>', entersubmit)
    
    #Run mainloop
    root.mainloop()

#some normal classes defined below

class Note(object):

    #This is used to create a note that will be put in a Music21 stream
    def __init__(self, name, letter, octave, sharp):

        self.name = name
        self.letter = letter
        self.octave = octave
        self.sharp = sharp

        if self.sharp == "True":
            
            temp = self.letter + "#" + self.octave

        else:

            temp = self.letter + self.octave

        self.music21note = music21.note.Note(temp)
        print("A new note has been created. " + str(self))
        
    def __str__(self):

        rep = self.music21note.fullName
        return rep

    def changeoctave(self, numofoct):

        try:

            self.octave = int(self.octave) + int(numofoct)
            self.octave = str(self.octave)

        except:

            input("Error type 5 occured: Please Debug")

    def changenote(self, newnote):

        if newnote in Note_list:

            self.letter = newnote

        else:

            input("An illegal note change was attempted and stopped. Notes can only be called something A-G.")

    def swapsharpstate(self):

        if self.sharp == "True":

            self.sharp = "False"

        elif self.sharp == "False":

            self.sharp = "True"

        else:

            input("A note sharp state swap was attempted but an issue occurred and as a preventive measure, was halted. You should debug this.")

class Song(object):

    #This is used to makes a groups of notes to create a song (or maybe just a single "voice" of a fugue)
    def __init__(self, name, speed, pitch, length):

        print("A new song has been created.")

        self.name = name
        self.speed = speed
        self.streamname = self.name + "music21stream"
        self.streamname = music21.stream.Stream()
        
        if pitch in Pitches:
            
            self.pitch = pitch
            self.noterange = Pitchdict[self.pitch]
            self.noterangelist = self.noterange.split("-")
            self.lownote = music21.note.Note(self.noterangelist[0])
            self.highnote = music21.note.Note(self.noterangelist[1])            
            print("Note range: " + str(self.noterangelist))

        else:

            self.pitch = "No pitch specified."

        self.length = length

    def __str__(self):

        rep = "song: "
        rep +=  "Name-" + str(self.name) + " " + "Speed-" + str(self.speed) + " " + "Pitch-" + str(self.pitch) + " " + "Length-" + str(self.length)
        return rep

    def add_notes(self):

        if self.pitch != "No pitch specified.":
            
            self.noterange = Pitchdict[self.pitch]
            self.noterangelist = self.noterange.split("-")
            self.lownote = music21.note.Note(self.noterangelist[0])
            self.highnote = music21.note.Note(self.noterangelist[1])
            print("Note range: " + str(self.noterangelist))
            i = 0
            while i < int(self.length):
                
                randomnote = random.choice(Note_list)
                randomoctave = random.choice(Octaves)
                randomsharp = random.randint(0,4)
                
                if randomsharp == 1:

                    issharp = "#"
                
                else:

                    issharp = ""

                tempnote = str(randomnote) + str(issharp) + str(randomoctave)
                tempmusic21note = music21.note.Note(tempnote)

                if tempmusic21note.pitch.frequency > self.lownote.pitch.frequency and tempmusic21note.pitch.frequency < self.highnote.pitch.frequency:

                    self.streamname.append(music21.note.Note(tempnote))            
                    i += 1

            for thisNote in self.streamname.notes:
                
                print("Music21 stream test: " + str(thisNote.fullName))
                            
            print("Notes added to song. Check testmusic.txt file for results.")
            self.savesonglist("testmusic", "default")

        else:

            print("Error with note ranges.")
        

    def print_songlist(self):
            
            rep = "song:\n"

            for thisNote in self.streamname.notes:
                
                rep += str(thisNote.fullName) + "\n"

            return rep

    def savesonglist(self, filename, path):

        if not path == "default":
        
            text_file_name = os.path.join(path, str(filename) + ".txt")

        else:

            text_file_name = os.path.join(globalsavepath, str(filename) + ".txt")

        text_file = open(text_file_name, "w")
        text_file.write("song: ")
        text_file.close()
        
        for thisNote in self.streamname.notes:
            
            text_file = open(text_file_name, "a")
            text_file.write(str(thisNote.pitch) + " - ")
            text_file.close()
            print("Song written to " + filename + ".txt")

    def append_notes(self, numofnotestoappend):

        if numofnotestoappend > 0:
            
            for i in range(numofnotestoappend):

                self.length += 1
        else:
            
            print("Error type 11: Appending note to song failed.")
    
    def transpose(self, semitones):

        badprogramming = "True"
        #if self.notedictionary:
        if badprogramming == "True":
            
            print("Transpose function used on song " + self.name + ". Transposed " + str(semitones) + " semitones.")        

    def changenotestolist(self, changelist):

        print("this should work")
    
class fugue(object):

    #Not even close to done
    def __init__(self, name, subjectsong, answers):

        print("A new fugue has been created.")
        self.name = name
        self.subjectsong = subjectsong
        self.answers = answers
        self.answercount = 0

    def __str__(self):

        rep = "Fugue: " + "Name- " + self.name + " " + "Subject- " + str(self.subjectsong)
        return rep

    def counterpoint(self):

        #idk what to do here so here is a print function that portrays my feelings :P
        print("Counterpoint is hard.")

    def createanswer(self, semitones):

        self.answer = Song("answer", self.subjectsong.speed, self.subjectsong.pitch, self.subjectsong.length)
        for thisNote in self.subjectsong.streamname:

            print("Note appended to answer.")
            self.answer.streamname.append(thisNote)

        print(self.answer.print_songlist())
        
    def createcountersubject(self):

        print("This program can't create a countersubject yet :(")
    
def main():
    
    #main function where everything happens.
    bach_test = input("Test bach_aof module? (y/n)")
    
    if bach_test != "n":
        
        print("Tesitng.....\n")
        bach_aof.miditest()
        print("Test successful")
        time.sleep(1)
    
    fuguesong1 = Song("fuguesong1", 60, "alto", 8)
    fuguesong1.add_notes()
    testfugue1 = fugue("testfugue1", fuguesong1, 1)
    testfugue1.createanswer(5)
    print(fuguesong1.print_songlist())    

    #Run GUI
    GUI()

    input("Press enter to exit.")

#Run main
main()

#This is the end for now
