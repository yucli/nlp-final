# -*- coding: utf-8 -*-
from pkg.model import TermSelection as TS

corpus = {
    'movie': {
        '哈嗚': ['哈哈哈', '嗚嗚嗚']
    }
}
TSModel = TS(corpus)
TSModel.score()