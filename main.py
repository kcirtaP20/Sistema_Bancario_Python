import datetime

# Listas para armazenar usuários e contas
usuarios = []
contas = []


# Função para criar um novo usuário
def criar_usuario(nome, data_nascimento, cpf, endereco):
    if any(usuario['cpf'] == cpf for usuario in usuarios):
        print("Erro: Usuário com esse CPF já existe.")
        return
    novo_usuario = {
        'nome': nome,
        'data_nascimento': data_nascimento,
        'cpf': cpf,
        'endereco': endereco
    }
    usuarios.append(novo_usuario)
    print("Usuário criado com sucesso!")


# Função para criar uma nova conta bancária
def criar_conta(cpf):
    usuario = next((usuario for usuario in usuarios if usuario['cpf'] == cpf), None)
    if not usuario:
        print("Erro: Usuário não encontrado.")
        return

    numero_conta = len(contas) + 1
    nova_conta = {
        'agencia': '0001',
        'numero_conta': numero_conta,
        'usuario': usuario,
        'saldo': 0.0,
        'extrato': [],
        'limite_saques': 3,
        'numeros_saques': 0
    }
    contas.append(nova_conta)
    print(f"Conta {numero_conta} criada com sucesso para o usuário {usuario['nome']}.")


# Função para listar todas as contas criadas
def listar_contas():
    for conta in contas:
        print(f"Agência: {conta['agencia']}, Conta: {conta['numero_conta']}, Usuário: {conta['usuario']['nome']}")


# Função de depósito
def deposito(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        extrato.append(f"Depósito: R${valor:.2f} - {datetime.datetime.now()}")
        print("Depósito realizado com sucesso!")
    else:
        print("Erro: Valor de depósito inválido.")
    return saldo, extrato


# Função de saque
def saque(*, saldo, valor, extrato, limite, numeros_saques, limite_saques):
    if numeros_saques >= limite_saques:
        print("Erro: Limite de saques diários atingido.")
    elif valor > saldo:
        print("Erro: Saldo insuficiente.")
    elif valor > 0:
        saldo -= valor
        extrato.append(f"Saque: R${valor:.2f} - {datetime.datetime.now()}")
        numeros_saques += 1
        print("Saque realizado com sucesso!")
    else:
        print("Erro: Valor de saque inválido.")
    return saldo, extrato


# Função para exibir extrato
def exibir_extrato(saldo, *, extrato):
    print("Extrato:")
    for movimento in extrato:
        print(movimento)
    print(f"Saldo atual: R${saldo:.2f}")


# Menu do sistema bancário
def menu():
    while True:
        print("\n----- MENU -----")
        print("1. Criar Usuário")
        print("2. Criar Conta")
        print("3. Depósito")
        print("4. Saque")
        print("5. Extrato")
        print("6. Listar Contas")
        print("0. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            nome = input("Nome: ")
            data_nascimento = input("Data de Nascimento (dd/mm/aaaa): ")
            cpf = input("CPF (apenas números): ")
            endereco = input("Endereço (logradouro, número - bairro - cidade/UF): ")
            criar_usuario(nome, data_nascimento, cpf, endereco)
        elif opcao == '2':
            cpf = input("CPF do usuário (apenas números): ")
            criar_conta(cpf)
        elif opcao == '3':
            numero_conta = int(input("Número da conta: "))
            valor = float(input("Valor do depósito: "))
            conta = next((conta for conta in contas if conta['numero_conta'] == numero_conta), None)
            if conta:
                conta['saldo'], conta['extrato'] = deposito(conta['saldo'], valor, conta['extrato'])
            else:
                print("Erro: Conta não encontrada.")
        elif opcao == '4':
            numero_conta = int(input("Número da conta: "))
            valor = float(input("Valor do saque: "))
            conta = next((conta for conta in contas if conta['numero_conta'] == numero_conta), None)
            if conta:
                conta['saldo'], conta['extrato'] = saque(
                    saldo=conta['saldo'],
                    valor=valor,
                    extrato=conta['extrato'],
                    limite=conta['saldo'],
                    numeros_saques=conta['numeros_saques'],
                    limite_saques=conta['limite_saques']
                )
                conta['numeros_saques'] += 1
            else:
                print("Erro: Conta não encontrada.")
        elif opcao == '5':
            numero_conta = int(input("Número da conta: "))
            conta = next((conta for conta in contas if conta['numero_conta'] == numero_conta), None)
            if conta:
                exibir_extrato(conta['saldo'], extrato=conta['extrato'])
            else:
                print("Erro: Conta não encontrada.")
        elif opcao == '6':
            listar_contas()
        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")


# Executar o menu do sistema bancário
if __name__ == "__main__":
    menu()

