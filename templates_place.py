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

class templates_place:
    def __init__(self):
        self.query=''
        self.name=''
        #f.write(self.query.content)
        self.cname=''
        self.region=''
        self.state=''
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
                if 'Country'==str(w[i]):
                    #print('true')
                    self.cname=str(w[i+1])
                    break
            #print(self.aname)
            for i in range(len(w)):
                if w[i]=='Region':
                    self.region=str(w[i+1])
                    break
            #print(self.genre)
            for i in range(len(w)):
                if w[i]=='State':
                    self.state=str(w[i+1])
                    break
           # print(self.lang)
            #print self.pubdate
            #return (self.name+' is a book written by '+self.aname+'in '+self.lang+' language.It is of the genre '+self.genre)

    def plot(self):
        #for i in range(len(sent)):
        #sents=''.join(plot)
        with open("plot.txt",'w') as f:
            f.write(self.query.summary.encode('ascii','replace'))
        cmd="chmod 777 plot.txt"
        os.system(cmd) 
        cmd="chown www-data:www-data plot.txt"
        os.system(cmd)
        with open('plot.txt','r') as f:
            sents=f.read()
            self.summary.append(sents.split('.')[1])
        x=textrank(sents)0
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
        #print(self.summary)
        return sents
    def sent_generation(self):
         if self.name and self.cname:
             self.summary.append('{0} is a place in the country {1}.'.format(self.name,self.cname))
         if self.state:
             self.summary.append(' It is in {0} state.'.format(self.state))
         if self.region:
             self.summary.append(' It is in {0} region.'.format(self.region))
         
         
         #self.summary.append(sent_analysis())
 
        

    def apply_permission(self,fname):          
        return
 
    def template_gen(self):
        li=[]
        fname=''
        for i in range(0,3):
            with open('data'+str(i)+'.txt','r') as f:
                s=f.read().split('\n')[0]
                if 'wikipedia' in s:
                    fname='data'+str(i)+'.txt'
                    break
        with open(fname,'r') as f:
            search_key=f.read().split('\n')[2]
        self.query=wikipedia.page('london')
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
        print ''.join(self.summary)
        file_name = self.path + "summary.txt"
        fout = open(file_name,'w')
        fout.write(''.join(self.summary))
        #fout.write(str(self.plot())+"\n")
        fout.close()
        cmd="chmod 777 %s" % (file_name)
        os.system(cmd) 
        cmd="chown www-data:www-data %s" % (file_name)
        os.system(cmd) 
        print (file_name)

if __name__=='__main__':
    x=templates_place()
    x.template_gen()
    
