class Raw(object):
    def __init__(self, marca, modelo, versao, tipo, transmissao, anomodelo, quilometragem, origem):
        self.__marca = marca
        self.__modelo = modelo
        self.__versao = versao
        self.__tipo = tipo
        self.__transmissao = transmissao
        self.__anomodelo = anomodelo
        self.__quilometragem = quilometragem
        self.__origem = origem
        self.__index = -1
    
    @property
    def marca(self):
        return self.__marca

    @property
    def modelo(self):
        return self.__modelo

    @property
    def versao(self):
        return self.__versao

    @property
    def tipo(self):
        return self.__tipo

    @property
    def transmissao(self):
        return self.__transmissao

    @property
    def anomodelo(self):
        return self.__anomodelo

    @property
    def quilometragem(self):
        return self.__quilometragem

    @property
    def origem(self):
        return self.__origem