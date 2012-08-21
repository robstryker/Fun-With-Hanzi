#!/bin/sh
cat count_hanzi | awk '{print "tac ../outputs/wordsInOrder.txt | tail -n +" $0 " ";}' | sh | awk '{print "./capture.php -a \"" $0 "\"";}' | sh

