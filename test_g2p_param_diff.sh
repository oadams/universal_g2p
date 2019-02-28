odir="param-test-odir2/"
mkdir -p param-test-odir/

function test_param {
    # $1 = lang
    # $2 = seq1max
    # $3 = seq2max
    lang=$1
    seq1_max=$2
    seq2_max=$3

    ./local/g2p_selection/train_g2p.sh --seq1_max ${seq1_max} --seq2_max ${seq2_max} $odir/${lang}_train $odir/g2p_${lang}
    ./local/g2p_selection/apply_g2p.sh <(awk '{print $1}' data/local/${lang}/lexicon.txt) $odir/g2p_${lang} $odir/g2p_${lang}/all_words
    cut -f 1,3 $odir/g2p_${lang}/all_words/lexicon_out.1 > $odir/g2p_${lang}/all_words/lexicon.txt
    python ./local/g2p_selection/compute_per.py $odir/g2p_${lang}/all_words/lexicon.txt data/local/${lang}/lexicon.txt > $odir/$lang/per_s1m${seq1_max}_s2m${seq2_max}.txt
}

langs="102 201 207 306 103 202 301 307 104 203 302 401 105 204 303 402 106 205 304 403 107 206 305 404"

for lang in $langs; do
    mkdir -p $odir/$lang/
    shuf -n 1000 data/local/${lang}/lexicon.txt > $odir/${lang}_train
    test_param $lang 2 2
    test_param $lang 2 3
    test_param $lang 3 2
    test_param $lang 3 3
done
