import tkinter as tk

# Variáveis globais para armazenar os valores do placar
score_team1 = 0
score_team2 = 0

# Função para atualizar o placar
def update_score():
    label_score1.config(text=str(score_team1))
    label_score2.config(text=str(score_team2))

# Criar a janela do placar
root = tk.Tk()
root.title("Placar")
root.geometry("800x600")  # Defina um tamanho adequado para a janela

# Criar labels para o placar
label_team1 = tk.Label(root, text="Equipe 1", font=("Arial", 72))
label_score1 = tk.Label(root, text=str(score_team1), font=("Arial", 144))

label_team2 = tk.Label(root, text="Equipe 2", font=("Arial", 72))
label_score2 = tk.Label(root, text=str(score_team2), font=("Arial", 144))

# Posicionar os labels na janela (exemplo com pack)
label_team1.pack()
label_score1.pack()
label_team2.pack()
label_score2.pack()

# Criar a janela de controle como uma janela secundária
control_window = tk.Toplevel(root)
control_window.title("Controles")
control_window.geometry("300x200")

#aumentar o placar
def increase_team1():
    global score_team1
    score_team1 += 1
    update_score()

def increase_team2():
    global score_team2
    score_team2 += 1
    update_score()

def decrease_team1():
    global score_team1
    score_team1 -= 1 
    update_score()

def decrease_team2():
    global score_team2
    score_team2 -= 1 
    update_score()

# criando os botões
button_team1_up = tk.Button(control_window, text="Aumentar Equipe 1", command=increase_team1)
button_team2_up = tk.Button(control_window, text="Aumentar Equipe 2", command=increase_team2)
button_team1_down = tk.Button(control_window, text="Diminuir Equipe 1", command=decrease_team1)
button_team2_down = tk.Button(control_window, text="Diminuir Equipe 2", command=decrease_team2)

# fazendo os botões aparecerem
button_team1_up.pack()
button_team2_up.pack()
button_team1_down.pack()
button_team2_down.pack()

# Iniciar o loop principal
root.mainloop()
