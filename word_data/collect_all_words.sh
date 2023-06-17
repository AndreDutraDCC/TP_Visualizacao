for base in clean
do
    for lang in en es #fa fr hi hu it pt ru sv tr zh #cs de
    do
        python3 collect_words.py $lang $base
    done
done
