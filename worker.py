# encoding:utf-8
import oursql
import redis
import datetime

# "endereço do servidor", "usuario", "senha" e "banco"
db_mysql = oursql.connect(host="localhost",user="root",passwd="",db="aulaivo")

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

lista_cpf = []
#Criar o Hash Redis cliente:cpf
for cliente in dados:
    string = "cpf:%s" %cliente['cpf']
    r.hmset(string,cliente)
    lista_cpf.append(cliente['cpf'])

r.set('cpf',','.join(lista_cpf))

############### Vamos ao menu!!!!
def menu():
    print "1 - Consultar Clientes"
    print "2 - Consultar Clientes e Mostrar os Pedidos"
    print "0 - Para sair"

def opcao(valor):
    if valor == "1":
        r_cpf = r.get('cpf')
        cpfs = r_cpf.split(',')
        i = 0
        for i in range(len(cpfs)):
            print "%s - %s - %s" %(i+1,cpfs[i],r.hmget('cpf:'+cpfs[i],'nome')[0])
        print "##########################################"


while True:
    menu()
    i = raw_input('Escolha a opção: ')
    if i == 0:
        break
    opcao(i)
