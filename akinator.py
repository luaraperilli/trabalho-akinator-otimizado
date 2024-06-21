import csv


# A classe Noh representa um nó na árvore de decisão. O nó é a pergunta
class Noh:
    def __init__(self, string, eh_pergunta: bool):
        # String é a pergunta ou o nome do personagem
        self.string = string
        # Se é uma pergunta vale True, senão é personagem
        self.eh_pergunta = eh_pergunta
        self.esq = None
        self.dir = None


def criar_noh(string: str) -> Noh:
    return Noh(string)

def encontrar_melhor_pergunta(personagens, perguntas):
    melhor_pergunta = None
    menor_diferenca = float('inf')

    for pergunta in perguntas:
        sim = sum(1 for p in personagens if p[pergunta] == 1)
        nao = sum(1 for p in personagens if p[pergunta] == 0)
        diferenca = abs(sim - nao)

        if diferenca < menor_diferenca:
            melhor_pergunta = pergunta
            menor_diferenca = diferenca

    return melhor_pergunta

# Lista de perguntas que estão no header (primeira linha do arquivo csv)
def criar_arvore(personagens, perguntas) -> Noh | None:
    if not personagens: # Se a lista de personagens estiver vazia, retorna None
        return None

    if len(personagens) == 1:  # Se houver apenas um personagem, cria um nó folha
        return Noh(personagens[0]["nome"], False)

    melhor_pergunta = encontrar_melhor_pergunta(personagens, perguntas)  # Encontra a melhor pergunta
    noh = Noh(melhor_pergunta, True)  # Cria um nó com a melhor pergunta

    # Divide os personagens em dois grupos com base na resposta à melhor pergunta
    personagens_sim = [p for p in personagens if p[melhor_pergunta] == 1]
    personagens_nao = [p for p in personagens if p[melhor_pergunta] == 0]

    # Remove a melhor pergunta da lista de perguntas restantes
    perguntas_restantes = [p for p in perguntas if p != melhor_pergunta]

    # Cria recursivamente os nós filhos esquerdo e direito
    noh.esq = criar_arvore(personagens_sim, perguntas_restantes)
    noh.dir = criar_arvore(personagens_nao, perguntas_restantes)

    return noh  # Retorna o nó criado


def contar_alturas_folhas(noh, altura=0, alturas=[]):
    if noh is None:
        return
    if not noh.eh_pergunta:  # Se for um nó folha (não é uma pergunta)
        alturas.append(altura)
    else:
        contar_alturas_folhas(noh.esq, altura + 1, alturas)
        contar_alturas_folhas(noh.dir, altura + 1, alturas)
    return alturas


def coletar_folhas_personagens(noh, folhas=[]):
    if noh is None:
        return
    if not noh.eh_pergunta:  # Se for um nó folha (não é uma pergunta)
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

        # Se não tiver ninguém na folha da esquerda, insere o personagem
        noh_atual.esq = Noh(personagem_dict["nome"], False)
    else:
        if noh_atual.dir != None:
            print(
                "Erro: folha já ocupada "
                + noh_atual.dir.string
                + " e "
                + personagem_dict["nome"]
            )
            exit(1)  # Sai do programa
        noh_atual.dir = Noh(personagem_dict["nome"], False)


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
    arvore = criar_arvore(lista_dicts, perguntas)  # criar_arvore retorna o Noh raiz da árvore
    
    # Insere personagens na árvore
    for personagem_dict in lista_dicts:
        insere_personagem(arvore, perguntas, personagem_dict)

    # Responde com 1 (sim) ou 0 (não)
    # -1 para sair
    imprimir_arvore(arvore)

    alturas_folhas = contar_alturas_folhas(arvore)
    print("Alturas das folhas:", alturas_folhas)

    personagens = coletar_folhas_personagens(arvore)
    print("Personagens:", personagens)


if __name__ == "__main__":
    main()