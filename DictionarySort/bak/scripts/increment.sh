#!/bin/sh
cat count_hanzi | perl -e '$a = <STDIN>; $a =~ s/(\d+)/$1+1/e; print $a;' > count_hanzi2 && mv count_hanzi2 count_hanzi 
