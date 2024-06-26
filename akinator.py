# 2023006500 - PEDRO NOGUEIRA BARBOZA
# 2022004841 - LUARA DO VAL PERILLI

import csv


# Classe Noh representando um nó na árvore de decisão.
class Noh:
    def __init__(self, string: str, eh_pergunta: bool):
        # string é a pergunta ou o nome do personagem
        self.string = string
        self.eh_pergunta = eh_pergunta
        # se é uma pergunta vale True, senão é personagem
        self.esq = None
        self.dir = None


# Função que calcula a diferença entre o número de respostas sim e não para uma pergunta
def calcular_diferenca(respostas: dict, pergunta: str, personagens: list[str]) -> int:
    sim, nao = 0, 0
    for personagem in personagens:
        if respostas[personagem][pergunta] == 1:
            sim += 1
        else:
            nao += 1
    return abs(sim - nao)


# Função que escolhe a melhor pergunta para ser a raiz da árvore
def escolher_melhor_pergunta(
    perguntas: list[str], respostas: dict, personagens: list[str]
) -> str | None:
    melhor_pergunta = None
    menor_diferenca = float("inf")
    for pergunta in perguntas:
        diferenca = calcular_diferenca(respostas, pergunta, personagens)
        if diferenca < menor_diferenca:
            menor_diferenca = diferenca
            melhor_pergunta = pergunta
    return melhor_pergunta


def criar_arvore_otimizada(
    perguntas: list[str], respostas: dict, personagens: list[str]
) -> Noh | None:

    # Caso base: se não houver personagens ou perguntas, retorna None
    if len(personagens) == 0 or len(perguntas) == 0:
        return None

    # Caso base: se houver apenas um personagem, retorna um nó folha
    if len(personagens) == 1:
        return Noh(personagens[0], False)

    melhor_pergunta = escolher_melhor_pergunta(perguntas, respostas, personagens)
    arvore = Noh(melhor_pergunta, True)  # Cria um nó com a melhor pergunta

    # Separa os personagens em dois grupos: aqueles que responderam sim e não à melhor pergunta
    sim_personagens = [p for p in personagens if respostas[p][melhor_pergunta] == 1]
    nao_personagens = [p for p in personagens if respostas[p][melhor_pergunta] == 0]

    # Remove a melhor pergunta da lista de perguntas
    novas_perguntas = [p for p in perguntas if p != melhor_pergunta]
    arvore.esq = criar_arvore_otimizada(novas_perguntas, respostas, sim_personagens)
    arvore.dir = criar_arvore_otimizada(novas_perguntas, respostas, nao_personagens)

    return arvore


def contar_alturas_folhas(noh: Noh, altura=0, alturas=[]) -> list[int]:
    # Caso base: se o nó for None, retorna
    if noh == None:
        return
    # Caso base: se o nó for uma folha, adiciona a altura à lista de alturas
    if not noh.eh_pergunta:
        alturas.append(altura)
    # Se o nó não for folha nem None, chama a função recursivamente para os filhos
    else:
        contar_alturas_folhas(noh.esq, altura + 1, alturas)
        contar_alturas_folhas(noh.dir, altura + 1, alturas)
    return alturas


def imprimir_arvore(noh, prefixo="", eh_esq=True):
    if noh != None:
        print(prefixo + ("|-- " if eh_esq else "\\-- ") + str(noh.string))
        prefixo += "|   " if eh_esq else "    "
        imprimir_arvore(noh.esq, prefixo, True)
        imprimir_arvore(noh.dir, prefixo, False)


def main():
    # Abre o arquivo CSV para leitura
    file_nome = input()
    file_perguntas = open(file_nome, "r")
    # Lê os cabeçalhos do arquivo que se referem as perguntas
    csvreader = csv.reader(file_perguntas)

    # lê a primeira linha do arquivo e coloca os valores separados por virgula em uma lista de strings
    headers = next(csvreader)

    # Headers[0] : 4 3
    # 4 personagens e 3 perguntas
    # 4 linhas e 3 colunas
    # '4 3' -> map(int,["4", "3"]) -> [4, 3]
    num_personagens, num_perguntas = map(int, headers[0].split())

    # adiciona as perguntas em uma lista
    perguntas = []
    for i in range(1, num_perguntas + 1):
        perguntas.append(headers[i])

    # no dicionário respostas cada chave é um nome que mapeia outro dicionário contendo as perguntas como chave e as respostas como valor
    respostas = {}
    personagens = []
    # Cria um dicionário respostas que mapeia o nome do personagem para um outro dicionário
    # Exemplo: respostas['nome_personagem'] = {'pergunta1': 1, 'pergunta2': 0, ...}
    for linha in csvreader:
        nome = linha[0]
        respostas[nome] = {
            perguntas[i]: int(linha[i + 1]) for i in range(num_perguntas)
        }
        personagens.append(nome)
    arvore_otimizada = criar_arvore_otimizada(perguntas, respostas, personagens)
    # imprimir_arvore(arvore_otimizada)

    alturas_folhas = contar_alturas_folhas(arvore_otimizada)

    # calculo da média das alturas
    media_alturas = sum(alturas_folhas) / len(alturas_folhas)
    print(f"{media_alturas:.2f}")


if __name__ == "__main__":
    main()
