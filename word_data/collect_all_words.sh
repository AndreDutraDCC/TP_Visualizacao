for base in dirty clean
do
    for lang in cs de en es fa fr hi hu it pt ru sv tr zh
    do
        python3 collect_words.py $lang $base
    done
done
