#cursor.execute("""SELECT est.ds_uf_sigla FROM uf est""")

#dados = cursor.fetchall()
#total_estados = []

#for dado in dados:
	#total_estados.append (str(dado['ds_uf_sigla']))
#r.set('total_estados',','.join(produtos))

#porcentagem = 0

#for var in total_estados:
	#cursor.execute(""" SELECT * FROM logradouro lo 
	#INNER JOIN bairros ba ON(lo.bairros_cd_bairro = ba.cd_bairro)
	#INNER JOIN cidades ci ON (ba.cidade_cd_cidade = ci.cd_cidade)
	#INNER JOIN uf ON (ci.uf_cd_uf = cd_uf)
	#WHERE ds_uf_sigla = "%s" """ %var)
	#dados2 = cursor.fetchall()
	#cd_logradouro_pool = []
	#porcentagem += 3.7037
	#print "%s%% - Populando: %s" %(str(porcentagem), str(var))
	#for dado2 in dados2:
		#string = 'estado:%s:logradouro:%s' %(var, str(dado2['cd_logradouro']))
		#r.hmset(string,dado2)
		#cd_logradouro_pool.append(str(dado2['cd_logradouro']))
		#string2 = 'cd_logradouro_pool:%s' %(var)
		#r.set (string2,','.join(cd_logradouro_pool))
