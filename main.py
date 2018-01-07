# -*- coding: utf-8 -*-
import os
import json
from pprint import pformat as pf
from pkg.model import TermSelection as TS
from pkg.model import TermOrdering as TO
from pkg.model import TitleLength as TL

def get_corpus():
    json_corpus = {}
    with open('corpus.json', 'r', encoding = 'UTF-8') as fr:
        json_corpus = json.load(fr)
    return json_corpus

corpus = get_corpus()
print(pf(corpus, indent = 4))
print(len(corpus['word_info'])) # term count

filename = []


"""
TSModel = TS(corpus)
TSModel.construct_scores()
TOModel = TO(corpus)
TLModel = TL(corpus)

tf_idf_words_10_test = [[('毀滅', 'V'), ('聯盟', 'N'), ('相逢', 'V')], []] # 10部測試電影, 共3000words

generated_words_10_test = TSModel.gen_words_num_test(tf_idf_words_10_test, 100)
generated_terms_titles_10_test = TOModel.gen_terms_titles_num_test(generated_words_10_test, 200)
generated_title_10_test = TLModel.gen_title_num_test(generated_terms_titles_10_test)

with open('output.txt', 'w', encoding = 'UTF-8') as fw:
for i in range(len(generated_title_10_test)):
    print(filename[i], generated_title_10_test[i], sep = '\t')
    fw.write('\t'.join([filename[i], generated_title_10_test[i]]) + '\n')
"""