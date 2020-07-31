# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 10:58:11 2020

@author: Manos
"""

import re

def special_trim_pub_9(mystring):
    mystring = mystring.replace("** ", "**")
    mystring = mystring.replace(" **", "**")
    mystring = mystring.replace("* ", "*")
    mystring = mystring.replace(" *", "*")
    mystring = mystring.replace("_ ", "_")
    mystring = mystring.replace(" _", "_")
    mystring = mystring.replace("` ", "`")
    mystring = mystring.replace(" `", "`")
    return mystring

def find_candidate_strings_for_pub_9(mystring):
    candidates1 = re.findall(r"_ [a-z]* _", mystring)
    candidates2 = re.findall(r"` [a-z]* `", mystring)
    candidates3 = re.findall(r"[*]+ [a-z]* [*]+", mystring)
    return candidates1 + candidates2 + candidates3

def trim_pub_9(mystring):
    candidates = find_candidate_strings_for_pub_9(mystring)
    for i in candidates:
        mystring = mystring.replace(i, special_trim_pub_9(i))
    return mystring