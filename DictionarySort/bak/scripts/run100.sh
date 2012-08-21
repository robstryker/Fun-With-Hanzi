#!/bin/sh
cat count_hanzi | awk '{print "tac ../outputs/wordsInOrder.txt | tail -n +" $0 " | head -n 100";}' | sh | awk '{print "./capture.php -a \"" $0 "\"";}' | sh

