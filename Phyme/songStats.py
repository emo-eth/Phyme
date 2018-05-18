import os
import json

file_path = os.path.dirname(__file__)
with open(os.path.join(file_path, 'data/word_keys.json')) as f:
    word_keys = json.load(f)


key_words = {v: k for k, v in word_keys.items()}

with open(os.path.join(file_path, 'data/keyed_counts.json')) as f:
    keyed_counts = json.load(f)

with open(os.path.join(file_path, 'data/keyed_pairs.json')) as f:
    keyed_pairs = json.load(f)


# TODO: regex for different(1) pronunciations
def get_count_rank(word):
    return keyed_counts.get(word_keys.get(word), float('inf'))


def get_paired_words(word):
    word_key = word_keys.get(word)
    if word_key is None:
        return dict()
    return {v: k for k, v in enumerate(list(map(lambda key: key_words[key],
                                                keyed_pairs.get(word_key,
                                                                [])
                                                )
                                            )[::-1]
                                       )
            }


def _sort_key(word, pair_dict):
    pair_rank = pair_dict.get(word)
    if pair_rank is not None:
        return pair_rank
    return 100000 * (get_count_rank(word) + 1)


def sort_words(inpt, words):
    pair_dict = get_paired_words(inpt)
    return sorted(words, key=lambda word: _sort_key(word, pair_dict))
