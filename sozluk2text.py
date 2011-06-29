#!/usr/bin/python
import sys
import urllib2
import urllib
import os

def html2text(filename,texttopic,root):
    os.popen('lynx -dump -nolist %s.html > %s.txt'%(filename,filename))
    os.popen('grep -v \'f tw\' %s.txt | grep -v \'no kitty!\' | \
	     grep -v \'inde ara\' | grep -v \'no kitty!\' | \
	     grep -v \'____________ ara\'  | grep -v \'   payla\' | \
             grep -v \'^$\' | grep -v \'   _______\' | \
	     grep -v \"      %s\" | \
	     grep -v \'ie8  ws\'  | \
	     grep -v \'1999-2012 sourtimes\' | \
	     grep -v \'(Submit)\'| \
	     grep -v \'   <<\' | grep -v \' >>\' >> %s_tot.txt'%(filename,texttopic,root))
    os.popen('rm %s.html %s.txt'%(filename,filename))

def get_entries(entryler, metatag, filename):
    sayfa = open('%s.html'%filename).readlines()
    bas = []
    son = []
    meta = []
    
    baskeyword = '<li value="'
    sonkeyword = '<div class="aul">'
    metakey = ')<div '
    for i in range(len(sayfa)):
        line = sayfa[i]
        bak = line.find(baskeyword)
        sonabak = line.find(sonkeyword)
        metabak = line.find(metakey)
        if bak!=-1:
            bas.append((i,bak))
        if sonabak !=-1:
            son.append((i,sonabak))
        #if metabak !=-1:
            meta.append(metabak)
    #print bas[2], son[2],meta[2]
    assert len(bas) == len(son)
    assert len(meta) == len(son)
    
    for i in range(len(bas)):
        entry = ''
        if bas[i][0] == son[i][0]:
            entry=entry+ sayfa[bas[i][0]][bas[i][1]:son[i][1]]
        elif bas[i][0] < son[i][0]:
            for j in range(bas[i][0],son[i][0]+1):
                if j == bas[i][0]:
                    entry = entry+ sayfa[j][bas[i][1]:]
                elif j == son[i][0]:
                    entry = entry+ sayfa[j][:son[i][1]]
                else:
                    entry = entry+ sayfa[j]
        else:
            print 'entry basi sonu dogru degil'
        entryler.append(entry)
        tags = sayfa[son[i][0]][son[i][1]+len(sonkeyword):meta[i]]+')<br>'
        metatag.append(tags)
        #return entryler, metatag


if __name__=='__main__':

  topic = urllib.quote(sys.argv[1]);
  topic_cl = (sys.argv[1]).replace(" ","").replace("\'","") #apostroflari ileride sorun cikarmamasi icin temizle
  os.popen('rm %s.html'%topic_cl);
  #textfile = topic+'_tot.txt';
  entryler = []
  metatag =[]

  print "\
			      sozluk2text		\n\
		cCc    ek$isozluk crawler aparati    cCc \n \
			ferayebend + der wille 2011  \n\
		 %s basligini davloyd ediyor          \n"%sys.argv[1]
  out = urllib2.urlopen("http://eksisozluk.com/show.asp?t=%s" % topic);
  data = out.read();

  i = data.find("</a> <a title=\"sonraki sayfa\"");
  if i != -1:
        j = i;
        while (data[i] != ">"):
                i-=1;
        page_count =  int(data[i+1:j]);
        #print page_count;

        for i in range(page_count):
		filename = '%s%i'%(topic_cl,i) #dosya kolayligi icin bosluklari temizle
		#f = open('%s%i.html'%(urllib.unquote(topic),i),'w')
		f = open('%s.html'%(filename),'w')
		#show.asp?t=hede&amp;kw=&amp;a=&amp;all=&amp;v=&amp;fd=&amp;td=&amp;au=&amp;g=&amp;p=8
		curr_page = urllib2.urlopen("http://eksisozluk.com/show.asp?t=%s&p=%d" % 
                                (topic, i+1));	
		f.write(curr_page.read());
		get_entries(entryler,metatag,filename);	
		#html2text(filename,urllib.unquote(topic),topic_cl)
		f.closed
		os.popen('rm %s.html'%filename);

  else:
	filename = '%s'%(topic_cl) 
	f = open('%s.html'%(filename),'w')
	f.write(data);
	get_entrys(entryler,metatag,filename);
	#html2text(filename,urllib.unquote(topic),topic_cl);
	f.close();
	os.popen('rm %s.html'%filename);

  out = open('%s.html'%topic_cl,'w')
  for i in range(len(entryler)):
        out.write(str(i+1)+'. '+entryler[i]+'\n')
        out.write(metatag[i]+'\n')
  out.close() 

  '''
  #obsolete
  print '   konululari filtreliyor   '
  os.popen('head -21 %s_tot.txt > filter'%(topic_cl))
  os.popen('grep -v -f filter %s_tot.txt > %s.txt'%(topic_cl, topic_cl))
  os.popen('rm filter %s_tot.txt'%(topic_cl))
  print '   bitdi. hayrini gor!'
  '''
