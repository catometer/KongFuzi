"""KongFuzi: Version 2.0

This program is intended for Chinese language students.
It helps in compiling and memorizing the required vocabulary.

Copyright (C) 2018  Ani Vardanyan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See the GNU General Public License at <http://www.gnu.org/licenses/>. """

import random
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

ttl = "KongFuzi: Version 2.0"

#Storing the number of correct/wrong/incomplete answers to display as feedback by the end of the practice session
stats_counter = {"correct":0,"wrong":0,"incomplete":0,"partially wrong":0}

#Pinyin characters for chinese tonal sounds (values) and non-pinyin conventions (keys) to type them in within the program
tonals = {"a1":"ā","a2":"á","a3":"ǎ","a4":"à"
          ,"e1":"ē","e2":"é","e3":"ě","e4":"è"
          ,"i1":"ī","i2":"í","i3":"ǐ","i4":"ì"
          ,"o1":"ō","o2":"ó","o3":"ǒ","o4":"ò"
          ,"u1":"ū","u2":"ú","u3":"ǔ","u4":"ù"
          ,"v1":"ǖ","v2":"ǘ","v3":"ǚ","v4":"ǜ"
         }

#Feedback message options for users' answers 
fbdict = {"correct":['Correct!','Great job!','Keep it up!','Yes!']
          ,"wrong":['Wrong! Try again!','Oops!','Nope!']
          ,"incomplete":"Correct, but it has more meanings!"}

run = True

def mainmenu():
    startwindow = tk.Tk()
    startwindow.title(ttl)
    tk.Label(startwindow, text="Hello! KongFuzi is here to help you with your Chinese vocabulary of the day! Choose an option to continue.\n",wraplength=400,width=60).grid(row=0)
    b1_select = tk.Button (startwindow, text="Select a file", width=13, command=lambda:select(startwindow))
    b1_select.grid(row=1)
    b2_input = tk.Button (startwindow, text="Input vocabulary", width=16, command=lambda:vocinput(startwindow))
    b2_input.grid(row=2)
    tk.Label(startwindow,text="\n").grid(row=3)
    startwindow.mainloop()
    
def backtomain(vocabulary,previouswindow):
    if len(vocabulary) == 1:
        if vocabulary[0] != "input":
            yesno = mb.askquestion(ttl, "Do you want to save your current submissions?")
            if yesno == "yes":
                save(vocabulary)
                previouswindow.destroy()
                mainmenu()
            else:
                previouswindow.destroy()
                mainmenu()
        else:
            previouswindow.destroy()
            mainmenu()
    else:
        save(vocabulary)
        previouswindow.destroy()
        mainmenu()

def select(previous_window):
    fchoice = fd.askopenfilename(title="Select a vocabulary file:",defaultextension="txt")
    try:
        handler = open(fchoice,encoding="utf-8-sig")
    except: "do nothing!"
    else:
        vocab = []
        for line in handler:
            line = line.strip().split(' - ')
            vocab.append(line)
        test(vocab,previous_window)


def vocinput(previouswindow):
    vocab = ["input"]
    previouswindow.destroy()
    vocinpwin = tk.Tk()
    vocinpwin.title(ttl)
    subttl = tk.Label(text = "VOCABULARY INPUT",width=60)
    subttl.grid(row=0,column=0,columnspan=3)
    hanzi_request = tk.Label(text = "Hanzi: ")
    hanzi_request.grid(row=1,column=0,sticky="e")
    hanzi_entry = tk.Entry(vocinpwin)
    hanzi_entry.grid(row=1,column=1,stick="w")
    pinyin_request = tk.Label(text = "Pinyin: ")
    pinyin_request.grid(row=2,column=0,sticky="e")
    pinyin_entry = tk.Entry(vocinpwin)
    pinyin_entry.grid(row=2,column=1,sticky="w")
    pinyin_info = tk.Label(text = "Note: for tonal marks type 1, 2, 3 or 4 after the vowel.\nFor 'u' with umlaut type 'v' followed by the tone number.\nE.g. 'e3' for 'ě' or 'v2' for 'ǘ'.",justify="left")
    pinyin_info.grid(row=3,column=1,sticky="e")
    trans_request = tk.Label(text = "Meaning: ")
    trans_request.grid(row=4,column=0,sticky="e")
    trans_entry = tk.Entry(vocinpwin)
    trans_entry.grid(row=4,column=1,sticky="w")
    showvoc = tk.Text(vocinpwin)
    sbmitbtn = tk.Button(text = "Submit", command=lambda:lineappend(hanzi_entry,pinyin_entry,trans_entry,showvoc,vocab),width=16)
    sbmitbtn.grid(row=5,column=1,sticky="w")
    savebtn = tk.Button(text = "Save", command=lambda:save(vocab),width=16)
    savebtn.grid(row=5,column=2,sticky="e")
    testbtn = tk.Button(text = "Go to test",command=lambda:test(vocab,vocinpwin),width=16)
    testbtn.grid(row=1,column=2,sticky="e")
    backbtn = tk.Button(text = "Main Menu",width=16,command=lambda:backtomain(vocab,vocinpwin))
    backbtn.grid(row=2,column=2,sticky="e")
    showvoc.grid(row=10,column=0,columnspan=3)
    vocinpwin.mainloop()

#helper function for lineappend
def getfrom(lst):
    errormsg = 0
    line = []
    for i in lst:
        e = i.get().lower()
        e = e.strip()
        if e != "":
            if lst.index(i) == 1:
                tonals_added = e
                for key,val in tonals.items():
                    if key in e:
                        tonals_added = tonals_added.replace(key,val)
                line.append(tonals_added)
            else:
                line.append(e)
        else:
            if errormsg == 0:
                errormsg = 1
                mb.showinfo(ttl,"One or more fields are empty!")
    return line

def lineappend(eh,ep,et,textbox,vocabulary):
    rawline = [eh,ep,et]    
    extracted = getfrom(rawline)
    if len(extracted) == 3:
        vocabulary.append(extracted)
        for i in rawline:
            i.delete(0, tk.END)
    textbox.delete(0.0,tk.END)
    for finalline in vocabulary:
        if finalline != "input":
            finalline = str(finalline[0])+" - "+str(finalline[1])+" - "+str(finalline[2])+"\n"
            textbox.insert(tk.END,finalline)

def save(vocabulary):
    if vocabulary[0] == "input":
        if len(vocabulary) == 1:
            mb.showinfo(ttl,"You don't have any submissions!")
        else:
            del vocabulary[0]
            save(vocabulary)
    else:
        filename = fd.asksaveasfilename(title="Save",defaultextension="txt")
        try:
            vocabfile = open(filename,"w+",encoding="utf-8-sig")
        except:
            "do nothing!"
        else:
            for i in vocabulary:
                vocabfile.write(i[0]+" - "+i[1]+" - "+i[2]+"\n")
            vocabfile.close()

def test(vocabulary,previous_window):
    if vocabulary[0] == "input":
        if len(vocabulary) == 1:
            yesno = mb.askquestion(ttl, "You don't have any submissions. Do you want to exit?", default="no")
            if yesno == "yes":
                exit()
        else:
            yesno = mb.askquestion(ttl, "Do you want to save your current submissions?", default="yes")
            if yesno == "yes":
                del vocabulary[0]
                save(vocabulary)
                test(vocabulary,previous_window)
            else:
                del vocabulary[0]
                test(vocabulary,previous_window)
    else:
        previous_window.destroy()
        def testwindow(p_or_t,answer):
            global run
            run = True
            testwin = tk.Tk()
            testwin.title(ttl)
            subttl = tk.Label(text = "PRACTICE SESSION",width=60)
            subttl.pack()
            input_req_ttl = 'Enter the '+p_or_t+' for '+hanzi+': '
            input_req = tk.Label(text = input_req_ttl, width=50)
            input_req.pack()
            userinput = tk.Entry(testwin)
            userinput.pack()
            b1 = tk.Button(text = "Submit", command=lambda:_feedback(answer,userinput,testwin))
            b1.pack()
            b2 = tk.Button(text = "Hint", command=lambda:_hint(answer))
            b2.pack()
            b3 = tk.Button(text = "Exit", command=_exit)
            b3.pack()
            n1 = tk.Label(text = "\n")
            n1.pack()
            testwin.mainloop()
        while run:
            line = random.choice(vocabulary)
            hanzi = line[0].lower()
            pinyin = line[1].lower()
            trans = line[2].lower()
            type_pinyin = "PINYIN"
            type_trans = "TRANSLATION"
            testwindow(type_pinyin,pinyin)
            if run:
                testwindow(type_trans,trans)

def _hint(correct_a):
    word = list(correct_a)
    hint = "none"
    if correct_a.startswith('to be '):
        hint = "It starts with '(to be ) "+str(word[6])+"'"
    elif correct_a.startswith('to '):
        hint = "It starts with '(to) "+str(word[3])+"'"
    elif correct_a.startswith('a '):
        hint = "It starts with '(a) "+str(word[2])+"'"
    elif correct_a.startswith('an '):
        hint = "It starts with '(a) "+str(word[3])+"'"
    elif correct_a.startswith('the '):
        hint = "It starts with '(a) "+str(word[4])+"'"
    else:
        hint = "It starts with '"+str(word[0])+"'!"
    mb.showinfo(ttl,hint)

def _feedback(correct_a,user_a_entry,window):
    user_a_raw = user_a_entry.get().lower()
    user_a = user_a_raw
    for key,val in tonals.items():
        if key in user_a_raw:
            user_a = user_a.replace(key,val)
    if correct_a == user_a:
        feedback = random.choice(fbdict["correct"])
        stats_counter["correct"] += 1
    elif correct_a != user_a and "," in correct_a and "," in user_a:
        correct_a = correct_a.split(', ')  
        correct_a.sort()
        user_a = user_a.split(', ')
        user_a.sort()
        if correct_a == user_a:
            feedback = random.choice(fbdict["correct"])
            stats_counter["correct"] += 1
        else:
            truefalse = []
            for n in user_a:
                if n in correct_a:
                    value = "true"
                    truefalse.append(value)
                if n not in correct_a:
                    value = "false"
                    truefalse.append(value)
            if "false" in truefalse and "true" in truefalse:
                feedback = "One or several answers are wrong."
                stats_counter["partially wrong"] += 1
            elif "false" in truefalse:
                feedback = random.choice(fbdict["wrong"])
                stats_counter["wrong"] += 1
            else:
                feedback = str(fbdict["incomplete"])
                stats_counter["incomplete"] += 1
    elif correct_a != user_a and "," in correct_a:
        correct_a = correct_a.split(', ')
        if user_a in correct_a:
            feedback = str(fbdict["incomplete"])
            stats_counter["incomplete"] += 1
        else:
            feedback = random.choice(fbdict["wrong"])
            stats_counter["wrong"] += 1
    else:
        feedback = random.choice(fbdict["wrong"])
        stats_counter["wrong"] += 1
    finalfeedback = feedback+"\nYour answer: "+str(user_a)+"\nCorrect answer: "+str(correct_a)
    mb.showinfo(ttl,finalfeedback)
    user_a_entry.delete(0,tk.END)
    window.destroy()

#Function for displaying a message about the number of correct/wrong/incomplete answers by the end of the practice session 
def stats(dct):
    text = ""
    for key in dct:
        val = stats_counter.get(key)
        if val == 1:
            line = str(val)+" "+str(key)+" answer\n"
        else:
            line = str(val)+" "+str(key)+" answers\n"
        text = text+line
    return text

def _exit():
    global run
    run = False
    msg = stats(stats_counter)
    x = mb.showinfo(ttl,msg)
    if x == "ok":
        exit()

mainmenu()
