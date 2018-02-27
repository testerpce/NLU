# NLU
NLU Assignment submission

1) First Assignment

a) Perplexity
The file perplexcalc.py calculates the perplexities of Kneyser Kney Bigram and Trigram for Brown and gutenberg corpus and their combinations.
It is called using "python3 perplexcalc.py"

b) Generating a pickle file to store the bigram and trigram probabilities
The file Senes.py calculates the bigram and trigram probabilities for the gutenberg corpus only. 
It is called using "python3 Senes.py"

c) 
The file Quicksent.py generates the sentence using the bigrams and trigrams created using pickle in Senes.py to generate a 12 to 13 token sentence.
It is called using "python3 Quicksent.py"
It takes a maximum of 4 minutes to run.

The generate_sentence.sh file is a bash file which is used to call the Quicksent.py file.
It is called using "sh generate_sentence.sh"


