#!/usr/bin/python
# -*- coding:utf-8 -*-
import os, sys
import ast
import json
import cgi, cgitb
from datetime import datetime
import store as store
cgitb.enable();
from templates_place import templates_place 

print "Content-Type: text/html\n\n"

def display_data(input_str):
    res = {}
    retlst = []
    if 1:
        jsonObj  = ast.literal_eval(input_str)
        search_key = jsonObj.get('search_key')
        tobj = templates_place()
    	tobj.template_gen()  
        retlst.append(tobj.blanks())
        retlst.append(tobj.plot())
        html_str = ''
        html_str+='<html><head><title>Get Summary</title><style type="text/css">h1{text-align:center;font-family:Cursive;color:0033FF;background-color:DCDCDC;}p {font-family:Cursive;font-size:14px;font-style:italic;font-weight:bold;color:000000;}</style></head><body bgcolor=#DCDCDC><h1>Summary....!!!!</h1>'
        for ele in retlst:
            html_str+='<p>'+ele+'</p>'
        html_str+='</body></html>'
        fname = "/var/www/html/summary.html"
        path = "http://localhost/summary.html"
        fout = open(fname,'w')
        fout.write(html_str)
        fout.close()   
        fname = "content.txt"
        cmd="chmod 777 %s" % (fname)
        os.system(cmd) 
        cmd="chown www-data:www-data %s" % (fname)
        os.system(cmd) 
        final_res = [path]
        res = final_res
        res = json.dumps(res)
        return res
        
if __name__=="__main__":
    form = cgi.FieldStorage()
    if (form.has_key("input_str")):
        tmp = display_data(form["input_str"].value)
        print tmp

