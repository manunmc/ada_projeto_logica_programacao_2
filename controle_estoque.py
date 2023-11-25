import csv
from pathlib import Path

class ControleEstoque:
    def __init__(self, nome_arquivo='produtos.csv'):
        self.nome_arquivo = nome_arquivo
        self.verificar_e_criar_arquivo()

    def verificar_e_criar_arquivo(self):
        if not Path(self.nome_arquivo).is_file():
            with open(self.nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
                writer = csv.writer(arquivo, delimiter=';')
                writer.writerow(["ID", "Nome", "Especificações", "Quantidade no Estoque", "Texto Descritivo"])

    def exibir_opcoes(self):
        print("Boas vindas ao nosso sistema:\n")
        print("1 - Cadastrar produto")
        print("2 - Consultar produto")
        print("3 - Listar produtos cadastrados")
        print("4 - Atualizar cadastro")
        print("5 - Excluir cadastro")
        print("6 - Sair")

    def obter_escolha(self):
        escolha = input("Digite o número da opção desejada e pressione Enter: ")
        if escolha.isdigit():
            return int(escolha)
        else:
            print("Por favor, digite um número válido.")
            return None

    def id_existe(self, id_produto):
        with open(self.nome_arquivo, mode='r', newline='', encoding='utf-8') as arquivo:
            reader = csv.reader(arquivo, delimiter=';')
            next(reader, None) 
            for linha in reader:
                if linha[0] == str(id_produto):
                    return True
        return False

    def cadastrar_produto(self):
        id_produto = input("ID (número identificador único): ")
        if not id_produto.isdigit():
            print("ID deve ser um número.")
            return

        if self.id_existe(id_produto):
            print("Este ID já existe. Por favor, insira um ID diferente.")
            return

        nome = input("Insira o nome do produto: ")
        especificacoes = input("Insira as especificações do produto: ")
        while True:
            try:
                quantidade_estoque = int(input("Quantidade do produto no estoque: "))
                break
            except ValueError:
                print("Por favor, insira um número inteiro válido para a quantidade do estoque.")
        texto_descritivo = input("Insira o texto descritivo opcional para o produto: ")

        with open(self.nome_arquivo, 'a', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo, delimiter=';')
            writer.writerow([id_produto, nome, especificacoes, quantidade_estoque, texto_descritivo])

        print("Produto cadastrado com sucesso.")

    def consultar_produto_por_id(self, id_produto):
        with open(self.nome_arquivo, 'r', newline='', encoding='utf-8') as arquivo:
            reader = csv.reader(arquivo, delimiter=';')
            for row in reader:
                if row[0] == id_produto:
                    print("Produto encontrado:", row)
                    break
            else:
                print("Produto não encontrado.")

    def listar_produtos(self):
        with open(self.nome_arquivo, mode='r', newline='', encoding='utf-8') as arquivo:
            reader = csv.DictReader(arquivo, delimiter=';')
            return [(linha['ID'], linha['Nome']) for linha in reader]

    def atualizar_produto(self, id_produto):
        if not id_produto.isdigit() or not self.id_existe(id_produto):
            print("ID inválido ou produto não encontrado.")
            return

        nome = input("Novo nome: ")
        especificacoes = input("Novas especificações: ")
        while True:
            try:
                quantidade_estoque = int(input("Quantidade do produto no estoque: "))
                break
            except ValueError:
                print("Por favor, insira um número inteiro válido para a quantidade do estoque.")
        texto_descritivo = input("Novo texto descritivo: ")

        produtos_atualizados = False
        produtos = []
        with open(self.nome_arquivo, mode='r', newline='', encoding='utf-8') as arquivo:
            reader = csv.reader(arquivo, delimiter=';')
            for produto in reader:
                if produto[0] == id_produto:
                    produtos.append([id_produto, nome, especificacoes, quantidade_estoque, texto_descritivo])
                    produtos_atualizados = True
                else:
                    produtos.append(produto)

        if produtos_atualizados:
            with open(self.nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
                writer = csv.writer(arquivo, delimiter=';')
                writer.writerows(produtos)
            print(f"Produto com ID {id_produto} atualizado com sucesso.")
        else:
            print(f"Produto com ID {id_produto} não encontrado.")

    def deletar_produto(self, id_produto):
        produtos = []
        produto_encontrado = False
        with open(self.nome_arquivo, 'r', newline='', encoding='utf-8') as arquivo:
            reader = csv.reader(arquivo, delimiter=';')
            for row in reader:
                if row[0] != id_produto:
                    produtos.append(row)
                else:
                    produto_encontrado = True

        if produto_encontrado:
            with open(self.nome_arquivo, 'w', newline='', encoding='utf-8') as arquivo:
                writer = csv.writer(arquivo, delimiter=';')
                writer.writerows(produtos)
            print("Produto deletado com sucesso.")
        else:
            print("Produto não encontrado.")

def main():
    ce = ControleEstoque()
    while True:
        ce.exibir_opcoes()
        escolha = ce.obter_escolha()

        if escolha == 1:
            ce.cadastrar_produto()
        elif escolha == 2:
            id_produto = input("Digite o ID do produto que deseja consultar: ")
            ce.consultar_produto_por_id(id_produto)
        elif escolha == 3:
            produtos = ce.listar_produtos()
            if produtos:
                print("Lista de produtos:")
                for id_produto, nome in produtos:
                    print(f"ID: {id_produto}, Nome: {nome}")
            else:
                print("Não há produtos cadastrados.")
        elif escolha == 4:
            id_produto = input("Digite o ID do produto que deseja atualizar: ")
            ce.atualizar_produto(id_produto)
        elif escolha == 5:
            id_produto = input("Digite o ID do produto que deseja deletar: ")
            ce.deletar_produto(id_produto)
        elif escolha == 6:
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()
