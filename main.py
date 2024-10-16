import tkinter as tk

# Variáveis globais
scoreTeam1 = 0
scoreTeam2 = 0

# Atualizar o placar (sempre adicionar ao final de cada função)
def updateScore():
    labelScore1.config(text=str(scoreTeam1))
    labelScore2.config(text=str(scoreTeam2))

# Janela principal
root = tk.Tk()
root.title("Placar")
root.geometry("800x600")  # MUDAR DEPOIS PARA 768X384 , NESSA RES FICA MAIS FACIL DE MEXER

# Labels do placar
labelTeam1 = tk.Label(root, text="Equipe 1", font=("Arial", 72))
labelScore1 = tk.Label(root, text=str(scoreTeam1), font=("Arial", 144))

labelTeam2 = tk.Label(root, text="Equipe 2", font=("Arial", 72))
labelScore2 = tk.Label(root, text=str(scoreTeam2), font=("Arial", 144))

# Posicionar os labels na janela (exemplo com pack)
labelTeam1.pack()
labelScore1.pack()
labelTeam2.pack()
labelScore2.pack()

# Criar a janela de controle como uma janela secundária
controlWindow = tk.Toplevel(root)
controlWindow.title("Controles")
controlWindow.geometry("300x200")

# Funções para aumentar/diminuir o placar
def increaseTeam1():
    global scoreTeam1
    scoreTeam1 += 1
    updateScore()

def increaseTeam2():
    global scoreTeam2
    scoreTeam2 += 1
    updateScore()

def decreaseTeam1():
    global scoreTeam1
    scoreTeam1 -= 1
    updateScore()

def decreaseTeam2():
    global scoreTeam2
    scoreTeam2 -= 1
    updateScore()

# Criando os botões
buttonTeam1Up = tk.Button(controlWindow, text="Aumentar Equipe 1", command=increaseTeam1)
buttonTeam2Up = tk.Button(controlWindow, text="Aumentar Equipe 2", command=increaseTeam2)
buttonTeam1Down = tk.Button(controlWindow, text="Diminuir Equipe 1", command=decreaseTeam1)
buttonTeam2Down = tk.Button(controlWindow, text="Diminuir Equipe 2", command=decreaseTeam2)

# Posicionar os botões
buttonTeam1Up.pack()
buttonTeam2Up.pack()
buttonTeam1Down.pack()
buttonTeam2Down.pack()

# Iniciar o loop principal
root.mainloop()
