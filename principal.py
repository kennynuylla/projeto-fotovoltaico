import projeto, economico

palmas = projeto.Projeto(1, 1980, 5.22, 0.722)
calculo_economico = economico.Economico(palmas, 950)

calculo_economico.gerar_resultados()