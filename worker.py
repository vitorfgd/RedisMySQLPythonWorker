# encoding:utf-8
import oursql
import redis
import datetime

#Ao início do programa, o programa espera as informacoes da base no modelo host, user, senha e db do MYSQL,
#caso algum dado seja digitado incorretamente, avisa o erro e tenta de novo.
#o programa então tenta conexão com o redis, caso consiga, prossegue, senão acusa o erro!

while True:
	my_SQL_host = raw_input ("Host (default: localhost): ");
	my_SQL_user = raw_input ("User MySQL: ");
	my_SQL_senha = raw_input ("Password MySQL: ");
	my_SQL_db = raw_input ("Database: ");

	try:
		db_mysql = oursql.connect(host = my_SQL_host, user=my_SQL_user, passwd=my_SQL_senha, db=my_SQL_db)
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

##### ETAPA 1
# Aqui precisamos popular o basico do REDIS para nossas operações
cursor = db_mysql.cursor(oursql.DictCursor)
cursor.execute("""SELECT * FROM cad_usuario""")
dados = cursor.fetchall()

#Populamos os clientes
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
def menu():

    r_cpf = r.get('cpf')
    cpfs = r_cpf.split(',')
    i = 0
    print "Id, Nome, e CPF"
    for i in range(len(cpfs)):
        print "%s - %s - %s" %(i+1,cpfs[i],r.hmget('cpf:'+cpfs[i],'nome')[0])
    print "##########################################"

    print "1 - Consultar Clientes e Mostrar os Pedidos"
    print "0 - Para sair"

def opcao(valor):
    if valor == "1":
        escolha = raw_input("Escolha o usuario por id: ")
        r_cpf = r.get('cpf')
        cpfs = r_cpf.split(',')
        print "##########################################"
        print "Pedido para %s" %str(r.hmget('cpf:'+cpfs[int(escolha)-1],'nome')[0])
        print "Codigo do pedido - Data pedido - Faturado - Nao Faturado - Data Entrega"
        pedidos = r.get('pedidos:'+cpfs[int(escolha)-1])
        pedidos = pedidos.split(',')

        if pedidos != ['']:
            for pedido in pedidos:
                cursor.execute("SELECT * FROM pedidos WHERE cod_pedido = %s" %pedido)
                resultado = cursor.fetchall()
                print "%s - %s - %s - %s - %s" %(resultado[0]['cod_pedido'],resultado[0]['dtped'],resultado[0]['faturado'],resultado[0]['naofaturado'],resultado[0]['dtentrega'])
        else:
            print "Nenhum pedido feito"
        print "##########################################"
while True:
    menu()
    i = raw_input('Escolha a opção: ')
    if i == "0":
        break
    opcao(i)
