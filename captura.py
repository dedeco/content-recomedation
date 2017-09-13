#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os
import re

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from database import Unidade, Curso, AreaConhecimento, Objetivo, Programa
from database import Base, engine, session

def init_Chrome():
	driver = "/Users/dedeco/Apps/chromedriver"
	os.environ["webdriver.chrome.driver"] = driver
	b = webdriver.Chrome(driver)	
	return b

def init_PhantomJS():
	return webdriver.PhantomJS()

def captura(url):

	b = init_Chrome()

	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')

	div = soup.find('div', {'id': 'ctl00_ctl44_g_72171b7e_5580_4b7d_aff0_6ea6fb733bbf_ctl00_divResultado'})
	children = div.findChildren()
	for child in children:

		print (child.name,'%%%%%%%%%%') 


		if child.name=='h3':
			u = Unidade()
			u.unidade = child.text
			session.add(u)
			session.commit()
			print ('Unidade:',u.unidade)

		if child.name=='a':
			l = child['href']
			b.get(l)
			#b.implicitly_wait(5)
			sp_curso = BeautifulSoup(b.page_source, 'html.parser')

			try:
				curso = sp_curso.select_one('h2.puc-pl-titulo-pg').text.strip()
			except AttributeError:
				continue

			ac = sp_curso.select_one('.puc-pl-pos-graduacao-conteudo-area-conhecimento ul') 

			conhecimentos = []
			for litag in ac.find_all('li'):
				conhecimentos.append(litag.text)

			div = sp_curso.find(id="ctl00_PlaceHolderMain_ctl08__ControlWrapper_RichHtmlField")
			texto = ''

			ptags = div.find_all("p")
			for tag in ptags:
				if len(tag.text) > 20:
					texto += '\r' + tag.text

			spantags = div.find_all("span")
			for tag in spantags:
				if len(tag.text) > 20:
					texto += '\r' + tag.text

			divs = div.find_all("div")
			for tag in divs:
				if len(tag.text) > 20:
					texto += "\r" + tag.text

			try:
				m = re.search('(.*)\\s*(?=Área)', texto)
				descricao = m.group(0)
			except AttributeError:
				descricao = None
				pass

			c = Curso()
			c.nome_curso = curso
			c.descricao = descricao
			c.texto = texto
			c.link = l
			c.unidade_id = 1

			print ('Curso:',curso)

			session.add(c)
			session.flush()

			#try:
			for co in conhecimentos:
				a = AreaConhecimento()
				a.area_conhecimento = co
				a.curso_id = c.id
				session.add(a)
			#except:
			#	print ('Erro para inserir area de conhecimento')

			ultags = div.find_all("ul")

			obj = []
			try:
				for litag in ultags[0].find_all('li'):
					obj.append(litag.text)
			except IndexError:
				print ('Erro para inserir objetivos')
				pass

			for i in obj:
				o = Objetivo()
				o.objetivo = i
				o.curso_id = c.id
				session.add(o)

			programa = []
			try:
				for litag in ultags[1].find_all('li'):
					programa.append(litag.text)
			except IndexError:
				print ('Erro para inserir programa')
				pass

			for i in programa:
				p = Programa()
				p.programa = i
				p.curso_id = c.id
				session.add(p)

			session.commit()

		#b.quit()

if __name__ == "__main__":
	url = "http://www.pucminas.br/Pos-Graduacao/IEC/modalidades/latusensu/Paginas/Especializa%C3%A7%C3%A3o%20e%20Master.aspx"
	captura(url)

