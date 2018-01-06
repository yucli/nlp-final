# -*- coding: utf-8 -*-
import math

class Model():
	def __init__(self, corpus):
		self.corpus = dict(corpus)
		self.movie_num = len(self.corpus['電影名'])
		self.titles = list(self.corpus['電影名'].keys()) # list type
		self.terms_of_titles = [self.corpus['電影名'][t]['電影名斷詞'] for t in titles] # 斷詞後
		self.pos_of_terms_of_titles = [self.corpus['電影名'][t]['電影名斷詞詞性'] for t in titles] # 斷詞後

	
	def score(self):
		print('score')

class TermSelection(Model):
	def __init__(self, corpus):
		super().__init__(corpus)
	
	def score(self):
		super().score()

	def gen_words_num_test(self, tf_idf_words_num_test, length):
		return list([[('毀滅', 'V'), ('聯盟', 'N'), ('相逢', 'V')], []])

class TermOrdering(Model):
	def __init__(self, corpus):
		super().__init__(corpus)
		self.train_pos_distribution = {}
		for pos_of_terms in self.pos_of_terms_of_titles:
			tuple_pos_of_terms = tuple(pos_of_terms)
			self.train_pos_distribution[tuple_pos_of_terms] = self.train_pos_distribution.get(tuple_pos_of_terms, 0) + 1
		for pos_of_terms in self.pos_of_terms_of_titles:
			tuple_pos_of_terms = tuple(pos_of_terms)
			self.train_pos_distribution[tuple_pos_of_terms] = self.train_pos_distribution.get(tuple_pos_of_terms) / self.movie_num
		# 如 train_pos_distribution[('V', 'N')] = 5 / 54
	def gen_terms_titles_num_test(self, selected_words_num_test, number):
		generated_terms_of_titles_num_test = []
		for test in selected_words_num_test:
			classified_by_pos = {} # 如{'V': ['毀滅', '相逢'], 'N', ['聯盟']} 將words依詞性分類, 且其有相似度的順序
			generated_terms_of_titles_num_test.append(self.gen_terms_titles(classified_by_pos, number)) # 如 [['毀滅', '聯盟'], ['相逢', '聯盟']]
		return list(generated_terms_of_titles_num_test)

	def score(self):
		super().score()

	def gen_terms_titles(self, classified_by_pos, number):
		terms_titles = []
		for ordered_pos_s, probability in self.train_pos_distribution.items():
			needed_count = int(number * probability)
			terms_titles.extend(gen_needed_terms_titles(classified_by_pos, ordered_pos_s, needed_count))
			"""
			temp_terms_titles = []
			while len(temp_terms_titles) != needed_count:
				if add_terms_title(temp_terms_titles, ordered_pos_s, classified_by_pos) == False:
					break
			terms_titles.extend(temp_terms_titles)
			"""
		return terms_titles

	def add_terms_title(self, temp_terms_titles, ordered_pos_s, classified_by_pos):
		terms_title = []
		while len(terms_title) != 1: # 或 == 0
			for pos in ordered_pos_s:
				if pos not in classified_by_pos.keys():
					return False
				terms_title.append(classified_by_pos[pos][])
			if terms_title in temp_terms_titles:
				terms_title = []
			else:
				temp_terms_titles.append(terms_title)
		return True

	def gen_needed_terms_titles(self, classified_by_pos, ordered_pos_s, needed_count):
		generated_needed_terms_titles = []
		
		for pos in ordered_pos_s:
			if pos not in classified_by_pos.keys():
				return []
			length_of_each_pos.append(len(classified_by_pos[pos]))
		
		generated_needed_terms_titles_length = 1
		for pos in ordered_pos_s:
			generated_needed_terms_titles_length *= length_of_each_pos

		generated_needed_terms_titles.extend()
		return generated_needed_terms_titles[:needed_count]

class TitleLength(Model):
	def __init__(self, corpus):
		super().__init__(corpus)
		self.lenterms_of_titles = [len(t) for t in self.terms_of_titles]
		self.lenchars_of_titles = [len(t) for t in self.titles]	
		self.g1 = 1
		self.g2 = 1

	def gen_title_num_test(self, generated_terms_of_titles_num_test):
		gen_titles = []
		for test in generated_terms_of_titles_num_test:
			scores = [self.score(terms) for terms in test]
			gen_titles.append(''.join(test[scores.index(max(scores))]))
		return gen_titles

	def score(self, terms):
		super().score()
		title = ''.join(terms)
		lenterms = len(terms)
		lenchars = len(title)
		N = self.movie_num
		# 加1避免0在log的錯誤
		P_term = (self.same_lenterms_num(lenterms) + 1 ) / N
		P_char = (self.same_lenchars_num(lenchars) + 1 ) / N

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
"""
class TitleLength2(Model): # 暫時不用, 尚未完全
	def __init__(self, corpus, titles):
		super().__init__(corpus)
		self.lenterms_of_titles = [len(t) for t in self.terms_of_titles]
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
"""

