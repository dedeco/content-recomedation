import pandas as pd
import numpy
import operator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class ContentEngine(object):

	def __init__(self):
		self.data = {}

	def train(self, aluno, query_cursos):
		df = pd.read_sql(query_cursos.statement,query_cursos.session.bind)
		dfaluno = pd.DataFrame([aluno.resumo],columns=['descricao'])
		r = pd.concat([dfaluno, df], ignore_index=True)
		
		self.data[aluno.id] = self._train(r)

	def _train(self, df):

		cursos_recomendados = {}

		tf = TfidfVectorizer()
		tfidf_matrix = tf.fit_transform(df['descricao'])
		
		resultado = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)

		for index, row in df[1:].iterrows():
			for (x,y), value in numpy.ndenumerate(resultado):
				if index == y:
					cursos_recomendados[index] = value

		cursos_recomendados = sorted(cursos_recomendados.items(), key=operator.itemgetter(1),reverse=True)

		return cursos_recomendados

	def predict(self, aluno_id, num):
		item = self.data[aluno_id]
		return item[:num]


content_engine = ContentEngine()