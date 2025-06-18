#!/usr/bin/python3

import textwrap

class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco

class Conta:
    LIMITE_SAQUE = 1000
    MAX_SAQUES = 5

    def __init__(self, numero, usuario):
        self.agencia = "0001"
        self.numero = numero
        self.usuario = usuario
        self.saldo = 0.0
        self.extrato = []
        self.saques_hoje = 0

    def depositar(self, valor):
        if valor <= 0:
            return False, "Valor inválido para depósito."
        self.saldo += valor
        self.extrato.append(f"Depósito: +R${valor:.2f}")
        return True, f"Depositado R${valor:.2f}"

    def sacar(self, valor):
        if valor <= 0:
            return False, "Valor inválido para saque."
        if valor > self.saldo:
            return False, "Saldo insuficiente."
        if valor > self.LIMITE_SAQUE:
            return False, f"Limite de saque excedido (R${self.LIMITE_SAQUE:.2f})"
        if self.saques_hoje >= self.MAX_SAQUES:
            return False, "Número máximo de saques diários atingido."

        self.saldo -= valor
        self.saques_hoje += 1
        self.extrato.append(f"Saque: -R${valor:.2f}")
        return True, f"Saque de R${valor:.2f} realizado."

    def ver_extrato(self):
        header = "=============== EXTRATO ==============="
        corpo = "\n".join(self.extrato) if self.extrato else "Nenhuma operação registrada."
        footer = f"\n\nSaldo atual: R$ {self.saldo:.2f}\n" + "=" * len(header)
        return f"{header}\n{corpo}{footer}"

def filtrar_usuario(cpf, usuarios):
    for usuario in usuarios:
        if usuario.cpf == cpf:
            return usuario
    return None

def criar_usuario(usuarios):
    cpf = input("CPF (somente números): ").strip()
    if filtrar_usuario(cpf, usuarios):
        print("Erro: CPF já cadastrado.")
        return
    nome = input("Nome completo: ").strip()
    data = input("Data de nascimento (dd-mm-aaaa): ").strip()
    endereco = input("Endereço (logradouro, nº - bairro - cidade/UF): ").strip()
    usuarios.append(Usuario(nome, data, cpf, endereco))
    print(f"Usuário {nome} criado com sucesso.")

def criar_conta(contas, usuarios, numero_conta):
    cpf = input("CPF do titular: ").strip()
    usuario = filtrar_usuario(cpf, usuarios)
    if not usuario:
        print("Erro: CPF não cadastrado.")
        return
    conta = Conta(numero_conta, usuario)
    contas.append(conta)
    print(f"Conta {numero_conta} criada para {usuario.nome}.")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
        Agência:\t{conta.agencia}
        Conta:\t\t{conta.numero}
        Titular:\t{conta.usuario.nome}
        """
        print("=" * 40)
        print(textwrap.dedent(linha))

def main():
    usuarios = []
    contas = []
    conta_ativa = None

    menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo Usuário
[nc] Nova Conta
[lc] Listar Contas
[q] Sair

=> """

    while True:
        opcao = input(menu).strip().lower()

        if opcao == "d":
            if not conta_ativa:
                print("Nenhuma conta ativa. Crie ou selecione uma.")
                continue
            try:
                valor = float(input("Valor do depósito: R$"))
                ok, msg = conta_ativa.depositar(valor)
                print(msg)
            except ValueError:
                print("Entrada inválida.")

        elif opcao == "s":
            if not conta_ativa:
                print("Nenhuma conta ativa.")
                continue
            try:
                valor = float(input("Valor do saque: R$"))
                ok, msg = conta_ativa.sacar(valor)
                print(msg)
            except ValueError:
                print("Entrada inválida.")

        elif opcao == "e":
            if not conta_ativa:
                print("Nenhuma conta ativa.")
                continue
            print(conta_ativa.ver_extrato())

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero = len(contas) + 1
            criar_conta(contas, usuarios, numero)
            conta_ativa = contas[-1]

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            print("Obrigado por usar nossos serviços.")
            break

        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()

