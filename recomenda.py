from engines import content_engine
from database import session, engine
from database import Curso, Alvo
import time

def info(msg):
	print(msg)

def treinamento():
	start = time.time()
	alvos = session.query(Alvo).filter(Alvo.resumo != None)

	for aluno in alvos:
		#print (aluno.nome)
		content_engine.train(aluno, session.query(Curso).filter(Curso.descricao != None).order_by(Curso.id))

	info("Engine trained in %s seconds." % (time.time() - start))

def recomeda():
	alvos = session.query(Alvo).filter(Alvo.resumo != None)

	for aluno in alvos:
		print ("ALUNO: %s" %aluno.nome)
		print (aluno.resumo)

		print ("TOP 3 CURSOS INDICADOS:")

		resultado = content_engine.predict(aluno.id,3)

		for curso_id, cosine_similarity in resultado:
			c = session.query(Curso).filter_by(id=curso_id).one()
			if c:
				print ('%s (%s)' % (c.nome_curso,cosine_similarity) )

		print ("###############")

if __name__ == '__main__':
	treinamento()
	recomeda()
