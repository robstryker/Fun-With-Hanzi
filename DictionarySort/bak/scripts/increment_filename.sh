#!/bin/sh
cat count_filename | perl -e '$a = <STDIN>; $a =~ s/(\d+)/$1+1/e; print $a;' > count_filename2 && mv count_filename2 count_filename 
