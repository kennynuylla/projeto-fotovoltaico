import numpy as np, equipamentos 

class Projeto:

    def __init__(self, ligacao, consumo_central, tempo, rendimento, iptu):
        #Consumo central é o consumo médio ou mediano da unidade consumidora
        #Ligação = 1 para monofásico, 2 para bifásico e 3 para trifásico

        self.consumo_central = consumo_central
        self.ligacao = ligacao
        self.tempo = tempo
        self.rendimento = rendimento
        self.equipamentos = equipamentos.Equipamentos(380)
        self.e = lambda t: rendimento - 0.008*t
        self.iptu = iptu
        self.dados = {}
        

        self.dados_geracao = []
        self.dados_e = []
        self.t = np.arange(0,26,1)
        
        if(self.ligacao == 1):
            self.consumo_minimo = 30
        
        elif(self.ligacao == 2):
            self.consumo_minimo = 50
        
        else:
            self.consumo_minimo = 100
        
        self.dimensionar_projeto()
        self.obter_dados_geracao()

        self.iaes = self.dados["potencia_instalada"]*0.8*5.54*30/self.consumo_central
    
    def __str__(self):
        retorno = "Custo: R$ %.04f\n" %(self.dados["custo"])
        retorno += "Kit: %s\n" %(self.dados["kit"]) 
        retorno += "Código: %s\n" %(self.dados["codigo"])
        retorno += "Potência Placa: %.04f\n" %(self.dados["potencia_placa"])
        retorno += "Potência Instalada: %.04f\n" %(self.dados["potencia_instalada"])
        retorno += "Potência Total: %.04f\n" %(self.dados["potencia_total"])
        
        return retorno

    def __repr__(self):
        return self.__str__()
    
    def dimensionar_projeto(self):        
        energia_dia = (self.consumo_central - self.consumo_minimo)/30
        potencia_total = energia_dia/(self.tempo * self.rendimento)
        self.dados["potencia_total"] = potencia_total
        
        kit = self.melhores_equipamentos(potencia_total)
        _, nome, potencia_placa, potencia_instalada, preco, link, _, codigo = kit

        self.dados["custo"] = (preco + 1000) * 1.2075
        self.dados["kit"] = nome
        self.dados["link"] = link
        self.dados["potencia_instalada"] = potencia_instalada
        self.dados["potencia_placa"] = potencia_placa
        self.dados["codigo"] = codigo
        self.dados["custo_inversor"] = preco * 0.2
        
    def melhores_equipamentos(self, potencia_total): #Sinta-se livre para mudar o algoritmo ou inserir IA aqui
        custo = None
        melhor_kit = None
        
        for kit in self.equipamentos.kits:
            preco = kit[4]
            nova_potencia_total = kit[3]
                
            if(potencia_total < 0.8*nova_potencia_total or nova_potencia_total > 1.2*potencia_total):
                continue
                
            if(custo == None or preco < custo):
                custo = preco
                melhor_kit = kit

        
        return melhor_kit
    
    def obter_dados_geracao(self):
        geracao = lambda t: self.e(t)*self.dados["potencia_instalada"]*self.tempo*30
        geracao_vec = np.vectorize(geracao)
        e_vec = np.vectorize(self.e)
        self.dados_geracao = geracao_vec(self.t)
        self.dados_e = e_vec(self.t)

    
        

                
                
        