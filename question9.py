#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Cria um pedido
import datetime

def question9_function(r,cursor):
	produtos = r.get('produtos')
	produtos = produtos.split(',')
	for i in range(0,len(produtos)-3,3):
		print "%s - %s | %s - %s | %s - %s" %(produtos[i], str(r.hmget("produto:"+produtos[i],'descricao')[0]),produtos[i+1], str(r.hmget("produto:"+produtos[i+1],'descricao')[0]),produtos[i+2], str(r.hmget("produto:"+produtos[i+2],'descricao')[0]))

	pedidos_produtos = []
	pedidos_quantidades = []
	pedidos = "S"
	while pedidos.upper() != "N":
		
		pedidos = raw_input("Insira o codigo do produto - (Digite 'N' para sair): ")
		
		if pedidos.upper() != "N":
			pedidos_qtd = int(raw_input("Insira a quantidade desse produto: "))
			pedidos_quantidades.append(pedidos_qtd)
			pedidos_produtos.append(pedidos)
				
	print "Escolha o usuario"
	cpfs = r.get('cpf')
	cpfs = cpfs.split(',')
	for cpf in cpfs:
		print "%s - %s" %(cpf, r.hmget('cpf:'+cpf,'nome')[0])
	cliente = raw_input("Escreva o cpf: ")
	
	
	#Criamos o pedido no MySQL
	cursor.execute("INSERT INTO pedidos (cad_usuario_cpf, dtped, faturado, naofaturado, dtentrega) VALUES (?, ?, ?, ?, ?)", [cliente, str(datetime.date.today()), None, None, None])
	pedido_id = cursor.lastrowid
	#Adicionamos os itens ao ItemPed MYSQL
	
	for i in range(len(pedidos_produtos)):
		cursor.execute("INSERT INTO itemped SET cod_itemp= NULL, qtditem = %s, ped_codpedidos = %s, prod_cod_produto = %s, estado_prod = NULL"  %(pedidos_quantidades[i],pedido_id,pedidos_produtos[i]))

	#Inserir pedido ao usuario 
	if (r.get('cpf:'+cliente+':pedidos')):
		string = r.get('cpf:'+cliente+':pedidos') + ',' + str(pedido_id)
	else:
		string = pedido_id
		
	r.set('cpf:'+cliente+':pedidos',string)

	if (r.get('pedidos')):
		string = r.get('pedidos') + ',' + str(pedido_id)
	else:
		string = str(pedido_id)
	
	r.set('pedidos',string)
	
	cursor.execute("SELECT * from pedidos WHERE cod_pedido = %s" %pedido_id)
	resultado = cursor.fetchall()
	for dado in resultado:
		
		r.hmset('pedido:'+str(pedido_id),dado)
