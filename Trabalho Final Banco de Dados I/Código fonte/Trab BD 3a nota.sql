/*	
	UFMA - Universidade Federal do Maranhão
    Gustavo Roberth Cruz Gomes
    Lucas de Jesus Carvalho Batalha
    
	CCCT0051 - Banco de Dados 2018.2
    
    Trabalho final

 	Este é um código SQL para craição de um banco de dados para um caixa de
		pizzaria, com venda de pratos e bebidas.
	O sistema armazena os dados dos pratos, bebidas, vendas e estoque, que
		são itens que estão contidos em um cardápio no banco de dados,
		podendo fazer alterações nos dados destes itens neste cardápio e pedidos.

*/

create database PIZZARIA;

use PIZZARIA;

create table tipo_de_produto (
	id_tipo int not null auto_increment,
	tipo varchar(15) not null,
	primary key (id_tipo)
);

create table produto (
	id_produto int not null auto_increment,
	id_tipo int not null,
	nome varchar(15) not null,
	descricao varchar(50) not null,
	tamanho varchar(10) not null,
    valor float not null,
	primary key (id_produto),
	foreign key (id_tipo) references tipo_de_produto (id_tipo)
);

create table pedido(
	id_pedido int not null auto_increment,
	estado int not null,
	data_dia_hora datetime not null,
	observacao varchar(50) null,
	primary key (id_pedido)
);

create table item(
	id_item int not null auto_increment,
	id_pedido int not null,
    id_produto int not null,
	quantidade int not null, /*de itens em um pedido de */
	PRIMARY KEY (id_item),
	FOREIGN KEY (id_pedido) REFERENCES pedido (id_pedido),
	FOREIGN KEY (id_produto) REFERENCES produto (id_produto)
);


/***** INSERÇÃO DE TIPOS DE PRODUTOS *****/
INSERT INTO tipo_de_produto (id_tipo, tipo) VALUES
	(1, 'Pizzas'),
    (2, 'Pratos'), /* e Acompanhamentos*/
    (3, 'Bebidas')
;
SELECT * FROM tipo_de_produto;

/***** INSERÇÃO DE PRODUTOS *****/
INSERT INTO produto (id_produto, id_tipo, nome, descricao, tamanho, valor) VALUES
	(1, 1, 'Calabresa', 'Uma tradicional pizza com muito queijo e calabresa', '8 fatias', 14.99),
    (2, 1, 'Pepperoni', 'Uma bela pizza de pepperoni e queijo parmesão', '8 fatias', 19.99),
    (3, 1, '4 Queijos', 'Uma maravilhosa pizza com 4 queijos deliciosos', '8 fatias', 24.99),
    (4, 1, 'Mussarela', 'Uma deliciosa pizza com muita mussarela', '8 fatias', 19.99),
    (5, 1, 'Portuguesa', 'Pizza de origem europeia, com ovos e toscana', '8 fatias', 19.99),
    (6, 1, 'Royale 007', 'Pizza Premium, OURO COMESTÍVEL, lagosta e caviar', '8 fatias', 99.99),
    (7, 2, 'Macarronada', 'Macarronada com muito molho de tomate e almôndegas', '2 porções', 14.99),
    (8, 2, 'Lasanha', 'Deliciosa lasanha italiana, perfeita a dois', '2 porções', 19.99),
    (9, 3, 'Refrigerante', 'Coca-cola, Guaraná Jesus e Guaraná Antartica', '2 L', 6.99),
    (10, 3, 'Refrigerante', 'Coca-cola, Guaraná Jesus e Guaraná Antartica', '1 L', 3.99),
    (11, 3, 'Vinho', 'Delicioso vinho, perfeito para qualquer ocasião', '600 ml', 17.99),
    (12, 1, '4 Queijos', 'Uma maravilhosa pizza com 4 queijos deliciosos',32, 24.99)
;
SELECT * FROM produto;

select id_pedido, estado, observacao, data_dia_hora, (Select SUM(produto.valor*item.quantidade) FROM item, produto WHERE item.id_pedido = pedido.id_pedido and produto.id_produto = item.id_produto) from pedido;

/*****  APRESENTA UM CARDÁPIO PEQUENO *****/
SELECT
	produto.nome AS 'Prato',
    produto.descricao AS 'Descricao',
    produto.tamanho AS 'Tamanho',
    produto.valor AS 'Valor'
FROM produto
;


/***** CRIA UM PEDIDO PARA INSERÇÃO DE ITENS *****/
INSERT INTO pedido (id_pedido, estado, observacao, data_dia_hora) VALUES
	(1, 1, 'Quero minha pizza bem quente', '2018-12-02 00:00:00'),
    (2, 1, 'Minha pizza deve estar com a borda dourada', '2018-12-02 12:03:00'),
	(3, 1, 'Quero Guaraná Jesus, sou maranhense', '2018-12-02 00:00:00'),
    (4, 1, 'Pizza e refri Jesus', '2018-12-02 12:03:00'),
	(5, 1, 'Por favor, refri e lasanha', '2018-12-02 00:00:00')
;
SELECT * FROM pedido;

/***** INSERÇÃO DE ITEM DE PRODUTOS *****/
INSERT INTO item (id_item, id_pedido, id_produto, quantidade) VALUES
    (1, 1, 1, 2),
    (2, 1, 9, 3),
    (3, 1, 2, 2),
    (4, 1, 3, 3),
    (5, 2, 2, 1),
    (6, 2, 3, 2),
    (7, 3, 9, 3),
    (8, 3, 3, 2),
    (9, 4, 9, 2),
    (10, 4, 2, 3),
    (11, 5, 8, 2),
    (12, 5, 10, 1)
;
SELECT * FROM item;

/***** APRESENTA OS ITENS DE UM PEDIDO JÁ REALIZADO *****/
SELECT
	produto.nome AS 'Produto',
	produto.descricao AS 'Descrição',
    produto.tamanho AS 'Tamanho (fatias)',
    pedido.id_pedido AS 'Senha',
    pedido.observacao AS 'Observação',
    item.quantidade AS 'Quantidade',
    pedido.data_dia_hora AS 'Data e Hora',
    produto.valor*item.quantidade AS 'Valor total'
FROM produto, pedido, item
WHERE produto.id_produto = item.id_produto
AND item.id_pedido = pedido.id_pedido
AND pedido.id_pedido = 1
;

/***** APRESENTA O VALOR TOTAL DE UM PEDIDO JÁ REALIZADO *****/
SELECT pedido.id_pedido, SUM(produto.valor*item.quantidade) AS 'TOTAL'
FROM produto, item, pedido
WHERE produto.id_produto = item.id_produto
AND item.id_pedido = pedido.id_pedido
;

/***** ALTERA UM ITEM DE UM PEDIDO ESPECIFICADO PELO SEU id_item *****/
UPDATE item AS I JOIN produto AS P ON  I.id_produto = P.id_produto
SET I.id_produto = 3
WHERE I.id_pedido = 1
AND I.quantidade = 3
AND P.nome = 'Calabresa'
;
SELECT * from item;

/***** ATUALIZA UM PRODUTO ESPECIFICADO PELO SEU id_item *****/
UPDATE produto
SET produto.nome = 'Frango'
WHERE produto.nome = '4 Queijos'
;


/***** EXCLUI UM ITEM DE UM PEDIDO ESPECIFICADO PELO SEU id_item *****/
DELETE FROM item WHERE item.id_item = 5;
SELECT * FROM item;

UPDATE item SET quantidade = 3 WHERE id_item = 1 AND id_pedido = 1;
