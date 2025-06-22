import random

perguntas = {
    0: "What's the largest animal species currently alive?",
    1: "What animal must sleep standing up?",
    2: "pergunta 3"
    }

# respostas_ID=[[0,1,2,3]]

respostas = [
    ["African elephant", "Colossal squid", "Great white shark", "Blue whale", "Sperm whale"],
    ["Kankoroo", "Elephant", "Horse", "Frog", "Monkey"],
    ["Camberra", "Melbourne", "Sydney", "Brisbane", "Perth"]
    ]

respostas_corretas = [3, 2, 0]

pergunta_sorteada = list(perguntas.keys()) [int(random.random()*len(perguntas.keys()))]

print("Pergunta_sorteada: ", pergunta_sorteada)

ordem_perguntas = random.sample(respostas[pergunta_sorteada], len(respostas[pergunta_sorteada]))
print(ordem_perguntas)

rep_correta = respostas_corretas[pergunta_sorteada]
print("Gabarito: ", rep_correta)

