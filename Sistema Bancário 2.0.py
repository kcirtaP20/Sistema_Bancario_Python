from datetime import date, datetime

class Transacao:
    def registrar(self, conta):
        raise NotImplementedError("Este método deve ser implementado pelas subclasses.")

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if self.valor > 0:
            conta.saldo += self.valor
            conta.historico.adicionar_transacao(f"Depósito: R${self.valor:.2f} - {datetime.now()}")
            print("Depósito realizado com sucesso!")
            return True
        else:
            print("Erro: Valor de depósito inválido.")
            return False

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.numeros_saques >= conta.limite_saques:
            print("Erro: Limite de saques diários atingido.")
            return False
        elif self.valor > conta.saldo:
            print("Erro: Saldo insuficiente.")
            return False
        elif self.valor > 0:
            conta.saldo -= self.valor
            conta.historico.adicionar_transacao(f"Saque: R${self.valor:.2f} - {datetime.now()}")
            conta.numeros_saques += 1
            print("Saque realizado com sucesso!")
            return True
        else:
            print("Erro: Valor de saque inválido.")
            return False

class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

class Conta:
    def __init__(self, cliente, numero):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = '0001'
        self.cliente = cliente
        self.historico = Historico()

    def saldo_atual(self):
        return self.saldo

    def sacar(self, valor):
        saque = Saque(valor)
        return saque.registrar(self)

    def depositar(self, valor):
        deposito = Deposito(valor)
        return deposito.registrar(self)

class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite, limite_saques):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numeros_saques = 0

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        if transacao.registrar(conta):
            print("Transação realizada com sucesso.")
        else:
            print("Erro ao realizar a transação.")

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

# Sistema bancário
def menu():
    clientes = []
    contas = []

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
            data_nascimento = datetime.strptime(data_nascimento, "%d/%m/%Y").date()
            cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)
            clientes.append(cliente)
            print("Usuário criado com sucesso!")
        elif opcao == '2':
            cpf = input("CPF do usuário (apenas números): ")
            cliente = next((cliente for cliente in clientes if cliente.cpf == cpf), None)
            if not cliente:
                print("Erro: Usuário não encontrado.")
            else:
                numero_conta = len(contas) + 1
                conta = ContaCorrente(cliente, numero_conta, limite=500, limite_saques=3)
                cliente.adicionar_conta(conta)
                contas.append(conta)
                print(f"Conta {numero_conta} criada com sucesso para o usuário {cliente.nome}.")
        elif opcao == '3':
            numero_conta = int(input("Número da conta: "))
            valor = float(input("Valor do depósito: "))
            conta = next((conta for conta in contas if conta.numero == numero_conta), None)
            if conta:
                conta.depositar(valor)
            else:
                print("Erro: Conta não encontrada.")
        elif opcao == '4':
            numero_conta = int(input("Número da conta: "))
            valor = float(input("Valor do saque: "))
            conta = next((conta for conta in contas if conta.numero == numero_conta), None)
            if conta:
                conta.sacar(valor)
            else:
                print("Erro: Conta não encontrada.")
        elif opcao == '5':
            numero_conta = int(input("Número da conta: "))
            conta = next((conta for conta in contas if conta.numero == numero_conta), None)
            if conta:
                print("Extrato:")
                for transacao in conta.historico.transacoes:
                    print(transacao)
                print(f"Saldo atual: R${conta.saldo:.2f}")
            else:
                print("Erro: Conta não encontrada.")
        elif opcao == '6':
            for conta in contas:
                print(f"Agência: {conta.agencia}, Conta: {conta.numero}, Usuário: {conta.cliente.nome}")
        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Executar o menu do sistema bancário
if __name__ == "__main__":
    menu()
