#! usr/bin/python
# test jp wordseg
# author: sunzhichuang
# date  : 2013/8/15

corpus = open("data/Norway_s_wood.txt").read()
slist = self.corpus.decode('utf-8').split('。'.decode('utf-8'))

def checkDic(word,conn):
    curs = conn.cursor()
    curs.execute('select wordid,hanzi, wordtype from wordtable where stem = ?',[word])
    row = curs.fetchone()
    if not row:
        wordid = -1
        wordtype = ""
        return wordid,wordtype
    else:
        (wordid,wordtype) = row
        return wordid,hanzi,wordtype

def isVerbStem(wordtype):
    verblist = ['自','他','五','下一','サ']
    if wordtype in verblist:
        return True
    else:
        return False

def isAdjStem(wordtype):
    adjlist = ['形容']
    if wordtype in adjlist:
        return True
    else:
        return False

def isAdjVerbStem(wordtype):
    adjverblist = ['形动','副.形动']
    if wordtype in adjverblist:
        return True
    else:
        return False

def isFirstcolVerb(hanzi):
    i_col = ['い','き','し','ち','に','ひ','み','り','ぎ','じ','ぢ','び','ぴ']
    e_col = ['え','け','せ','て','ね','へ','め','れ','げ','ぜ','で','べ','ぺ']
    ie_col = i_col + e_col
    spFifthcolVerb = ['帰る','入る','知る','切る','走る','茂る','入る','張り切る','喋る','要る','握る','参る']
    if hanzi.encode('utf-8') in spFifthcolVerb:
        return False
    elif hanzi[-2].encode('utf-8') in ie_col and hanzi[-1].encode('utf-8') in ['る']:
        return True
    else:
        return False

def isSaBianVerb(hanzi):
    if hanzi[-2:].encode('utf-8') in ['する']:
        return True
    else:
        return False

def isKaBianVerb(hanzi):
    if hanzi.encode('utf-8') in ['来る']:
        return True
    else:
        return False


def matchVerbTail(sentence, start, L,hanzi):
    scope = min(10,L-start)
    matched = 0
    verbTail = []
    if  isFirstcolVerb(hanzi):
        # first col verb, list verbTail
        verbTail = ['て','ぬ','な','ない','せる','させる','られる','た','ます','ました','ません','る','れ','よ','ろ','う','よう'] 
    elif isSaBianVerb(hanzi):
        # 　サ变动词
        verbTail = ['する','しぬ','しない','しな','しろ','せよ','される','できる','して','した','します','しました','しう','しよう','すれ','しません']
    elif isKaBianVerb(hanzi):
        # カ变动词 needs special care, we regolize KaBianVerb in isParticle(),
        # for it is not very normal
        verbTail = ['れ']
    else:
        # the rest is taken as fifthcol verb 
        verbTail = ['れ','','','','','','','','','','','','','','','','','','','']
        tail = hanzi[-1].encode('utf-8')
        taillist = ['う','く','す','つ','ぬ','ふ','む','ゆ','る','ぐ','ず','づ','ぶ',
                    'ぷ',]
        if tail in ['う']:
            verbTail = ['って','わぬ','わな','わない','われる','える','いた','います','いました','え','おう','およう']
        elif tail in ['く']:
            verbTail = ['って','かぬ','かな','かない','かれる','ける','けた','きます','きました','け','かう','かよう']
        elif tail in ['す']:
            verbTail = ['して','さぬ','さな','さない','される','しる','した','します','しました','','かう','かよう']
        elif tail in ['く']:
            verbTail = ['って','かぬ','かな','かない','かれる','きる','きた','きます','きました','け','かう','かよう']
        elif tail in ['く']:
            verbTail = ['って','かぬ','かな','かない','かれる','きる','きた','きます','きました','け','かう','かよう']
        elif tail in ['く']:
            verbTail = ['って','かぬ','かな','かない','かれる','きる','きた','きます','きました','け','かう','かよう']
        elif tail in ['く']:
            verbTail = ['って','かぬ','かな','かない','かれる','きる','きた','きます','きました','け','かう','かよう']
        elif tail in ['く']:
            verbTail = ['って','かぬ','かな','かない','かれる','きる','きた','きます','きました','け','かう','かよう']
        elif tail in ['く']:
            verbTail = ['って','かぬ','かな','かない','かれる','きる','きた','きます','きました','け','かう','かよう']
        elif tail in ['く']:
            verbTail = ['って','かぬ','かな','かない','かれる','きる','きた','きます','きました','け','かう','かよう']
        elif tail in ['く']:
            verbTail = ['って','かぬ','かな','かない','かれる','きる','きた','きます','きました','け','かう','かよう']
        elif tail in ['く']:
            verbTail = ['って','かぬ','かな','かない','かれる','きる','きた','きます','きました','け','かう','かよう']
        elif tail in ['く']:
            verbTail = ['って','かぬ','かな','かない','かれる','きる','きた','きます','きました','け','かう','かよう']
            
    for i in range(1,scope):
        word = sentence[start:start + i]
        if word in verbTail:
            matched = i  

def matchAdjTail(sentence, start, L):
    scope = min(10,L-start)
    matched = 0
    adjTail = []
    for i in range(1,scope):
        word = sentence[start:start + i]
        if word in adjTail:
            matched = i  

def matchAdjVerbTail(sentence, start, L):
    scope = min(10,L-start)
    matched = 0
    adjVerbTail = []
    for i in range(1,scope):
        word = sentence[start:start + i]
        if word in adjVerbTail:
            matched = i  

def isParticle(word):
    # guess particle may refer to words like 'is', 'of' ,'a' in english, in japanese,
    # may refer to              
    particleList=['は','よ','と','に','の','で','を','て','が','では']
    if word in particleList:
        return True
    else:
        return False

def wordseg(sentence,conn,SCOPE):
    # algorithm: 1. scan the sentence from start to start+SCOPE, find the longest matched word
    #            2. redo first step until reach the end
    L = len(sentence)
    start = 0
    regonized = []
    regonizedWordid = []
    while start < L :
        lenArray = [0]*SCOPE
        flag = -1 
        longest = 0
        wordid = -1
        twordid = -1
        for i in range(1,SCOPE+1):
            twordid = -1
            if start + i <= L:
                word = sentence[start:start+i]
                twordid,hanzi,wordtype = checkDic(word,conn)
                if  twordid != -1:
                    # we find the word in database's wordtable
                    if isVerbStem(wordtype) :
                        tailLen = matchVerbTail(sentence,start+i,L,hanzi)
                    elif isAdjStem(wordtype) :
                        tailLen = matchAdjTail(sentence,start+i,L)
                    elif isAdjVerbStem(wordtype) :
                        tailLen = matchAdjVerbTail(sentence,start+i,L)
                    else:
                        tailLen = 0

                elif isParticle(word):
                    # it seems it's a particle word, so it has no tail
                    tailLen = 0
                else:
                    # it find no match words, so skip it
                    continue

                # we update the length here uniformally
                lenArray[i-1] = i + tailLen
                if i+tailLen > bigest:
                    longest = i + tailLen
                    flag = i
                    wordid = twordid

        # add newly regonized word and update start position
        if flag == -1:
            # no word matched, we take one step further
            regonized.append(sentence[start:start+1])
            start = start + 1
        else:
            length = lenArray[flag-1]
            regonized.append(sentence[start:start+length])
            start = start + length
        regonizedwordid.append(wordid)
