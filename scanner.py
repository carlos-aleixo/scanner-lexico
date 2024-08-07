import re

reservadas = {'while', 'do'}

def analisador_lexico(conteudo):
    lista_token = [
        ('Identificador', r'[ij]'),
        ('Reservado', r'\b(?:while|do)\b'),
        ('Constante', r'\d+'),
        ('Operador', r'[+\-*/%&|^!~<>=]'),
        ('String', r'\".*?\"'),
        ('Linha', r'\n'),
        ('Espaço', r'[ \t]+'),
        ('Outros', r'.'),
    ]
    regex = '|'.join('(?P<%s>%s)' % pair for pair in lista_token)
    token = re.compile(regex).match

    linha = 0
    inicio = 0
    tokens = []
    tabela_simbolos = {}
    index = 1
    tk = token(conteudo)
    while tk is not None:
        tipo = tk.lastgroup
        valor = tk.group(tipo)
        coluna = tk.start() - inicio
        if tipo == 'Linha':
            inicio = tk.end()
            linha += 1
        elif tipo == 'Espaço':
            pass
        elif tipo == 'Outros':
            return False, valor
        else:
            if tipo == 'Reservado':
                pass
            elif tipo == 'Identificador':
                if valor not in tabela_simbolos:
                    tabela_simbolos[valor] = index
                    index += 1
            elif tipo == 'Constante':
                if valor not in tabela_simbolos:
                    tabela_simbolos[valor] = index
                    index += 1
            tokens.append((valor, tipo, len(valor), (linha, coluna)))
        tk = token(conteudo, tk.end())

    return True, tokens, tabela_simbolos

def arquivo(arq):
    print("Tentando abrir o arquivo:", arq)
    with open(arq, 'r') as doc:
        conteudo = doc.read()
    return conteudo

def main():
    nome = input("Digite o nome do arquivo a ser analisado: ")
    parametro = arquivo(nome)

    resultado = analisador_lexico(parametro)

    if resultado[0]:
        _, tokens, tabela_simbolos = resultado
        print("Tabela de Tokens:")
        print(f"{'token':<15} {'identificação':<30} {'tamanho':<10} {'posição (lin, col)':<15}")
        for token, tipo, length, position in tokens:
            print(f"{token:<15} {tipo:<30} {length:<10} {position}")
        
        print("\nTabela de Símbolos:")
        print(f"{'índice':<10} {'símbolo':<10}")
        for symbol, index in tabela_simbolos.items():
            print(f"{index:<10} {symbol:<10}")
    else:
        _, valor = resultado
        print(f"Token não identificado: {valor}")

if __name__ == "__main__":
    main()
