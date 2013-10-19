#! /usr/bin/env python
# encoding: utf-8
# Author: sunzhichuang(sunzc522@gmail.com)
# Date  : 2013/10/3
# Task:
#     realize a japanese word segmentation program, which 
# can divide a sentence into a list of japanese words.
import sqlite3

class WordSeg:
    def __init__(self,corpse,dicDatabaseConn,wordlist,SCOPE=10):
        self.corpse = corpse
        self.conn = dicDatabaseConn
        self.wordlist = wordlist
        self.SCOPE = 10 # the length limit we scan the sentence for each word

    def cutIntoSentence(self):
        return self.corpse.split(u'。')

    def wordSeg(self):
        sentenceList = self.cutIntoSentence()
        wordResult = []
        wordidResult = []
        freqResult = []
        for sen in sentenceList:
            print("[in wordSeg] sentence is : %s" % sen)
            wordList,wordidList,freqList = self.wordSegSentence(sen)
            wordResult += wordList
            wordidResult += wordidList
            freqResult += freqList
        print("=========Program for simple wordseg task========")
        print("corpse : \n %s " % self.corpse)
        print("word Result: ")
        for word in wordResult:
            print("%s" % word)
        print("wordid Result: ")
        for wordid in wordidResult:
            print("%d" % wordid)
        print("word freq  Result: ")
        for freq in freqResult:
            print("%d" % freq)

    def wordSegSentence(self,sentence):
        sentenceLength = len(sentence)
        print("[in wordSegSentence]sentence is %s , length = %d" % (sentence, sentenceLength))
        start = 0
        regonizedWordList = []
        wordidList = []
        freqList = []
        while start < sentenceLength: 
            # scan start point should within the sentence length

            maxWordLength = 0
            for i in range(1,self.SCOPE+1):
                if (start + i) <= sentenceLength:
                    word = sentence[start:start + i]
                    if self.isJapaneseWord(word) or self.isCharNumString(word):
                        maxWordLength = i
                    else:
                        continue # if not a word, check a longer one
                else:
                    break # will only break for circle

            if maxWordLength == 0: # nothing regonized,step one letter down
                maxWordLength = 1

            word = sentence[start: start + maxWordLength]
            if self.isEntity(word):
                # if match something, then do the index work here
                wordid,freq = self.queryTheDatabase(word)
                wordidList.append(wordid)
                freqList.append(freq)
            
            regonizedWordList.append(sentence[start:start + maxWordLength])
            start = start + maxWordLength
        print("[in wordSegSentence] result is :")
        for word in regonizedWordList:
            print("%s" % word)
        return regonizedWordList,wordidList,freqList

    def isJapaneseWord(self,word):
        if self.isParticle(word) or self.isEntity(word):
            return True
    def isCharNumString(self,word):
        for i in range(len(word)):
            if word[i].encode('utf-8').isdigit() or word[i].encode('utf-8').isalpha():
                continue
            else:
                return False
        return True

    def isParticle(self,word):
        particleList = [u'は',u'よ',u'と',u'に',u'の',u'で',u'を',u'て',u'が',u'か']
        punctuationList = [u'、',u'？',u'「',u'」']
        if word in particleList or word in punctuationList:
            return True
        else:
            return False

    def isEntity(self,word):
        if self.queryTheDatabase(word):
            return True
        else:
            return False

    def queryTheDatabase(self,word):
        curs = self.conn.cursor()
        curs.execute('select wordid,freq from wordtable where stem = ?',[word])
        row = curs.fetchone()
        return row

if __name__ == '__main__':
    corpse = u"私は学生です。私の名前はZC Sunzc522 です。あなたは学生ですか。はい、そうです。いいえ、\
学生ではありません。"
    wordlist = ['私','学生','あなた','です','はい','そう','いいえ','ありません']
    wordlistUnicode = []

    for word in wordlist:
        wordlistUnicode.append(word.decode('utf-8'))
    conn = sqlite3.connect('test_jadic')
    wordseg = WordSeg(corpse,conn,None)
    wordseg.wordSeg() 

