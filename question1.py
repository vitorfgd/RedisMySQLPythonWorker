#!/usr/bin/env python
# -*- coding: utf-8 -*-

def question1_function(r):

	#recebe a pool de cpf do redis
	r_cpf = r.get('cpf')
	cpfs = r_cpf.split(',')

	#limpa a tela das opcoes anteriores
	print(chr(27) + "[2J")

	#apresenta os dados no formato ID - CPF - Nome
	print ("Apresentação dos dados no formato 'ID - CPF - Nome': \n")
	print ("-----")

	#ID é a iteracão i+1, cpf é o o vetor CPF na posicão i, nome vem da chave (cpf:"cpf da pessoa", nome)
	for i in range(len(cpfs)):
		print ("%s - %s - %s") %(i+1,cpfs[i],r.hmget('cpf:'+cpfs[i],'nome')[0])
	print ("-----\n")

	#espera o usuário digitar o ID.
	escolha = raw_input("\nDigite o ID do usuario desejado: ")

	#depois que o usuario entrar com o ID, limpa a tela
	print(chr(27) + "[2J")

	#Confirma a escolha dizendo Pedido para (cpf:"cpf da pessoa", nome)
	print "\n-----\n"
	print "Pedido para %s" %str(r.hmget('cpf:'+cpfs[int(escolha)-1],'nome')[0])

	#Define o formato de apresentacão como "Codigo do pedido - Data pedido - Faturado - Nao Faturado - Data Entrega"
	print "Codigo do pedido - Data pedido - Faturado - Nao Faturado - Data Entrega"

	#pega todos os pedidos da chave (pedidos:"cpf da pessoa")
	pedidos = r.get('cpf:'+cpfs[int(escolha)-1]+':pedidos')

	#pedidos estão todos juntos como uma sting única separada por virgulas
	#é feito o split para tornar um vetor de pedidos
	pedidos = pedidos.split(',')
	print "\n-----\n"

	#se pedidos não for vazio
	if pedidos != ['']:
		#para cada pedido no vetor de pedidos
		for pedido in pedidos:
			#pegue do mysql os dados daquele pedido usando o ID como referência
			cursor.execute("SELECT * FROM pedidos WHERE cod_pedido = %s" %pedido)
			#traga tudo
			resultado = cursor.fetchall()
			#print no formato definido anteriormente
			print "%s - %s - %s - %s - %s" %(resultado[0]['cod_pedido'],resultado[0]['dtped'],resultado[0]['faturado'],resultado[0]['naofaturado'],resultado[0]['dtentrega'])
	else:
		#se for vazio nada a fazer
		print "Nenhum pedido feito"
	print "\n-----"
