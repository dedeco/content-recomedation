from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI_mysql = 'mysql://recouser:recopass@localhost/recodb?charset=utf8'
#DATABASE_URI_sqlite = 'sqlite:///////Users/dedeco/Projetos/scrp-andre/Sample.db'

engine = create_engine(DATABASE_URI_mysql)
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

class Curso(Base):
	__tablename__ = 'cursos'
	id = Column(Integer(), primary_key = True)
	nome_curso = Column(String(255),)
	descricao = Column(Text)
	texto = Column(Text)
	link = Column(String(255))
	unidade_id = Column(Integer(), ForeignKey('unidades.id'), nullable=False)

class AreaConhecimento(Base):
	__tablename__ = 'areas_conhecimentos'
	id = Column(Integer(), primary_key = True)
	area_conhecimento = Column(String(255))
	curso_id = Column(Integer(), ForeignKey('cursos.id'), nullable=False)

class Objetivo(Base):
	__tablename__ = 'objetivos'
	id = Column(Integer(), primary_key = True)
	objetivo = Column(String(4000))
	curso_id = Column(Integer(), ForeignKey('cursos.id'), nullable=False)

class Programa(Base):
	__tablename__ = 'programas'
	id = Column(Integer(), primary_key = True)
	programa = Column(String(4000))
	curso_id = Column(Integer(), ForeignKey('cursos.id'), nullable=False)

class Unidade(Base):
	__tablename__ = 'unidades'
	id = Column(Integer(), primary_key = True)
	unidade = Column(String(80), unique=True)

class  Alvo(Base):
	__tablename__ = 'alvos'
	id = Column(Integer(), primary_key = True)
	nome = Column(String(150))
	titulo = Column(String(250))
	localizacao = Column(String(150))
	setor = Column(String(150))
	numconexao = Column(String(10))
	formacao = Column(String(200))
	curso = Column(String(350))
	link = Column(String(200))
	resumo = Column(Text)
