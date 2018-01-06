# -*- coding: utf-8 -*-
from pkg.model import TermSelection as TS
from pkg.model import TermOrdering as TO
from pkg.model import TitleLength as TL

corpus = {
    '電影名': {
        '復仇者聯盟': {
            '電影名斷詞': ['復仇者', '聯盟']
            '電影名斷詞詞性': ['N', 'N']
            '字': ['我', '打']
            '字詞性': ['N', 'V']
            '字數量': ['1000', '50']
        }

    }
}
tf_idf_words_10_test = [[('毀滅', 'V'), ('聯盟', 'N'), ('相逢', 'V')], []] # 10部測試電影, 共3000words

TSModel = TS(corpus)
TOModel = TO(corpus)
TLModel = TL(corpus)

generated_words_10_test = TSModel.gen_words_num_test(tf_idf_words_10_test, 5)
generated_terms_titles_10_test = TOModel.gen_terms_titles_num_test(generated_words_10_test, 200)
generated_title_10_test = TLModel.gen_title_num_test(generated_terms_titles_10_test)

for i in range(len(generated_title_10_test)):
    print(filename[i], generated_title_10_test[i], sep = '\t')