#!/usr/bin/env python
# -*- coding: utf-8 -*-

def question1_function(r):
	
	r_cpf = r.get('cpf')
	cpfs = r_cpf.split(',')

	print(chr(27) + "[2J")
	print ("Apresentação dos dados no formato 'ID - CPF - Nome': \n")
	print ("-----")
	for i in range(len(cpfs)):
		print ("%s - %s - %s") %(i+1,cpfs[i],r.hmget('cpf:'+cpfs[i],'nome')[0])
	print ("-----\n")

	escolha = raw_input("\nDigite o ID do usuario desejado: ")

	print(chr(27) + "[2J")
	print "\n-----\n"
	print "Pedido para %s" %str(r.hmget('cpf:'+cpfs[int(escolha)-1],'nome')[0])
	print "Codigo do pedido - Data pedido - Faturado - Nao Faturado - Data Entrega"
	pedidos = r.get('pedidos:'+cpfs[int(escolha)-1])
	pedidos = pedidos.split(',')
	print "\n-----\n"

	if pedidos != ['']:
		for pedido in pedidos:
			cursor.execute("SELECT * FROM pedidos WHERE cod_pedido = %s" %pedido)
			resultado = cursor.fetchall()
			print "%s - %s - %s - %s - %s" %(resultado[0]['cod_pedido'],resultado[0]['dtped'],resultado[0]['faturado'],resultado[0]['naofaturado'],resultado[0]['dtentrega'])
	else:
		print "Nenhum pedido feito"
	print "\n-----"

