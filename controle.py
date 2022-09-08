from PyQt5 import uic,QtWidgets
import mysql.connector
from reportlab.pdfgen import canvas
import pandas as pd

numero_id = 0

banco = mysql.connector.connect (
    host="localhost",
    user="root",
    passwd="",
    database="cadastro_produtos"
)

def gerar_pdf():
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    y = 0
    pdf = canvas.Canvas("cadastro_produto.pdf")
    pdf.setFont("Times-Bold", 25)
    pdf.drawString(200,800, "Produtos cadastrados:")
    pdf.setFont("Times-Bold", 5)

    pdf.drawString(10,750, "ID")
    pdf.drawString(110,750, "CODIGO")
    pdf.drawString(210,750, "PRODUTO")
    pdf.drawString(310,750, "PRECO")
    pdf.drawString(410,750, "CATEGORIA")

    for i in range(0, len(dados_lidos)):
        y = y + 50
        pdf.drawString(10,750 - y, str(dados_lidos[i][0]))
        pdf.drawString(110,750 - y, str(dados_lidos[i][1]))
        pdf.drawString(210,750 - y, str(dados_lidos[i][2]))
        pdf.drawString(310,750 - y, str(dados_lidos[i][3]))
        pdf.drawString(410,750 - y, str(dados_lidos[i][4]))

    pdf.save()
    print("PDF FOI GERADO COM SUCESSO!")

    formplist.close()

def gerar_csv(): #ainda precisa organizar o csv em linhas e colunas
    print("csv")
    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()
    
    tdl = pd.DataFrame(data= dados_lidos)
    tdl.columns = ['ID', 'CODIGO', 'PRODUTO', 'PRECO', 'CATEGORIA'] 
    print("=-" * 38)
    print(tdl)
    tdl.to_csv("cadastro_produtos.csv", index= False)

    formplist.close()  

def funcao_principal():
    linha1 = formprodutos.lineEdit_1.text() #Código
    linha2 = formprodutos.lineEdit_2.text() #Descrição
    linha3 = formprodutos.lineEdit_3.text() #Preço

    categoria = ""

    if formprodutos.radioButton_1.isChecked(): # Os "radioButton_1" é o nome definido para o botão
        print("A categoria Pisos foi selecionada")
        categoria = "Pisos" 
    elif formprodutos.radioButton_2.isChecked(): # O método "isChecked()" é útilizado para confirmar que o botão foi selecionado
        print("A categoria Telhas foi selecionada")
        categoria = "Telhas" 
    elif formprodutos.radioButton_3.isChecked():
        print("A categoria Produtos de Banheiro foi selecionada")
        categoria = "Banheiro" 
    else:
        print("None")
        categoria = "None" 

    print("Código:", linha1) #Código
    print("Descrição:", linha2) #Descrição
    print("Preço:", linha3) #Preço

    cursor = banco.cursor()
    comando_SQL = "INSERT INTO produtos (codigo,descricao,preco,categoria) VALUES (%s,%s,%s,%s)"
    dados = (str(linha1), str(linha2), str(linha3), categoria)
    cursor.execute(comando_SQL, dados)
    banco.commit() 

    formprodutos.lineEdit_1.setText("")
    formprodutos.lineEdit_2.setText("")
    formprodutos.lineEdit_3.setText("")

def chama_segunda_tela():
    formplist.show()

    cursor = banco.cursor()
    comando_SQL = "SELECT * FROM produtos"
    cursor.execute(comando_SQL)
    dados_lidos = cursor.fetchall()

    formplist.tableWidget.setRowCount(len(dados_lidos))
    formplist.tableWidget.setColumnCount(5)

    for i in range (0, len(dados_lidos)):
        for j in range (0, 5):
            formplist.tableWidget.setItem(i,j,QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

def chama_tela_edit():
    global numero_id
    linha = formplist.tableWidget.currentRow()

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("SELECT * FROM produtos WHERE id =" + str(valor_id))
    produto = cursor.fetchall()
    formpedit.show()

    numero_id = valor_id

    formpedit.lineEdit.setText(str(produto[0][0]))
    formpedit.lineEdit_2.setText(str(produto[0][1]))
    formpedit.lineEdit_3.setText(str(produto[0][2]))
    formpedit.lineEdit_4.setText(str(produto[0][3]))
    formpedit.lineEdit_5.setText(str(produto[0][4]))

def salvar_edit():
    # pega o número do id
    global numero_id
    #valor digitado no lineEdit
    codigo = formpedit.lineEdit_2.text()
    descricao = formpedit.lineEdit_3.text()
    preco = formpedit.lineEdit_4.text()
    categoria = formpedit.lineEdit_5.text()
    #atualizar os dados no banco
    cursor = banco.cursor()
    cursor.execute("UPDATE produtos SET codigo = '{}', descricao = '{}', preco = '{}', categoria = '{}' WHERE id = {}".format(codigo,descricao,preco,categoria,numero_id))
    #atualizar as janelas
    formpedit.close()
    formplist.close()
    chama_segunda_tela()

def apagar_linha():
    linha = formplist.tableWidget.currentRow()
    formplist.tableWidget.removeRow(linha)

    cursor = banco.cursor()
    cursor.execute("SELECT id FROM produtos")
    dados_lidos = cursor.fetchall()
    valor_id = dados_lidos[linha][0]
    cursor.execute("DELETE FROM produtos WHERE id =" + str(valor_id))
    
app=QtWidgets.QApplication([])
formprodutos=uic.loadUi("formprodutos.ui") #tela 1
formplist=uic.loadUi("formprodutoslist.ui") #tela 2
formpedit=uic.loadUi("formprodutosedit.ui") #tela 3 
formprodutos.pushButton.clicked.connect(funcao_principal) #chama a função de acrescentar um produto
formprodutos.pushButton_2.clicked.connect(chama_segunda_tela) #chama a segunda tela
formplist.pushButton_3.clicked.connect(apagar_linha) #apaga um item do banco de dados
formplist.pushButton_4.clicked.connect(gerar_csv) #gera um csv
formplist.pushButton_5.clicked.connect(gerar_pdf) #gera um pdf
formplist.pushButton_6.clicked.connect(chama_tela_edit) #chama a tela de edição que se encontra na segunda tela
formpedit.pushButton_7.clicked.connect(salvar_edit) #salvar o item editado

formprodutos.show()
app.exec()


#criando a tabela MySQL

""" create table produtos (
    id INT NOT NULL AUTO_INCREMENT,
    codigo INT,
    descricao VARCHAR(50),
    preco DOUBLE,
    categoria VARCHAR(20),
    PRIMARY KEY (id)
); """

# inserindo registros na tabela

""" INSERT INTO produtos (codigo,descricao,preco,categoria) VALUES (123, "Piso Esmaltado Tipo A MT", 75.00, "Pisos"); """