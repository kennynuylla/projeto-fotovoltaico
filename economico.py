import numpy as np

class Economico:

    def phi(self, consumo, t):
        if(consumo <= 30): preco = 0.50533
        if(consumo <= 100): preco = 0.65234
        if(consumo <= 220): preco = 0.82851
        preco = 0.88724

        return consumo*(preco+t*0.1)

    def desconto_iptu(self, t):
        if(self.projeto.iaes > 1): return self.projeto.iptu*0.8*t
        if(self.projeto.iaes > 0.75): return self.projeto.iptu*0.65*t
        if(self.projeto.iaes > 0.5): return self.projeto.iptu*0.5*t
        if(self.projeto.iaes > 0.25): return self.projeto.iptu*0.35*t
        
        return self.projeto.iptu*0.2*t

    def custo_manutencao(self,t):
        custo = t//10 * self.projeto.dados["custo_inversor"]
        custo += t*800

        return  custo

    def inflacao(self, valor, t):
        return valor*(1-0.0375)**t

    def amortizacao(self, t):
        if(12*t > self.qtd_parcelas):
            return self.valor_inicial
        
        return 12*t*self.valor_parcela

    def poupanca(self, t):

        return self.projeto.dados["custo"]*(1+0.0112)**t


    def __init__(self, projeto):
        self.projeto = projeto
        self.valor_conta = self.phi(self.projeto.consumo_central, 0)
        self.t = self.projeto.t

        self.phi_vec = np.vectorize(self.phi)
        self.iptu_vec = np.vectorize(self.desconto_iptu)
        self.manutencao_vec = np.vectorize(self.custo_manutencao)
        self.inflacao_vec = np.vectorize(self.inflacao)
        self.amortizacao_vec = np.vectorize(self.amortizacao)
        self.poupanca_vec = np.vectorize(self.poupanca)
        
        """
        print("Fatura Mensal Atual: R$ %.02f\n" %(self.valor_conta))
        print("Valor do Sistema sem Financiamento: R$ %.02f\n" %(self.projeto.dados["custo"]))
        print("Código do Kit: %s\n" %(self.projeto.dados["codigo"]))

        self.qtd_parcelas = int(input("Quantidade de Parcelas: "))
        self.valor_parcela = float(input("Valor da Parcela: "))
        """

        self.qtd_parcelas = 60
        self.valor_parcela = 2248.97
        self.valor_inicial = self.qtd_parcelas*self.valor_parcela


    def retorno_simples(self):
        self.valor_geracao = self.phi_vec(self.projeto.dados_geracao, self.t)*12 
        self.valor = [self.valor_geracao[0] - self.valor_inicial]

        for i in range(1, len(self.valor_geracao)):
            self.valor.append(self.valor[i-1] + self.valor_geracao[i])

    def retorno_completo(self):
        self.retorno_simples()
        self.valor_completo = self.valor + self.iptu_vec(self.t)
        self.valor_completo -= self.manutencao_vec(self.t)
        self.valor_completo -= self.amortizacao_vec(self.t)
        self.valor_completo = self.inflacao_vec(self.valor_completo, self.t)

        self.valor_poupanca = self.poupanca_vec(self.t)


