from abc import ABC, abstractmethod


class Medivel(ABC):
    @abstractmethod
    def tamanho(self):
        pass


class Item(Medivel, ABC):
    __slots__ = ("__nome", "__pai")

    def __init__(self, nome, pai=None):
        self.__nome = nome
        self.__pai = None
        self.definir_pai(pai)

    @property
    def nome(self):
        return self.__nome

    @property
    def pai(self):
        return self.__pai

    def definir_pai(self, novo_pai):
        self.__pai = novo_pai
        if novo_pai:
            novo_pai.adicionar(self)

    def mover_para(self, novo_pai):
        if self.__pai:
            self.__pai.remover(self)
        self.definir_pai(novo_pai)

    @property
    def caminho(self):
        if not self.__pai:
            return self.__nome
        return f"{self.__pai.caminho}/{self.__nome}"

    @abstractmethod
    def mostrar(self, recuo=0):
        pass


class Arquivo(Item):
    __slots__ = ("__tamanho_bytes",)

    def __init__(self, nome, tamanho_bytes, pai=None):
        super().__init__(nome, pai)
        self.__tamanho_bytes = tamanho_bytes

    def tamanho(self):
        return self.__tamanho_bytes

    def mostrar(self, recuo=0):
        print("  " * recuo + f"- {self.nome} ({self.tamanho()} bytes)")


class Pasta(Item):
    __slots__ = ("__itens",)

    def __init__(self, nome, pai=None):
        super().__init__(nome, pai)
        self.__itens = []

    def adicionar(self, item):
        if item not in self.__itens:
            self.__itens.append(item)

    def remover(self, item):
        if item in self.__itens:
            self.__itens.remove(item)

    def tamanho(self):
        total = 0
        for item in self.__itens:
            total += item.tamanho()
        return total

    def mostrar(self, recuo=0):
        print("  " * recuo + f"+ {self.nome}/")
        for item in self.__itens:
            item.mostrar(recuo + 1)

    def contem(self, item_procurado):
        if item_procurado == self:
            return True
        for item in self.__itens:
            if isinstance(item, Pasta) and item.contem(item_procurado):
                return True
            if item == item_procurado:
                return True
        return False


class Lixeira(Pasta):
    __slots__ = ()

    def mostrar(self, recuo=0):
        print("  " * recuo + f"[Lixeira] {self.nome}/")
        for item in self._Pasta__itens:
            item.mostrar(recuo + 1)


class Atalho(Item):
    __slots__ = ("__destino",)

    def __init__(self, nome, destino, pai=None):
        super().__init__(nome, pai)
        self.redirecionar(destino)

    @property
    def destino(self):
        return self.__destino

    def redirecionar(self, novo_destino):
        if novo_destino == self:
            raise ValueError("O atalho nao pode apontar para si mesmo.")
        if isinstance(novo_destino, Pasta) and novo_destino.contem(self):
            raise ValueError("O atalho nao pode apontar para uma pasta que o contem.")
        self.__destino = novo_destino

    def tamanho(self):
        return 1

    def mostrar(self, recuo=0):
        print("  " * recuo + f"@ {self.nome} -> {self.__destino.caminho}")


def espaco_total(colecao):
    total = 0
    for item in colecao:
        total += item.tamanho()
    return total


def tentar(funcao):
    try:
        funcao()
    except Exception as erro:
        print(f"[Erro]: {erro}")


if __name__ == "__main__":
    raiz = Pasta("C:")
    usuarios = Pasta("Users", raiz)
    emanuela = Pasta("Emanuela", usuarios)
    desktop = Pasta("Desktop", emanuela)

    documento = Arquivo("relatorio.txt", 1500, desktop)
    foto = Arquivo("ferias.png", 40000, desktop)

    atalho_arquivo = Atalho("atalho_relatorio", documento, desktop)
    atalho_pasta = Atalho("atalho_desktop", desktop, emanuela)

    print("--- Arvore Completa ---")
    raiz.mostrar()

    print("\n--- Testes de Falha ---")
    tentar(lambda: setattr(atalho_arquivo, "destino", foto))
    tentar(lambda: atalho_arquivo.redirecionar(atalho_arquivo))
    tentar(lambda: atalho_arquivo.redirecionar(desktop))