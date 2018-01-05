# -*- coding: utf-8 -*-
import math

class Model():
	def __init__(self, corpus):
		self.corpus = dict(corpus)
		self.num_of_movies = len(self.corpus['movie']) 
	
	def score(self):
		print('score')

	def corpus(self):
		return self.corpus
	
	def movie_num(self):
		return self.num_of_movies

class TermSelection(Model):
	def __init__(self, corpus):
		super().__init__(corpus)
	
	def score(self):
		super().score()

	def words(self, length):
		return ['神鬼', '聯盟']

class TermOrdering(Model):
	def __init__(self, corpus):
		super().__init__(corpus)

	def score(self):
		super().score()

class TitleLength(Model):
	def __init__(self, corpus, titles):
		super().__init__(corpus)
		self.titles = titles # list type
		self.terms_of_titles = [['不可能的', '任務'], ['露西']]
		self.lenterms_of_titles = [len(t) for t in self.title_terms]
		self.lenchars_of_titles = [len(t) for t in self.titles]	
		self.g1 = 1
		self.g2 = 1

	def gen_title():
		scores = [score(t) for t in self.titles]
		return self.titles[scores.index(max(scores))]

	def score(self, title):
		super().score()
		terms = terms_of_titles[self.titles.index(title)]
		lenterms = len(terms)
		lenchars = len(title)
		N = super().movie_num()
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

