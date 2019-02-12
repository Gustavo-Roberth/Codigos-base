
from mysql import *
##import pymysql
import mysql.connector

import tkinter as tk
from tkinter import ttk

# Fontes essenciais para o programa
FONTE_10_N = ("Arial", 10)
FONTE_12_N = ("Arial", 12)
FONTE_12_B = ("Arial", 12, "bold")
FONTE_14_B = ("Arial", 14, "bold")
###

USUARIO = 'root'
SENHA = '12345'
PORTA = '3306'
LOCAL = '127.0.0.1'
BASE = 'pizzaria'


#outros
msg_sobre_menu = "Produzido por:\nGustavo Gomes e Lucas Batalha\nDesenvolvido para o trabalho da 3a nota da disciplina:\nCCCT0051 - Banco de Dados 2018.2\n\n© 2018"
###

###
                              
# Função que apresenta uma mensagem        
def popup_msg(msg):
    popup = tk.Tk()

    popup.wm_title("!")
    label = tk.Label(popup, text = msg, font = FONTE_10_N)
    label.pack(side = "top", fill = "x", pady = 10)
    button_mensagem = ttk.Button(popup, text = "Ok", command = popup.destroy)
    button_mensagem.pack()
    popup.mainloop()
###

def popup_pagamento(msg, cod_pedido):
    cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
    cursor = cnx.cursor()
        
    query = "select id_pedido, estado, observacao, data_dia_hora from pedido where id_pedido = "+cod_pedido
    cursor.execute(query)

    linha = cursor.fetchall()

    for (vid_pedido, v_estado, v_observacao, v_dia_hora) in linha:
        id_pedido = vid_pedido
        if v_estado == 1:
            estado = 'Aberto'
        else:
            estado = 'Pago'
        observacao = v_observacao
        dia_hora = v_dia_hora

    
    popup = tk.Tk()

    popup.wm_title(msg)
    
    label = tk.Label(popup, text = "Pedido: " + str(id_pedido), font = FONTE_10_N)
    label.pack(pady = 10, padx = 10)

    label = tk.Label(popup, text = "Estado: " + str(estado), font = FONTE_10_N)
    label.pack(pady = 10, padx = 10)

    label = tk.Label(popup, text = "Observação: " + str(observacao), font = FONTE_10_N)
    label.pack(pady = 10, padx = 10)

    label = tk.Label(popup, text = "Dia e Hora: " + str(dia_hora), font = FONTE_10_N)
    label.pack(pady = 10, padx = 10)

    label.pack(side = "top", fill = "x", pady = 10)
    button_concluir = ttk.Button(popup, text = "Concluir Pagamento", command = lambda : popup_confirm_pag("Deseja realmente finalizar a compra ?", id_pedido))
    button_concluir.pack()
    button_cancelar = ttk.Button(popup, text = "Cancelar", command = lambda : popup_canc_pag("Deseja realmente cancelar o pagamento ?", id_pedido))
    button_cancelar.pack()
    popup.mainloop()
    controle.show_frame(Finalizar_Pedido)

def popup_confirm_pag(msg, cod_pedido):
    cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
    cursor = cnx.cursor()
        
    query = "select id_pedido, estado, observacao, data_dia_hora, (Select SUM(produto.valor*item.quantidade) FROM item, produto WHERE item.id_pedido = pedido.id_pedido and produto.id_produto = item.id_produto)  from pedido where id_pedido = "+str(cod_pedido)+";"
    cursor.execute(query)

    linha = cursor.fetchall()
    cursor.close()
    cnx.close()

    for (vid_pedido, v_estado, v_observacao, v_dia_hora, v_valor_total) in linha:
        id_pedido = vid_pedido
        if v_estado == 1:
            estado = 'Aberto'
        else:
            estado = 'Pago'
        observacao = v_observacao
        dia_hora = v_dia_hora
        valor_total =  v_valor_total

    
    popup = tk.Tk()

    popup.wm_title("Recibo")
    
    label = tk.Label(popup, text = "Pedido: " + str(id_pedido), font = FONTE_10_N)
    label.pack(pady = 10, padx = 10)

    label = tk.Label(popup, text = "Estado: " + str(estado), font = FONTE_10_N)
    label.pack(pady = 10, padx = 10)

    label = tk.Label(popup, text = "Observação: " + str(observacao), font = FONTE_10_N)
    label.pack(pady = 10, padx = 10)

    label = tk.Label(popup, text = "Dia e Hora: " + str(dia_hora), font = FONTE_10_N)
    label.pack(pady = 10, padx = 10)

    label = tk.Label(popup, text = "Valor Total: " + str(valor_total), font = FONTE_10_N)
    label.pack(pady = 10, padx = 10)
    


    # Estabelecer conexão para buscar todos os itens do pedido
    cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
    cursor = cnx.cursor()
        
    query = "UPDATE pedido SET estado = "+str(2)+" WHERE id_pedido = "+str(cod_pedido)+";"
    cursor.execute(query)

    count = cursor.rowcount

    cursor.close()
    cnx.close()

    label.pack(side = "left", fill = "x", pady = 10)
    popup.mainloop()
    controle.show_frame(Finalizar_Pedido)

    label = tk.Label(popup, text = "Pedido Pago", font = FONTE_10_N)
    label.pack(pady = 10, padx = 10)
    label = tk.Label(popup, text = "Obrigado pela preferência!!!", font = FONTE_10_N)
    label.pack(pady = 10, padx = 10)
        

# Função Realiza uma impressão de texto na tela
def print_string(String_to_print):
    print(String_to_print)
###


##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
##########**********************************************************************************************************************************************##########
#####                                                                  Aplicação                                                                             #####



# Classe em que roda o programa
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        
        #tk.Tk.wm_iconbitmap(self, "icone-pizzaria.bmp")
        tk.Tk.wm_title(self, "PIZZARIA LOMBARDIA")
        
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}

        for F in (Inicio, Cardapio, Criar_Pedido, Pagamento_Pedido, Editar_Pedido, Editar_Cardapio, Alterar_Item, Excluir_Item, Alterar_Pedido, Excluir_Pedido, Editar_Cardapio, Adicionar_Tipo, Adicionar_Produto, Alterar_Tipo, Alterar_Produto, Excluir_Tipo, Excluir_Produto):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Inicio)

        barra_menu = tk.Menu(container)
        menu_file = tk.Menu(barra_menu, tearoff = 0)
        menu_file.add_command(label = "Sobre", command = lambda: popup_msg(msg_sobre_menu))
        menu_file.add_separator()
        menu_file.add_command(label = "Sair", command = quit)
        barra_menu.add_cascade(label = "File", menu = menu_file)

        tk.Tk.config(self, menu = barra_menu)

# Função que apresenta os quadros na tela, a partir da diretiva 'controle'
    def show_frame(self, controle):
        frame = self.frames[controle]
        frame.tkraise()
###

##################################################################################################################################################################
##########**********************************************************************************************************************************************##########
#####                                                                    Início                                                                              #####
                              
# Classe da Página inicial /*** inicialmente configurada como cardápio
class Inicio(tk.Frame):

    def __init__(self, parent, controle):
        tk. Frame.__init__(self, parent)

        label = tk.Label(self, text = "PIZZARIA LOMBARDIA", font = FONTE_14_B)
        label.pack(pady = 10, padx = 10)
        
        label = tk.Label(self, text = "Seja muito bem vindo !!!", font = FONTE_12_N)
        label.pack(pady = 10, padx = 10)

        label = tk.Label(self, text = "Você pode realizar uma ação clicando em qualquer botão para entrar", font = FONTE_10_N)
        label.pack(pady = 10, padx = 10)

        botao_para_Cardapio = ttk.Button(self, text = "Cardápio",
                                command = lambda: controle.show_frame(Cardapio))
        botao_para_Cardapio.pack(pady = 10, padx = 10)
        
        botao_para_Editar_Pedido = ttk.Button(self, text = "Pagamento de Pedido",
                                command = lambda: controle.show_frame(Pagamento_Pedido))
        botao_para_Editar_Pedido.pack(pady = 10, padx = 10)

        botao_para_Editar_Pedido = ttk.Button(self, text = "Editar Pedido",
                                command = lambda: controle.show_frame(Editar_Pedido))
        botao_para_Editar_Pedido.pack(pady = 10, padx = 10)

        botao_para_Editar_Pedido = ttk.Button(self, text = "Editar Cardápio",
                                command = lambda: controle.show_frame(Editar_Cardapio))
        botao_para_Editar_Pedido.pack(pady = 10, padx = 10)
###

##################################################################################################################################################################
##########**********************************************************************************************************************************************##########
#####                                                                   Cardápio                                                                             #####

## *****
# Classe de onde serão adicionados os itens do Cardapio
class Cardapio(tk.Frame):

    def __init__(self, parent, controle):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text = "Cardápio", font = FONTE_12_B)
        label.pack(pady = 10, padx = 10)

        self.tv = ttk.Treeview(self, columns=('Código', 'Prato', 'Descrição', 'Tamanho', 'Valor'))
        self.tv.column("#0",minwidth=0,width=0)
        self.tv.column('Código', width=50, anchor='center')
        self.tv.heading('Código', text='Código')
        self.tv.column('Prato', width=100, anchor='center')
        self.tv.heading('Prato', text='Prato')
        self.tv.column('Descrição', width=300, anchor='center')
        self.tv.heading('Descrição', text='Descrição')
        self.tv.column('Tamanho', width=70, anchor='center')
        self.tv.heading('Tamanho', text='Tamanho')
        self.tv.column('Valor', width=50, anchor='center')
        self.tv.heading('Valor', text='Valor')
        
        self.tv.pack()

        #gera conexão para inserção dos dados do banco para a treeview
        #cnx = pymysql.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)

        cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
        cursor = cnx.cursor()
        
        query = "select * from produto"

        cursor.execute(query)

        linha = cursor.fetchall()
        count = cursor.rowcount

        if count != 0:

            for (vid_produto, vid_tipo, vnome, vdescricao, vtamanho, vvalor) in linha:
                self.tv.insert("", "end", text = "Produtos", values = (vid_produto, vnome, vdescricao, vtamanho, vvalor))

        cursor.close()

        cnx.close()
    
        botao_para_Alterar_Pedido = ttk.Button(self, text = "Criar Novo Pedido",
                                command = lambda: controle.show_frame(Criar_Pedido))
        botao_para_Alterar_Pedido.pack(pady = 10, padx = 10)
        
        botao_para_Alterar_Pedido = ttk.Button(self, text = "Alterar Pedido Existente",
                                command = lambda: controle.show_frame(Alterar_Pedido))
        botao_para_Alterar_Pedido.pack(pady = 10, padx = 10)
        
        botao_para_Inicio = ttk.Button(self, text = "Início",
                                command = lambda: controle.show_frame(Inicio))
        botao_para_Inicio.pack(pady = 10, padx = 10)
        
###
#### *****

##################################################################################################################################################################
##########**********************************************************************************************************************************************##########
#####                                                                  Criar Pedido                                                                          #####

##*****
# Adiciona item um a um, com o código do pedido
def adicionar_item(c_id_pedido, c_id_produto, c_quantidade):
    #cnx = pymysql.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)

    cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
    cursor = cnx.cursor()
    query = "INSERT INTO item (id_pedido, id_produto, quantidade) VALUES (%s, %s, %s);"
    dados_produto = (c_id_pedido, c_id_produto, c_quantidade)
    cursor.execute(query, dados_produto)
    cnx.commit()

    id_item = cursor.lastrowid
    print("Item inserido. Código = ", id_item)

    cursor.close()
    cnx.close()
###

# Classe de onde serão adicionados os itens do Cardapio
class Criar_Pedido(tk.Frame):

    def __init__(self, parent, controle):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text = "Novo Pedido", font = FONTE_12_B)
        label.pack(pady = 10, padx = 10)

        self.tv = ttk.Treeview(self, columns=('Código', 'Prato', 'Descrição', 'Tamanho', 'Valor'))
        self.tv.column("#0",minwidth=0,width=0)
        self.tv.column('Código', width=50, anchor='center')
        self.tv.heading('Código', text='Código')
        self.tv.column('Prato', width=100, anchor='center')
        self.tv.heading('Prato', text='Prato')
        self.tv.column('Descrição', width=300, anchor='center')
        self.tv.heading('Descrição', text='Descrição')
        self.tv.column('Tamanho', width=70, anchor='center')
        self.tv.heading('Tamanho', text='Tamanho')
        self.tv.column('Valor', width=50, anchor='center')
        self.tv.heading('Valor', text='Valor')        
        self.tv.pack()

        #gera conexão para inserção dos dados do banco para a treeview
        #cnx = pymysql.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)

        cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
        cursor = cnx.cursor()
        
        query = "select * from produto;"
 
        cursor.execute(query)

        linha = cursor.fetchall()
        count = cursor.rowcount

        if count != 0:

            for (vid_produto, vid_tipo, vnome, vdescricao, vtamanho, vvalor) in linha:
                self.tv.insert("", "end", text = "Produtos", values = (vid_produto, vnome, vdescricao, vtamanho, vvalor))

        cursor.close()

        cnx.close()
    
        botao_para_Alterar_Pedido = ttk.Button(self, text = "Criar Pedido",
                                command = lambda: self.adiciona_pedido)
        botao_para_Alterar_Pedido.pack(pady = 10, padx = 10)
        
        botao_para_Inicio = ttk.Button(self, text = "Início",
                                command = lambda: controle.show_frame(Inicio))
        botao_para_Inicio.pack(pady = 10, padx = 10)
        
    def cria_pedido(self):
        #cnx = pymysql.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)

        cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
        cursor = cnx.cursor()

        query = "INSERT INTO pedido (estado, observacao, data_dia_hora) VALUES (%s, %s, now());"
        dados_pedido = (1, 'nenhuma')
        cursor.execute(query, dados_pedido)
        cnx.commit()

        cursor.close()
        cnx.close()

        id_pedido = cursor.lastrowid
        print("Pedido criado. Código = ", id_pedido)

        texto_pedido = ttk.Label(self, text = "Adicione os dados e clique em \"Salvar Alterações\" para adicioná-lo", font = FONTE_10_N)
        texto_pedido.pack()
        
        label_pedido = ttk.Label(self, text = "Código de pedido: "+id_pedido, font = FONTE_10_N)
        label_pedido.pack()

        label_tamanho = ttk.Label(self, text = "Código do produto:", font = FONTE_10_N)
        label_tamanho.pack()
        caixa_entrada_produto = ttk.Entry(self, width = 50)
        caixa_entrada_produto.pack(pady = 10, padx = 10)

        label_valor = ttk.Label(self, text = "Quantidade:", font = FONTE_10_N)
        label_valor.pack()
        caixa_entrada_quantidade = ttk.Entry(self, width = 50)
        caixa_entrada_quantidade.pack(pady = 10, padx = 10)

        botao_para_Cardapio = ttk.Button(self, text = "Concluir",
                                command = lambda: adicionar_item(id_pedido, caixa_entrada_produto.get(), caixa_entrada_quantidade.get()))
        botao_para_Cardapio.pack(pady = 2, padx = 10)
        
        botao_para_Cardapio = ttk.Button(self, text = "Concluir",
                                command = lambda: adicionar_item(id_pedido, caixa_entrada_produto.get(), caixa_entrada_quantidade.get()))
        botao_para_Cardapio.pack(pady = 2, padx = 10)
###

##################################################################################################################################################################
##########**********************************************************************************************************************************************##########
#####                                                               Pagamento de Pedido                                                                           #####

# Cria pedido
def cria_pedido():
    #cnx = pymysql.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)

    cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
    cursor = cnx.cursor()

    query = "INSERT INTO pedido (estado, observacao, data_dia_hora) VALUES (%s , %s, %s);"
    dados_pedido = (1 , 'nenhum', now())
    cursor.execute(query, dados_pedido)
    cnx.commit()

    cursor.close()
    cnx.close()

    id_pedido = cursor.lastrowid
    print("Pedido criado. Código = ", id_pedido, ".")
    if estado == 1:
        print("Estado = aberto.")
    else:
        print("Estado = pago.")

# Classe de alterações realizadas no pedido
class Pagamento_Pedido(tk.Frame):

    def __init__(self, parent, controle):
        tk.Frame.__init__(self, parent)

        self.id_pedido = 0

        label = tk.Label(self, text = "Pagamento de Pedido", font = FONTE_12_B)
        label.pack(pady = 10, padx = 10)

        texto_pedido = ttk.Label(self, text = "Clique no item para seleciona-lo", font = FONTE_10_N)
        texto_pedido.pack()
        
        self.tv = ttk.Treeview(self, columns=('Código do Pedido', 'Estado', 'Observação', 'Data e Hora'))
        self.tv.column("#0",minwidth=0,width=0)
        self.tv.column('Código do Pedido', width=50, anchor='center')
        self.tv.heading('Código do Pedido', text='Código do Pedido')
        self.tv.column('Estado', width=50, anchor='center')
        self.tv.heading('Estado', text='Estado')
        self.tv.column('Observação', width=250, anchor='center')
        self.tv.heading('Observação', text='Observação')
        self.tv.column('Data e Hora', width=120, anchor='center')
        self.tv.heading('Data e Hora', text='Data e Hora')
        self.tv.pack()

        #gera conexão para inserção dos dados do banco para a treeview
        #cnx = pymysql.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)

        cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
        cursor = cnx.cursor()
        
        query = "select id_pedido, estado, observacao, data_dia_hora, (Select SUM(produto.valor*item.quantidade) FROM item, produto WHERE item.id_pedido = pedido.id_pedido and produto.id_produto = item.id_produto) from pedido;"
 
        cursor.execute(query)

        linha = cursor.fetchall()
        count = cursor.rowcount

	# lista os pedidos e organiza com seu código, estado, observações, horário de realização e valor total
        if count != 0:
            for ( v_id_pedido, v_est_pedido, v_obs_pedido, v_dat_hor_pedido, v_valor_total) in linha:
                if v_est_pedido == 1:
                    self.tv.insert("", "end", text = "Produtos", values = (v_id_pedido, 'Aberto', v_obs_pedido, v_dat_hor_pedido, v_valor_total))
                else:
                    self.tv.insert("", "end", text = "Produtos", values = (v_id_pedido, 'Pago', v_obs_pedido, v_dat_hor_pedido, v_valor_total))
        cursor.close()

        cnx.close()
        
        label_idpedido = ttk.Label(self, text = "Senha do pedido:", font = FONTE_10_N)
        label_idpedido.pack()
        caixa_entrada_idpedido = ttk.Entry(self, width = 50)
        caixa_entrada_idpedido.pack(pady = 10, padx = 10)

        # Botões para modificação do pedido
        botao_Produto = ttk.Button(self, text = "Concluir pagamento",
                                command = lambda: popup_pagamento("Informações do Pedido", caixa_entrada_idpedido.get()))
        botao_Produto.pack(pady = 2, padx = 10)

        botao_para_Inicio = ttk.Button(self, text = "Início",
                                command = lambda: controle.show_frame(Inicio))
        botao_para_Inicio.pack(pady = 10, padx = 10)           
            
###
        
##################################################################################################################################################################
##########**********************************************************************************************************************************************##########
#####                                                               Edição de Pedido                                                                         #####

# Classe para Editar o cardápio completo, como todos os produtos e tipos de produtos disponíveis
class Editar_Pedido(tk.Frame):

    def __init__(self, parent, controle):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text = "Editar Cardápio", font = FONTE_12_B)
        label.pack(pady = 10, padx = 10)

        # Adiciona um produto ou tipo de produto
        texto_adicionar = ttk.Label(self, text = "Tipos de modificação:", font = FONTE_10_N)
        texto_adicionar.pack()

        # Botões para modificação do item
        botao_Produto = ttk.Button(self, text = "Alterar Item",
                                command = lambda: controle.show_frame(Alterar_Item))
        botao_Produto.pack(pady = 10, padx = 10)
        botao_Tipo = ttk.Button(self, text = "Excluir Item",
                                command = lambda: controle.show_frame(Excluir_Item))
        botao_Tipo.pack(pady = 10, padx = 10)

        # Botões para modificação do pedido
        botao_Produto = ttk.Button(self, text = "Alterar Pedido",
                                command = lambda: controle.show_frame(Alterar_Pedido))
        botao_Produto.pack(pady = 10, padx = 10)
        botao_Tipo = ttk.Button(self, text = "Excluir Pedido",
                                command = lambda: controle.show_frame(Excluir_Pedido))
        botao_Tipo.pack(pady = 10, padx = 10)

        # Botões para concluir ou cancelar essas ações, se selecionados, realizam suas ações e redireciionam para o início
        
        botao_para_Inicio = ttk.Button(self, text = "Início",
                                command = lambda: controle.show_frame(Inicio))
        botao_para_Inicio.pack(pady = 30, padx = 10)
###

##################################################################################################################################################################
##########**********************************************************************************************************************************************##########
#####                                                            Modificação de Item                                                                         #####


def alterar_item(v_id_item, v_id_pedido, v_quantidade):
    #cnx = pymysql.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)

    cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
    cursor = cnx.cursor()

    query = "UPDATE item SET quantidade = %s WHERE id_item = %s AND id_pedido = %s;"
    dados_pedido = (v_quantidade, v_id_item, v_id_pedido)
    cursor.execute(query, dados_pedido)
    cnx.commit()

    cursor.close()
    cnx.close()

    print("Item alterado. Código = ", v_id_item, ".")
    print("Pedido = ", v_id_pedido, ".")
    
####

# Classe de onde serão alterados os itens do Cardápio
class Alterar_Item(tk.Frame):

    def __init__(self, parent, controle):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text = "Alterar Item", font = FONTE_12_B)
        label.pack(pady = 10, padx = 10)
        
        self.tv = ttk.Treeview(self, columns=('Código do Item', 'Código do Pedido', 'Código do Produto', 'Quantidade'))
        self.tv.column("#0",minwidth=0,width=0)
        self.tv.column('Código do Item', width=100, anchor='center')
        self.tv.heading('Código do Item', text='Código do Item')
        self.tv.column('Código do Pedido', width=150, anchor='center')
        self.tv.heading('Código do Pedido', text='Código do Pedido')
        self.tv.column('Código do Produto', width=150, anchor='center')
        self.tv.heading('Código do Produto', text='Código do Produto')
        self.tv.column('Quantidade', width=100, anchor='center')
        self.tv.heading('Quantidade', text='Quantidade')
        
        self.tv.pack()

        #gera conexão para inserção dos dados do banco para a treeview
        #cnx = pymysql.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)

        cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
        cursor = cnx.cursor()
        
        query = "select * from item;"
 
        cursor.execute(query)

        linha = cursor.fetchall()
        count = cursor.rowcount

        if count != 0:

            for (vid_item, vid_pedido, vid_produto, quantidade) in linha:
                self.tv.insert("", "end", text = "Produtos", values = (vid_item, vid_pedido, vid_produto, quantidade))

        cursor.close()

        cnx.close()
        
        texto_pedido = ttk.Label(self, text = "Adicione os dados e clique em \"Salvar Alterações\" para adicionar o item", font = FONTE_10_N)
        texto_pedido.pack()
        texto_pedido = ttk.Label(self, text = "Para voltar ou cancelar, clique em Início \"Início\"", font = FONTE_10_N)
        texto_pedido.pack()
        
        label_iditem = ttk.Label(self, text = "Código do item:", font = FONTE_10_N)
        label_iditem.pack()
        caixa_entrada_iditem = ttk.Entry(self, width = 50)
        caixa_entrada_iditem.pack(pady = 10, padx = 10)

        label_idpedido = ttk.Label(self, text = "Código do produto:", font = FONTE_10_N)
        label_idpedido.pack()
        caixa_entrada_idpedido = ttk.Entry(self, width = 50)
        caixa_entrada_idpedido.pack(pady = 10, padx = 10)

        label_quantidade = ttk.Label(self, text = "Quantidade:", font = FONTE_10_N)
        label_quantidade.pack()
        caixa_entrada_quantidade = ttk.Entry(self, width = 50)
        caixa_entrada_quantidade.pack(pady = 10, padx = 10)

        botao_para_Cardapio = ttk.Button(self, text = "Concluir",
                                command = lambda: alterar_item(caixa_entrada_iditem.get(), caixa_entrada_idpedido.get(), caixa_entrada_quantidade.get()))
        botao_para_Cardapio.pack(pady = 2, padx = 10)
        
        botao_para_Cardapio = ttk.Button(self, text = "Início",
                                command = lambda: controle.show_frame(Inicio))
        botao_para_Cardapio.pack(pady = 2, padx = 10)
###

##*****
# Exclui item um a um, com o código do item
def exclui_item(v_id_pedido, v_id_item):
    #cnx = pymysql.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)

    cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
    cursor = cnx.cursor()
    query = "DELETE FROM item WHERE id_item = %s AND id_pedido = %s;"
    dados_tipo = (v_id_item, v_id_pedido)
    cursor.execute(query, dados_tipo)
    cnx.commit()

    print("Deletado com sucesso!")

    cursor.close()
    cnx.close()
###

# Classe para Excluir um Item
class Excluir_Item(tk.Frame):

    def __init__(self, parent, controle):
        tk.Frame.__init__(self, parent)

        self.id_item = 0

        label = tk.Label(self, text = "Excluir Item", font = FONTE_12_B)
        label.pack(pady = 10, padx = 10)

        texto_pedido = ttk.Label(self, text = "Adicione os dados e clique em \"Salvar Alterações\" para adicionar o item", font = FONTE_10_N)
        texto_pedido.pack()
        texto_pedido = ttk.Label(self, text = "Para voltar ou cancelar, clique em Início \"Início\"", font = FONTE_10_N)
        texto_pedido.pack()
        
        self.tv = ttk.Treeview(self, columns=('Código do Item', 'Código do Pedido', 'Código do Produto', 'Quantidade'))
        self.tv.column("#0",minwidth=0,width=0)
        self.tv.column('Código do Item', width=100, anchor='center')
        self.tv.heading('Código do Item', text='Código do Item')
        self.tv.column('Código do Pedido', width=150, anchor='center')
        self.tv.heading('Código do Pedido', text='Código do Pedido')
        self.tv.column('Código do Produto', width=150, anchor='center')
        self.tv.heading('Código do Produto', text='Código do Produto')
        self.tv.column('Quantidade', width=100, anchor='center')
        self.tv.heading('Quantidade', text='Quantidade')
        
        self.tv.pack()

        #gera conexão para inserção dos dados do banco para a treeview
        #cnx = pymysql.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)

        cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
        cursor = cnx.cursor()
        
        query = "select * from item;"
 
        cursor.execute(query)

        linha = cursor.fetchall()
        count = cursor.rowcount

        if count != 0:

            for (vid_item, vid_pedido, vid_produto, quantidade) in linha:
                self.tv.insert("", "end", text = "Produtos", values = (vid_item, vid_pedido, vid_produto, quantidade))

        cursor.close()

        cnx.close()

        label_idItem = ttk.Label(self, text = "Código do Item:", font = FONTE_10_N)
        label_idItem.pack()
        caixa_entrada_idItem = ttk.Entry(self, width = 50)
        caixa_entrada_idItem.pack(pady = 10, padx = 10)

        label_idPedido = ttk.Label(self, text = "Código do Pedido:", font = FONTE_10_N)
        label_idPedido.pack()
        caixa_entrada_idPedido = ttk.Entry(self, width = 50)
        caixa_entrada_idPedido.pack(pady = 10, padx = 10)

        botao_para_Cardapio = ttk.Button(self, text = "Concluir",
                                command = lambda: exclui_item(caixa_entrada_idPedido.get(), caixa_entrada_idItem.get()))
        botao_para_Cardapio.pack(pady = 2, padx = 10)
        
        botao_para_Inicio = ttk.Button(self, text = "Início",
                                command = lambda: controle.show_frame(Inicio))
        botao_para_Inicio.pack(pady = 10, padx = 10)

    def selecionar_pedido(codigo_pedido):
        pedido = self.tv.selection()[0]
        self.id_item = self.tv.pedido(pedido)['values'][0]

        texto_pedido = ttk.Label(self, text = "Código do item: " + self.id_pedido, font = FONTE_10_N)
        texto_pedido.pack()
####

##################################################################################################################################################################
##########**********************************************************************************************************************************************##########
#####                                                           Modificação de Pedido                                                                        #####

##*****
# Altera pedido
def alterar_pedido(v_id_pedido, v_observacao):
    #cnx = pymysql.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)

    cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
    cursor = cnx.cursor()

    query = "UPDATE pedido SET pedido.observacao = %s WHERE id_pedido = %s;"
    dados_pedido = (v_observacao, v_id_pedido)
    cursor.execute(query, tuple(dados_pedido))
    cnx.commit()

    cursor.close()
    cnx.close()

    print("Pedido alterado. Senha do pedido = ", v_id_pedido, ". Nova observação: ", v_observacao)


# Classe de onde serão alterados os itens do Cardápio
class Alterar_Pedido(tk.Frame):

    def __init__(self, parent, controle):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text = "Alterar Pedido", font = FONTE_12_B)
        label.pack(pady = 10, padx = 10)

        self.tv = ttk.Treeview(self, columns=('Senha do Pedido', 'Estado', 'Observação', 'Data e Hora'))
        self.tv.column("#0",minwidth=0,width=0)
        self.tv.column('Senha do Pedido', width=50, anchor='center')
        self.tv.heading('Senha do Pedido', text='Senha do Pedido')
        self.tv.column('Estado', width=100, anchor='center')
        self.tv.heading('Estado', text='Estado')
        self.tv.column('Observação', width=250, anchor='center')
        self.tv.heading('Observação', text='Observação')
        self.tv.column('Data e Hora', width=150, anchor='center')
        self.tv.heading('Data e Hora', text='Data e Hora')
        
        self.tv.pack()

        #gera conexão para inserção dos dados do banco para a treeview
        #cnx = pymysql.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)

        cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
        cursor = cnx.cursor()
        
        query = "select * from pedido;"
 
        cursor.execute(query)

        linha = cursor.fetchall()
        count = cursor.rowcount

        if count != 0:

            for (vid_pedido, v_estado, v_observacao, v_dia_hora) in linha:
                self.tv.insert("", "end", text = "Pedido", values = (vid_pedido, v_estado, v_dia_hora, v_observacao))

        cursor.close()
        cnx.close()
        
        texto_pedido = ttk.Label(self, text = "Adicione os dados e clique em \"Salvar Alterações\" para adicionar o item", font = FONTE_10_N)
        texto_pedido.pack()
        texto_pedido = ttk.Label(self, text = "Para voltar ou cancelar, clique em Início \"Início\"", font = FONTE_10_N)
        texto_pedido.pack()

        label_idpedido = ttk.Label(self, text = "Senha do Pedido:", font = FONTE_10_N)
        label_idpedido.pack()
        caixa_entrada_idpedido = ttk.Entry(self, width = 50)
        caixa_entrada_idpedido.pack(pady = 10, padx = 10)

        label_observacao = ttk.Label(self, text = "Observação:", font = FONTE_10_N)
        label_observacao.pack()
        caixa_entrada_observacao = ttk.Entry(self, width = 50)
        caixa_entrada_observacao.pack(pady = 10, padx = 10)

        botao_para_Cardapio = ttk.Button(self, text = "Concluir",
                                command = lambda: alterar_pedido(caixa_entrada_idpedido.get(), caixa_entrada_observacao.get()))
        botao_para_Cardapio.pack(pady = 2, padx = 10)
        
        botao_para_Cardapio = ttk.Button(self, text = "Início",
                                command = lambda: controle.show_frame(Inicio))
        botao_para_Cardapio.pack(pady = 2, padx = 10)
###
        
##*****
# Exclui item um a um, com o código do pedido
def exclui_pedido(c_id_pedido):
    #cnx = pymysql.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)

    cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
    cursor = cnx.cursor()

    query = "select * from item where id_pedido = "+str(c_id_pedido)
    
    cursor.execute(query)

    linha = cursor.fetchall()
    count = cursor.rowcount

    for (v_id_item) in linha:
        if count != 0 :
            cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
            cursor = cnx.cursor()
            
            query = "DELETE FROM item where id_item = %s"
            dados_tipo = (v_id_item)
            cursor.execute(query, dados_tipo)
            cnx.commit()
            
            cursor.close()
            cnx.close()
    
    query = "DELETE FROM pedido WHERE id_pedido = "+str(c_id_pedido)
    cursor.execute(query)
    cnx.commit()

    print("Deletado com sucesso!")

    cursor.close()
    cnx.close()
###

# Classe para Excluir um pedido
class Excluir_Pedido(tk.Frame):

    def __init__(self, parent, controle):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text = "Excluir Pedido", font = FONTE_12_B)
        label.pack(pady = 10, padx = 10)

        texto_pedido = ttk.Label(self, text = "Clique em cima do pedido para selecioná-lo", font = FONTE_10_N)
        texto_pedido.pack()
        texto_pedido = ttk.Label(self, text = "Clique \"Concluir\" para finalizar", font = FONTE_10_N)
        texto_pedido.pack()
        texto_pedido = ttk.Label(self, text = "Clique \"Início\" para cancelar ou voltar", font = FONTE_10_N)
        texto_pedido.pack()

        self.tv = ttk.Treeview(self, columns=('Senha', 'Estado', 'Observação', 'Data e Hora'))
        self.tv.column("#0",minwidth=0,width=0)
        self.tv.column('Senha', width=50, anchor='center')
        self.tv.heading('Senha', text='Senha')
        self.tv.column('Estado', width=100, anchor='center')
        self.tv.heading('Estado', text='Estado')
        self.tv.column('Observação', width=250, anchor='center')
        self.tv.heading('Observação', text='Observação')
        self.tv.column('Data e Hora', width=150, anchor='center')
        self.tv.heading('Data e Hora', text='Data e Hora')
        
        self.tv.pack()

        #gera conexão para inserção dos dados do banco para a treeview
        #cnx = pymysql.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)

        cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
        cursor = cnx.cursor()
        
        query = "select * from pedido;"
 
        cursor.execute(query)

        linha = cursor.fetchall()
        count = cursor.rowcount

        if count != 0:

            for (vid_pedido, v_estado, v_observacao, v_dia_hora) in linha:
                self.tv.insert("", "end", text = "Pedido", values = (vid_pedido, v_estado, v_dia_hora, v_observacao))

        cursor.close()
        cnx.close()

        label_idpedido = ttk.Label(self, text = "Senha do Pedido:", font = FONTE_10_N)
        label_idpedido.pack()
        caixa_entrada_idpedido = ttk.Entry(self, width = 50)
        caixa_entrada_idpedido.pack(pady = 10, padx = 10)

        botao_para_Cardapio = ttk.Button(self, text = "Concluir",
                                command = lambda: exclui_pedido(caixa_entrada_idpedido.get()))
        botao_para_Cardapio.pack(pady = 2, padx = 10)
        
        botao_para_Inicio = ttk.Button(self, text = "Início",
                                command = lambda: controle.show_frame(Inicio))
        botao_para_Inicio.pack(pady = 10, padx = 10)
        
###
        
##################################################################################################################################################################
##########**********************************************************************************************************************************************##########
#####                                                           Edição de Cardápio                                                                           #####

# Classe para Editar o cardápio completo, como todos os produtos e tipos de produtos disponíveis
class Editar_Cardapio(tk.Frame):

    def __init__(self, parent, controle):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text = "Editar Cardápio", font = FONTE_12_B)
        label.pack(pady = 10, padx = 10)

        # Adiciona um produto ou tipo de produto
        texto_adicionar = ttk.Label(self, text = "Adicionar:", font = FONTE_10_N)
        texto_adicionar.pack()

        botao_Produto = ttk.Button(self, text = "Produto",
                                command = lambda: controle.show_frame(Adicionar_Produto))
        botao_Produto.pack(pady = 10, padx = 10)
        botao_Tipo = ttk.Button(self, text = "Tipo de produto",
                                command = lambda: controle.show_frame(Adicionar_Tipo))
        botao_Tipo.pack(pady = 10, padx = 10)

        # Altera um produto ou tipo de produto
        texto_pedido = ttk.Label(self, text = "Alterar:", font = FONTE_10_N)
        texto_pedido.pack()

        botao_para_Cardapio = ttk.Button(self, text = "Produto",
                                command = lambda: controle.show_frame(Alterar_Produto))
        botao_para_Cardapio.pack(pady = 10, padx = 10)
        botao_para_Cardapio = ttk.Button(self, text = "Tipo de produto",
                                command = lambda: controle.show_frame(Alterar_Tipo))
        botao_para_Cardapio.pack(pady = 10, padx = 10)

        # Remove um produto ou tipo de produto
        texto_pedido = ttk.Label(self, text = "Remover:", font = FONTE_10_N)
        texto_pedido.pack()

        botao_para_Cardapio = ttk.Button(self, text = "Produto",
                                command = lambda: controle.show_frame(Excluir_Produto))
        botao_para_Cardapio.pack(pady = 10, padx = 10)
        botao_para_Cardapio = ttk.Button(self, text = "Tipo de produto",
                                command = lambda: controle.show_frame(Excluir_Tipo))
        botao_para_Cardapio.pack(pady = 10, padx = 10)

        # Botões para concluir ou cancelar essas ações, se selecionados, realizam suas ações e redireciionam para o início
        botao_para_Cardapio = ttk.Button(self, text = "Concluir",
                                command = lambda: controle.show_frame(Inicio))
        botao_para_Cardapio.pack(pady = 30, padx = 10)
        botao_para_Inicio = ttk.Button(self, text = "Início",
                                command = lambda: controle.show_frame(Inicio))
        botao_para_Inicio.pack(pady = 30, padx = 10)
###

##################################################################################################################################################################
##########**********************************************************************************************************************************************##########
#####                                                               Edição do Tipo                                                                           #####

# Função para Inserir um tipo
def adicionar_Tipo(c_tipo):
    #cnx = pymysql.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)

    cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
    cursor = cnx.cursor()
    query = "insert into tipo_de_produto (tipo) values (%s)"
    dados_tipo = (c_tipo)
    cursor.execute(query, dados_tipo)
    cnx.commit()

    cod_tipo = cursor.lastrowid
    print("Contato inserido. Código = ", cod_tipo)

    cursor.close()
    cnx.close()
###

# Classe para Adicionar um tipo
class Adicionar_Tipo(tk.Frame):

    def __init__(self, parent, controle):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text = "Adicionar Tipo", font = FONTE_12_B)
        label.pack(pady = 10, padx = 10)

        label_nome = tk.Label(self, text = "Nome:", font = FONTE_10_N)
        label_nome.pack(pady = 10, padx = 10)
        caixa_entrada_nome = ttk.Entry(self, width = 50)
        caixa_entrada_nome.pack(pady = 10, padx = 10)

        botao_para_Cardapio = ttk.Button(self, text = "Concluir",
                                command = lambda: adicionar_Tipo(caixa_entrada_nome.get()))
        botao_para_Cardapio.pack(pady = 2, padx = 10)
        
        botao_para_Inicio = ttk.Button(self, text = "Início",
                                command = lambda: controle.show_frame(Inicio))
        botao_para_Inicio.pack(pady = 10, padx = 10)
###
        
## *****
# Função para alterar um tipo
def alterar_Tipo(c_tipo, c_novo_tipo):

    #cnx = pymysql.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)

    cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
    cursor = cnx.cursor()
    query = "UPDATE tipo_de_produto SET tipo = %s WHERE tipo = %s"
    dados_tipo = (c_novo_tipo, c_tipo)
    cursor.execute(query, dados_tipo)
    cnx.commit()

    cod_tipo = cursor.lastrowid
    print("Alterado com sucesso!")

    cursor.close()
    cnx.close()
###
#### *****
    
## *****
# Classe para Alterar um tipo
class Alterar_Tipo(tk.Frame):

    def __init__(self, parent, controle):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text = "Adicionar Tipo", font = FONTE_12_B)
        label.pack(pady = 10, padx = 10)

        label_nome = tk.Label(self, text = "Nome atual:", font = FONTE_10_N)
        label_nome.pack(pady = 10, padx = 10)
        caixa_entrada_nome = ttk.Entry(self, width = 50)
        caixa_entrada_nome.pack(pady = 10, padx = 10)

        label_novo_nome = tk.Label(self, text = "Novo nome:", font = FONTE_10_N)
        label_novo_nome.pack(pady = 10, padx = 10)
        caixa_entrada_novo_nome = ttk.Entry(self, width = 50)
        caixa_entrada_novo_nome.pack(pady = 10, padx = 10)

        botao_para_Cardapio = ttk.Button(self, text = "Concluir",
                                command = lambda: alterar_Tipo(caixa_entrada_nome.get(), caixa_entrada_novo_nome.get()))
        botao_para_Cardapio.pack(pady = 2, padx = 10)
        
        botao_para_Inicio = ttk.Button(self, text = "Início",
                                command = lambda: controle.show_frame(Inicio))
        botao_para_Inicio.pack(pady = 10, padx = 10)
###
#### *****

## *****
# Classe para Excluir um tipo
def excluir_Tipo(c_tipo, c_id_tipo):
    #cnx = pymysql.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)

    cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
    cursor = cnx.cursor()
    query = "DELETE FROM tipo_de_produto WHERE id_tipo = %s OR tipo = %s;"
    dados_tipo = (c_id_tipo, c_tipo)
    cursor.execute(query, dados_tipo)
    cnx.commit()

    print("Deletado com sucesso!")

    cursor.close()
    cnx.close()
###
#### *****

## *****
# Classe para Excluir um tipo
class Excluir_Tipo(tk.Frame):

    def __init__(self, parent, controle):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text = "Excluir Tipo", font = FONTE_12_B)
        label.pack(pady = 10, padx = 10)

        label_nome = tk.Label(self, text = "Tipo:", font = FONTE_10_N)
        label_nome.pack(pady = 10, padx = 10)
        caixa_entrada_tipo = ttk.Entry(self, width = 50)
        caixa_entrada_tipo.pack(pady = 10, padx = 10)

        label_id = tk.Label(self, text = "Código do Tipo:", font = FONTE_10_N)
        label_id.pack(pady = 10, padx = 10)
        caixa_entrada_id = ttk.Entry(self, width = 50)
        caixa_entrada_id.pack(pady = 10, padx = 10)

        botao_para_Cardapio = ttk.Button(self, text = "Concluir",
                                command = lambda: excluir_Tipo(caixa_entrada_tipo.get(), caixa_entrada_id.get()))
        botao_para_Cardapio.pack(pady = 2, padx = 10)
        
        botao_para_Inicio = ttk.Button(self, text = "Início",
                                command = lambda: controle.show_frame(Inicio))
        botao_para_Inicio.pack(pady = 10, padx = 10)
###
#### *****

##################################################################################################################################################################
##########**********************************************************************************************************************************************##########
#####                                                              Edição do Produto                                                                         #####

# Função para Inserir um produto
def adicionar_Produto(c_nome, c_descricao, c_tamanho, c_valor, c_tipo):
    #cnx = pymysql.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)

    cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
    cursor = cnx.cursor()
    query = "INSERT INTO produto (nome, descricao, tamanho, valor, id_tipo) VALUES (%s, %s, %s, %s, %s)"
    dados_produto = (c_nome, c_descricao, c_tamanho, c_valor, c_tipo)
    cursor.execute(query, dados_produto)
    cnx.commit()

    cod_produto = cursor.lastrowid
    print("Produto inserido. Código = ", cod_produto)

    cursor.close()
    cnx.close()
###

# Classe para Adicionar um produto
class Adicionar_Produto(tk.Frame):

    def __init__(self, parent, controle):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text = "Adicionar Produto", font = FONTE_12_B)
        label.pack(pady = 10, padx = 10)

        label_nome = tk.Label(self, text = "Nome", font = FONTE_10_N)
        label_nome.pack(pady = 10, padx = 10)
        caixa_entrada_nome = ttk.Entry(self, width = 50)
        caixa_entrada_nome.pack(pady = 10, padx = 10)

        label_descricao = ttk.Label(self, text = "Descrição:", font = FONTE_10_N)
        label_descricao.pack()
        caixa_entrada_descricao = ttk.Entry(self, width = 50)
        caixa_entrada_descricao.pack(pady = 10, padx = 10)

        label_tamanho = ttk.Label(self, text = "Tamanho:", font = FONTE_10_N)
        label_tamanho.pack()
        caixa_entrada_tamanho = ttk.Entry(self, width = 50)
        caixa_entrada_tamanho.pack(pady = 10, padx = 10)

        label_valor = ttk.Label(self, text = "Valor:", font = FONTE_10_N)
        label_valor.pack()
        caixa_entrada_valor = ttk.Entry(self, width = 50)
        caixa_entrada_valor.pack(pady = 10, padx = 10)
        
        label_tipo = ttk.Label(self, text = "Tipo: (somente inteiros)", font = FONTE_10_N)
        label_tipo.pack()
        caixa_entrada_tipo = ttk.Entry(self, width = 50)
        caixa_entrada_tipo.pack(pady = 10, padx = 10)

        botao_para_Cardapio = ttk.Button(self, text = "Concluir",
                                command = lambda: inserir_Produto(caixa_entrada_nome.get(), caixa_entrada_descricao.get(), caixa_entrada_tamanho.get(), caixa_entrada_valor.get(), caixa_entrada_tipo.get()))
        botao_para_Cardapio.pack(pady = 2, padx = 10)

        botao_para_Inicio = ttk.Button(self, text = "Início",
                                command = lambda: controle.show_frame(Inicio))
        botao_para_Inicio.pack(pady = 10, padx = 10)
###


## *****
# Classe para Alterar um produto
def alterar_Produto(c_nome, c_descricao, c_tamanho, c_valor, c_id_tipo, id_pedido):
    #cnx = pymysql.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)

    cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
    cursor = cnx.cursor()
    query = "UPDATE produto SET nome = %s, descricao = %s, tamanho = %s, valor = %s, id_tipo = %s WHERE id_produto = %s"
    dados_produto = (c_nome, c_descricao, c_tamanho, c_valor, c_id_tipo, id_pedido)
    cursor.execute(query, dados_produto)
    cnx.commit()

    cod_produto = cursor.lastrowid
    print("Alterado com sucesso!")

    cursor.close()
    cnx.close()
###
#### *****

## *****
# Classe para Alterar um produto
class Alterar_Produto(tk.Frame):

    def __init__(self, parent, controle):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text = "Alterar Produto", font = FONTE_12_B)
        label.pack(pady = 10, padx = 10)
        label = tk.Label(self, text = "Complete todos os campos", font = ("Arial", 8))
        label.pack(pady = 10, padx = 10)


        label_nome = tk.Label(self, text = "Nome:", font = FONTE_10_N)
        label_nome.pack(pady = 10, padx = 10)
        caixa_entrada_nome = ttk.Entry(self, width = 50)
        caixa_entrada_nome.pack(pady = 10, padx = 10)

        label_descricao = ttk.Label(self, text = "Descrição:", font = FONTE_10_N)
        label_descricao.pack()
        caixa_entrada_descricao = ttk.Entry(self, width = 50)
        caixa_entrada_descricao.pack(pady = 10, padx = 10)

        label_tamanho = ttk.Label(self, text = "Tamanho:", font = FONTE_10_N)
        label_tamanho.pack()
        caixa_entrada_tamanho = ttk.Entry(self, width = 50)
        caixa_entrada_tamanho.pack(pady = 10, padx = 10)

        label_valor = ttk.Label(self, text = "Valor:", font = FONTE_10_N)
        label_valor.pack()
        caixa_entrada_valor = ttk.Entry(self, width = 50)
        caixa_entrada_valor.pack(pady = 10, padx = 10)

        label_tipo = ttk.Label(self, text = "Tipo:", font = FONTE_10_N)
        label_tipo.pack() 
        caixa_entrada_tipo = ttk.Entry(self, width = 50)
        caixa_entrada_tipo.pack(pady = 10, padx = 10)

        label_codigo = ttk.Label(self, text = "Código do produto:", font = FONTE_10_N)
        label_codigo.pack()
        caixa_entrada_codigo= ttk.Entry(self, width = 50)
        caixa_entrada_codigo.pack(pady = 10, padx = 10)

        botao_para_Alterar = ttk.Button(self, text = "Concluir",
                                command = lambda: alterar_Produto(caixa_entrada_nome.get(), caixa_entrada_descricao.get(), caixa_entrada_tamanho.get(), caixa_entrada_valor.get(), caixa_entrada_tipo.get(), caixa_entrada_codigo.get()))
        botao_para_Alterar.pack(pady = 10, padx = 10)
        botao_para_Inicio = ttk.Button(self, text = "Início",
                                command = lambda: controle.show_frame(Inicio))
        botao_para_Inicio.pack(pady = 10, padx = 10)
###
#### *****

## *****
# Função para Excluir um Produto
def excluir_Produto(c_id_produto):
    #cnx = pymysql.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)

    cnx = mysql.connector.connect(user = USUARIO, password = SENHA, port = PORTA, host = LOCAL, database = BASE)
    cursor = cnx.cursor()
    query = "DELETE FROM produto WHERE id_produto = '%s';"
    dados_produto = (c_id_produto)
    cursor.execute(query, dados_produto)
    cnx.commit()

    print("Deletado com sucesso!")

    cursor.close()
    cnx.close()
###
#### *****
    
## *****
# Classe para Excluir um produto
class Excluir_Produto(tk.Frame):

    def __init__(self, parent, controle):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text = "Excluir Produto", font = FONTE_12_B)
        label.pack(pady = 10, padx = 10)
        
        label_codigo = ttk.Label(self, text = "Código do produto:", font = FONTE_10_N)
        label_codigo.pack()
        caixa_entrada_codigo= ttk.Entry(self, width = 50)
        caixa_entrada_codigo.pack(pady = 10, padx = 10)

        botao_para_Excluir = ttk.Button(self, text = "Concluir",
                                command = lambda: excluir_Produto(caixa_entrada_codigo.get()))
        botao_para_Excluir.pack(pady = 10, padx = 10)
        botao_para_Inicio = ttk.Button(self, text = "Início",
                                command = lambda: controle.show_frame(Inicio))
        botao_para_Inicio.pack(pady = 10, padx = 10)
###
#### *****

app = Application()
app.mainloop()
