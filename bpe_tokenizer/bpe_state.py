import re
from collections import Counter, defaultdict


class BpeState:
    def __init__(self, epoch=50, separator='</w>'):
        self.__map = {}
        self.__dictionary = {}
        self.__epoch = epoch
        self.__separator = separator
        self.__separator_mask = ' {separator}'

    def update(self, source: str):
        self.__update_dictionary(source.split())

        for i in range(self.__epoch):
            pairs = self.__gather_statistics()
            if not pairs:
                break

            best = max(pairs, key=pairs.get)

            self.__merge(best)

        self.__update_map()

    def words(self):
        return len(self.__map.keys())

    def encode(self, word):
        if word in self.__map:
            return self.__map[word]
        else:
            return ' '.join(word) + self.__separator_mask.format(separator=self.__separator)

    def _get_map(self):
        return self.__map

    def _set_map(self, cached_map):
        self.__map = cached_map

    def __update_dictionary(self, data: list):
        self.__dictionary.update(Counter([(' '.join(word) + self.__separator_mask.format(separator=self.__separator),
                                           word)
                                          for word in data]))

    def __gather_statistics(self):
        pairs = defaultdict(int)
        for word, frequency in self.__dictionary.items():
            symbols = word[0].split()

            for i in range(len(symbols) - 1):
                pairs[symbols[i], symbols[i + 1]] += frequency

        return pairs

    def __merge(self, pair: list):
        resulted_dictionary = {}

        p = re.compile(r'(?<!\S)' + re.escape(' '.join(pair)) + r'(?!\S)')

        for word in self.__dictionary:
            merged_word = (p.sub(''.join(pair), word[0]), word[1])
            resulted_dictionary[merged_word] = self.__dictionary[word]

        self.__dictionary = resulted_dictionary

    def __update_map(self):
        self.__map.update({it[1]: it[0] for it in self.__dictionary.keys()})
