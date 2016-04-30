#!/usr/bin/env python
# -*- coding: utf-8 -*-

def question2_function(r, cursor):
			
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
	estado_escolha = input ("Por favor, digite o código do estado que deseja buscar: ")
	
	if (r.get('estado:'+str(estado_escolha))):
		cpfs = r.get('estado:'+str(estado_escolha)).split(',')
		for cpf in cpfs:
			print ("%s") %(r.hmget('cpf:'+cpf,'nome')[0])
	else:
		print ("Não existem clientes neste estado!")
		
	
