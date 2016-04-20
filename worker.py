# encoding:utf-8
import oursql
import redis
import datetime

#Função que pega os dados do mysql e transforma em um dicionario lindo!
def FetchOneAssoc(cursor) :
    data = cursor.fetchone()
    if data == None :
        return None
    desc = cursor.description

    dict = {}

    for (name, value) in zip(desc, data) :
        dict[name[0]] = value

    return dict


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

#Criar o Hash Redis cliente:cpf
for cliente in dados:
    string2 = "cpf:%s" %cliente['cpf']
    string1 = "Nome '%s' EMAIL %s RG %s tel %s cel %s" %(cliente['nome'],cliente['email'],cliente['rg'],cliente['tel'],cliente['cel'])
    r.hmset(string2,cliente)
