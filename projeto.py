import numpy as np, equipamentos 

class Projeto:

    def __init__(self, ligacao, consumo_central, tempo, rendimento):
        #Consumo central é o consumo médio ou mediano da unidade consumidora
        #Ligação = 1 para monofásico, 2 para bifásico e 3 para trifásico

        self.consumo_central = consumo_central
        self.ligacao = ligacao
        self.tempo = tempo
        self.rendimento = rendimento
        self.equipamentos = equipamentos.Equipamentos()
        self.dados = {}
        
        if(self.ligacao == 1):
            self.consumo_minimo = 30
        
        elif(self.ligacao == 2):
            self.consumo_minimo = 50
        
        else:
            self.consumo_minimo = 100
        
        self.projeto = {}
        self.dimensionar_projeto()
    
    def __str__(self):
        retorno = "Custo: R$ %.04f\n" %(self.dados["custo"])
        retorno += "%d x Placas: %s\n" %(self.dados["qtd_placas"], self.dados["placa"])
        retorno += "Inversor: %s\n" %(self.dados["inversor"])
        retorno += "Potência Instalada: %.04f\n" %(self.dados["potencia_instalada"])
        
        return retorno
    
    def dimensionar_projeto(self):        
        energia_dia = (self.consumo_central - self.consumo_minimo)/30
        potencia_total = energia_dia/(self.tempo * self.rendimento)
        
        placa, inversor, custo, qtd_placas = self.melhores_equipamentos(potencia_total)
        id_placa, potencia_placa, nome_placa, preco_placa, loja_placa = placa
        id_inversor, potencia_inversor, nome_inversor, preco_inversor, loja_inversor = inversor
        
        self.dados["custo"] = custo
        self.dados["placa"] = nome_placa + " - " + str(potencia_placa) + " - " + loja_placa
        self.dados["inversor"] = nome_inversor + " - " + str(potencia_inversor) + "- " + loja_inversor
        self.dados["qtd_placas"] = qtd_placas
        self.dados["potencia_instalada"] = qtd_placas * potencia_placa
        self.dados["custo_inversor"] = preco_inversor
        
    def melhores_equipamentos(self, potencia_total): #Sinta-se livre para mudar o algoritmo ou inserir IA aqui
        custo = None
        melhor_placa = None
        melhor_inversor = None
        melhor_qtd_placas = None
        
        for placa in self.equipamentos.placas:
            for inversor in self.equipamentos.inversores:
                potencia_placa = placa[1]
                preco_placa = placa[3]
                potencia_inversor = inversor[1]
                preco_inversor = inversor[3]
                
                qtd_placas = np.ceil(potencia_total/potencia_placa)
                nova_potencia_total = qtd_placas * potencia_placa
                novo_custo = qtd_placas*preco_placa + preco_inversor
                
                if(potencia_total < 0.8*nova_potencia_total or nova_potencia_total > 1.2*potencia_total):
                    continue
                
                if(custo == None or novo_custo < custo):
                    custo = novo_custo
                    melhor_placa = placa
                    melhor_inversor = inversor
                    melhor_qtd_placas = qtd_placas
        
        return [melhor_placa, melhor_inversor, custo, melhor_qtd_placas]
        

                
                
        