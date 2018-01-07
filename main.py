# -*- coding: utf-8 -*-
from pkg.model import TermSelection as TS
from pkg.model import TermOrdering as TO
from pkg.model import TitleLength as TL

corpus = {
    '電影名': {
        '復仇者聯盟': {
            '斷詞': ['復仇者', '聯盟'],
            '斷詞命名實體': [False, False], # 應該可不用??放了避免發現哪裡有需要
            '斷詞詞性': ['N', 'N']
        },
        '瑪莉是瑪莉': {
            '斷詞': ['瑪莉', '是', '瑪莉'],
            '斷詞命名實體': [True, False, True],
            '斷詞詞性': ['N', 'V', 'N']
        },
        '瑪莉': {
            '斷詞': ['瑪莉'],
            '斷詞命名實體': [True],
            '斷詞詞性': ['N']
        }
    },
    '詞訊' = {
        '瑪莉': {
            '詞性': 'N', # 應該可不用??放了避免發現哪裡有需要
            '命名實體': True,
            '詞在電影名': {
                '瑪莉是瑪莉': 2
                '瑪莉': 1
            },
            '詞在電影字幕': {
                '瑪莉是瑪莉': 2000
                '瑪莉': 10000
            }
        },
        '復仇者': {
            ...
        }
    }
}
tf_idf_words_10_test = [[('毀滅', 'V'), ('聯盟', 'N'), ('相逢', 'V')], []] # 10部測試電影, 共3000words

TSModel = TS(corpus)
TOModel = TO(corpus)
TLModel = TL(corpus)

generated_words_10_test = TSModel.gen_words_num_test(tf_idf_words_10_test, 100)
generated_terms_titles_10_test = TOModel.gen_terms_titles_num_test(generated_words_10_test, 200)
generated_title_10_test = TLModel.gen_title_num_test(generated_terms_titles_10_test)

for i in range(len(generated_title_10_test)):
    print(filename[i], generated_title_10_test[i], sep = '\t')