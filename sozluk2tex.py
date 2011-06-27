#!/usr/bin/python
from deasciifier import Deasciifier
import sys
import os

def turkce(line):
    dea = Deasciifier(line)
    result = dea.convert_to_turkish()
    return result

def get_entry(lines):
   indicies = []
   nicknames = []
   entries = []
   entries.append(0)
   for i in range(len(lines)):
      if len(lines[i].split()[-1]) > 4:  
	if lines[i].split()[0][0]=='(' and lines[i].split()[-1][-4]==':' and lines[i].split()[-1][-1]==')':
	  indicies.append(i)
	  entries.append(i+1)
#	  if len(lines[i].split())==3:
      	  nicknames.append(lines[i][lines[i].find('(')+1:lines[i].find(',')])
#	  else:
#		for j in range(len(lines[i].split())):
#	       	    nick = lines[i].split()[0]
   return entries, nicknames

def lineformat(filename):
    lines = open(filename).readlines()
    newfile = open('yenimunazara.tex','w')
    for line in lines:
	newfile.write(line.replace("&","\&").replace(".\n",".\\\\ \n &").replace("$","\$"))

def getsame(data):
    result=[]
    number=[]
    num = 0
    for i in range(len(data)):
        if data[i] in result:
            num=num+1
        else:
            number.append(num)
            num=0
            result.append(data[i])
    return result,number

if __name__=='__main__':
   lines = open(sys.argv[1]).readlines()
   texfile = open(sys.argv[1][:-8]+'.tex','w')
   entries = []
   entry_ind,nicknames = get_entry(lines)
   for i in range(len(nicknames)):
	texfile.write('\\\\ \\\\ \n'+nicknames[i]+': &')
	ind = entry_ind[i+1]-entry_ind[i]-1
	for j in range(ind):
#	   if j == ind-1:
#		texfile.write(lines[entry_ind[i]+j][6:].replace(".\n",".\\\\\n"))
#	   else:
	   texfile.write(lines[entry_ind[i]+j][6:])
   texfile.close()
   
   lineformat(sys.argv[1][:-8]+'.tex')

   yazarlar, sayi =  getsame(nicknames)
   headerfile = open(+'.head','w')
   for yazar in yazarlar:
      headerfile.write(yazar+': \\\\')
   headerfile.close()
