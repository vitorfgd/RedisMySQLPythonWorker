#!/usr/bin/env python
# -*- coding: utf-8 -*-

def question2_function(r):
	if (r.get('estado:'+str(r))):
		cpfs = r.get('estado:'+str(r)).split(',')
		for cpf in cpfs:
			print ("%s") %(r.hmget('cpf:'+cpfs[i],'nome')[0])
