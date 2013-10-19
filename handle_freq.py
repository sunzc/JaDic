#! /usr/bin/env python
# encoding: utf-8
import re
import sqlite3
debug_count = 0
conn = sqlite3.connect('test_jadic')
curs = conn.cursor()
with open('data/term_aggregates.txt') as f:
    for line in f:
        if re.match('.*未知語.*',line):
            continue
        fields = line.split()
        #print "full line: %s" % line,
        #for field in fields:
        #    print "#%s#" % field ,
        word = fields[1]
        freq = int(fields[0])
        #print("word : %s, freq : %d"%(word,freq))
        qycmd = 'select hanzi,meaning from wordtable where hanzi = ?'
        curs.execute(qycmd,[word.decode('utf-8')])
        row = curs.fetchone()
        if not row:
            continue
        else:
            hanzi,meaning = row
            #print("match one!row : %s, meaning: %s, freq: %d" % (hanzi.encode('utf-8'),meaning.encode('utf-8'),freq))
            qycmd = 'update wordtable set freq = ? where hanzi = ?'
            curs.execute(qycmd,[freq,hanzi])
        debug_count += 1

print("update : %d terms"%debug_count)
conn.commit()

if False:    
    qycmd = 'select hanzi,freq from wordtable where hanzi = ?'
    curs.execute(qycmd,[word.decode('utf-8')])
    row = curs.fetchone()
    n_hanzi,n_freq = row
    print("new value after updated: hanzi: %s, freq = %d"%( n_hanzi.encode('utf-8'),n_freq))
