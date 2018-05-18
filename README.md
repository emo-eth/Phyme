# Phyme
Phyme is a Python rhyming dictionary for songwriting.

Pronunciation is taken from [The CMU Pronouncing Dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict). Some background information on rhyming for songwriting can be found [here](http://songchops.com/2013/10/rhyme-families-your-secret-weapon/).

To install Phyme, use `pip install phyme`

By default, Phyme rhymes words based on the last stressed syllable or last stressed-unstressed pair of syllables. Passing in the `num_sylls=x` keyword arg will find rhymes with more syllables.

Phyme supports 6 types of rhymes:  

```
from Phyme import Phyme

ph = Phyme()

# find perfect rhymes. DOG -> COG
ph.get_perfect_rhymes(word, num_sylls=None)

# find rhymes with the same vowels and consonants of the same type (fricative, plosive, etc) and voicing (voiced or unvoiced). FOB -> DOG
ph.get_family_rhymes(word, num_sylls=None)

 # find rhymes with the same vowels and consonants of the same type, regardless of voicing. HAWK -> DOG
ph.get_partner_rhymes(word)

# find rhymes with the same vowels and consonants, as well as any extra consonants. DUDES -> DUES
ph.get_additive_rhymes(word)

# find rhymes with the same vowels and a subset of the same consonants. DUDE -> DO
ph.get_subtractive_rhymes(word)  

# find rhymes with the same vowels and some of the same consonants, with some swapped out for other consonants. FACTOR -> FASTER
ph.get_substitution_rhymes(word) 

# find rhymes with the same vowels and arbitrary consonants. CASH -> CATS
ph.get_assonance_rhymes(word)

# find word that do not have the same vowels, but have the same consonants. CAT -> BOT
ph.get_consonant_rhymes(word)
```