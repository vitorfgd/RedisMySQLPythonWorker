#encoding:utf-8

import oursql
import redis
import datetime

from question1 import question1_function
from question2 import question2_function
from question3 import question3_function
from question4 import question4_function
from question5 import question5_function
from question6 import question6_function
from question7 import question7_function
from question8 import question8_function
from question9 import question9_function

#Ao início do programa, o programa espera as informacoes da base no modelo host, user, senha e db do MYSQL,
#Caso algum dado seja digitado incorretamente, avisa o erro e tenta de novo.
#O programa então tenta conexão com o redis, caso consiga, prossegue, senão acusa o erro!

while True:
	my_SQL_host = raw_input ("Host MySQL (default: localhost): ")
	my_SQL_user = raw_input ("User MySQL: ")
	my_SQL_senha = raw_input ("Password MySQL: ")
	my_SQL_db = raw_input ("Database MySQL: ")

	try:
		db_mysql = oursql.connect(host = my_SQL_host, user=my_SQL_user, passwd=my_SQL_senha, db=my_SQL_db)
		print(chr(27) + "[2J")
		print ("\n-----")
		print ("Conexão realizada com sucesso!")
		print ("-----\n")
		break
	except:
		print ("\n-----")
		print ("Dados incorretos - Por favor tente novamente")
		print ("-----\n")
		True

r = redis.StrictRedis(host='localhost', port=6379, db=0)
try:
    r.ping()
except:
    print "Não foi possivel conectar ao Redis"

#### POPULA O BANCO REDIS COM DADOS DO MYSQL!
#### Para performace time iremos coletar o inicio e final da execução
date_start = datetime.datetime.now()

## ------------- START DA QUESTÃO 1 ------------- ##

## Precisamos popular o basico do REDIS para nossas operações
cursor = db_mysql.cursor(oursql.DictCursor)
cursor.execute("""SELECT * FROM cad_usuario""")
dados = cursor.fetchall()
lista_cpf = []

#Criar o hash no formato (cpf:"cpf_do_usuário")
for cliente in dados:
	string = "cpf:%s" %cliente['cpf']
	r.hmset(string,cliente)
	lista_cpf.append(cliente['cpf'])

#Guarda o pool de CPF
r.set('cpf',','.join(lista_cpf))
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

## ------------- FIM DA QUESTÃO 1 ------------- ##
## ------------- START DA QUESTÃO 2 ------------- ##

##POPULA ESTADO
#Executa o query para trazer como resultado o cpf da pessoa
#e o estado referente à pessoa;

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

#se existir dois no mesmo estado não duplica
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

#Consultar as cidades e retornar os usuarios
cursor.execute("""
SELECT cad.cpf, cid.cd_cidade, cid.ds_cidade_nome
FROM cad_usuario cad
INNER JOIN logradouro log ON(cad.log_cd_logradouro=log.cd_logradouro)
INNER JOIN bairros b ON(log.bairros_cd_bairro=b.cd_bairro)
INNER JOIN cidades cid ON(b.cidade_cd_cidade=cid.cd_cidade)
""")
dados = cursor.fetchall()
cidades = r.keys('cidade*')
for cidade in cidades:
	r.delete(cidade)

cidades = []
nomes_cidades = []
for dado in dados:
	if (r.get('cidade:'+str(dado['cd_cidade'])+':cpfs')):
		string = str(r.get('cidade:'+str(dado['cd_cidade']+':cpfs')))+str(dado['cpf'])
		r.set('cidade:'+str(dado['cd_cidade']+':cpfs',string))
	else:
		cidades.append(str(dado['cd_cidade']))
		nomes_cidades.append(str(dado['ds_cidade_nome'].encode('utf-8')))
		r.set('cidade:'+str(dado['cd_cidade'])+':cpfs',str(dado['cpf']))


r.set('cidades',','.join(cidades))

for i in range(len(nomes_cidades)):
	codigo = 'cidade:%s' %cidades[i]
	r.set(codigo,nomes_cidades[i])


### Terimamos de povar o Redis vamos ver quanto tempo levou?
date_finish = datetime.datetime.now()
menu = True
while menu:
	print ("-----")
	print ("Tempo para povoar o redis: %s" %(date_finish - date_start))
	print ("Selecione a questão: ")
	print ("\n1) Consultar o nome do usuário e retornar os pedidos deste usuário!") #FEITO (BANCO,EXECUÇÃO)
	print ("2) Consultar o estado e retornar os usuários deste estado!") #FEITO (BANCO,EXECUÇÃO)
	print ("3) Consultar o produto e retornar os dados dos produtos!") #FEITO (BANCO)
	print ("4) Consultar pelo pedido e retornar os dados do pedido!") #FEITO (BANCO)
	print ("5) Consultar o usuário e retornar os dados do usuário!") # FEITO (BANCO)
	print ("6) Consultar a cidade e retornar os dados do usuário!") # FEITO (BANCO, EXECUCAO)
	print ("7) Consultar o estado e retornar os dados de todos os logradouros deste estado!")
	print ("8) Cadastrar um novo usuário!")
	print ("9) Inserir um pedido para determinado usuário!")
	print ("0) Sair")
	print ("-----")
	escolha = input ("\nDigite a questão: ")

	if escolha == 1:
		question1_function (r, cursor)

	elif escolha == 2:
		question2_function (r, cursor)

	elif escolha == 3:
		print "Não implementado ainda"

	elif escolha == 4:
		print "Não implementado ainda"

	elif escolha == 5:
		print "Não implementado ainda"

	elif escolha == 6:
		question6_function (r)

	elif escolha == 7:
		print "Não implementado ainda"

	elif escolha == 8:
		print "Não implementado ainda"

	elif escolha == 9:
		print "Não implementado ainda"

	elif escolha == 9:
		print "Não implementado ainda"
	elif escolha == 0:
		menu = False
