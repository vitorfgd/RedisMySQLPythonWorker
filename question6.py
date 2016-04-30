#!/usr/bin/env python
# -*- coding: utf-8 -*-

def question6_function(r):
	#Vamos pegar as ids das cidades presentes
	r_cidades = r.get('cidades')
	r_cidades = r_cidades.split(',')

	print "Escolha uma das cidades abaixos"
	for i in range(len(r_cidades)):
		print "%s - %s" %(i+1,r.get('cidade:'+r_cidades[i]))
	valor = raw_input("Escolha o numero da cidade desejada: ")

	if int(valor)>len(r_cidades)+1 or int(valor)<0:
		print "valor invalido"
	else:
		cpfs = r.get('cidade:'+r_cidades[int(valor)-1]+':cpfs')
		cpfs = cpfs.split(',')
		#apresenta os dados no formato ID - CPF - Nome
		print ("Apresentação dos dados no formato 'ID - CPF - Nome - Tel - Cel - Rg - Email': \n")
		print ("-----")

		#ID é a iteracão i+1, cpf é o o vetor CPF na posicão i, nome vem da chave (cpf:"cpf da pessoa", nome)
		for i in range(len(cpfs)):
		 	print ("%s - %s - %s - %s - %s - %s - %s") %(i+1,cpfs[i],r.hmget('cpf:'+cpfs[i],'nome')[0],r.hmget('cpf:'+cpfs[i],'tel')[0],r.hmget('cpf:'+cpfs[i],'cel')[0],r.hmget('cpf:'+cpfs[i],'rg')[0],r.hmget('cpf:'+cpfs[i],'email')[0])
		print ("-----\n")
