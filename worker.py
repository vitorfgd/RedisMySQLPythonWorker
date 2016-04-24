# encoding:utf-8
import oursql
import redis
import datetime

def menu_questao1():
	
    r_cpf = r.get('cpf')
    cpfs = r_cpf.split(',')
    i = 0
    print ("Apresentação dos dados no formato 'ID - Nome - CPF': \n")
    print ("-----")
    for i in range(len(cpfs)):
        print "%s - %s - %s" %(i+1,cpfs[i],r.hmget('cpf:'+cpfs[i],'nome')[0])
    print ("-----\n")

    print "1 - Consultar Clientes e Mostrar os Pedidos"
    print "0 - Para sair\n"
    
def opcao_questao1(valor):
    if valor == "1":
        escolha = raw_input("Escolha o usuario por id: ")
        r_cpf = r.get('cpf')
        cpfs = r_cpf.split(',')
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

#Ao início do programa, o programa espera as informacoes da base no modelo host, user, senha e db do MYSQL,
#Caso algum dado seja digitado incorretamente, avisa o erro e tenta de novo.
#O programa então tenta conexão com o redis, caso consiga, prossegue, senão acusa o erro!

while True:
	my_SQL_host = raw_input ("Host MySQL (default: localhost): ")	
	my_SQL_user = raw_input ("User MySQL: ")
	my_SQL_senha = raw_input ("Password MySQL: ")
	my_SQL_db = raw_input ("Database MySQL: ")

	##fiz só para não ficar digitando o tempo todo que to testando!
	if my_SQL_host == "admin_vitor":
		my_SQL_host = "localhost"
		my_SQL_user = "root"
		my_SQL_senha = "root"
		my_SQL_db = "aulaivo"
	
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

print ("-----")
print ("Selecione a questão: ")
print ("\n1) Consultar o nome do usuário e retornar os pedidos deste usuário!")
print ("2) Consultar o estado e retornar os usuários deste estado!")
print ("3) Consultar o produto e retornar os dados dos produtos!")
print ("4) Consultar pelo pedido e retornar os dados do pedido!")
print ("5) Consultar o usuário e retornar os dados do usuário!")
print ("6) Consultar a cidade e retornar os dados do usuário!")
print ("7) Consultar o estado e retornar os dados de todos os logradouros deste estado!")
print ("8) Cadastrar um novo usuário!")
print ("9) Inserir um pedido para determinado usuário!")
print ("0) Sair")
print ("-----")
escolha = input ("\nDigite a questão: ")

## Se a escolha for a questão 1:
## Precisamos popular o basico do REDIS para nossas operações
if escolha == 1:
	
	print(chr(27) + "[2J")
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

	#populamos os Pedidos
	cpfs = r.get('cpf').split(',')
	for cpf in cpfs:
		cursor.execute("SELECT cod_pedido FROM pedidos WHERE cad_usuario_cpf = %s" %(cpf))
		dados = cursor.fetchall()
		lista_pedido = []
		if len(dados) > 0:
			for dado in dados:
				lista_pedido.append(str(dado['cod_pedido']))
			r.set('pedidos:'+cpf,','.join(lista_pedido))
		else:
			r.set('pedidos:'+cpf,'')

	############### Vamos ao menu!!!!


	while True:
		menu_questao1()
		i = raw_input('Escolha a opção: ')
		if i == "0":
			break
		opcao_questao1(i)

## Se a escolha for a questão 2:
## Precisamos popular o REDIS com as informarcoes sobre os usuarios em um determinado Estado!
elif escolha == 2:
	

	print(chr(27) + "[2J")
	cursor = db_mysql.cursor(oursql.DictCursor)
	
	## Para apresentacao o cursor ira percorrer e apresentar todas as opcoes de estado!
	cursor.execute("""SELECT * FROM uf""")
	dados_estado = cursor.fetchall()
	lista_estado = []
	estado_index = 0
	
	print "-----"
	for estado in dados_estado:
		estado_index += 1
		lista_estado.append(['ds_uf_nome'])
		print "%d - %s" %(estado_index, estado['ds_uf_nome'])
		
	print "-----\n"
	estado_escolha = input ("Por favor, digite o código do estado que deseja buscar: ")


elif escolha == 3:
	print "Não implementado ainda"

elif escolha == 4:
	print "Não implementado ainda"

elif escolha == 5:
	print "Não implementado ainda"
	
elif escolha == 6:
	print "Não implementado ainda"
	
elif escolha == 7:
	print "Não implementado ainda"

elif escolha == 8:
	print "Não implementado ainda"
	
elif escolha == 9:
	print "Não implementado ainda"
	
elif escolha == 9:
	quit ()
