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
        self.dados = []
        
        if(self.ligacao == 1):
            self.consumo_minimo = 30
        
        elif(self.ligacao == 2):
            self.consumo_minimo = 50
        
        else:
            self.consumo_minimo = 100
        
        self.projeto = {}
        self.dimensionar_projeto()
    
    def dimensionar_projeto(self):        
        energia_dia = (self.consumo_central - self.consumo_minimo)/30
        potencia_total = energia_dia/(self.tempo * self.rendimento)
        
        total = {}
        custo = None
        
        for placa in self.equipamentos.placas:
            for inversor in self.equipamentos.inversores:
                id_placa, potencia_placa, nome_placa, preco_placa, loja_placa = placa
                id_inversor, potencia_inversor, nome_inversor, preco_inversor, loja_inversor = inversor
                
                qtd_placas = np.ceil(potencia_total/potencia_placa)
                nova_potencia_total = qtd_placas * potencia_placa
                novo_custo = qtd_placas * preco_placa
                
                if(potencia_inversor < 0.8*nova_potencia_total or potencia_inversor > 1.2*nova_potencia_total):
                    continue
                
                if(total == {} or custo == None or novo_custo < custo):
                    custo = novo_custo
                    total["custo"] = custo
                    total["placa"] = nome_placa + " - " + str(potencia_placa) + " - " + loja_placa
                    total["inversor"] = nome_inversor + " - " + str(potencia_inversor) + "- " + loja_inversor
                    total["qtd_placas"] = qtd_placas
                    total["potencia_instalada"] = nova_potencia_total
                    total["custo_inversor"] = preco_inversor
        
        self.dados = total
                
                
        