#!/usr/bin/env python
# -*- coding: utf-8 -*-

def question5_function(r, cursor):
	cpfs = r.get('cpf').split(',')
	
	for cpf in cpfs:
		print ("%s - %s - %s - %s - %s - %s") %(cpf, r.hmget('cpf:'+cpf,'rg')[0], r.hmget('cpf:'+cpf,'nome')[0], r.hmget('cpf:'+cpf,'email')[0], r.hmget('cpf:'+cpf,'tel')[0], r.hmget('cpf:'+cpf,'cel')[0])
