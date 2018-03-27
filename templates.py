#!/usr/bin/python
# -*- coding: utf-8 -*-
import wikipedia
import nltk
import string
from nltk.tokenize import sent_tokenize,word_tokenize
import re
from tr import textrank
import os,sys
from random import randint
from sa import sent_analysis

#print (sys.getdefaultencoding())

class templates_book:
    def __init__(self):
        self.query=''
        self.name=''
        #f.write(self.query.content)
        self.aname=''
        self.genre=''
        self.lang=''
        self.chars=[]
        self.pub=''
        self.pubdate=''
        self.path = "/var/www/html/output/"
        self.ip = "192.168.1.100"
        self.wikiname = ''
        self.summary=[]

    def blanks(self):
        #with open('./extracted data/harry potter data.txt','r') as f:
        with open(self.wikiname,'r') as f:
            s=f.read()
            w=s.split('\n')
            #print(w)
            for i in range(len(w)):
                if 'Author'==str(w[i]):
                    #print('true')
                    self.aname=str(w[i+1])
                    break
            #print(self.aname)
            for i in range(len(w)):
                if w[i]=='Genre':
                    self.genre=str(w[i+1])
                    break
            #print(self.genre)
            for i in range(len(w)):
                if w[i]=='Language':
                    self.lang=str(w[i+1])
                    break
           # print(self.lang)
            for i in range(len(w)):
                if w[i]=='Publisher':
                    self.pub=str(w[i+1])
                    break
            #print(self.pub)
            for i in range(len(w)):
                if w[i]=='Publication Date':
                    self.pubdate=str(w[i+1])
                    break
            #print self.pubdate
            #return (self.name+' is a book written by '+self.aname+'in '+self.lang+' language.It is of the genre '+self.genre)

    def plot(self):
        with open('content.txt','r') as f:
            s=f.read()
        sent=s.split('\n')
        plot=[]
        for i in range(len(sent)):
            if re.match(r'^== [§]*Plot',sent[i]):
                #print sent[i]
                self.summary.append(sent[i+1])
                x=i+1
                while re.match(r'^== [§]*',sent[x])==None:
                    plot.append(str(sent[x]))
                    x=x+1
        #print plot
        sents=''.join(plot)
        with open("plot.txt",'w') as f:
            f.write(sents)
        cmd="chmod 777 plot.txt"
        os.system(cmd) 
        cmd="chown www-data:www-data plot.txt"
        os.system(cmd) 
        x=textrank(sents)
        num=0
        l=[]
        #self.summary.append(x[0][1])
        for i in x:
            try:
              word=word_tokenize(str(x[1]))
            except:
              word=''  
            if num+len(word)<=250:
                num=num+len(word)
                self.summary.append(str(i[1]))
        #print(l)
        sents=''.join(l)
        #print(sents)
        return sents
    def sent_generation(self):
         b1=['novel','book','best seller','narrative','tale','potboiler']
         b2=['written','penned','authored']
         b3=['written','penned','authored']
         b4=['genre','category','type of novel']
         b5=['published','promulgated']
         blank=[]
         #print 'hello'
         for i in range(0,5):
             #print 'b'+str(i+1)
             x=len('b'+str(i+1))
             #print x
             blank.append(randint(0,x-1))
         if self.name and self.aname:
             self.summary.append('{0} was a {1} {2} by {3}.'.format(self.name,b1[blank[0]],b2[blank[1]],self.aname))
         if self.lang:
             self.summary.append(' It was {0} in {1} language.'.format(b3[blank[2]],self.lang))
         if self.genre:
             if blank[3]==2:
                 self.summary.append(' It is a {0} {1}.'.format(self.genre,b4[blank[3]]))
             else:
                 self.summary.append(' It is of {0} {1}.'.format(self.genre,b4[blank[3]]))
         if self.pub:
             self.summary.append(' It was {0} by {1}.'.format(b5[blank[4]],self.pub))
         self.summary.append(sent_analysis())
 
        

    def apply_permission(self,fname):          
        return
 
    def template_gen(self):
        li=[]
        fname=''
        '''for i in range(0,2):
            with open('data'+str(i)+'.txt','r') as f:
                    s=f.read().split('\n')[0]
                    if re.search(r'wikipedia',s):
                        fname='data'+str(i)+'.txt'
                        break'''
        for i in range(0,3):
            with open('data'+str(i)+'.txt','r') as f:
                s=f.read().split('\n')[0]
                if 'wikipedia' in s:
                    fname='data'+str(i)+'.txt'
                    break
    	#print(fname)
        with open(fname,'r') as f:
            search_key=f.read().split('\n')[2]
        self.query=wikipedia.page(search_key)
        self.name=self.query.title
        self.wikiname=fname
        fname = 'content.txt'
        cmd="chmod 777 %s" % (fname)
        os.system(cmd) 
        cmd="chown www-data:www-data %s" % (fname)
        os.system(cmd) 
        with open(fname,'w') as f:
            f.write(self.query.content.encode('ascii', 'replace'))
        #print(x.name)
        self.blanks()
        self.sent_generation()
        self.plot()
        #print ''.join(self.summary)
        file_name = self.path + "summary.txt"
        fout = open(file_name,'w')
        fout.write(''.join(self.summary))
        #fout.write(str(self.plot())+"\n")
        fout.close()
        cmd="chmod 777 %s" % (file_name)
        os.system(cmd) 
        cmd="chown www-data:www-data %s" % (file_name)
        os.system(cmd) 
        #print (file_name)
        return(self.summary)

if __name__=='__main__':
    x=templates_book()
    x.template_gen()
    
