import sys
import os
import re

match=re.compile(r'nectar!qld@')
word='nectar!qld@cn8.qld.nectar.org.au'

if match.search(word):
    print "Found occurences"
else:
    print "not found"
