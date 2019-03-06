import os, numpy as np, matplotlib.pyplot as plt  

class Economico:
    
    def __init__(self, projeto, iptu, sem_beneficio = False):
        self.projeto = projeto
        self.e = lambda t: 1 - 0.0113333333*t + 0.00013333333*t**2
        self.sem_beneficio = sem_beneficio
        self.iptu = iptu
        self.desconto_iptu = self.D()
        
        self.rendimento_fotovoltaico = np.vectorize(self.rendimento_foto)
        self.rendimento_poupanca = np.vectorize(self.rendimento_poup)
        
        if(not(os.path.exists("./Saídas/"))):
            os.mkdir("./Saídas/")
            
        plt.rcParams["font.size"] = 22
        
        self.arquivo = open("./Saídas/relatório.txt", "w")
        
    def phi(self, consumo): #Preço do kWh
        if(self.sem_beneficio): return consumo * 0.60530
        if(consumo <= 30): return consumo * 0.20553
        if(consumo <= 100): return consumo * 0.35234
        if(consumo <= 220): return consumo * 0.52851
        return consumo * 0.58724
    
    def D(self): #Desconto do IPTU
        iaes = self.projeto.dados["potencia_instalada"]*5.54*0.8*30/self.projeto.consumo_central
        if(iaes > 1): return 0.8
        if(iaes >= 0.75): return 0.65
        if(iaes >= 0.5): return 0.5
        if(iaes >= 0.25): return 0.35
        return 0.2
    
    def rendimento_foto(self, t):
        f = 0.0375 #Inflação em 2018
        
        r = 12*t*self.phi(self.e(t) * (self.projeto.consumo_central - self.projeto.consumo_minimo))
        r += t*self.desconto_iptu*self.iptu
        r -= t//10 * self.projeto.dados["custo_inversor"]
        r *= (1-f)**t
        
        return r
    
    def rendimento_poup(self, t):
        i = 1.12/100 #Rendimento Real em 2018
        r = self.projeto.dados["custo"] * (1+i)**t
        
        return r
    
    def gerar_resultados(self):
        t = np.arange(0, 26, 1)
        foto = self.rendimento_fotovoltaico(t)
        poup = self.rendimento_poupanca(t)
        
        plt.figure(figsize=(20,12), dpi=128)
        
        plt.plot(t, foto, "k-")
        plt.plot(t, poup, "r-")
        
        plt.grid(True)
        plt.title("Rendimento")
        plt.ylabel("Retorno [R$]")
        plt.xlabel("Ano")
        
        plt.legend(["Sistema Fotovoltaico", "Poupança"])
        
        plt.savefig("./Saídas/rendimento.png")
        
        self.arquivo.write("%s\n" %(str(self.projeto)))
        self.arquivo.write("==============================================\n")
        self.arquivo.write("Rendimento Final Poupança: R$ %f\n" %(poup[-1]))
        self.arquivo.write("Redimento Final sistema: R$ %f\n" %(foto[-1]))
        
        for i in range(len(foto)):
            if(foto[i] > self.projeto.dados["custo"]):
                self.arquivo.write("Payback: %d anos\n" %(t[i]))
                break
            
 
    def __del__(self):
        self.arquivo.close()
        