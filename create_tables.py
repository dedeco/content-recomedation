#!/usr/bin/env python
# -*- coding: utf-8 -*-
from database import Unidade
from database import Base, engine, session

def create_tables():
	#Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)

if __name__ == "__main__":
	print ('Criando tabelas...')
	create_tables()
	print ('Pronto!')