import random

perguntas={0:"pergunta 1",1:"pergunta 2",2:"pergunta 3"}
respostas_ID=[[0,1,2,3], [0,1,2,3], [0,1,2,3]]
respostas=[["Um mamífero","ABCD","1235","7890"], ["Era", "Apenas", "Uma", "Teste"], ["Calma", "Bixo", "Loco", "Touro"]]
respostas_corretas=[1,3,2]

pergunta_sorteada=list(perguntas.keys())[int(random.random()*len(perguntas.keys()))]
print(pergunta_sorteada)

ordem_perguntas=random.sample(respostas[pergunta_sorteada],len(respostas[pergunta_sorteada]))
print(ordem_perguntas)

rep_correta=respostas_corretas[pergunta_sorteada]
print(rep_correta)