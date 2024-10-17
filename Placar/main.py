import tkinter as tk
from tkinter import *

# Variáveis globais do cronômetro
timer_running = False
time_seconds = 0

# Variáveis do placar e sets
scoreTeam1 = 0
scoreTeam2 = 0
setTeam1 = 0
setTeam2 = 0
current_set = 0  # Para saber qual set está rodando
set_scores = [[0, 0] for _ in range(5)]  # Armazena os placares de cada set

# variáveis de cor
colorFont = "white"
colorBackground = "black"

####################################################

# Função para atualizar o cronômetro
def update_timer():
    if timer_running:
        global time_seconds
        time_seconds += 1
        # Converter os segundos em minutos e segundos
        minutes, seconds = divmod(time_seconds, 60)
        timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        # Atualizar o cronômetro a cada 1000ms (1 segundo)
        root.after(1000, update_timer)

# Função para iniciar o cronômetro
def start_timer():
    global timer_running
    if not timer_running:
        timer_running = True
        update_timer()

# Função para parar o cronômetro
def stop_timer():
    global timer_running
    timer_running = False

# Função para reiniciar o cronômetro
def reset_timer():
    global time_seconds
    time_seconds = 0
    timer_label.config(text="00:00")
    stop_timer()

# Atualizar o placar e os sets
def update_score():
    labelScore1.config(text=str(scoreTeam1))
    labelScore2.config(text=str(scoreTeam2))
    labelSet1.config(text=f"Sets: {setTeam1}")
    labelSet2.config(text=f"Sets: {setTeam2}")

    # Atualizar o label com o número total de sets
    labelTotalSets.config(text=f"Número de sets: {setTeam1 + setTeam2}")

# Função para armazenar o placar do set atual
def store_set_score():
    global set_scores, current_set
    set_scores[current_set][0] = scoreTeam1
    set_scores[current_set][1] = scoreTeam2
    set_score_labels[current_set][1].config(text=f"{scoreTeam1} x {scoreTeam2}")

# Função para mudar para o próximo set
def next_set():
    global scoreTeam1, scoreTeam2, current_set
    # Armazenar o placar do set atual
    store_set_score()
    # Passar para o próximo set
    current_set += 1
    scoreTeam1, scoreTeam2 = 0, 0
    update_score()

###############################################################
# Criar a janela principal
root = tk.Tk()
root.title("Placar e Cronômetro")
root.geometry("768x384")
root.configure(bg=colorBackground)  # Fundo preto

# Brazão times
team1 = PhotoImage(file="team1.png")
small_team1 = team1.subsample(2,2)
team2 = PhotoImage(file="team2.png")
small_team2 = team2.subsample(2,2)

# Labels do placar
labelTeam1 = tk.Label(root, text="Equipe 1", font=("Arial", 15), bg=colorBackground, fg=colorFont)
labelScore1 = tk.Label(root, text=str(scoreTeam1), font=("Arial", 60), bg=colorBackground, fg=colorFont)

labelTeam2 = tk.Label(root, text="Equipe 2", font=("Arial", 15), bg=colorBackground, fg=colorFont)
labelScore2 = tk.Label(root, text=str(scoreTeam2), font=("Arial", 60), bg=colorBackground, fg=colorFont)

# Labels dos sets
labelSet1 = tk.Label(root, text=f"Sets: {setTeam1}", font=("Arial", 15), bg=colorBackground, fg=colorFont)
labelSet2 = tk.Label(root, text=f"Sets: {setTeam2}", font=("Arial", 15), bg=colorBackground, fg=colorFont)

# label do brazão dos times
labelBrazaoTime1 = tk.Label(root, image=small_team1, bg=colorBackground)
labelBrazaoTime2 = tk.Label(root, image=small_team2,  bg=colorBackground)

# Posicionando label brazão dos times
labelBrazaoTime1.place(relx=0, rely=0.2, relwidth=0.1, relheight=0.3)
labelBrazaoTime2.place(relx=1, rely=0.2, relwidth=0.1, relheight=0.3, anchor="ne")

# Posicionar os labels do placar e sets
labelTeam1.place(relx=0.07, rely=0.1, relwidth=0.2, relheight=0.2)
labelScore1.place(relx=0.07, rely=0.3, relwidth=0.2, relheight=0.2)
labelSet1.place(relx=0.07, rely=0.5, relwidth=0.2, relheight=0.2)
labelTeam2.place(relx=0.93, rely=0.1, relwidth=0.2, relheight=0.2, anchor="ne")
labelScore2.place(relx=0.93, rely=0.3, relwidth=0.2, relheight=0.2, anchor="ne")
labelSet2.place(relx=0.93, rely=0.5, relwidth=0.2, relheight=0.2, anchor="ne")

# Label do cronômetro
timer_label = tk.Label(root, text="00:00", font=("Arial", 20), bg=colorBackground, fg=colorFont)
timer_label.pack(pady=20)

# Label do número de sets no placar
labelTotalSets = tk.Label(root, text=f"Número de sets: {setTeam1 + setTeam2}", font=("Arial", 15), bg="red", fg=colorFont)
labelTotalSets.place(relx=0.4, rely=0.6, relwidth=0.25, relheight=0.1)

# Labels para exibir o placar de cada set
set_score_labels = []
for i in range(5):
    set_label = tk.Label(root, text=f"SET {i + 1}", font=("Arial", 15), bg=colorBackground, fg=colorFont)
    score_label = tk.Label(root, text="0 x 0", font=("Arial", 15), bg=colorBackground, fg=colorFont)
    set_label.place(relx=0.1 + i * 0.15, rely=0.82, relwidth=0.12, relheight=0.1)
    score_label.place(relx=0.1 + i * 0.15, rely=0.90, relwidth=0.12, relheight=0.1)
    set_score_labels.append((set_label, score_label))

###############################################################

# Criar a janela de controle
controlWindow = tk.Toplevel(root)
controlWindow.title("Controles")
controlWindow.geometry("700x600")

# Funções para aumentar/diminuir o placar
def increaseTeam1():
    global scoreTeam1
    scoreTeam1 += 1
    update_score()

def increaseTeam2():
    global scoreTeam2
    scoreTeam2 += 1
    update_score()

def decreaseTeam1():
    global scoreTeam1
    if scoreTeam1 > 0:
        scoreTeam1 -= 1
    update_score()

def decreaseTeam2():
    global scoreTeam2
    if scoreTeam2 > 0:
        scoreTeam2 -= 1
    update_score()

# Funções para aumentar/diminuir o número de sets
def increaseSet1():
    global setTeam1
    setTeam1 += 1
    update_score()

def decreaseSet1():
    global setTeam1
    setTeam1 -= 1
    update_score()

def increaseSet2():
    global setTeam2
    setTeam2 += 1
    update_score()

def decreaseSet2():
    global setTeam2
    setTeam2 -= 1
    update_score()

# Zerar os sets (panic button)
def reset_sets():
    global setTeam1, setTeam2, scoreTeam1, scoreTeam2, current_set
    setTeam1 = 0
    setTeam2 = 0
    scoreTeam1 = 0
    scoreTeam2 = 0
    current_set = 0
    update_score()

# Botões para controle do placar
buttonTeam1Up = tk.Button(controlWindow, text="1 +", command=increaseTeam1)
buttonTeam2Up = tk.Button(controlWindow, text="2 +", command=increaseTeam2)
buttonTeam1Down = tk.Button(controlWindow, text="1 -", command=decreaseTeam1)
buttonTeam2Down = tk.Button(controlWindow, text="2 -", command=decreaseTeam2)

# Botões para controle dos sets
buttonSet1Up = tk.Button(controlWindow, text="Set 1 +", command=increaseSet1)
buttonSet1Down = tk.Button(controlWindow, text="Set 1 -", command=decreaseSet1)
buttonSet2Up = tk.Button(controlWindow, text="Set 2 +", command=increaseSet2)
buttonSet2Down = tk.Button(controlWindow, text="Set 2 -", command=decreaseSet2)

# Botão para zerar os sets
buttonResetSets = tk.Button(controlWindow, text="Zerar Sets", command=reset_sets)

# Botão para avançar para o próximo set
buttonNextSet = tk.Button(controlWindow, text="Próximo Set", command=next_set)

# Posicionar os botões do placar
buttonTeam1Up.place(relx=0.1, rely=0.6, relwidth=0.1, relheight=0.1)
buttonTeam2Up.place(relx=0.8, rely=0.6, relwidth=0.1, relheight=0.1, anchor="ne")
buttonTeam1Down.place(relx=0.2, rely=0.6, relwidth=0.1, relheight=0.1)
buttonTeam2Down.place(relx=0.9, rely=0.6, relwidth=0.1, relheight=0.1, anchor="ne")

# Posicionar os botões dos sets
buttonSet1Up.place(relx=0.1, rely=0.7, relwidth=0.1, relheight=0.1)
buttonSet2Up.place(relx=0.8, rely=0.7, relwidth=0.1, relheight=0.1, anchor="ne")
buttonSet1Down.place(relx=0.2, rely=0.7, relwidth=0.1, relheight=0.1)
buttonSet2Down.place(relx=0.9, rely=0.7, relwidth=0.1, relheight=0.1, anchor="ne")

# Botões de controle do cronômetro
buttonStartTimer = tk.Button(controlWindow, text="Iniciar Cronômetro", command=start_timer)
buttonStopTimer = tk.Button(controlWindow, text="Parar Cronômetro", command=stop_timer)
buttonResetTimer = tk.Button(controlWindow, text="Reiniciar Cronômetro", command=reset_timer)

# Posicionar os botões do cronômetro
buttonStartTimer.place(relx=0.1, rely=0.85, relwidth=0.35, relheight=0.1)
buttonStopTimer.place(relx=0.55, rely=0.85, relwidth=0.35, relheight=0.1)

# Posicionar o botão de avançar set
buttonNextSet.place(relx=0.3, rely=0.9, relwidth=0.4, relheight=0.1)

# Iniciar o loop principal
root.mainloop()