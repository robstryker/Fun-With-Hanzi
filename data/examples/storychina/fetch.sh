#!/bin/sh

# starts from 5000
# already did 510000 through 512700
for i in `seq 526700 545700` 
do
  wget http://www.storychina.cn/frmPopAuthor_Detail.aspx?ID=$i

   tail -n +162 frmPopAuthor_Detail.aspx\?ID\=$i  | head -n 1 | sed 's/&nbsp;//g' | sed 's/<\/div><div>/\
/g' | sed 's/<div>//g' | sed 's/<\/div>//g' > $i.txt
  rm frmPopAuthor_Detail.aspx\?ID\=$i
done
wc -l * | grep txt | sed 's/^ *//g' | grep "^1 " | cut -f 2 -d " " | awk '{ print "rm " $0;}' | sh
