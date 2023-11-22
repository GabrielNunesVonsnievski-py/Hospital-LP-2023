import mysql.connector
from tkinter import Tk, Label, Button, Entry, StringVar, messagebox, Listbox

conexao = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="hospital",
)
cursor = conexao.cursor()

# Funções para manipulação de pacientes
def adicionar_paciente(entry_id, entry_nome, entry_idade, entry_telefone, entry_endereco, listbox_pacientes):
    id_paciente = entry_id.get()
    nome = entry_nome.get()
    idade = entry_idade.get()
    telefone = entry_telefone.get()
    endereco = entry_endereco.get()

    comando = f'INSERT INTO pacientes (id, nome, idade, telefone, endereco) VALUES ("{id_paciente}", "{nome}", {idade}, {telefone}, "{endereco}")'
    cursor.execute(comando)
    conexao.commit()

    messagebox.showinfo("Sucesso", "Paciente adicionado com sucesso!")

    # Atualizar a lista de pacientes após adicionar um novo
    atualizar_lista_pacientes(listbox_pacientes)

def mostrar_pacientes(listbox_pacientes):
    comando = 'SELECT * FROM pacientes'
    cursor.execute(comando)
    resultado = cursor.fetchall()

    listbox_pacientes.delete(0, 'end')  # Limpar a lista atual

    for i in resultado:
        listbox_pacientes.insert('end', f"ID: {i[0]}    NOME: {i[1]}   IDADE: {i[2]}   TELEFONE: {i[3]}  ENDERECO: {i[4]}")

def editar_paciente(listbox_pacientes, entry_id, entry_nome, entry_idade, entry_telefone, entry_endereco):
    selecionado = listbox_pacientes.curselection()
    
    if not selecionado:
        messagebox.showinfo("Aviso", "Selecione um paciente para editar.")
        return

    id_paciente = int(listbox_pacientes.get(selecionado[0]).split()[1])

    # Recuperar informações do paciente selecionado do banco de dados
    comando = f'SELECT * FROM pacientes WHERE id = {id_paciente}'
    cursor.execute(comando)
    paciente_selecionado = cursor.fetchone()

    # Preencher as entradas com as informações do paciente
    entry_id.delete(0, 'end')
    entry_id.insert('end', paciente_selecionado[0])
    entry_nome.delete(0, 'end')
    entry_nome.insert('end', paciente_selecionado[1])
    entry_idade.delete(0, 'end')
    entry_idade.insert('end', paciente_selecionado[2])
    entry_telefone.delete(0, 'end')
    entry_telefone.insert('end', paciente_selecionado[3])
    entry_endereco.delete(0, 'end')
    entry_endereco.insert('end', paciente_selecionado[4])

    # Criar botão de salvar alterações
    button_salvar = Button(root, text="Salvar Alterações", command=lambda: salvar_alteracoes_paciente(id_paciente, entry_id, entry_nome, entry_idade, entry_telefone, entry_endereco, listbox_pacientes, button_salvar))
    button_salvar.grid(row=8, column=0, columnspan=2)

def salvar_alteracoes_paciente(id_paciente, entry_id, entry_nome, entry_idade, entry_telefone, entry_endereco, listbox_pacientes, button_salvar):
    novo_id = entry_id.get()
    novo_nome = entry_nome.get()
    nova_idade = entry_idade.get()
    novo_telefone = entry_telefone.get()
    novo_endereco = entry_endereco.get()

    comando = f'UPDATE pacientes SET id="{novo_id}", nome="{novo_nome}", idade={nova_idade}, telefone={novo_telefone}, endereco="{novo_endereco}" WHERE id={id_paciente}'
    cursor.execute(comando)
    conexao.commit()

    messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")

    # Remover botão de salvar após salvar as alterações
    button_salvar.destroy()

    # Limpar as entradas
    entry_id.delete(0, 'end')
    entry_nome.delete(0, 'end')
    entry_idade.delete(0, 'end')
    entry_telefone.delete(0, 'end')
    entry_endereco.delete(0, 'end')

    # Atualizar a lista de pacientes após editar
    atualizar_lista_pacientes(listbox_pacientes)

def deletar_paciente(listbox_pacientes):
    selecionado = listbox_pacientes.curselection()

    if not selecionado:
        messagebox.showinfo("Aviso", "Selecione um paciente para deletar.")
        return

    id_paciente = int(listbox_pacientes.get(selecionado[0]).split()[1])

    op = messagebox.askquestion("Deletar Paciente", "Tem certeza que deseja deletar este paciente?")
    if op == 'yes':
        comando = f'DELETE from pacientes WHERE id = {id_paciente}'
        cursor.execute(comando)
        conexao.commit()
        messagebox.showinfo("Sucesso", "Paciente deletado com sucesso.")
        atualizar_lista_pacientes(listbox_pacientes)


def atualizar_lista_pacientes(listbox_pacientes):
    listbox_pacientes.delete(0, 'end')  # Limpar a lista atual

    comando = 'SELECT * FROM pacientes'
    cursor.execute(comando)
    resultado = cursor.fetchall()

    for i in resultado:
        listbox_pacientes.insert('end', f"ID: {i[0]}    NOME: {i[1]}   IDADE: {i[2]}   TELEFONE: {i[3]}  ENDERECO: {i[4]}")

def criar_interface():
    global root  # Declarei root como variável global para poder acessá-la em outras funções

    root = Tk()
    root.title("Hospital Management System")

    label_id = Label(root, text="Id:")
    label_nome = Label(root, text="Nome:")
    label_idade = Label(root, text="Idade:")
    label_telefone = Label(root, text="Telefone:")
    label_endereco = Label(root, text="Endereço:")

    entry_id = Entry(root)
    entry_nome = Entry(root)
    entry_idade = Entry(root)
    entry_telefone = Entry(root)
    entry_endereco = Entry(root)

    listbox_pacientes = Listbox(root, selectmode="single", width=40)
    listbox_pacientes.grid(row=0, column=2, rowspan=5)

    button_adicionar = Button(root, text="Adicionar Paciente", command=lambda: adicionar_paciente(entry_id, entry_nome, entry_idade, entry_telefone, entry_endereco, listbox_pacientes))
    button_mostrar = Button(root, text="Mostrar Pacientes", command=lambda: mostrar_pacientes(listbox_pacientes))
    button_editar = Button(root, text="Editar Paciente", command=lambda: editar_paciente(listbox_pacientes, entry_id, entry_nome, entry_idade, entry_telefone, entry_endereco))
    button_deletar = Button(root, text="Deletar Paciente", command=lambda: deletar_paciente(listbox_pacientes))

    label_id.grid(row=0, column=0)
    label_nome.grid(row=1, column=0)
    label_idade.grid(row=2, column=0)
    label_telefone.grid(row=3, column=0)
    label_endereco.grid(row=4, column=0)

    entry_id.grid(row=0, column=1)
    entry_nome.grid(row=1, column=1)
    entry_idade.grid(row=2, column=1)
    entry_telefone.grid(row=3, column=1)
    entry_endereco.grid(row=4, column=1)

    button_adicionar.grid(row=5, column=0, columnspan=2)
    button_mostrar.grid(row=6, column=0, columnspan=2)
    button_editar.grid(row=7, column=0, columnspan=2)
    button_deletar.grid(row=8, column=0, columnspan=2)

    root.mainloop()

# Chamada da interface
criar_interface()
