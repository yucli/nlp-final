# -*- coding: utf-8 -*-
import os
import glob
import jieba.analyse as analyse
import jieba.posseg as pseg
import json
import logging
import pysrt
from pprint import pformat as pf
from pkg.model import TermSelection as TS
from pkg.model import TermOrdering as TO
from pkg.model import TitleLength as TL
from gensim.models import word2vec
from gensim import models

def get_corpus():
    json_corpus = {}
    with open('corpus.json', 'r', encoding = 'UTF-8') as fr:
        json_corpus = json.load(fr)

    logging.info('Get trainning corpus')
    return json_corpus

def get_files():
    files = []
    path_files = glob.glob(os.path.join('input', '*.srt'))
    files = [os.path.basename(path) for path in path_files]
    return files

def get_text_rank_words_10_test(files):
    EXTRACT_POS = ['n', 'nr', 'ns', 'nt', 'nz', 'ng', 'v', 'vg', 'vd', 'vn', 'nr', 'ns', 'nt', 'nz']
    words_list = []

    for file in files:
        srt = pysrt.open(file, encoding='utf-8')
        # Write the lines to a .txt file
        with open('srt_lines.txt', 'w') as srt_txt:
            for i in range(len(srt)):
                srt_txt.write(srt[i].text.encode('utf-8') + '\n')

        textrank = analyse.textrank
        content = open('srt_lines.txt', 'rb').read()
        keywords = textrank(content, topK = 30, allowPOS = (EXTRACT_POS))

        keywords_per_movie = []
        # Do posseg to each keywords to get their pos taggings
        for word in keywords:
            words = pseg.cut(w)
            for word, flag in words:
                if flag in NOUN:
                    pos = 'n'
                elif flag in VERB:
                    pos = 'v'
                else:
                    pos = flag
                keywords_per_movie.append((word, pos))
        words_list.append(keywords_per_movie)
    
    return words_list

def get_sentences(files): # get sentences to be trained in w2v_model
    NO_NEED = ['x', 'eng', 'w', 'm', 'mq', 'mg']
    sentences = []
    for file in files:
        srt = pysrt.open(file, encoding = 'utf-8')
        for i in range(len(srt)):
            line = srt[i].text.encode('utf-8')
            words = pseg.cut(line)
            sentence = []
            for word, flag in words:
                if flag not in NO_NEED:
                    sentence.append(word)
            sentences.append(sentence)
    
    return sentences

def get_w2v_model(sentences): # get word2vec model, sentences = [['first', 'sentence'], ['second', 'sentence']]
    w2v_model = models.Word2Vec.load('med250.model.bin')
    # Train the model again with new sentences
    for sentence in sentences:
        model.build_vocab(sentence, update=True)
        model.train(sentence)
 
    logging.info('Get word2vec model')
    return w2v_model

def pause_for_start_to_generate_titles():
    start = input()
    while start != 'start':
        start = input()
    logging.info('Generate titles')

def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    corpus = get_corpus()
    # print(pf(corpus, indent = 4))
    # print(len(corpus['word_info'])) # term count

    files = get_files() # files = ['1.srt', '2.srt', '3.srt']
    text_rank_words_10_test = get_text_rank_words_10_test(files = files)# 範例[[('毀滅', 'V'), ('聯盟', 'N'), ('相逢', 'V')], []] 10部測試電影依順序, 共300words
    
    sentences = get_sentences(files = files)
    w2v_model = get_w2v_model(sentences = sentences)
    
    TSModel = TS(corpus, w2v_model)
    TOModel = TO(corpus)
    TLModel = TL(corpus)
    logging.info('Construct models: term selection, term ordering, title length')

    pause_for_start_to_generate_titles()

    generated_words_10_test = TSModel.gen_words_num_test(text_rank_words_10_test, each_trained_words_num = 5)
    generated_terms_titles_10_test = TOModel.gen_terms_titles_num_test(generated_words_10_test, candidates_num = 120)
    generated_title_10_test = TLModel.gen_title_num_test(generated_terms_titles_10_test)

    with open('output.txt', 'w', encoding = 'UTF-8') as fw:
        for i in range(len(generated_title_10_test)):
            print(files[i].rstrip('.srt'), generated_title_10_test[i], sep = '\t')
            fw.write('\t'.join([files[i].rstrip('.srt'), generated_title_10_test[i]]) + '\n')
        logging.info('Write to ouput.txt')


if __name__ == "__main__":
    main()
