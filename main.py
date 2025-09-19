import os
import re
import sys
import argparse

def gerarsenhas(comprimento, tipo_de_caracter):
    senhas = []
    for _ in range(5):
        senha = grerarsenha(comprimento, tipo_de_caracter)
        senhas.append(senha)
    return senhas

def grerarsenha(comprimento, tipo_de_caracter):
    caracteres = {
        'maiusculas': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
        'minusculas': 'abcdefghijklmnopqrstuvwxyz',
        'numeros': '0123456789',
        'simbolos': '!@#$%^&*()-_=+[]{}|;:,.<>?/'
    }
    conjunto_caracteres = ''.join(caracteres[tipo] for tipo in tipo_de_caracter if tipo in caracteres)
    if not conjunto_caracteres:
        raise ValueError("Nenhum tipo de caractere válido fornecido.")
    senha = ''.join(conjunto_caracteres[ord(os.urandom(1)) % len(conjunto_caracteres)] for _ in range(int(comprimento)))
    return senha

def verificar_forca_senhas(arquivo):
    if not os.path.isfile(arquivo):
        print(f"Arquivo {arquivo} não encontrado.")
        return

    with open(arquivo, 'r') as f:
        senhas = f.readlines()

    for senha in senhas:
        senha = senha.strip()
        if len(senha) < 8:
            print(f"Senha '{senha}' é fraca: menos de 8 caracteres.")
            continue
        if not re.search(r'[A-Z]', senha):
            print(f"Senha '{senha}' é fraca: falta letra maiúscula.")
            continue
        if not re.search(r'[a-z]', senha):
            print(f"Senha '{senha}' é fraca: falta letra minúscula.")
            continue
        if not re.search(r'[0-9]', senha):
            print(f"Senha '{senha}' é fraca: falta número.")
            continue
        if not re.search(r'[!@#$%^&*()-_=+[\]{}|;:,.<>?/]', senha):
            print(f"Senha '{senha}' é fraca: falta símbolo especial.")
            continue
        print(f"Senha '{senha}' é forte.")

def main():
    if len(sys.argv) > 3 or len(sys.argv) == 1:
        print("Usage: python main.py --c<comprimeto_senha> <tipo_de_caracter 1,tipo_de_caracter 2,...>")
        print("    --help: Show this help message and exit")
        print("    --verficar: Verifica a força das senhas do arquivo senhas.txt")
        sys.exit(1)

    if sys.argv[1] == '--verficar':
        verificar_forca_senhas('senhas.txt')
        sys.exit(0)
    if sys.argv[1] in ('--help', '-h'):
        print("Usage: python main.py --c<comprimeto_senha> <tipo_de_caracter 1,tipo_de_caracter 2,...>")
        print("    --comprimeto_senha: tamanho da senha (e.g., 8, 12, 16)")
        print("    <tipo_de_caracter>: tipos de caracteres a incluir na senha (maiusculas, minusculas, numeros, simbolos)")
        sys.exit(0)

    comprimento = sys.argv[1].removeprefix('--c')
    print(comprimento)
    try:
        tipo_de_caracter = [t.strip() for t in sys.argv[2].split(',')]
    except IndexError:
        tipo_de_caracter = [""]
    
    print(f"Comprimento: {comprimento}")
    print(f"Regras: {tipo_de_caracter}")

    if tipo_de_caracter == "" or tipo_de_caracter is None:
        tipo_de_caracter = ['maiusculas','minusculas','numeros','simbolos']
    senhas = gerarsenhas(comprimento, tipo_de_caracter)
    conter = 1
    for senha in senhas:
        print(f"{conter} PASSWORD {senha}")
        conter += 1
    escolha = input("Deseja salvar as senhas em um arquivo? (s/n): ").strip().lower()
    if escolha == 's':
        with open("senhas.txt", "w") as f:
            for senha in senhas:
                f.write(f"{senha}\n")
        print("Senhas salvas em senhas.txt")

if __name__ == "__main__":
    main()
