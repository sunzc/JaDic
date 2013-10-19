#!/usr/bin/python
# encoding: utf-8
# Author: sunzhichuang@mprc.pku.edu.cn
# Date  : 2013/7/4

# Task:
#    This task aims at building a japanese dictionary. 
#    Basic functions include:
#       1. type in a new japanese word, it returns its meanning ;
#       2. some related sample sentences are returned too;

# What we expect the program to do ?
#
# For new words processing part we have:
#
#    a. process the wordlist,extract the word, hiragana, word type,
#       meanning;
#    b. store the words in database,in the follow format:
#       +--------+------+----------+------+----------+-------+------+------+
#       | wordid | hanzi| hiragana | type | meaning  | freq  | stem | tail |
#       +----------------------------------------------------+------+------+
#       | Int    | Str  | Str      | Str  | Str      | int   | Str  | Str  |
#       +----------------------------------------------------+------+------+
#       | 4 B    | 60   | 60       | 10   | 120      | 4     | 60   |  3   |
#       +----------------------------------------------------+------+------+
#       NOTE: 1. hiragana: stores the stem of verbs,adjs,adj-verbs;
#             2. head: store the word stem ;
#             3. tail: stores the last hiragana;
#             4. freq: stores the difficulty degree ,which is assoicated 
#                with the word frequency;
#             5. type: store whether it's a verb,non, or adj,adv
#    c. scan the word frequency list, fill the word's level field;
#       well , how translate word frequency into level is quite three-pipe
#       problem, it needs careful design. we want it can be used to reflect
#       the sentence's quality.

# For corpus processing part :
#
#   a. divide paragraph into sentences by period;
#   b. stores a full sentence into database;
#   c. set up inverse index in unit of sentence; 
#      for example: wordid sentenceid
#   
#   However, we separate corpus by their source, assign them different importance
#   eg. 1. most important, sentences from text book & class ;
#       2. second important, those from <Nuowei De Senlin> my favourite novel;
#       3. third important, those from Internet articles;
#       4. fourth important, those from Twitter;

# Algorithm:
#   a. Wordlist processing is easy;
#   b. Japanese Word Segmentation is the most challenging part, we can develop
#      a simple version, and then complete it;
#   c. Graph User Interface put off to tomorrow;, we first develop a pure text 
#      version;
#   d. Gather corpus from Internet, we need a crawler;
#   e. In order to support retrieval, we need set up inverse index for sentences;
#   f. We need interface to access database;

import xlrd
import sqlite3
import re
class WordProcessor:
    # this class handles word processing part
    # it deals with word-meaning lists, extract info fields to fill the database
    # it needs to connect to a database
    def handleXLS(self,filename):
        # read a XLS file, store the record one by one into a list
        # return a wordlist
        # TODO
        data = xlrd.open_workbook(filename)
        sheet0 = data.sheets()[0]
        col0 = sheet0.col_values(0)
        return col0 

    def connectDatabase(self,databaseName):
        # connect to a database
        # return the connector
        # TODO
        conn = sqlite3.connect(databaseName)
        return conn

    def createWordTable(self,conn):
        # create table for storing words
        # TODO
        curs = conn.cursor()
        tbcmd = 'create table wordtable (wordid int(4),hanzi char(80),\
                hiragana char (80), meaning char(150),stem char(80), \
                tail char(3),wordtype char(10),freq int(4))'
        curs.execute(tbcmd)
        conn.commit()

    def processWordlist(self,wordlist,conn):
        # get a wordlist, return a recordlist
        # analysis the term, extract structural info to fill a record
        # TODO
        curs = conn.cursor()
        num = 1
        for word in wordlist:
            # filter those term with '?',which are misleading
            if re.match(".*\?.*",word):
                print("meaningless word term: %s"% word.encode('utf-8'))
                continue
            wordid = num
            num += 1
            hanzi = self.getHanzi(word)
            hiragana = self.getHiragana(word)
            wordtype = self.getWordType(word)
            meaning = self.getWordMeaning(word)
            stem = self.getWordStem(word)
            tail = self.getWordTail(word)
            freq = 1
            curs.execute('insert into wordtable values(?,?,?,?,?,?,?,?)',\
            (wordid,hanzi,hiragana,meaning,stem,tail,wordtype,freq))
        conn.commit()

    def getHanzi(self,wordTerm):
        # extract the Hanzi part of a wordTerm
        # TODO
        matchobj = re.match('(.*)\【',wordTerm.encode('utf-8'))
        if matchobj == None:
            print('first match is None,word = %s' % wordTerm.encode('utf-8'))
            matchobj = re.match('(.*)\[',wordTerm)
            if matchobj != None:
                hanzi = matchobj.group(1)
            else :
                hanzi = "error"
                print('extract hanzi error! word= %s' % wordTerm.encode('utf-8'))
            return hanzi
        else:
            hanzi = matchobj.group(1)
            return hanzi.decode('utf-8')

    def getHiragana(self,wordTerm):
        # extract the hiragana part of a wordTerm, 
        # this part may be missing
        # TODO
        matchobj = re.match('.*\【(.*)\】',wordTerm.encode('utf-8'))
        if matchobj == None:
            print('first match is None word = %s'%wordTerm.encode('utf-8'))
            matchobj = re.match('(.*)\[',wordTerm)
            if matchobj != None:
                hiragana = matchobj.group(1)
            else :
                hiragana = "error"
                print('extract hiragana error! word= %s' % wordTerm.encode('utf-8'))
            return hiragana
        else:
            hiragana = matchobj.group(1)
            return hiragana.decode('utf-8')

    def getWordType(self,wordTerm):
        # TODO
        matchobj = re.match('.*\[(.*)\]',wordTerm)
        if matchobj == None:
            print('no wordtype given word = %s ' % wordTerm.encode('utf-8'))
            wordtype = "error"
            return wordtype
        else:
            wordtype = matchobj.group(1)
            return wordtype
        
    def getWordMeaning(self,wordTerm):
        # TODO
        matchobj = re.match('.*\](.*)',wordTerm)
        if matchobj == None:
            print("no wordMeaning given word = %s" % wordTerm.encode('utf-8'))
            wordmeaning = "error"
            return wordmeaning
        else:
            wordmeaning = matchobj.group(1)
            return wordmeaning
        
    def getWordStem(self,wordTerm):
        # TODO
        """
wordtype list:
名
自
副
形动
他
感
词组
接续
后缀
外
前缀
连体
形容
量
代
副助
五
数
副.形动
其它
下一
サ
终助
"""
        # sometimes the typemark is not accurate, so we have  to check it.
        # we extract word stem for word segmentation, a coarse cut is enough!
        wordtype = self.getWordType(wordTerm)
        hiragana = self.getHiragana(wordTerm)
        hanzi = self.getHanzi(wordTerm)
        verblist = ['自','他','五','下一','サ']
        adjlist = ['形容']
        adjverblist = ['形动','副.形动']
        wordtype = wordtype.encode('utf-8')
        if wordtype in verblist :
            if hiragana[-2:].encode('utf-8') in ['する']:
                print('match する, word = %s'%wordTerm.encode('utf-8'))
                wordstem = hanzi[:-2]
            else:
                wordstem = hanzi[:-1]
        elif wordtype in adjlist :
            wordstem = hanzi[:-1]
        else:
            wordstem = hanzi

        return wordstem

    def getWordTail(self,wordTerm):
        # NOTE:only verb,adj,adj-verb have word tail
        # TODO
        wordtype = self.getWordType(wordTerm)
        hiragana = self.getHiragana(wordTerm)
        hanzi = self.getHanzi(wordTerm)
        verblist = ['自','他','五','下一','サ']
        adjlist = ['形容']
        adjverblist = ['形动','副.形动']
        wordtype = wordtype.encode('utf-8')
        if wordtype in verblist:
            wordtail = hiragana[-1]
        elif wordtype in adjlist:
            wordtail = hiragana[-1]
        elif wordtype in adjverblist:
            wordtail = "だ".decode('utf-8')
        else:
            wordtail = ""

        return wordtail

from wordseg_prototype import WordSeg
class CorpusProcessor :
    # the common part of corpus processing, including dividing articles into 
    # sentences, the sentences will then be indexed by the words it contains.
    # we will set up database for storing sentences here.
    def __init__(self,source,dbname):
        # the content for processing, a piece of raw text with several sentences.
        # source indicates where this corpus comes from.
        corpus = open(source).read()
        self.corpus = corpus
        self.conn = sqlite3.connect(dbname)
        self.wordseg = WordSeg(self.corpus,self.conn,None)
        self.sentenceId = 0

    def splitCorpus(self):
        # split corpus into sentences
        # return sentences list
        # TODO
        slist = self.corpus.decode('utf-8').split('。'.decode('utf-8'))
        return slist
        
    def calculateSentenceScore(self,wordFreqList):
        # calculate the difficulty degree of a sentence
        # it gets a wordlist of a sentence, return its score
        # TODO needs careful design
        scoreTotal = 0
        for freq in wordFreqList:
            scoreTotal += self.freqToScore(freq)
        scoreAvg = scoreTotal/len(wordFreqList)
        return scoreAvg

    def freqToScore(self,freq):
        score = 1
        if freq < 5 :
            score = 1
        elif freq <10 :
            score = 2
        elif freq <100:
            score = 4
        elif freq <500:
            score = 8
        elif freq <1000:
            score = 16
        elif freq <5000:
            score = 32
        elif freq <10000:
            score = 48
        else:
            score = 60
        return score

    def indexAllSentences(self):
        slist = self.splitCorpus()
        for sentence in slist:
            self.indexSentence(sentence)

    def indexSentence(self,sentence):
        # handle all the  sentence in the sentenceList;
        # it calls the wordSegmentation() function
        # TODO
        sentenceLength =  len(sentence.encode('utf-8'))
        if sentenceLength > 240 or sentenceLength < 15: 
            # sentence too long or too short is ignored!
            return None
        self.sentenceId += 1
        wordList,wordidList,freqList = self.wordseg.wordSegSentence(sentence)
        score = self.calculateSentenceScore(freqList)
        self.storeSentenceToDatabase(self.sentenceId,sentence,score)
        self.linkWord2Sentence(wordidList,self.sentenceId)
         

    def linkWord2Sentence(self,wordidList,sentenceId):
        curs = self.conn.cursor()
        tbcmd = 'insert into word2sentencetable values(?,?)'
        for wordid in wordidList:
            curs.execute(tbcmd,(wordid,sentenceId))
        self.conn.commit()
            
    def storeSentenceToDatabase(self,s_id,sentence,score):
        curs = self.conn.cursor()
        tbcmd = 'insert into sentencetable values(?,?,?)'
        curs.execute(tbcmd,(s_id,sentence,score))
        self.conn.commit()

    def createSentenceTable(self):
        curs = self.conn.cursor()
        tbcmd = 'create table sentencetable (s_id int(4),sentence char(240), \
        score int(4))'
        # a sentence too long is not a good sentence to be shown for newbies
        # so we set the length limit to less than 80 words,that is 240 chars
        curs.execute(tbcmd)
        self.conn.commit()

    def createWord2SentenceTable(self):
        curs = self.conn.cursor()
        tbcmd = 'create table word2sentencetable (w_id int(4),s_id int(4))'
        # a sentence too long is not a good sentence to be shown for newbies
        # so we set the length limit to less than 80 words,that is 240 chars
        curs.execute(tbcmd)
        self.conn.commit()


class TextBookCorpus(CorpusProcessor):
    # this class handles corpus from text book, in our design, each article
    # is stored in a file named by the number.
    # we scan every articles and call the CorpusProcessor to processing it. 
    def scanTextBook(self,pathname):
        # scan every file in the pathname/
        # processing them one by one
        # TODO
        pass
    def splitTextBook(self,textContent):
        # sometimes we need to separate whether a sentence comes from
        # the text article, grammer, exercise ,translating part
        # this function split the textContent,which is organised in a certain 
        # format, into several parts due to the position they lay.
        # TODO
        pass

class OnlineNewsCorpus(CorpusProcessor):
    # this class handles corpus from online news website, a crawler is
    # responsible for grabbing data from the Internet, and then store 
    # them into a certain directory, each file is named after the website name
    # TODO
    def scanOnlineNews(self,pathname):
        # the same with scanTextBook()
        # I don't know why I not merge it with its father class
        # TODO
        pass

class TwitterCorpus(CorpusProcessor):
    # this class handles corpus from twitter, a crawler is needed to collect
    # perple's japanese tweet and store them by the author's name in separate
    # files
    def scanTwitter(self,pathname):
        # TODO
        pass

class NorwaysWoodCorpus(CorpusProcessor):
    # this class handles corpus from the novel Norway's Wood, my favourate novel
    # we split it into several chapters
    def splitNovel(self,text,pathname):
        # split Novel into several chapters and store them into each file
        # in the given pathname
        # TODO
        pass
    def scanChapters(self,pathname):
        # TODO
        pass

import urllib2
from BeautifulSoup import BeautifulSoup
import re
class NewsCrawler:
    # a crawler that grab news from given japanese news website
    # the seedURL is the startpoint for the crawler, content will be stored in
    # the path/
    def __init__(self,seed,path,depth=3):
        self.seedURL = seed
        self.storePath = path
        self.depth=depth
    
    def crawler(self):
        # TODO
        pages = [self.seedURL]
        for i in range(self.depth):
            for page in pages:
                try:
                    webpage = urllib2.urlopen(page)
                except:
                    print "Could not open %s "% page
                    continue
                soup = BeautifulSoup(webpage.read())
                self.extractContent(page,soup)

                links
            webpage = urllib2.urlopen(self.seedURL)
            soup = BeautifulSoup(webpage.read())
            print(soup('a'))
        pass
    def show(self):
        print("seedURL = %s, storePath = %s"%(self.seedURL,self.storePath))
    def extractContent(self,page,soup):
        # extract the news body ,otherwise disert it
        # TODO
        pass
