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

if __name__=='__main__':

  topic = urllib.quote(sys.argv[1]);
  topic_cl = (sys.argv[1]).replace(" ","").replace("\'","") #apostroflari ileride sorun cikarmamasi icin temizle
  os.popen('rm %s_tot.txt'%topic_cl);
  #textfile = topic+'_tot.txt';

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
		html2text(filename,urllib.unquote(topic),topic_cl)
                f.closed

  else:
	filename = '%s'%(topic_cl) 
        f = open('%s.html'%(filename),'w')
        f.write(data);
	html2text(filename,urllib.unquote(topic),topic_cl);
        f.close();
