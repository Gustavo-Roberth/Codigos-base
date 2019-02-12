from datetime import date
import mysql.connector

cnx = mysql.connector.connect(
                                user='root',
                                password='12345',
                                port='3306',
                                host='127.0.0.1',
                                database='PIZZARIA'
                              )
cursor = cnx.cursor()
# Executa a consulta na tabela selecionada
cursor.execute("SELECT * FROM seudb.suatabela")
# Conta o numero de linhas na tabela
numrows = int(cursor.rowcount)
# Obtendo resultados
print ("--------------------------------------------------")
print ("| ID  Campo                                      |")
print ("--------------------------------------------------")
# Laço for para retornar os valores, ex.: row[0] primeira coluna, row[1] segunda coluna, row[2] terceira coluna, etc.
for row in cursor.fetchall():
   print (" ",row[0]," ",row[1])

cnx.close()

'''
cursor = cnx.cursor()

query = ("SELECT sum(produto.valor*item.quantidade) as 'TOTAL' FROM produto, item, pedido WHERE produto.id_produto = item.id_produto and item.id_pedido = pedido.id_pedido AND pedido.id_pedido = 1")

cursor.execute(query)

linha = cursor.fetchall()
count = cursor.rowcount

if count != 0:
    print("Retornado",count,"registro")

    for (query) in linha:
        print(query)
else:
    print("Registro não encontrado!")

cursor.close()

cnx.close()

'''
### Apresentado registros do Banco de Dados 28/11/2018
'''
cursor = cnx.cursor()

s = input("Digite o código:")

query = "select * from contato where id_contato = " + s

cursor.execute(query)

linha = cursor.fetchall()
count = cursor.rowcount

if count != 0:
    print("Retornado",count,"registro")

    for (vid_contato, vnome, vfone, vdata_nasc) in linha:
        print(vid_contato, vnome, vfone, vdata_nasc)
else:
    print("Registro não encontrado!")

cursor.close()

cnx.close()
'''


### Inserindo dados no Banco de Dados 30/11/2018
'''
cnx = mysql.connector.connect(user='root', password='12345', port='3306',
                              host='127.0.0.1', database='agenda')

cursor = cnx.cursor()

query = "insert into contato (nome, fone, data_nasc) values (%s, %s, %s)"
dados_contato = ('João das Neves', '(98)8877-1234',date(1979,10,13))

cursor.execute(query, dados_contato)
cnx.commit()
vid_contato = cursor.lastrowid

print("Contato inserido. Seu código é", vid_contato)


cursor.close()
cnx.close()
'''

### Inserindo dados do Banco de Dados através da entrada do usuário
'''
cursor = cnx.cursor()

query = "insert into contato (nome, fone, data_nasc) values (%s, %s, %s)"

vnome = input("Nome: ")
vfone = input("Telefone: ")
vdata_nasc = input("Data de nascimento (yyyy-mm-dd): ")

dados_do_usuário = (vnome, vfone, vdata_nasc)

cursor.execute(query, dados_do_usuário)
cnx.commit()
vid_contato = cursor.lastrowid

print("Contato inserido. Seu código é", vid_contato)

cursor.close()
cnx.close()
'''


### Excluindo registro de dados do Banco de Dados através da entrada do usuário
'''
from datetime import date
import mysql.connector

cnx = mysql.connector.connect(
                                user='conexão_comunista_poha',
                                password='12345',
                                port='3306',
                                host='127.0.0.1',
                                database='agenda'
                              )

cursor = cnx.cursor()

indice = input("Digite o código:")

query = "delete from contato where id_contato = %s"

cursor.execute(query, tuple(indice)) ### força, transforma a variável 'indice' em uma lista
cnx.commit()

print("Contato excluído")

cursor.close()
cnx.close()
'''
