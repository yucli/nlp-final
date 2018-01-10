# -*- coding: utf-8 -*-
import math

class Model():
	def __init__(self, corpus):
		self.corpus = corpus
		self.movie_num = len(self.corpus['movie_title'])

class TermSelection(Model):
	def __init__(self, corpus, w2v_model):
		super().__init__(corpus)
		self.w2v_model = w2v_model
		self.word_info = self.corpus['word_info']  # word_info之後與text_rank_words_num_test做處理
		self.selection_score = {} # selection_score['聯盟'] == 9487
		self.pos_score = 0.08 # 給pos分, 目前假如是n (0.08 * 1.2 = 0.096), v(0.08)
		self.ne_score = 0.22 # 暫時
		self.title_score = {}
		self.g_score = {} # 自己的nbl變形
		# self.r_score = {} # 暫時去掉
		self.construct_scores()

	def gen_words_num_test(self, text_rank_words_num_test, each_trained_words_num):
		generated_words_num_test = []
		trained_words = self.get_highest_scores_words(each_trained_words_num = each_trained_words_num)
		test_words_num = each_trained_words_num * 3
		
		for test in text_rank_words_num_test:
			generated_words_num_test.append(self.gen_words(
				test = test, 
				test_words_num = test_words_num, 
				trained_words = trained_words))

		# generated_words_num_test = [[('毀滅', 'V'), ('聯盟', 'N'), ('相逢', 'V')], []]		

		return list(generated_words_num_test)

	def gen_words(self, test, test_words_num, trained_words):
		generated_words = self.gen_words_sorted_by_similarity(test = test, trained_words = trained_words)
		return generated_words[:test_words_num]

	def gen_words_sorted_by_similarity(self, test, trained_words):
		generated_words_sorted_by_similarity = []
		temp_dictionary = {}
		
		for word, pos in test:
			for trained_word in trained_words:
				temp_dictionary[(word, pos, trained_word)] = self.w2v_model.similarity(word, trained_word)
				# print(word, trained_word, temp_dictionary[(word, pos, trained_word)])
		
		temp_sorted_list = sorted(temp_dictionary.items(), key = lambda d: d[1], reversed = True)
		generated_words_sorted_by_similarity = [(triple_cos[0][0], triple_cos[0][1]) for triple_cos in temp_sorted_list] # tripler_cos == (('w', 'w_pos', 'test_w'), cos_value)
		return generated_words_sorted_by_similarity

	def construct_scores(self):
		for word in self.word_info.keys():
			self.get_selection_score(word)
		# print(self.selection_score)
	
	def get_highest_scores_words(self, each_trained_words_num):
		scores_words_sorted_by_score = sorted(self.selection_score.items(), key = lambda d: d[1], reverse = True)
		scores_words_sorted_by_score = [word for word, score in scores_words_sorted_by_score]
		words_num = self.movie_num * each_trained_words_num
		return scores_words_sorted_by_score[:words_num]
	
	def get_selection_score(self, word):
		if word not in self.selection_score.keys():
			self.selection_score[word] = self.get_pos_score(word) \
				+ self.get_ne_score(word) \
				+ math.log(self.get_title_score(word = word) * self.get_g_score(word = word), 10) # \
				# + self.get_r_score(word = word)
		
		return self.selection_score[word]

	def get_pos_score(self, word):
		word_pos_score = 0
		
		if self.word_info[word]['pos'] in ['n', 'v']:
			word_pos_score = self.pos_score
			if self.word_info[word]['pos'] == 'n':
				word_pos_score *= 1.2
		
		return word_pos_score

	def get_ne_score(self, word):
		word_ne_score = 0
		
		if self.word_info[word]['ne'] == True:
			word_ne_score = self.ne_score

		return word_ne_score

	def get_title_score(self, word):
		if word not in self.title_score.keys():
			self.title_score[word] = (len(self.word_info[word]['word_in_titles']) + 1) / (len(self.word_info[word]['word_in_subs']) + 1)# 各加1避免0在log的錯誤

		return self.title_score[word]

	def get_g_score(self, word):
		if word not in self.g_score.keys():
			self.g_score[word] = self.get_g_score_numerator(word = word) / self.get_g_score_denominator(word = word)

		return self.g_score[word]

	"""
	def get_r_score(self, word):
		if word not in self.r_score.keys():
			self.r_score[word] =  self.get_title_score(word = word) + self.get_g_score(word = word)
		
		return self.r_score[word]
	"""

	def get_g_score_numerator(self, word):
		# 加1避免0在log的錯誤
		numerator = 1
		movies_name = []

		for name in self.word_info[word]['word_in_titles'].keys():
			if name not in movies_name:
				movies_name.append(name)
		
		for name in self.word_info[word]['word_in_subs'].keys():
			if name not in movies_name:
				movies_name.append(name)
		
		for name in movies_name:
			numerator += self.word_info[word]['word_in_titles'].get(name, 0) \
				* self.word_info[word]['word_in_subs'].get(name, 0)
		
		return numerator

	def get_g_score_denominator(self, word):
		# 加1避免除0錯誤
		denominator = len(self.word_info[word]['word_in_subs']) + 1
		return denominator


class TermOrdering(Model):
	def __init__(self, corpus):
		super().__init__(corpus)
		self.titles = list(self.corpus['movie_title'].keys())
		self.terms_pos_titles = [self.corpus['movie_title'][t]['pos'] for t in self.titles]
		self.distro_pos = {} # distro means distribution		
		
		for terms_pos in self.terms_pos_titles:
			tuple_terms_pos = tuple(terms_pos)
			self.distro_pos[tuple_terms_pos] = self.distro_pos.get(tuple_terms_pos, 0) + 1
		
		for tuple_terms_pos, count in self.distro_pos.items():
			self.distro_pos[tuple_terms_pos] = count / self.movie_num
		# 如 distro_pos[('V', 'N')] = 5 / 54
	def gen_terms_titles_num_test(self, generated_words_num_test, candidates_num):
		generated_terms_titles_num_test = []
		
		distro_pos_sorted_by_probability = sorted(self.distro_pos.items(), key = lambda d: d[1], reverse = True)
		for test in generated_words_num_test:
			classified_by_pos = self.gen_classified_by_pos(test = test) # 如{'V': ['毀滅', '相逢'], 'N', ['聯盟']} 將words依詞性分類, 且其有相似度的順序
			generated_terms_titles_num_test.append(self.gen_terms_titles(
				classified_by_pos = classified_by_pos, 
				candidates_num = candidates_num,
				distro_pos_sorted_by_probability = distro_pos_sorted_by_probability))
		
		return list(generated_terms_titles_num_test)

	def gen_classified_by_pos(self, test):
		generated_classified_by_pos = {}

		for word, pos in test:
			if pos not in generated_classified_by_pos.keys():
				generated_classified_by_pos[pos] = list(word)
			else:
				generated_classified_by_pos[pos].append(word)

		return generated_classified_by_pos

	def gen_terms_titles(self, classified_by_pos, candidates_num, distro_pos_sorted_by_probability):
		terms_titles = [] # 如 [['毀滅', '聯盟'], ['相逢', '聯盟']]

		for ordered_pos, probability in distro_pos_sorted_by_probability:
			ordered_pos_needed_num = int(candidates_num * probability)
			terms_titles.extend(self.gen_needed_terms_titles(
				classified_by_pos = classified_by_pos, 
				ordered_pos = ordered_pos, 
				ordered_pos_needed_num = ordered_pos_needed_num))

		if len(terms_titles) == 0:
			for ordered_pos, probability in distro_pos_sorted_by_probability:
				ordered_pos_needed_num = int(candidates_num * probability)
				last_pos = ordered_pos[-1] # 假如最後的字較重要
				last_pos_words = classified_by_pos[last_pos]
				needed_num_last_pos_words = last_pos_words[:ordered_pos_needed_num]
				for word in needed_num_last_pos_words:
					word_term_title = list(word)
					if word_term_title not in terms_titles:
						terms_titles.append(word_term_title)

		return terms_titles

	def gen_needed_terms_titles(self, classified_by_pos, ordered_pos, ordered_pos_needed_num):
		generated_needed_terms_titles = []
		
		each_pos_words_length = []
		for pos in ordered_pos:
			if pos not in classified_by_pos.keys():
				return []
			each_pos_words_length.append(len(classified_by_pos[pos]))
		
		generated_needed_terms_titles_length = 1
		for num in each_pos_words_length:
			generated_needed_terms_titles_length *= num

		for i in range(generated_needed_terms_titles_length):
			generated_needed_terms_titles.append([])

		every_length = generated_needed_terms_titles_length # 共幾個基礎下, 表every
		for reverse in reversed(range(len(each_pos_words_length))): # 假如最後的字較重要
			pos = ordered_pos[reverse]
			pos_words_length = each_pos_words_length[reverse] # 或 len(classified_by_pos[pos])
			in_length = int(every_length / pos_words_length) #every中有幾個
			# insert
			iterate_times = int(generated_needed_terms_titles_length / every_length)
			for i in range(pos_words_length):
				word = classified_by_pos[pos][i]
				insert_positions = []

				for time in range(iterate_times):
					start = (time * every_length) + (i * in_length)
					end = (time * every_length) + ((i + 1) * in_length)
					insert_positions.extend(list(range(start, end))) # argument can be range(start, end)

				for position in insert_positions:
					generated_needed_terms_titles[position].insert(0, word)

			# 完
			every_length = in_length # 更新基礎

		# remove duplicate words
		for title_i in range(len(generated_needed_terms_titles)):
			for word in generated_needed_terms_titles[title_i]:
				if generated_needed_terms_titles[title_i].count(word) > 1:
					generated_needed_terms_titles[title_i]
					break
		generated_needed_terms_titles = [t for t in generated_needed_terms_titles if t != []]
		
		return generated_needed_terms_titles[:ordered_pos_needed_num]

class TitleLength(Model):
	def __init__(self, corpus):
		super().__init__(corpus)
		self.titles = list(self.corpus['movie_title'].keys())
		self.terms_titles = [self.corpus['movie_title'][t]['word'] for t in self.titles]		
		self.titles_lenchars = [len(t) for t in self.titles]
		self.titles_lenterms = [len(t) for t in self.terms_titles]
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
		p_char = (self.get_same_lenchars_num(lenchars = lenchars) + 1 ) / N
		p_term = (self.get_same_lenterms_num(lenterms = lenterms) + 1 ) / N

		return math.log(math.pow(p_term, self.g1) * math.pow(p_char, self.g2), 2)
		# return math.log(math.pow(p_term, self.g1), 2)
	
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