#! /usr/bin/python
# encoding: utf-8
# Author: sunzhichuang
# Date  : 2013/7/13

# this file is used to test the code in jadic.py
# Testing variable
TestingCrawler = 0 
TestingFileRead = 0 
TestingChnJp = 0
TestingReadXLS = 0
TestingWordProcessor = 0
TestingCorpusProcessor = 1

# subsequent to TestingWordProcessor
TestGetHanzi = 0 
TestGetHiragana = 0
TestGetWordType = 0 
TestGetWordMeaning = 0
TestGetWordStem = 0
TestGetWordTail = 0
TestConnectDatabase = 0 # implict open TestCreateWordTable & TestProcessWordlist = 1
TestFetchResults = 0

# subsequent to TestingCOrpusProcessor
TestSplitCorpus = 0
TestCalculateSentenceScore = 0
TestCreateSentenceTable = 0 
TestCreateWord2SentenceTable = 0
TestStoreSentenceToDatabase = 0
TestLinkWord2Sentence = 0
TestIndexSentence = 0 
TestIndexAllSentence = 1 

if TestingCorpusProcessor == 1:
    from jadic import CorpusProcessor
    sourceFile = "data/Norway_s_wood.txt"
    dbname = 'test_jadic'
    cp = CorpusProcessor(sourceFile,dbname)
    if TestSplitCorpus == 1:
        senlist = cp.splitCorpus()
        print("first sentence : %s"%senlist[0].encode('utf-8'))

    if TestCalculateSentenceScore == 1:
        wordFreqList = [2,8,95,200,750,1250,6000,11000]
        score = cp.calculateSentenceScore(wordFreqList)
        print "score : %d " % score
    if TestCreateSentenceTable == 1:
        cp.createSentenceTable()
    if TestCreateWord2SentenceTable == 1:
        cp.createWord2SentenceTable()
    
    if TestStoreSentenceToDatabase == 1:
        s_id = 0
        sentence = '私は学生です。'
        score = 21
        cp.storeSentenceToDatabase(s_id,sentence.decode('utf-8'),score)
    if TestLinkWord2Sentence == 1 :
        wordlist = [1,3,5]
        sentenceId = 1
        cp.linkWord2Sentence(wordlist,sentenceId)
    if TestIndexSentence == 1:
        sentence = u'私は学生です。'
        cp.indexSentence(sentence)
    if TestIndexAllSentence == 1:
        cp.indexAllSentences()

# Testing Crawler
if TestingCrawler == 1 :
    from jadic import NewsCrawler 
    crawler = NewsCrawler('http:\\www.baidu.com','data/onlineData/')
    crawler.crawler()
    crawler.show()

if TestingFileRead == 1:
    path = r'./data/term_aggregates.txt'
    filehandler = open(path)
    lines = filehandler.readlines()
    num = 1
    for line in lines:
        if num < 10:
            num += 1
            print(line.strip())

if TestingChnJp == 1:
    print('中文和日本語')

if TestingWordProcessor == 1:
    from jadic import WordProcessor
    wp = WordProcessor()
    wordlist = wp.handleXLS('data/wordlist.xls')
    #word = wordlist[0]
    #print(word)
    wordtypelist = []
    dbname = "test_jadic"
    print("length = %d "%len(wordlist))
    if TestConnectDatabase == 1:
        conn = wp.connectDatabase(dbname)
        wp.createWordTable(conn)
        wp.processWordlist(wordlist,conn)
        conn.close()
        
    if TestFetchResults == 1:
        conn = wp.connectDatabase(dbname)
        curs = conn.cursor()
        curs.execute('select * from wordtable')
        for (wordid,hanzi,hiragana,meaning,stem,tail,wordtype,freq) in curs.fetchall():
            print("%d , %s,%s,%s,%s,%s,%s, %d"%(wordid,hanzi.encode('utf-8'),hiragana.encode('utf-8'),meaning.encode('utf-8'),stem.encode('utf-8'),tail.encode('utf-8'),wordtype.encode('utf-8'),freq))
        conn.close()
         
    for word in wordlist:
        if TestGetHanzi==1 :
            hanzi = wp.getHanzi(word)
            if hanzi == "error":
                continue 
            else:
                print(hanzi.encode('utf-8'))
        if TestGetHiragana==1 :
            hiragana = wp.getHiragana(word)
            if hiragana == "error":
                continue 
            else:
                print(hiragana.encode('utf-8'))
        if TestGetWordType==1 :
            wordtype = wp.getWordType(word)
            if wordtype == "error":
                continue 
            else:
                if wordtype not in wordtypelist:
                    wordtypelist.append(wordtype)
                print(wordtype.encode('utf-8'))
        if TestGetWordMeaning==1 :
            meaning = wp.getWordMeaning(word)
            if meaning == "error":
                continue 
            else:
                print(meaning.encode('utf-8'))
        if TestGetWordStem == 1:
            wordstem = wp.getWordStem(word)
            hanzi = wp.getHanzi(word)
            if wordstem != hanzi:
                print("word :%s, stem : %s"% (word.encode('utf-8'),wordstem.encode('utf-8')))
        if TestGetWordTail == 1:
            wordtail = wp.getWordTail(word)
            if wordtail != "":
                print("word :%s, tail : %s"% (word.encode('utf-8'),wordtail.encode('utf-8')))

            
    if TestGetWordType == 1:    
        print("wordtypelist:")
        for wordtype in wordtypelist:
            print(wordtype.encode('utf-8'))

