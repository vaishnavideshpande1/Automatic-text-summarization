import nltk
import re
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import movie_reviews
from textblob import TextBlob

def sent_analysis():
    amazon=[]
    data=[]
    for i in range(0,3):
        with open('data'+str(i)+'.txt','r') as f:
            s=f.read().split('\n')[0]
            if 'amazon' in s:
                amazon.append('data'+str(i)+'.txt')

    for i in range(len(amazon)):
        with open(amazon[i],'r') as f:
            st=f.read()
            st=st.split('\n')
                #print(len(st))
            for j in range(len(st)):
                #print()
                if re.match('Customer Reviews',st[j]):
                    #print('hello')
                    x=j+1
                    while 'Search Customer Reviews' not in st[x]:
                        data.append(str(st[x]))
                        x=x+1
        with open('review.txt','w') as f:
            f.write('\n'.join(data))
        #sa.sent_ana(sa.data)
    s=''
    with open('review.txt','r') as f:
        s=f.read()
        y=s.split('\n')[1]
    text=TextBlob(s,classifier=NaiveBayesClassifier)
            #print text.sentiment
        
    if text.sentiment.polarity<text.sentiment.subjectivity:
        return (str(text.sentiment.subjectivity)+' '+y)
    else:
        return (str(text.sentiment.polarity)+' '+y)
            
        
        '''for i in y:
            i=i.split()
            k='Thank you for your feedback.'.split()
            for j in range(0,len(i)-1):
                if len(i)>=len(k) and i[j]==k[j] and i[j+1]==k[j+1] and i[j+2]==k[j+2]:
                    y.remove(i)
            
        print('\n'.join(y))'''
        
                

    

if __name__=='__main__':
    print sent_analysis()
