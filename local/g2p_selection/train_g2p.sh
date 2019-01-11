#!/bin/bash
cmd=run.pl
encoding=utf-8
g2p_iters=6
stage=0
known_words=50
nj=10

. ./utils/parse_options.sh
. ./path.sh

# To get the word list ...
# comm -23 <(grep -v '<.*>' hub4_words | grep -v 'SIL' | sort) \
#          <(awk '{print $1}' pron_lex | sort) > hub4_oov
#
# comm -23 <(grep -v '<.*>' lorelei_words | sort) \
#          <(awk '{print $1}' pron_lex | sort) > lorelei_oov
#
# cat hub4_oov lorelei_oov | sort -u > oov.txt
#
# comm -12 <(grep -v '<.*>' hub4_words | grep -v 'SIL' | sort) \
#          <(awk '{print $1}' pron_lex | sort) > hub4_words
#
# awk 'FNR==NR{a[$1]=$0; next}($1 in a)' pron_lex > hub4_pron_lex


if [ $# -eq 0 ]; then
  echo "Usage: ./local/g2p/apply_g2p.sh <lexicon> <odir>"
  exit 1
fi

output=$2
lexicon=$1

mkdir -p $output/log

echo "--------- Params ------"
echo "LEX: $lexicon"
echo "output: $output"
echo "------------------------"

phonetisaurus-align \
  --seq1_del=false --seq2_del=false \
  --input=$lexicon  \
  --ofile=$output/g2p.corpus || true 

ngram-count -lm $output/g2p.arpa  -maxent -maxent-convert-to-arpa \
  -kndiscount1 -gt1min 0 -kndiscount2 -gt2min 2 -kndiscount3 -gt3min 2 \
  -order 3 -text $output/g2p.corpus -sort 2>&1

#ngram-count -lm $output/g2p.arpa  -maxent -maxent-convert-to-arpa \
#  -kndiscount1 -gt1min 0 -kndiscount2 -gt2min 2 \
#  -order 2 -text $output/g2p.corpus -sort 2>&1


echo >&2 "$0: Converting P2G into a fst..."
phonetisaurus-arpa2wfst \
  --lm=$output/g2p.arpa \
  --ofile=$output/g2p.fst --ssyms=$output/g2p.syms 2>&1

