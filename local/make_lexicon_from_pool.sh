#!/bin/bash


# Takes a pool of selected words (selected_words), extracts the lexicon subset
# associated with those words. A G2P is trained on this subset. We finally use
# this G2P to create pronunciations for a new set of words (test_words).

words_name=test_words

. ./utils/parse_options.sh

if [ $# -ne 4 ]; then
  echo "Usage: ./local/make_lexicon_from_pool.sh <selected_words> <test_words> <candidate_prons> <odir>"
  exit 1;
fi

# Takes all prons from candidates prons corresponding to selected words
selected_words=$1
test_words=$2
candidate_prons=$3
odir=$4

mkdir -p ${odir}
selected_lexicon=${odir}/selected_lexicon.txt

echo "Selecting lexicon subset from selected words ..."
awk '(NR==FNR) {
    counts[$1]+=1;
    a[$1][counts[$1]]=$0;
    next
    } 
    ($1 in a) {
      for (i in a[$1]) {
        print a[$1][i]
      }
    }' $candidate_prons $selected_words | sort -u > ${selected_lexicon}   


echo "Training G2P ..."
./local/g2p_selection/train_g2p.sh ${selected_lexicon} ${odir}/g2p

# This line removes any oov graphemes and replaces them with a uromanized grapheme
# (See http://www.aclweb.org/anthology/P18-4003.pdf for more details)
# Must have uroman (available at https://github.com/isi-nlp/uroman)
echo "Romanizing oov characters"
python local/transliterate_oov_graphemes.py ${test_words} ${selected_words} ${odir}/${words_name}.transform
#mv ${test_words} ${odir}/${words_name}.transform

echo "Applying G2P ..."
./local/g2p_selection/apply_g2p.sh --nbest 1 \
  ${odir}/${words_name}.transform ${odir}/g2p ${odir}/g2p/${words_name}

 

