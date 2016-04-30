#### POPULA O BANCO REDIS COM DADOS DO MYSQL!
#### Para performace time iremos coletar o inicio e final da execução
date_start = datetime.datetime.now()

## Se a escolha for a questão 1:
## Precisamos popular o basico do REDIS para nossas operações

cursor = db_mysql.cursor(oursql.DictCursor)
cursor.execute("""SELECT * FROM cad_usuario""")
dados = cursor.fetchall()
lista_cpf = []

#Criar o Hash Redis cliente:cpf
for cliente in dados:
	string = "cpf:%s" %cliente['cpf']
	r.hmset(string,cliente)
	lista_cpf.append(cliente['cpf'])

r.set('cpf',','.join(lista_cpf))

#Populamos os Pedidos
cpfs = r.get('cpf').split(',')
for cpf in cpfs:
	cursor.execute("SELECT cod_pedido FROM pedidos WHERE cad_usuario_cpf = %s" %(cpf))
	dados = cursor.fetchall()
	lista_pedido = []
	if len(dados) > 0:
		for dado in dados:
			lista_pedido.append(str(dado['cod_pedido']))
		r.set('cpf:'+cpf+':pedidos',','.join(lista_pedido))
	else:
		r.set('cpf:'+cpf+':pedidos','')



#Populamos os estados
cursor.execute("""
SELECT cad.cpf, uf.cd_uf as idUF
FROM cad_usuario cad
INNER JOIN logradouro log ON(cad.log_cd_logradouro=log.cd_logradouro)
INNER JOIN bairros b ON(log.bairros_cd_bairro=b.cd_bairro)
INNER JOIN cidades cid ON(b.cidade_cd_cidade=cid.cd_cidade)
INNER JOIN uf ON(cid.uf_cd_uf=uf.cd_uf);
""")


dados = cursor.fetchall()

#Pegamos os estados mas precisamos apagar dados antigos
chaves = r.keys('estado*')
for chave in chaves:
	r.delete(chave)
estados = []
for dado in dados:
	if (r.get('estado:'+str(dado['idUF']))):
		r.set('estado:'+str(dado['idUF']),r.get('estado:'+str(dado['idUF']))+','+str(dado['cpf']))
	else:
		r.set('estado:'+str(dado['idUF']),str(dado['cpf']))
		estados.append(str(dado['idUF']))

r.set('estado',','.join(estados))

#Produtos
cursor.execute("SELECT * FROM produto")
dados = cursor.fetchall()
for dado in dados:
	string = "produto:%s" %dado['cod_produto']
	r.hmset(string,dado)

#Pedidos
cursor.execute("SELECT * FROM pedidos")
dados = cursor.fetchall()
for dado in dados:
	string = "pedido:%s" %dado['cod_pedido']
	r.hmset(string,dado)

### Terimamos de povar o Redis vamos ver quanto tempo levou?
date_finish = datetime.datetime.now()
