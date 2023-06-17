for base in clean
do
    for lang in sv #tr ru it pt fr es en zh #cs de fa hi hu
    do
        python3 collect_words.py $lang $base
    done
done
