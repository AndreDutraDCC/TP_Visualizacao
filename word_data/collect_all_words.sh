for base in clean
do
    for lang in   hi zh #hu sv tr ru it pt fr es en #cs de fa 
    do
        python3 collect_words.py $lang $base
    done
done
