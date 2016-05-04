#!/usr/bin/env python
# -*- coding: utf-8 -*-

def question8_function(r, cursor):
	nome = raw_input("Dijite o nome: ")
	email = raw_input("Dijite o email: ")
	cpf = raw_input("Dijite o cpf: ")
	rg = raw_input("Dijite o rg: ")
	tel = raw_input("Dijite o telefone: ")
	cel = raw_input("Dijite o celular: ")

	#VAMOS PEGAR A LISTA DE ESTADOS
	print "Escolha o estado:"
	cursor.execute("SELECT cd_uf, ds_uf_nome FROM uf")
	dados = cursor.fetchall()
	for dado in dados:
		print "%s - %s" %(dado['cd_uf'],dado['ds_uf_nome'])
	estado = raw_input("Escolha o valor do estado: ")


	#VAMOS ADICIONAR A CIDADE
	cursor.execute("SELECT cd_cidade,ds_cidade_nome FROM cidades WHERE uf_cd_uf = %s" %estado)
	dados = cursor.fetchall()
	print "Escolha a cidade:"
	for dado in dados:
		print "%s - %s" %(dado['cd_cidade'],dado['ds_cidade_nome'])
	cidade = raw_input("Escolha o codigo da cidade: ")

	#Adicionar o bairro
	print "Escolha o bairro:"
	cursor.execute("SELECT cd_bairro,ds_bairro_nome FROM bairros WHERE cidade_cd_cidade = %s" %cidade)
	dados = cursor.fetchall()
	for dado in dados:
		print "%s - %s" %(dado['cd_bairro'],dado['ds_bairro_nome'])
	bairro = raw_input("Escolha o codigo do Bairro: ")

	#Vamos finalmente adicionar o logradouro
	print "Escolha a rua:"
	cursor.execute("SELECT cd_logradouro,ds_logradouro_nome FROM logradouro WHERE bairros_cd_bairro = %s" %bairro)
	dados = cursor.fetchall()
	for dado in dados:
		print "%s - %s" %(dado['cd_logradouro'],dado['ds_logradouro_nome'])
	logradouro = raw_input("Escolha o codigo da Rua: ")

	#VAMOS POVOAR O REDIS

	#Criar novo cpf
	usuario = {}
	usuario['cpf'] = cpf
	usuario['rg'] = rg
	usuario['nome'] = nome
	usuario['email'] = email
	usuario['tel'] = tel
	usuario['cel'] = cel
	usuario['log_cd_logradouro'] = logradouro

	r.hmset('cpf:'+cpf,usuario)
	cursor.execute("INSERT INTO cad_usuario SET cpf = '%s', rg = '%s', nome = '%s', email = '%s', tel = '%s', cel = '%s', log_cd_logradouro = '%s' " %(cpf,rg,nome,email,tel,cel,logradouro))

	cpfs = r.get('cpf')
	r.set('cpf',cpfs+',%s' %cpf)
	if (r.get('estado:'+estado)):
		string = "%s,%s" %(cpf,r.get('estado:'+estado))
		r.set('estado:'+estado,string)
	else:
		r.set('estado:'+estado,cpf)
	estados = str(r.get('estados')).split(',')
	if estado not in estados:
		estados.append(estado)
		r.set('estados',','.join(estados))
	r.set('cpf:'+cpf+':pedidos','')
	
	
