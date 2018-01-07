# -*- coding: utf-8 -*-
import math

class Model():
	def __init__(self, corpus):
		self.corpus = dict(corpus)
		self.movie_num = len(self.corpus['電影名'])
		self.titles = list(self.corpus['電影名'].keys()) # list type
		self.terms_titles = [self.corpus['電影名'][t]['斷詞'] for t in titles] # 斷詞後
		self.terms_pos_titles = [self.corpus['電影名'][t]['斷詞詞性'] for t in titles] # 斷詞後

class TermSelection(Model):
	def __init__(self, corpus):
		super().__init__(corpus)
		self.words_info = self.corpus['詞訊']  # words_info之後與tf_idf_words_num_test做處理
		self.selection_score = {} # selection_score['聯盟'] == 9487
		self.ne_score = 0 # 暫時
		self.title_score = {}
		self.nbl_score = {}
		self.r_score = {}

	def construct_scores(self):
		for word in self.words_info.keys():
			get_selection_score(word)	

	def gen_words_num_test(self, tf_idf_words_num_test, length):
		generated_words_num_test = [[('毀滅', 'V'), ('聯盟', 'N'), ('相逢', 'V')], []]
		return list(generated_words_num_test)
	
	def get_selection_score(self, word):
		if word not in self.selection_score.keys():
			self.selection_score[word] = self.ne_score \
				+ math.log(self.get_title_score(word) * self.get_nbl_score(word), 10) \
				+ self.get_r_score(word)
		
		return self.selection_score[word]

	def get_title_score(self, word):
		if word not in self.title_score.keys():
			self.title_score[word] = (len(self.words_info[word]['詞在電影名']) + 1) \ 
				/ len(self.words_info[word]['詞在電影字幕']) # 加1避免0在log的錯誤

		return self.title_score[word]

	def get_nbl_score(self, word):
		if word not in self.nbl_score.keys():
			self.nbl_score[word] = sum(self.words_info[word]['詞在電影字幕'].values()) \
				* get_word_titles_word_subtitles_p(word)

		return self.nbl_score[word]

	def get_r_score(self, word):
		if word not in self.r_score.keys():
			self.r_score[word] =  self.get_title_score(word) \
				+ self.get_nbl_score(word)
		
		return self.r_score[word]

	def get_word_titles_word_subtitles_p(self, word):
		# 加1避免0在log的錯誤
		numerator = 1
		movies_name = []

		for name in self.words_info[word]['詞在電影名'].keys():
			if name not in movies_name:
				movies_name.append(name)
		
		for name in self.words_info[word]['詞在電影字幕'].keys():
			if name not in movies_name:
				movies_name.append(name)
		
		for name in movies_name:
			numerator += self.words_info[word]['詞在電影名'].get(name, 0) \
				* self.words_info[word]['詞在電影字幕'].get(name, 0)

		denominator = sum(self.words_info[word]['詞在電影字幕'].values())
		
		return numerator / denominator # 暫時有問題, 分母恆等於要相乘的另一項



class TermOrdering(Model): # classified_by_pos 尚未, 得依賴於generated_words_num_test
	def __init__(self, corpus):
		super().__init__(corpus)
		self.distro_pos = {} # distro means distribution
		
		for terms_pos in self.terms_pos_titles:
			tuple_terms_pos = tuple(terms_pos)
			self.distro_pos[tuple_terms_pos] = self.distro_pos.get(tuple_terms_pos, 0) \ 
				+ 1
		
		for tuple_terms_pos, count in self.distro_pos.items():
			self.distro_pos[tuple_terms_pos] = count / self.movie_num
		# 如 distro_pos[('V', 'N')] = 5 / 54
	def gen_terms_titles_num_test(self, generated_words_num_test, candidates_number):
		generated_terms_titles_num_test = []
		
		for test in generated_words_num_test:
			classified_by_pos = {} # 如{'V': ['毀滅', '相逢'], 'N', ['聯盟']} 將words依詞性分類, 且其有相似度的順序
			generated_terms_titles_num_test.append(self.gen_terms_titles(
				classified_by_pos = classified_by_pos, 
				candidates_number = candidates_number)) # 如 [['毀滅', '聯盟'], ['相逢', '聯盟']]
		
		return list(generated_terms_titles_num_test)

	def gen_terms_titles(self, classified_by_pos, candidates_number):
		terms_titles = []
		
		for ordered_pos, probability in self.distro_pos.items():
			ordered_pos_needed_number = int(candidates_number * probability)
			terms_titles.extend(self.gen_needed_terms_titles(
				classified_by_pos = classified_by_pos, 
				ordered_pos = ordered_pos, 
				ordered_pos_needed_number = ordered_pos_needed_number))

		if len(terms_titles) == 0:
			for ordered_pos, probability in self.distro_pos.items():
				ordered_pos_needed_number = int(candidates_number * probability)
				for pos_words in classified_by_pos:
					terms_titles.extend(pos_words[:ordered_pos_needed_number])

		return terms_titles

	def gen_needed_terms_titles(self, classified_by_pos, ordered_pos, ordered_pos_needed_number):
		generated_needed_terms_titles = []
		
		each_pos_words_length = []
		for pos in ordered_pos:
			if pos not in classified_by_pos.keys():
				return []
			each_pos_words_length.append(len(classified_by_pos[pos]))
		
		generated_needed_terms_titles_length = 1
		for number in range(len(each_pos_words_length)):
			generated_needed_terms_titles_length *= number

		for i in range(generated_needed_terms_titles_length):
			generated_needed_terms_titles.append([])

		every_length = generated_needed_terms_titles_length # 共幾個基礎下, 表every
		for reverse in reversed(range(len(each_pos_words_length))): # 假如最後的字較重要
			pos = ordered_pos[reverse]
			pos_words_length = each_pos_words_length[reverse] # 或 len(classified_by_pos[pos])
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
			
		return generated_needed_terms_titles[:ordered_pos_needed_number]

class TitleLength(Model):
	def __init__(self, corpus):
		super().__init__(corpus)
		self.titles_lenterms = [len(t) for t in self.terms_titles]
		self.titles_lenchars = [len(t) for t in self.titles]	
		self.g1 = 1
		self.g2 = 1

	def gen_title_num_test(self, generated_terms_titles_num_test):
		generated_num_test = []

		for test in generated_terms_titles_num_test:
			scores = [self.get_length_score(terms = terms) for terms in test]
			generated_num_test.append(''.join(test[scores.index(max(scores))]))
		
		return generated_num_test

	def get_length_score(self, terms):
		title = ''.join(terms)
		lenterms = len(terms)
		lenchars = len(title)
		N = self.movie_num
		# 加1避免0在log的錯誤
		p_term = (self.get_same_lenterms_num(lenterms = lenterms) + 1 ) / N
		p_char = (self.get_same_lenchars_num(lenchars = lenchars) + 1 ) / N

		return math.log(math.pow(p_term, self.g1) * math.pow(p_char, self.g2), 2)
	
	def get_same_lenchars_num(self, lenchars):
		num = 0
		
		for length in self.titles_lenchars:
			if lenchars == length:
				num += 1
		
		return num

	def get_same_lenterms_num(self, lenterms):
		num = 0
		
		for length in self.titles_lenterms:
			if lenterms == length:
				num += 1
		
		return num