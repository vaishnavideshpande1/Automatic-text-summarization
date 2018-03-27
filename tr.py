import networkx as nx
import numpy as np
import time
from nltk.tokenize.punkt import PunktSentenceTokenizer
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
 
def textrank(document):
    sentence_tokenizer = PunktSentenceTokenizer()
    sentences = sentence_tokenizer.tokenize(document)
    try: 
       bow_matrix = CountVectorizer().fit_transform(sentences)
       #print (bow_matrix)
       #print(type(bow_matrix))
    except:
       bow_matrix = []   
    normalized = TfidfTransformer().fit_transform(bow_matrix)
 
    similarity_graph = normalized * normalized.T
 
    nx_graph = nx.from_scipy_sparse_matrix(similarity_graph)
    scores = nx.pagerank(nx_graph)
    return sorted(((scores[i],s) for i,s in enumerate(sentences)),
                  reverse=True)

def main(argv):
    with open(argv[1],'r') as f:
        document=f.read()
    s=time.clock()
    sent=textrank(document)
    print(time.clock()-s)
    val=0.0
    for x in sent:
        val+=x[0]
    thres=val/len(sent)
    
    with open('output.txt','w') as f:
        for x in sent:
            if x[0]>=thres:
                f.write(x[1])
    #print(sent)

if __name__=='__main__':
	main()

