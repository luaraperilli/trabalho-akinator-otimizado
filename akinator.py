import csv


# A classe Noh representa um nó na árvore de decisão. O nó é a pergunta
class Noh:
    def __init__(self, string):
        self.string = string  # string é a pergunta ou o nome do personagem
        self.esq = None
        self.dir = None


def criar_noh(string: str) -> Noh:
    return Noh(string)


# lista de perguntas que estão no header (primeira linha do arquivo csv)
def criar_arvore(perguntas: list) -> Noh | None:

    if len(perguntas) == 0:  # Se não houver perguntas no header ele não cria a árvore
        return None

    arvore = criar_noh(perguntas[0])  # cria o nó raiz com a primeira pergunta

    # uso da recursão para criar a árvore da esquerda e da direita
    arvore.esq = criar_arvore(perguntas[1:])
    arvore.dir = criar_arvore(perguntas[1:])
    return arvore


def imprimir(arvore):
    if arvore == None:
        return

    print("(", end="")

    imprimir(arvore.esq)
    print(", ", str(arvore.string), ", ", end="")
    imprimir(arvore.dir)
    print(")", end="")
    return


def insere_personagem(noh_raiz_arvore: Noh, perguntas: list, personagem_dict: dict):
    noh_atual = noh_raiz_arvore

    # Nesse for ele percorre todas as perguntas menos a última
    # perguntas[:-1] -> pega todas as perguntas menos a última
    for p in perguntas[:-1]:
        # Se a resposta for 1, vai para a esquerda, senão vai para a direita
        if personagem_dict[p] == 1:  # 1 = sim
            noh_atual = noh_atual.esq
        else:
            noh_atual = noh_atual.dir

    # noh_atual é o nó que representa a última pergunta agora

    # Trata a última pergunta
    ultima_pergunta = perguntas[-1]
    # Se a resposta for 1, insere o personagem na esquerda, senão insere na direita
    if personagem_dict[ultima_pergunta] == 1:
        if noh_atual.esq != None:
            string = (
                "Erro: folha já ocupada "
                + noh_atual.esq.string
                + " e "
                + personagem_dict["nome"]
            )
            print(string)
            exit(1)  # Sai do programa

        # se não tiver ninguém na folha da esquerda, insere o personagem
        noh_atual.esq = criar_noh(personagem_dict["nome"])
    else:
        if noh_atual.dir != None:
            print(
                "Erro: folha já ocupada "
                + noh_atual.dir.string
                + " e "
                + personagem_dict["nome"]
            )
            exit(1)  # Sai do programa
        noh_atual.dir = criar_noh(personagem_dict["nome"])


def main():
    # Abre o arquivo CSV para leitura
    file_perguntas = open("animais.csv", "r")
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

    # print(num_personagens, num_perguntas)
    # print(perguntas)

    # lista de dicionários que contém os personagens com seus nomes e respostas
    lista_dicts = []

    # Cria um dicionário para cada personagem
    for linha in csvreader:
        personagem_dict = {}
        personagem_dict["nome"] = linha[0]
        respostas = [int(i) for i in linha[1:]]

        for j in range(0, num_perguntas):
            personagem_dict[perguntas[j]] = respostas[j]
        # persongem_dict = exemplo: {'nome': 'Gato', 'É mamífero?': 1, 'Late?': 0, 'Cria em casa?': 1}
        # print(personagem_dict)
        lista_dicts.append(personagem_dict)

    # Cria a árvore com as perguntas mas sem personagem
    arvore = criar_arvore(perguntas)  # criar_arvore retorna o Noh raiz da árvore

    # Insere personagens na árvore
    for personagem_dict in lista_dicts:
        insere_personagem(arvore, perguntas, personagem_dict)

    # Responde com 1 (sim) ou 0 (não)
    # -1 para sair
    # imprimir(arvore)
    # exit()
    option_input = 2
    atual = None  # Ponteiro para o nó atual da árvore
    while option_input != -1:
        if atual is None:
            atual = arvore
        print(atual.string)  # imprime a pergunta ou o personagem
        option_input = int(input())
        if option_input == 1:
            atual = atual.esq
        elif option_input == 0:
            atual = atual.dir
        elif option_input == -1:

            break


if __name__ == "__main__":
    main()
