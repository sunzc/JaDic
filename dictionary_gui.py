#! /usr/bin/env python
# Author: Sun Zhichuang(sunzc522@gmail.com)
# Date  : 2013/10/5
# Task:
#   Set up a GUI for the Japanese Electronic Dictionary.

from Tkinter import *
from dictionary_prototype import JED

class GUI_JED(Frame):
    def __init__(self, jed,parent=None, **options):
        Frame.__init__(self, parent, **options)
        self.pack()
        self.config(height=23,width=80)

        self.jed = jed

        rowLbl = Frame(self)
        titleLbl = Label(rowLbl,text='Sunzc\'s Japanese Dictionary',height=2,width=80)
        rowLbl.pack(side=TOP)
        titleLbl.config(bg='pink')
        titleLbl.config(font=('times',12,'bold'),fg='blue')
        titleLbl.pack(fill=X,expand=YES)
        
        row = Frame(self)
        self.entInput = Entry(row)
        btnSearch = Button(row, text='Search',command=self.search)
        row.pack(side=TOP, fill=X)
        row.config(height=1,width=80)
        self.entInput.pack(side=LEFT,expand=YES,fill=X) #grow horizontal
        btnSearch.pack(side=RIGHT)
        btnSearch.config(height=1,width=15,bg='light blue')
        btnSearch.config(font=('times',10,'bold'),fg='blue')
        self.entInput.bind('<Return>',(lambda event: self.search()))

        resultRow = Frame(self)
        self.resultVar = StringVar()
        resultMsg = Label(textvariable=self.resultVar)
        resultMsg.config(bg='light blue',height=20,width=80,justify=LEFT)
        resultRow.pack(side=TOP,fill=X,expand=YES)
        resultMsg.pack(fill=X,expand=YES)
    def search(self):
        word = self.entInput.get().strip()
        outputResult = self.jed.handleQuery(word.encode('utf-8'))
        self.resultVar.set(outputResult)

if __name__=='__main__':
    jed = JED('test_jadic')
    GUI_JED(jed).mainloop()
