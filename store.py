import urllib,os,sys
from BeautifulSoup import BeautifulSoup
import re

class store:
    def __init__(self):
        return

    def apply_permission(self,fname):          
        cmd="chmod 777 %s" % (fname)
        os.system(cmd) 
        cmd="chown www-data:www-data %s" % (fname)
        os.system(cmd) 
        return 

    def visible_text(self,element):
        if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
           return ''
        result = re.sub('<!--.*-->|\r', '', str(element), flags=re.DOTALL)
        result = re.sub('\s{2,}|&nbsp;', ' ', result)
        result = result.replace('[','')
        result = result.replace(']','')
        result = result.replace(':&#160;','')
        result = result.replace('&','')
        result = result.replace('#','')
	#result = result.replace(' ','\n')
	result=re.sub('\n\n+','\n',result)
        if result.find('.')>=0:
           retlst = result + "\n"
        return result

    def save(self,idata): 
        retlst = []
        ref_count = []
        store_key = idata.get('store_key')
        #action_type = idata.get('action_type') 
        #search_key = idata.get('search_key') 
        store_li = store_key.split('^!!^')
        update_flag = False
        fname = "data.txt"
        #fout = open(fname,"w") 
        for i,path in enumerate(store_li):
	    fout = open("data"+str(i)+".txt","w")
            html = urllib.urlopen(path).read()  
            a = BeautifulSoup(html)
            texts_li = a.findAll(text=True)
            visible_elements = [self.visible_text(elem) for elem in texts_li]
            for ww in visible_elements:
                if ww.find('References')>=0:
                   ref_count.append(ww)
            tmp_li = []
            cc = 0
            start_st="start writting the data of  %s \n" %(str(path))
            fout.write(start_st)
            start_st="\n===================================================================\n"
            fout.write(start_st)
            for words in visible_elements:
                if words.find('References')>=0:
                   cc+=1
                if cc==len(ref_count):     
                   break                  
                fout.write(words) 
                update_flag = True 
            start_st="\n===================================================================\n"
            fout.write(start_st)
            start_st="\nending writting the data of  %s \n" %(str(path))
            fout.write(start_st)
            start_st="\n===================================================================\n"
            fout.write(start_st)
        fout.close()
	for i in range(0, 3):
		with open("data"+str(i)+".txt",'r') as f:
			s=f.read()
		w=re.sub('\n\n+','\n',s)
		with open("data"+str(i)+".txt",'w') as f:
			f.write(w)
        ff = self.apply_permission(fname)     
        if update_flag:
           retlst.append("data stored successfully")
        else:
           retlst.append("data not stored successfully")
        #if action_type=='B':
        #   #import templates as templates
        #   #tobj = templates.templates_book(search_key)  
        #   #retlst.append(tobj.blanks())
        #   #retlst.append(tobj.plot())
        #   summary_path = "http://localhost/output/summary.txt" 
        #   retlst = [summary_path]  
        #elif action_type=='M':
        #   pass
        #   #import templates as templates
        #else: 
        #   pass
        #   #import templates as templates
        return retlst 

if __name__ == '__main__':  
   obj=store()
   obj.save({'store_key':'http://en.wikipedia.org/wiki/Harry Potter','action_type':'B','search_key':'Harry Potter'})
