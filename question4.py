#!/usr/bin/env python
# -*- coding: utf-8 -*-

def question4_function(r, cursor):
	
	#recebe a pool de pedidos e separa em um vetor
	r_pedidos = r.get ('pedidos');
	pedidos = r_pedidos.split (',')
	
	#limpa a tela das opcoes anteriores
	print(chr(27) + "[2J")
	
	#apresenta os dados no formato ID - Data do Pedido - Faturado - Não Faturado - Data Entrega
	print ("Apresentacão no formato: ID - CPF do Cliente - Data do Pedido - Faturado - Não Faturado - Data Entrega")
	print ("-----")
	
	for pedido in pedidos:
		print ("%s - %s - %s - %s - %s - %s") %(r.hmget('pedido:'+pedido,'cod_pedido')[0], r.hmget('pedido:'+pedido,'cad_usuario_cpf')[0], r.hmget('pedido:'+pedido,'dtped')[0], r.hmget('pedido:'+pedido,'faturado')[0], r.hmget('pedido:'+pedido,'naofaturado')[0], r.hmget('pedido:'+pedido,'dtentrega')[0])

