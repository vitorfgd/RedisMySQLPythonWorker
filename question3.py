#!/usr/bin/env python
# -*- coding: utf-8 -*-

def question3_function(r, cursor):
	
	#recebe a pool de pedidos e separa em um vetor
	r_produtos = r.get ('produtos');
	produtos = r_produtos.split (',')
	contador = 0;
	
	#limpa a tela das opcoes anteriores
	print(chr(27) + "[2J")
	
	for prod in produtos:
		contador += 1
	
	
	#apresenta os dados no formato Cod. Produto - Descrição - Preço Unitário - Preço Emb. - Qtd. Emb. - Qtd. Produto - Emb. Cod. Embalagem
	produto_desejado = str(input ("Digite o código do produto desejado (1 - %s): " %str(contador)))
	print ("\n-----")
	print ("Código: %s \nDescrição: %s \nPreço Unitário: %s \nPreço Embalagem: %s \nQuantidade Embalagem: %s \nQuantidade Produto: %s \nEmb. Cod. Embalagem: %s") %(r.hmget('produto:'+produto_desejado,'cod_produto')[0], r.hmget('produto:'+produto_desejado,'descricao')[0], r.hmget('produto:'+produto_desejado,'preco_unit')[0], r.hmget('produto:'+produto_desejado,'preco_emb')[0], r.hmget('produto:'+produto_desejado,'qtd_emb')[0], r.hmget('produto:'+produto_desejado,'qtd_produto')[0], r.hmget('produto:'+produto_desejado,'emb_cod_produto')[0])

