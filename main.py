import tkinter as tk #Biblioteca para interfaces gráficas
from tkinter import messagebox #Exibe mensagens de alerta, aviso ou informações ao usuário
import sqlite3 #biblioteca para interagir com o banco de dados SQLite


conn = sqlite3.connect('agenda.db') # cria ou abre o banco "agenda.db"
cursor = conn.cursor() # cria um cursor para interagir com o banco

# criação da tabela se não existir
cursor.execute('''
               Create TABLE IF NOT EXISTS contatos(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               nome TEXT UNIQUE NOT NULL,
               telefone TEXT NOT NULL
               )
               ''')
conn.commit()


def adicionar():
    nome = entry_nome.get().strip().title()
    telefone = entry_telefone.get().strip()
    if nome and telefone:
        try:
            cursor.execute("INSERT INTO contatos (nome, telefone) VALUES(?, ?)", (nome, telefone))
            conn.commit()
            messagebox.showinfo("Sucesso", "Contato adicionado com sucesso!")
        except sqlite3.IntegrityError:
            messagebox.showwarning ("Atenção", "Contato com este nome já existe!")
    else:
        messagebox.showwarning("Atenção", "Preencha todos os campos!")

def exibir():
    cursor.execute("SELECT nome, telefone FROM contatos")
    contatos = cursor.fetchall() # retorna todos os contatos do banco.
    if contatos:
        contatos_formatados = "\n".join([f'Nome: {nome}, Telefone: {telefone}' for nome, telefone in contatos])
        messagebox.showinfo("Lista de contatos", contatos_formatados)
    else:
        messagebox.showinfo("Lista de contatos", "Sem contatos adicionados.")


def buscar():
    nome = entry_nome.get().strip().title()
    cursor.execute("SELECT telefone FROM contatos WHERE nome = ?", (nome, ))
    resultado = cursor.fetchone()
    if resultado:
        telefone = resultado[0]
        messagebox.showinfo("Contato encontrado", f'Nome: {nome}\nTelefone: {telefone}')
    else:
        messagebox.showinfo("Atenção", "Contato não encontrado!")


def atualizar():
    nome_atual = entry_nome.get().strip().title()
    telefone = entry_telefone.get().strip().title()
    cursor.execute("SELECT * FROM contatos WHERE nome = ?", (nome_atual,))
    if cursor.fetchone():
        if telefone:
            cursor.execute("UPDATE contatos SET telefone = ? WHERE nome = ?", (telefone, nome_atual))
            conn.commit()
            messagebox.showinfo("Sucesso", "Contato atualizado com sucesso!")
        else: # Se o telefone não for fornecido, atualiza o nome
            novo_nome = entry_novo_nome.get().strip().title()
            if novo_nome and novo_nome != nome_atual:
                try:
                    cursor.execute("UPDATE contatos SET nome = ? WHERE nome = ?", (novo_nome, nome_atual))
                    conn.commit()
                    messagebox.showinfo("Sucesso", "Contato atualizado com sucesso!")
                except sqlite3.IntegrityError:
                    messagebox.showwarning("Atenção", "Contato com esse nome já existe!")
    else:
        messagebox.showwarning("Atenção", "Contato não encontrado!")


def deletar():
    nome = entry_nome.get().strip().title()
    cursor.execute("SELECT * FROM contatos WHERE nome = ?", (nome,))
    if cursor.fetchone():
        cursor.execute("DELETE FROM contatos WHERE nome = ?", (nome,))
        conn.commit()
        messagebox.showinfo("Sucesso", "Contato deletado com sucesso!")
    else:
        messagebox.showwarning("Atenção", "Contato não encontrado!")


# Inicializando a janela principal
root = tk.Tk()
root.title("Agenda de contatos")

# Adicionando rótulos e campos de entrada
# (a) nome
tk.Label(root, text="Nome:").grid(row=0, column=0)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1)

# (b) telefone
tk.Label(root, text="Telefone:").grid(row=1, column=0)
entry_telefone = tk.Entry(root)
entry_telefone.grid(row=1, column=1)

# (c) novo nome para atualização
tk.Label(root, text="Novo nome(para atualizar):").grid(row=2, column=0)
entry_novo_nome = tk.Entry(root)
entry_novo_nome.grid(row=2, column=1)

# Adicionando botões
# (a) Botão "Adicionar"
tk.Button(root, text="Adicionar", command=adicionar).grid(row=3, column=0)

# (b) Botão "Exibir"
tk.Button(root, text="Exibir", command=exibir).grid(row=3, column=1)

# (c) Botão "Buscar"
tk.Button(root, text="Buscar", command=buscar).grid(row=4, column=0)

# (d) Botão "Atualizar"
tk.Button(root, text="Atualizar", command=atualizar).grid(row=4, column=1)

# (e) Botão "Deletar"
tk.Button(root, text="Deletar", command=deletar).grid(row=5, column=0)

root.mainloop()

conn.close()