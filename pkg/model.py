# -*- coding: utf-8 -*-
import math

class Model():
	def __init__(self, corpus):
		self.corpus = dict(corpus)
		self.movie_num = len(self.corpus['movie'])
		self.titles = list(self.corpus['movie'].keys()) # list type
		self.terms_of_titles = [['不可能的', '任務'], ['露西']] # 斷詞後

	
	def score(self):
		print('score')

class TermSelection(Model):
	def __init__(self, corpus):
		super().__init__(corpus)
	
	def score(self):
		super().score()

	def words(self, length):
		return ['神鬼', '聯盟']

class TermOrdering(Model):
	def __init__(self, corpus, words):
		super().__init__(corpus)
		self.words = words
		self.pos = {'N': ['飯', '麵'], 'V', ['吃']} # 將words依詞性分類

	def gen_titles(self):
		generated_titles = []
		return generated_titles

	def score(self):
		super().score()

	def gen_n_gram(self):
		tri_gram = {}
		trigram['(N, V)'] = 5
		

class TitleLength(Model):
	def __init__(self, corpus, generated_titles):
		super().__init__(corpus)
		self.generated_titles = generated_titles
		self.lenterms_of_titles = [len(t) for t in self.title_terms]
		self.lenchars_of_titles = [len(t) for t in self.titles]	
		self.g1 = 1
		self.g2 = 1

	def gen_title(self):
		scores = [self.score(t) for t in self.generated_titles]
		return self.generated_titles[scores.index(max(scores))]

	def score(self, title):
		super().score()
		terms = ['產生', '標題的', '斷', '詞']
		lenterms = len(terms)
		lenchars = len(title)
		N = self.movie_num
		P_term = same_lenterms_num(lenterms) / N
		P_char = same_lenchars_num(lenchars) / N

		return math.log(math.pow(P_term, self.g1) * math.pow(P_char, self.g2), 2)
	
	def same_lenchars_num(self, lenchars):
		num = 0
		for length in self.lenchars_of_titles:
			if lenchars == length:
				num = num + 1
		return num

	def same_lenterms_num(self, lenterms):
		num = 0
		for length in self.lenterms_of_titles:
			if lenterms == length:
				num = num + 1
		return num

class TitleLength2(Model): # 暫時不用, 尚未完全
	def __init__(self, corpus, titles):
		super().__init__(corpus)
		self.lenterms_of_titles = [len(t) for t in self.title_terms]
		self.lenchars_of_titles = [len(t) for t in self.titles]

	def get_maxlen_pairs(self):
		maxlen_pairs = []
		maxlen_terms = get_max_cnt_lengths(self.lenterms_of_titles)
		maxlen_chars = get_max_cnt_lengths(self.lenchars_of_titles)
		for lenterms in maxlen_terms:
			for lenchars in maxlen_chars:
				maxlen_pairs.append((lenterms, lenchars))
		return maxlen_pairs

	def get_maxcnt_lengths(self, lenelement_of_titles):
		cnt = {}
		maxcnt_lengths = []

		for len in lenelement_of_titles:
			cnt[len] = cnt.get(len, 0) + 1
		
		maxcnt = max(cnt.values())
		for k, v in cnt.items():
			if v == maxcnt:
				maxcnt_lengths.append(k)

		return maxcnt_lengths

