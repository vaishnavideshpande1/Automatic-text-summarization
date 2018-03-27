#!/usr/bin/python
# -*- coding:utf-8 -*-
import os, sys
import ast
import json
import cgi, cgitb
from datetime import datetime
import store as store
cgitb.enable();

print "Content-Type: text/html\n\n"

def display_data(input_str):
    res = {}
    if 1:
        jsonObj  = ast.literal_eval(input_str)
        dObj = store.store()
        res = dObj.save(jsonObj)
        res = json.dumps(res)
        return res
        
if __name__=="__main__":
    form = cgi.FieldStorage()
    if (form.has_key("input_str")):
        tmp = display_data(form["input_str"].value)
        print tmp

