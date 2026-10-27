import os
import sys

 FATORES_TDEE = {
    1: {"fator": 1.2, "descricao": "Sedentário (pouco ou nenhum exercício)"},
    2: {"fator": 1.375, "descricao": "Levemente ativo (exercício leve 1-3 dias/semana)"},
    3: {"fator": 1.55, "descricao": "Moderadamente ativo (exercício moderado 3-5 dias/semana)"},
    4: {"fator": 1.725, "descricao": "Muito ativo (exercício intenso 6-7 dias/semana)"},
    5: {"fator": 1.9, "descricao": "Extremamente ativo (exercício muito intenso ou trabalho físico)"}
}

def limpar_tela():
    """Limpa o console, funciona em Windows, Mac e Linux."""
    os.system('cls' if os.name == 'nt' else 'clear')

def obter_numero(prompt: str, val_min: int, val_max: int) -> int:
    """
    Solicita um número inteiro ao usuário, validando a entrada dentro de um intervalo.
    Esta função substitui a sub-rotina :obterNumero do script Batch.
    """
    while True:
        try:
            entrada = input(prompt)
            numero = int(entrada)
            if val_min <= numero <= val_max:
                return numero
            else:
                print(f"  [ERRO] O valor deve estar entre {val_min} e {val_max}. Tente novamente.")
        except ValueError:
            print("  [ERRO] Entrada inválida. Digite apenas um número inteiro.")

def exibir_cabecalho():
    """Exibe o cabeçalho principal do programa."""
    print("======================================================================")
    print("                CALCULADORA DE SAÚDE COMPLETA - vPython")
    print("======================================================================")
    print("Esta ferramenta estima:")
    print(" > TMB:  Calorias gastas em repouso absoluto")
    print(" > TDEE: Calorias diárias para manter o peso")
    print(" > IMC:  Índice de Massa Corporal e peso ideal para sua altura")
    print("----------------------------------------------------------------------")

def coletar_dados_usuario():
    """Coleta e valida todos os dados do usuário (sexo, idade, altura, peso)."""
    print("\n=== 1. INFORME SEUS DADOS =========================================")
    
     while True:
        sexo = input("Sexo (M / F): ").upper().strip()
        if sexo in ['M', 'F']:
            break
        print("  [ERRO] Resposta inválida. Informe M ou F.")
    
     idade = obter_numero("Idade (anos): ", 1, 120)
    altura_cm = obter_numero("Altura (cm): ", 100, 250)
    peso_kg = obter_numero("Peso (kg): ", 30, 300)
    
    return sexo, idade, altura_cm, peso_kg

def calcular_tmb(formula: int, sexo: str, peso: int, altura: int, idade: int) -> tuple[float, str]:
    """Calcula a Taxa Metabólica Basal (TMB) usando a fórmula escolhida."""
    nome_formula = ""
    tmb = 0.0

    if formula == 1: # Mifflin-St Jeor
        nome_formula = "Mifflin-St Jeor"
        if sexo == 'M':
            tmb = (10 * peso) + (6.25 * altura) - (5 * idade) + 5
        else: # 'F'
            tmb = (10 * peso) + (6.25 * altura) - (5 * idade) - 161
    
    elif formula == 2: # Harris-Benedict (versão simplificada do script original)
        nome_formula = "Harris-Benedict"
        if sexo == 'M':
            # Fórmula do Batch: (660 + (137 * peso) + (50 * altura) - (68 * idade)) / 10
            tmb = 66 + (13.7 * peso) + (5 * altura) - (6.8 * idade)
        else: # 'F'
            # Fórmula do Batch: (6550 + (96 * peso) + (18 * altura) - (47 * idade)) / 10
            tmb = 655.1 + (9.6 * peso) + (1.8 * altura) - (4.7 * idade)
            
    return tmb, nome_formula

def calcular_tdee(tmb: float) -> tuple[float, str]:
    """Calcula o Gasto Energético Diário Total (TDEE) com base no nível de atividade."""
    print("\n=== 2. NÍVEL DE ATIVIDADE FÍSICA ====================================")
    for key, value in FATORES_TDEE.items():
        print(f"  {key}. {value['descricao']}")
    
    nivel_escolhido = obter_numero("\nEscolha o nível de atividade [1-5]: ", 1, 5)
    
    fator_info = FATORES_TDEE[nivel_escolhido]
    tdee = tmb * fator_info["fator"]
    
    return tdee, fator_info["descricao"].split(" (")[0] # Retorna apenas o nome, ex: "Sedentário"

def calcular_imc(peso: int, altura: int) -> dict:
    """Calcula o Índice de Massa Corporal (IMC), classificação e faixa de peso ideal."""
    if altura == 0:
        return {"imc": 0, "classificacao": "Erro", "recomendacao": "Altura inválida.", "ideal_min": 0, "ideal_max": 0}
        
    altura_m = altura / 100
    imc = peso / (altura_m ** 2)
    
    ideal_min = 18.5 * (altura_m ** 2)
    ideal_max = 24.9 * (altura_m ** 2)
    
    if imc < 18.5:
        classificacao = "Abaixo do peso"
        recomendacao = "Considere aumentar sua ingestão calórica com orientação profissional."
    elif imc < 25:
        classificacao = "Peso normal"
        recomendacao = "Continue com seus hábitos saudáveis para manter seu bem-estar."
    elif imc < 30:
        classificacao = "Sobrepeso"
        recomendacao = "Um leve déficit calórico e mais atividades podem ser benéficos."
    elif imc < 35:
        classificacao = "Obesidade Grau I"
        recomendacao = "Mudanças no estilo de vida são importantes. Considere buscar ajuda."
    elif imc < 40:
        classificacao = "Obesidade Grau II"
        recomendacao = "Risco de saúde elevado. Acompanhamento profissional é recomendado."
    else:
        classificacao = "Obesidade Grau III"
        recomendacao = "Procure ajuda médica e nutricional com urgência."
        
    return {
        "imc": imc, 
        "classificacao": classificacao, 
        "recomendacao": recomendacao,
        "ideal_min": ideal_min,
        "ideal_max": ideal_max
    }

def exibir_resultados(dados: dict, resultados: dict):
    """Formata e exibe todos os resultados da avaliação."""
    limpar_tela()
    print("======================================================================")
    print("                     RESULTADOS DA AVALIAÇÃO")
    print("======================================================================")
    print("\n DADOS INFORMADOS:")
    print(" -----------------")
    print(f" | Sexo:           {'Masculino' if dados['sexo'] == 'M' else 'Feminino'}")
    print(f" | Idade:          {dados['idade']} anos")
    print(f" | Altura:         {dados['altura']} cm")
    print(f" | Peso:           {dados['peso']} kg")
    
    print("\n GASTO CALÓRICO ESTIMADO:")
    print(" ------------------------")
    print(f" | TMB ({resultados['nome_formula']}):".ljust(40) + f"{resultados['tmb']:.0f} kcal/dia")
    print(f" | TDEE ({resultados['nivel_atividade']}):".ljust(40) + f"{resultados['tdee']:.0f} kcal/dia")

    print("\n ÍNDICE DE MASSA CORPORAL (IMC):")
    print(" -------------------------------")
    print(f" | Seu IMC:".ljust(40) + f"{resultados['imc']:.1f}")
    print(f" | Classificação:".ljust(40) + f"{resultados['classificacao']}")
    print(f" | Faixa de Peso Ideal:".ljust(40) + f"{resultados['ideal_min']:.1f} kg a {resultados['ideal_max']:.1f} kg")
    print(f" | Recomendação:   {resultados['recomendacao']}")
    
    print("\n======================================================================")
    print("  AVISO: Esta é uma ferramenta de estimativa. Não substitui a")
    print("  orientação de um profissional de saúde.")
    print("======================================================================")

def main():
    """Função principal que executa o loop do programa."""
    while True:
        limpar_tela()
        exibir_cabecalho()
        
        # Escolha da Fórmula
        print("Qual fórmula de TMB deseja usar?")
        print("  1. Mifflin-St Jeor (Mais moderna e precisa)")
        print("  2. Harris-Benedict (Fórmula clássica)")
        formula_escolhida = obter_numero("\nEscolha a fórmula [1 ou 2]: ", 1, 2)

        sexo, idade, altura, peso = coletar_dados_usuario()
        
        # Cálculos
        tmb, nome_formula = calcular_tmb(formula_escolhida, sexo, peso, altura, idade)
        tdee, nivel_atividade = calcular_tdee(tmb)
        resultados_imc = calcular_imc(peso, altura)
        
        # Agrupando dados para exibição
        dados_usuario = {"sexo": sexo, "idade": idade, "altura": altura, "peso": peso}
        todos_resultados = {
            "tmb": tmb,
            "nome_formula": nome_formula,
            "tdee": tdee,
            "nivel_atividade": nivel_atividade,
            **resultados_imc # Adiciona todas as chaves do dicionário IMC
        }
        
        exibir_resultados(dados_usuario, todos_resultados)
        
        # Loop para novo cálculo ou sair
        while True:
            continuar = input("\nDeseja fazer um novo cálculo? (S/N): ").upper().strip()
            if continuar in ['S', 'N']:
                break
        
        if continuar == 'N':
            print("\nObrigado por usar a Calculadora de Saúde!")
            break

# Ponto de entrada do programa
if __name__ == "__main__":
    main()