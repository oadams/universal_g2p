#languages="swedish cebuano kurmanji tagalog hausa malay tajik hindi marathi tamil indonesian russian thai spanish"
languages="indonesian"

odir="wholepool-odir-series"

for lang in $languages; do
    echo "Creating lexicon for ${lang} based on G2P trained on the whole pool of pronunciation lexicon data (minus gold data in that language)."
    mkdir -p $odir/${lang}
    local/make_lexicon_from_pool.sh data/local/${lang}/lexicon/words.pool data/local/${lang}/text/words data/local/${lang}/lexicon/lexicon.pool ${odir}/${lang}
done
