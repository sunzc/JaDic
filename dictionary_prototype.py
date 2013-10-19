#! /usr/bin/env python
# encoding: utf-8
# Author: Sun Zhichuang(sunzc522@gmail.com)
# Date  : 2013/10/4
# Task:
#   realize a simple Japanese Electric Dictionary based on the database setup by jadic.py

import sqlite3
import re
class JED:
    def __init__(self, dbname):
        self.conn = sqlite3.connect(dbname)
        self.curs = self.conn.cursor()
    def queryEntry(self):
        word = 'start'
        while True:
            word = raw_input('jed > ')
            if re.match('^end.*',word):
                print("Good Bye!")
                break
            print(self.handleQuery(word))

    def handleQuery(self,word):
        self.curs.execute('select wordid, hiragana, wordtype, meaning from wordtable where hanzi = ?',[word.decode('utf-8')])
        row = self.curs.fetchone()
        outputResult=""
        if not row :
            outputResult=word.decode('utf-8') + " is not found!"
            return outputResult 
        wordid,hiragana,wordtype,meaning = row
        outputResult += word.strip() + " " +"[" + hiragana.strip().encode('utf-8') + "]"+"  "+ "【" + wordtype.strip().encode('utf-8') + "】"+"\n"
        outputResult += "解释： "+meaning.strip().encode('utf-8')+"\n"
        
        self.curs.execute('select * from word2sentencetable where w_id = ?',[wordid])
        sentenceList = self.getOrderedSentenceList(wordid)
        if len(sentenceList) == 0:
           return outputResult 
        outputResult += "Sample Sentences: \n"
        s_id = 1
        for sentence in sentenceList:
            if s_id >3:
                break
            newSentence = self.reconstructSentence(sentence)
            outputResult += str(s_id) + ". " + newSentence.strip().encode('utf-8')  + "。\n"
            s_id += 1
        return outputResult
        
    def getOrderedSentenceList(self,wordid):
        curs = self.conn.cursor()
        curs.execute('select * from word2sentencetable where w_id = ?',[wordid])
        rows = curs.fetchall()
        sIdList = []
        for row in rows:
            w_id,s_id = row
            sIdList.append(s_id)
        sentenceScoreList = []
        for sid in sIdList:
            curs.execute('select sentence,score from sentencetable where s_id = ?',[sid])
            row = curs.fetchone()
            (sentence,score)=row
            # print("sentence : %s , score : %d" %( sentence,score))
            sentenceScoreList.append((sentence,score))
        
        newSentenceScoreList = sorted(sentenceScoreList,key = lambda sentencescore: sentencescore[1])
        return [ss[0] for ss in newSentenceScoreList]
    def reconstructSentence(self,sentence):
        length = len(sentence)
        print("sentence : %s length: %d"% (sentence,length))
        j = length/35
        if j==0:
            return sentence
        newSentence = ""
        for i in range(j+1):
            end = min(i*35+35,length)
            newSentence += sentence[i*35:end]+u'\n'
        return newSentence
               
if __name__ == '__main__':
    jed = JED('test_jadic')
    jed.queryEntry()


        



