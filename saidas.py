import matplotlib.pyplot as plt 
import os

class Saidas:

    def __init__(self, projeto, economico):
        self.projeto = projeto
        self.economico = economico

        if(not(os.path.exists("./Saídas"))):
            os.mkdir("./Saídas")
        
        self.dir = "./Saídas/"

        plt.rcParams.update({"font.size": 22})
        
        self.arquivo = open(self.dir + "relatório.txt", "w")

    def nova_figura(self):
        plt.figure(figsize=(20,10), dpi=128)

    def geracao_queda(self):
        self.nova_figura()

        plt.subplot(2,1,1)
        plt.plot(self.projeto.t, self.projeto.dados_geracao * 12)
        plt.title("Geração ao Longo dos Anos")
        plt.ylabel("kWh")
        plt.grid(True)

        plt.subplot(2,1,2)
        plt.plot(self.projeto.t, self.projeto.dados_e)
        plt.title("Eficiência ao Longo dos Anos")
        plt.ylabel("Eficiência")
        plt.xlabel("Anos")
        plt.grid(True)

        plt.savefig(self.dir + "geracao_queda.png")

    def retorno_simples(self):
        self.nova_figura()

        plt.subplot(2,1,1)
        plt.plot(self.economico.t, self.economico.valor)
        plt.title("Fluxo de Caixa Acumulado")
        plt.ylabel("Rendimento Simples")
        plt.grid(True)

        plt.subplot(2,1,2)
        plt.plot(self.economico.t, self.economico.valor_geracao)
        plt.title("Geração do Ano")
        plt.ylabel("Remuneração")
        plt.xlabel("Anos")
        plt.grid(True)

        plt.savefig(self.dir + "retorno_simples.png")

    def retorno_completo(self):
        self.nova_figura()

        plt.plot(self.economico.t, self.economico.valor_completo, "g-")
        plt.plot(self.economico.t, self.economico.valor_poupanca, "r-")
        plt.title("Retorno do Investimento")
        plt.xlabel("Anos")
        plt.ylabel("Retorno Acumulado em R$")
        plt.legend(["Retorno do Sistema Fotovoltaico", "Retorno da Poupança"])
        plt.grid(True)

        plt.savefig(self.dir + "retorno_completo.png")

        self.arquivo.write(".:DADOS\n")
        self.arquivo.write("=>Custo Inicial: %.02f\n" %(self.projeto.dados["custo"]))
        self.arquivo.write("=>Kit: %s-%.02f@%.02f\n\n" %(self.projeto.dados["kit"], self.projeto.dados["potencia_placa"],
                self.projeto.dados["potencia_instalada"]))
        self.arquivo.write("=>Link: %s\n" %(self.projeto.dados["link"]))
        self.arquivo.write(".:DADOS FINANCEIROS")
        self.arquivo.write("=>Quantidade de Parcelas: %d\n" %(self.economico.qtd_parcelas))
        self.arquivo.write("=>Valor de Cada Parcela: %.02f\n" %(self.economico.valor_parcela))
        self.arquivo.write("=>Total Pago: %.02f\n" %(self.economico.valor_inicial))
        self.arquivo.write("=>Rendimento Poupança: %.02f\n" %(self.economico.valor_poupanca[-1]))
        self.arquivo.write("=>Rendimento Fotovoltaico: %.02f\n" %(self.economico.valor_completo[-1]))

        for i in range(len(self.economico.t)):
            if(self.economico.valor_completo[i] >= 0):
                self.arquivo.write("=>Payback: %d anos\n" %(self.economico.t[i]))
                break

    def __del__(self):
        self.arquivo.close()
        