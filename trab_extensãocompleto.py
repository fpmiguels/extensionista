import mysql.connector
import bcrypt
from unidecode import unidecode 

# Função para conectar ao banco de dados
def conectar_bd():
    return mysql.connector.connect(host= ----, user= -----, password= ---- , database= ----) #Conecta ao servidor e banco de dados, motivo de segurança está incompleto

# Função para cadastrar um novo trabalhador
def cadastrar_trabalhador(idCPF, email, nome, bairro, servico, contato, senha):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        # Criptografar a senha
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("INSERT INTO Trabalhador (idCPF, Email, Nome, Bairro, Serviço, Contato, Senha_hash) VALUES (%s, %s, %s, %s, %s, %s, %s)", (idCPF, email, nome, bairro, servico, contato, senha_hash))
        conn.commit()
        print("Trabalhador cadastrado com sucesso.")
    except mysql.connector.Error as err:
        print(f"Erro ao cadastrar trabalhador: {err}")
    finally:
        cursor.close()
        conn.close()
        menu_principal() 

# Função para cadastrar um novo usuário
def cadastrar_usuario(idCPF, email, nome, endereco, bairro, senha):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        # Criptografar a senha
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        cursor.execute("INSERT INTO Usuário (idCPF, Email, Nome, Endereço, Bairro, Senha_hash) VALUES (%s, %s, %s, %s, %s, %s)", (idCPF, email, nome, endereco, bairro, senha_hash))
        conn.commit()
        print("Usuário cadastrado com sucesso.")
    except mysql.connector.Error as err:
        print(f"Erro ao cadastrar usuário: {err}")
    finally:
        cursor.close()
        conn.close()
        menu_principal() 

# Função para realizar o login de um trabalhador
def login_trabalhador(idCPF, senha):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Senha_hash FROM Trabalhador WHERE idCPF = %s", (idCPF,))
        trabalhador = cursor.fetchone()
        if trabalhador:
            # Verificar a senha
            if bcrypt.checkpw(senha.encode('utf-8'), trabalhador[0].encode('utf-8')):
                print("Login bem-sucedido!")
                return True
            else:
                print("Senha incorreta.")
                return False
        else:
            print("Cadastro não encontrado.")
            return False
    except mysql.connector.Error as err:
        print(f"Erro ao realizar login: {err}")
    finally:
        cursor.close()
        conn.close()

# Função para realizar o login de um usuário
def login_usuario(idCPF, senha):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT Senha_hash FROM Usuário WHERE idCPF = %s", (idCPF,))
        usuario = cursor.fetchone()
        if usuario:
            # Verificar a senha
            if bcrypt.checkpw(senha.encode('utf-8'), usuario[0].encode('utf-8')):
                print("Login bem-sucedido!")
                return True
            else:
                print("Senha incorreta.")
                return False
        else:
            print("Usuário não encontrado.")
            return False
    except mysql.connector.Error as err:
        print(f"Erro ao realizar login: {err}")
    finally:
        cursor.close()
        conn.close()

# Função para cadastro de trabalhador
def cadastro_trabalhador():
    idCPF = input("Digite seu CPF: ")
    email = input("Digite seu email: ")
    nome = input("Digite seu nome: ")
    bairro = input("Digite seu bairro: ")
    servico = input("Digite seu serviço: ")
    contato = input("Digite seu contato: ")
    senha = input("Digite sua senha: ")

    cadastrar_trabalhador(idCPF, email, nome, bairro, servico, contato, senha)
    menu_principal()

# Função para cadastro de usuário
def cadastro_usuario():
    idCPF = input("Digite seu CPF: ")
    email = input("Digite seu email: ")
    nome = input("Digite seu nome: ")
    endereco = input("Digite o seu endereço: ")
    bairro = input("Digite seu bairro: ")
    senha = input("Digite sua senha: ")

    cadastrar_usuario(idCPF, email, nome, endereco, bairro, senha)
    menu_principal()

# Função para menu de consulta de trabalhadores
def menu_consulta_trabalhadores():
    servico = input("Digite o serviço desejado: ")
    bairro = input("Digite o bairro desejado: ")
    
    consultar_trabalhadores(servico, bairro)

# Função para obter os dados do trabalhador com base no CPF
def obter_dados_trabalhador(idCPF):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT idCPF, Email, Nome, Bairro, Serviço, Contato FROM Trabalhador WHERE idCPF = %s", (idCPF,))
        resultado = cursor.fetchone()
        return resultado  # Retorna os dados do trabalhador se encontrado
    except mysql.connector.Error as err:
        print(f"Erro ao obter dados do trabalhador: {err}")
    finally:
        cursor.close()
        conn.close()

# Função para consultar serviços disponíveis
def consultar_trabalhadores(servico, bairro):
    conn = conectar_bd()
    cursor = conn.cursor()
    try:
        # Normalizar os termos de pesquisa removendo a acentuação e convertendo para minúsculas
        servico_normalizado = unidecode(servico).lower()
        bairro_normalizado = unidecode(bairro).lower()

        # Consultar trabalhadores sem diferenciar maiúsculas de minúsculas
        cursor.execute("SELECT Nome, Serviço, Contato FROM Trabalhador WHERE LOWER(Serviço) = %s AND LOWER(Bairro) = %s", (servico_normalizado, bairro_normalizado))
        resultados = cursor.fetchall()
        if resultados:
            print("Trabalhadores encontrados:")
            for resultado in resultados:
                print("Nome:", resultado[0])
                print("Serviço:", resultado[1])
                print("Contato:", resultado[2])
        else:
            print("Nenhum trabalhador encontrado.")
    except mysql.connector.Error as err:
        print(f"Erro ao consultar trabalhadores: {err}")
    finally:
        cursor.close()
        conn.close()

# Função para login de trabalhador
def login_trabalhador_opcao():
    idCPF = input("Digite o CPF: ")
    senha = input("Digite a senha: ")

    if login_trabalhador(idCPF, senha):
        dados_trabalhador = obter_dados_trabalhador(idCPF)
        if dados_trabalhador:
            print("Seus dados cadastrados:")
            print("CPF:", dados_trabalhador[0])
            print("Email:", dados_trabalhador[1])
            print("Nome:", dados_trabalhador[2])
            print("Bairro:", dados_trabalhador[3])
            print("Serviço:", dados_trabalhador[4])
            print("Contato:", dados_trabalhador[5])
        else:
            print("Trabalhador não encontrado.")
    else:
        print("Login falhou. Tente novamente.")
        menu_principal() 

# Função Login do usuario
def login_usuario_opcao():
    idCPF = input("Digite o CPF: ")
    senha = input("Digite a senha: ")

    if login_usuario(idCPF, senha):        
        menu_consulta_trabalhadores()
    else:
        print("Login falhou. Tente novamente.")
        menu_principal()

# Menu principal
def menu_principal():
    print("1. Cadastro")
    print("2. Login")
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        print("1. Cadastro de Trabalhador")
        print("2. Cadastro de Usuário")
        opcao_cadastro = input("Escolha uma opção de cadastro: ")

        if opcao_cadastro == "1":
            cadastro_trabalhador()
        elif opcao_cadastro == "2":
            cadastro_usuario()
        else:
            print("Opção inválida.")
    elif opcao == "2":
        print("1. Login de Trabalhador")
        print("2. Login de Usuário")
        opcao_login = input("Escolha uma opção de login: ")

        if opcao_login == "1":
            login_trabalhador_opcao()
        elif opcao_login == "2":
            login_usuario_opcao()
        else:
            print("Opção inválida.")
    else:
        print("Opção inválida.")

# Executar o programa
menu_principal()
