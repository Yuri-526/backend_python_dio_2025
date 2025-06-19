def order_by_age(pacientes):
    # pacientes já está no formato [(nome, idade, status)]
    return sorted(pacientes, key=lambda x: x[1], reverse=True)

def main():
    # Entrada do número de pacientes
    n = int(input().strip())

    # Listas para armazenar pacientes
    urgentes = []
    idosos = []
    normais = []

    # Loop para entrada de dados
    for _ in range(n):
        nome, idade, status = input().strip().split(", ")
        idade = int(idade)

        if status == "urgente":
            urgentes.append((nome, idade, status))
        elif idade > 60 and status == "normal":
            idosos.append((nome, idade, status))
        else:
            normais.append((nome, idade, status))

    # Ordena cada grupo por idade decrescente
    urgentes = order_by_age(urgentes)
    idosos = order_by_age(idosos)
    normais = order_by_age(normais)

    # Combina os nomes na ordem correta
    final = [p[0] for p in urgentes + idosos + normais]

    # Exibe o resultado
    print("Ordem de Atendimento:", ', '.join(final))

if __name__ == "__main__":
    main()
