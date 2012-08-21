#!/bin/sh
# Turn the downloaded file into only a line of
# English, Pinyin, or Hanzi
sed "s/.*this, '//" | sed "s/', '');\"><\/span>//" | sed "s/');\"><\/span>//" | sed "s/', '/\n/"
