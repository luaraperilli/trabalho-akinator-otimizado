import csv


# Classe Noh representando um nó na árvore de decisão.
class Noh:
    def __init__(self, string, eh_pergunta: bool):
        self.string = string
        self.eh_pergunta = eh_pergunta
        self.esq = None
        self.dir = None


def criar_noh(string: str) -> Noh:
    return Noh(string, True)


def calcular_diferenca(respostas, pergunta, personagens):
    sim, nao = 0, 0
    for personagem in personagens:
        if respostas[personagem][pergunta] == 1:
            sim += 1
        else:
            nao += 1
    return abs(sim - nao)


def escolher_melhor_pergunta(perguntas, respostas, personagens):
    melhor_pergunta = None
    menor_diferenca = float("inf")
    for pergunta in perguntas:
        diferenca = calcular_diferenca(respostas, pergunta, personagens)
        if diferenca < menor_diferenca:
            menor_diferenca = diferenca
            melhor_pergunta = pergunta
    return melhor_pergunta


def criar_arvore_otimizada(perguntas, respostas, personagens) -> Noh:
    if len(personagens) == 0 or len(perguntas) == 0:
        return None
    if len(personagens) == 1:
        return Noh(personagens[0], False)

    melhor_pergunta = escolher_melhor_pergunta(perguntas, respostas, personagens)
    arvore = Noh(melhor_pergunta, True)

    sim_personagens = [p for p in personagens if respostas[p][melhor_pergunta] == 1]
    nao_personagens = [p for p in personagens if respostas[p][melhor_pergunta] == 0]

    novas_perguntas = [p for p in perguntas if p != melhor_pergunta]
    arvore.esq = criar_arvore_otimizada(novas_perguntas, respostas, sim_personagens)
    arvore.dir = criar_arvore_otimizada(novas_perguntas, respostas, nao_personagens)

    return arvore


def contar_alturas_folhas(noh, altura=0, alturas=[]):
    if noh is None:
        return
    if not noh.eh_pergunta:
        alturas.append(altura)
    else:
        contar_alturas_folhas(noh.esq, altura + 1, alturas)
        contar_alturas_folhas(noh.dir, altura + 1, alturas)
    return alturas


def coletar_folhas_personagens(noh, folhas=[]):
    if noh is None:
        return
    if not noh.eh_pergunta:
        folhas.append(noh.string)
    else:
        coletar_folhas_personagens(noh.esq, folhas)
        coletar_folhas_personagens(noh.dir, folhas)
    return folhas


def imprimir_arvore(noh, prefixo="", eh_esq=True):
    if noh is not None:
        print(prefixo + ("|-- " if eh_esq else "\\-- ") + str(noh.string))
        prefixo += "|   " if eh_esq else "    "
        imprimir_arvore(noh.esq, prefixo, True)
        imprimir_arvore(noh.dir, prefixo, False)


def insere_personagem(noh_raiz_arvore: Noh, perguntas: list, personagem_dict: dict):
    noh_atual = noh_raiz_arvore
    for p in perguntas[:-1]:
        if personagem_dict[p] == 1:
            noh_atual = noh_atual.esq
        else:
            noh_atual = noh_atual.dir

    ultima_pergunta = perguntas[-1]
    if personagem_dict[ultima_pergunta] == 1:
        if noh_atual.esq != None:
            print(
                "Erro: folha já ocupada "
                + noh_atual.esq.string
                + " e "
                + personagem_dict["nome"]
            )
            exit(1)
        noh_atual.esq = Noh(personagem_dict["nome"], False)
    else:
        if noh_atual.dir != None:
            print(
                "Erro: folha já ocupada "
                + noh_atual.dir.string
                + " e "
                + personagem_dict["nome"]
            )
            exit(1)
        noh_atual.dir = Noh(personagem_dict["nome"], False)


def main():
    file_perguntas = open("pessoas.csv", "r")
    csvreader = csv.reader(file_perguntas)
    headers = next(csvreader)
    num_personagens, num_perguntas = map(int, headers[0].split())
    perguntas = headers[1 : num_perguntas + 1]

    respostas = {}
    personagens = []
    # Cria um dicionário para cada personagem

    for linha in csvreader:
        nome = linha[0]
        respostas[nome] = {
            perguntas[i]: int(linha[i + 1]) for i in range(num_perguntas)
        }
        personagens.append(nome)

    arvore_otimizada = criar_arvore_otimizada(perguntas, respostas, personagens)
    # imprimir_arvore(arvore_otimizada)

    alturas_folhas = contar_alturas_folhas(arvore_otimizada)
    # print("Alturas das folhas:", alturas_folhas)

    # personagens_folhas = coletar_folhas_personagens(arvore_otimizada)
    # print("Personagens:", personagens_folhas)

    # calculo da média das alturas
    media_alturas = sum(alturas_folhas) / len(alturas_folhas)
    print(f"{media_alturas:.2f}")

    exit()


if __name__ == "__main__":
    main()
