# -*- coding: utf-8 -*-
import math

class Model():
	def __init__(self, corpus):
		self.corpus = dict(corpus)
		self.movie_num = len(self.corpus['電影名'])
		self.titles = list(self.corpus['電影名'].keys()) # list type
		self.terms_of_titles = [self.corpus['電影名'][t]['電影名斷詞'] for t in titles] # 斷詞後
		self.pos_of_terms_of_titles = [self.corpus['電影名'][t]['電影名斷詞詞性'] for t in titles] # 斷詞後

class TermSelection(Model):
	def __init__(self, corpus):
		super().__init__(corpus)

	def gen_words_num_test(self, tf_idf_words_num_test, length):
		generated_words_num_test = [[('毀滅', 'V'), ('聯盟', 'N'), ('相逢', 'V')], []]
		return list(generated_words_num_test)

class TermOrdering(Model): # classified_by_pos 尚未, 得依賴於generated_words_num_test
	def __init__(self, corpus):
		super().__init__(corpus)
		self.train_pos_distribution = {}
		
		for pos_of_terms in self.pos_of_terms_of_titles:
			tuple_pos_of_terms = tuple(pos_of_terms)
			self.train_pos_distribution[tuple_pos_of_terms] = self.train_pos_distribution.get(tuple_pos_of_terms, 0) + 1
		
		for tuple_pos_of_terms, count in self.train_pos_distribution.items():
			self.train_pos_distribution[tuple_pos_of_terms] = count / self.movie_num
		# 如 train_pos_distribution[('V', 'N')] = 5 / 54
	def gen_terms_titles_num_test(self, generated_words_num_test, number_of_candidates):
		generated_terms_titles_num_test = []
		
		for test in generated_words_num_test:
			classified_by_pos = {} # 如{'V': ['毀滅', '相逢'], 'N', ['聯盟']} 將words依詞性分類, 且其有相似度的順序
			generated_terms_titles_num_test.append(self.gen_terms_titles(classified_by_pos = classified_by_pos, number_of_candidates = number_of_candidates)) # 如 [['毀滅', '聯盟'], ['相逢', '聯盟']]
		
		return list(generated_terms_titles_num_test)

	def gen_terms_titles(self, classified_by_pos, number_of_candidates):
		terms_titles = []
		
		for ordered_pos_s, probability in self.train_pos_distribution.items():
			ordered_pos_s_needed_number = int(number_of_candidates * probability)
			terms_titles.extend(self.gen_needed_terms_titles(classified_by_pos = classified_by_pos, ordered_pos_s = ordered_pos_s, ordered_pos_s_needed_number = ordered_pos_s_needed_number))

		if len(terms_titles) == 0:
			for ordered_pos_s, probability in self.train_pos_distribution.items():
				ordered_pos_s_needed_number = int(number_of_candidates * probability)
				for pos_words in classified_by_pos:
					terms_titles.extend(pos_words[:ordered_pos_s_needed_number])

		return terms_titles

	def gen_needed_terms_titles(self, classified_by_pos, ordered_pos_s, ordered_pos_s_needed_number):
		generated_needed_terms_titles = []
		
		length_of_each_pos = []
		for pos in ordered_pos_s:
			if pos not in classified_by_pos.keys():
				return []
			length_of_each_pos.append(len(classified_by_pos[pos]))
		
		generated_needed_terms_titles_length = 1
		for number in range(len(length_of_each_pos)):
			generated_needed_terms_titles_length *= number

		for i in range(generated_needed_terms_titles_length):
			generated_needed_terms_titles.append([])

		every_length = generated_needed_terms_titles_length # 共幾個基礎下, 表every
		for reverse in reversed(range(len(length_of_each_pos))): # 假如最後的字較重要
			pos = ordered_pos_s[reverse]
			pos_words_length = length_of_each_pos[reverse] # 或 len(classified_by_pos[pos])
			in_length = every_length / pos_words_length #every中有幾個
			# insert
			iterate_times = generated_needed_terms_titles_length / every_length
			for i in range(pos_words_length):
				word = classified_by_pos[pos][i]
				insert_positions = []

				for time in range(iterate_times):
					start = (time * every_length) + (i * in_length)
					end = (time * every_length) + ((i + 1) * in_length)
					insert_positions.extend(list(range(start, end)))

				for position in insert_positions:
					generated_needed_terms_titles[position].insert(0, word)

			# 完
			every_length = in_length # 更新基礎
			
		return generated_needed_terms_titles[:ordered_pos_s_needed_number]

class TitleLength(Model):
	def __init__(self, corpus):
		super().__init__(corpus)
		self.lenterms_of_titles = [len(t) for t in self.terms_of_titles]
		self.lenchars_of_titles = [len(t) for t in self.titles]	
		self.g1 = 1
		self.g2 = 1

	def gen_title_num_test(self, generated_terms_of_titles_num_test):
		generated_num_test = []

		for test in generated_terms_of_titles_num_test:
			scores = [self.compute_score(terms = terms) for terms in test]
			generated_num_test.append(''.join(test[scores.index(max(scores))]))
		
		return generated_num_test

	def compute_score(self, terms):
		super().score()
		title = ''.join(terms)
		lenterms = len(terms)
		lenchars = len(title)
		N = self.movie_num
		# 加1避免0在log的錯誤
		P_term = (self.get_same_lenterms_num(lenterms = lenterms) + 1 ) / N
		P_char = (self.get_same_lenchars_num(lenchars = lenchars) + 1 ) / N

		return math.log(math.pow(P_term, self.g1) * math.pow(P_char, self.g2), 2)
	
	def get_same_lenchars_num(self, lenchars):
		num = 0
		
		for length in self.lenchars_of_titles:
			if lenchars == length:
				num += 1
		
		return num

	def get_same_lenterms_num(self, lenterms):
		num = 0
		
		for length in self.lenterms_of_titles:
			if lenterms == length:
				num += 1
		
		return num