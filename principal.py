import projeto, economico, saidas

palmas = projeto.Projeto(3, 1980, 5.31, 0.8048, 950)

calculo_economico = economico.Economico(palmas)
calculo_economico.retorno_completo()

saidas = saidas.Saidas(palmas, calculo_economico)

saidas.geracao_queda()
saidas.retorno_completo()