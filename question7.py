#!/usr/bin/env python
# -*- coding: utf-8 -*-

def question7_function(r, cursor):
	
	print(chr(27) + "[2J")

	## Para apresentacao o cursor ira percorrer e apresentar todas as opcoes de estado!
	cursor.execute("""SELECT * FROM uf""")
	dados_estado = cursor.fetchall()
	lista_estado = []
	estado_index = 0

	print "-----"
	for estado in dados_estado:
		estado_index += 1
		lista_estado.append(['ds_uf_nome'])
		print "%d - %s" %(estado_index, estado['ds_uf_nome'])
		
	print "-----\n"
	estado_escolha = raw_input ("Por favor, digite o UF do estado que deseja buscar: ")
	estado_escolha_str = str(estado_escolha)
	estado_escolha_str.upper()
	
	cursor.execute(""" SELECT * FROM logradouro lo 
	INNER JOIN bairros ba ON(lo.bairros_cd_bairro = ba.cd_bairro)
	INNER JOIN cidades ci ON (ba.cidade_cd_cidade = ci.cd_cidade)
	INNER JOIN uf ON (ci.uf_cd_uf = cd_uf)
	WHERE ds_uf_sigla = "%s" """ %estado_escolha_str)
	dados = cursor.fetchall()
	
	for dado in dados:
		print "%s - %s - %s" %(dado['cd_logradouro'], dado['cd_tipo_logradouro'], dado['ds_logradouro_nome'])
	
	
