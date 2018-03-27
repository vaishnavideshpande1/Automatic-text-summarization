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
import time
from sa import sent_analysis

#print (sys.getdefaultencoding())

class templates_movies:
    def __init__(self):
        self.query=''
        self.name=''
        self.direct=''
        self.produce=''
        self.written=''
        self.star=''
        self.cinema=''
        self.reldate=''
        self.lang=''
        self.country=''
        self.path = "/var/www/html/output/"
        self.ip = "192.168.1.100"
        self.line2=''
        self.genre=''
        self.wikifile=''
        self.summary=[]

    def blanks(self):
       # with open('./extracted data/interstellardata.txt','r') as f:
        with open('content.txt','r') as f:
            y=f.read().split('.')
            s=y[0].split()
            x=[]
            for i in range(len(s)):
                if s[i]=='is' and s[i+1]=='a':
                    j=i+2
                    while s[j]!='film':
                        x.append(s[j])
                        j=j+1
                    i=j
            self.genre=' '.join(x)
            #print(self.genre)
            self.line=y[1]
        
        with open(self.wikifile,'r') as f:
            s=f.read()
            w=s.split('\n')
            #print(w)
            for i in range(len(w)):
                if 'Directed by'==str(w[i]):
                    #print('true')
                    self.direct=str(w[i+1])
                    break
            #print(self.direct)
            for i in range(len(w)):
                if w[i]=='Produced by':
                    self.produce=str(w[i+1])
                    break
            #print(self.produce)
            for i in range(len(w)):
                if w[i]=='Written by':
                    self.written=str(w[i+1])
                    break
            # print(self.written)
            for i in range(len(w)):
                x=[]
                if w[i]=='Starring':
                    x.append(str(w[i+1]))
                    x.append(str(w[i+2]))
                    x.append(str(w[i+3]))
                    self.star=','.join(x)
                    break
            #print(self.star)
            for i in range(len(w)):
                if w[i]=='Cinematography':
                    self.cinema=str(w[i+1])
                    break
            #print self.cinema
            for i in range(len(w)):
                if w[i]=='Release dates':
                    self.reldate=str(w[i+1])
                    break
            #print self.reldate
            for i in range(len(w)):
                if w[i]=='Language':
                    self.lang=str(w[i+1])
                    break
            #print self.lang
            for i in range(len(w)):
                if w[i]=='Country':
                    self.country=str(w[i+1])
                    break
            #print self.country
            #return (self.name+' is a movie directed by '+self.direct+' produced by '+self.produce+' written by '+self.written+'
                #stars in the movie '+','.join(self.star)+' cinematography by '+self.cinema+' in '+self.lang+' language and was released in '+self.country)

    def sent_generation(self):
        b1=['movie','cinema','feature','motion picture','picture']
        b2=['movie was written','sceenplay']
        b3=[' It stars','are starred in the movie']

        blank=[]
        for i in range(0,3):
             #print 'b'+str(i+1)
             x=len('b'+str(i+1))
             #print x
             blank.append(randint(0,x-1))

        if self.name:
            self.summary.append('{0} is a {1} '.format(self.name,b1[blank[0]]))
        if self.direct and self.produce:
            if self.direct==self.produce:
                self.summary.append('directed and produced by {0}. '.format(self.direct))
            else:
                self.summary.append('directed by {0} and produced by {1}. '.format(self.direct,self.produce))
        if self.genre:
            self.summary.append(' It is a {0} {1}.'.format(self.genre,b1[blank[0]]))
        if self.star:
            if blank[2]==0:
                self.summary.append('{0} {1}. '.format(b3[blank[2]],self.star))
            else:
                self.summary.append('{0} {1}. '.format(self.star,b3[blank[2]]))                                    
        if self.line:
            self.summary.append(self.line)
        if self.written:
            self.summary.append(' The {0} by {1}.'.format(b2[blank[1]],self.written))
        if self.lang:
            self.summary.append(' Movie was in {0} and was released in {1}.'.format(self.lang,self.country))
        self.summary.append(sent_analysis())
            


    def plot(self):
        with open('content.txt','r') as f:
            s=f.read()
        sent=s.split('\n')
        plot=[]
        for i in range(len(sent)):
            if re.match(r'^== [§]*Plot',sent[i]):
                #print sent[i]
                #print(sent[i+1])
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
        for i in x:
            try:
                word=word_tokenize(str(x[1]))
            except:
                word=''
            if num+len(word)<=250:
                num=num+len(word)
                self.summary.append(str(i[1]))
        sents=''.join(l)
        #print(sents)
        return sents
     
    def apply_permission(self,fname):          
        return
        

    def template_gen(self):
        li=[]
        fname=''
        start=time.clock()
        '''for i in range(0,3):
            with open('data'+str(i)+'.txt','r') as f:
                s=f.read().split('\n')[0]
                #s=f.read().split('\n')[0]
                if 'wikipedia' in s:
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
        self.wikifile=fname
        fname = 'content.txt'
        cmd="chmod 777 %s" % (fname)
        os.system(cmd) 
        cmd="chown www-data:www-data %s" % (fname)
        os.system(cmd) 
        with open(fname,'w') as f:
            f.write(self.query.content.encode('ascii', 'replace'))
        #x=templates_movies(search_key,fname)
        #print search_key
        #print(x.name)
        self.blanks()
        self.sent_generation()
        self.plot()
        #print(time.clock()-start)
        #print(''.join(x.summary))
        file_name = self.path + "summary.txt"
        fout = open(file_name,'w')
        fout.write(''.join(self.summary))
        #fout.write(str(x.plot())+"\n")
        fout.close()
        cmd="chmod 777 %s" % (file_name)
        os.system(cmd) 
        cmd="chown www-data:www-data %s" % (file_name)
        os.system(cmd) 
        #print (file_name)
        return(self.summary)

if __name__=='__main__':
    x=templates_movies()
    x.template_gen()
	    
