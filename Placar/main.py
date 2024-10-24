import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
# Variáveis globais do cronômetro
timer_running = False
time_seconds = 0
timer_label_control = None  # Label para o cronômetro na janela de controle

# Variáveis do placar e sets
scoreTeam1 = 0
scoreTeam2 = 0
setTeam1 = 0
setTeam2 = 0
current_set = 0  # Para saber qual set está rodando
set_scores = [[0, 0] for _ in range(5)]  # Armazena os placares de cada set
current_set_display = 1  # Set atual, começa no 1

# Variáveis para contagem de substituições
subsTeam1 = 0
subsTeam2 = 0

# Variáveis para contagem de tempos
timeTeam1 = 0
timeTeam2 = 0

# variáveis de cor
colorFont = "white"
colorBackground = "black"

#definir o time que está sacando 
serving_team = 1  # Começa com a Equipe 1 
####################################################

# Função para atualizar o cronômetro
def update_timer():
    if timer_running:
        global time_seconds
        time_seconds += 1
        # Converter os segundos em minutos e segundos
        minutes, seconds = divmod(time_seconds, 60)
        time_formatted = f"{minutes:02d}:{seconds:02d}"

        # Atualiza o cronômetro nas duas janelas
        timer_label.config(text=time_formatted)
        timer_label_control.config(text=time_formatted)  # Atualiza também na janela de controle


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
    timer_label_control.config(text="00:00")
    stop_timer()

# Atualizar o placar e os sets
def update_score():
    labelScore1.config(text=str(scoreTeam1))
    labelScore2.config(text=str(scoreTeam2))
    labelSet1.config(text=f"Sets: {setTeam1}")
    labelSet2.config(text=f"Sets: {setTeam2}")

    # Atualizar o label com o número total de sets
    labelTotalSets.config(text=f"Número de sets: {setTeam1 + setTeam2}")

# Update visualização set atual na janela de comando
def update_current_set_control_label():
    labelCurrentSetControl.config(text=current_set_display)

# Função para armazenar o placar do set atual
def store_set_score():
    global set_scores, current_set
    set_scores[current_set][0] = scoreTeam1
    set_scores[current_set][1] = scoreTeam2
    set_score_labels[current_set][1].config(text=f"{scoreTeam1} x {scoreTeam2}")

# Função para mudar o set
def next_set():
    global scoreTeam1, scoreTeam2, current_set, current_set_display
    # Armazenar o placar do set atual
    store_set_score()
    # Passar para o próximo set
    current_set += 1
    current_set_display += 1
    scoreTeam1, scoreTeam2 = 0, 0
    update_score()
    update_current_set_control_label()  # Atualiza o label na janela de controle
    update_current_set_label()  # Atualiza o label na janela principal
    
def prev_set():
    global scoreTeam1, scoreTeam2, current_set, current_set_display
    # Armazenar o placar do set atual
    store_set_score()
    # Voltar para o set anterior
    if current_set > 0:
        current_set -= 1
        current_set_display -= 1
    scoreTeam1, scoreTeam2 = 0, 0
    update_score()
    update_current_set_control_label()  # Atualiza o label na janela de controle
    update_current_set_label()  # Atualiza o label na janela principal

# Função para atualizar o ícone do saque
def update_serve_icon():
    if serving_team == 1:
        labelServe1.place(relx=0.12, rely=0.05, relwidth=0.1, relheight=0.1)
        labelServe2.place_forget()  # Remove o ícone da Equipe 2
    else:
        labelServe2.place(relx=0.88, rely=0.05, relwidth=0.1, relheight=0.1, anchor="ne")
        labelServe1.place_forget()  # Remove o ícone da Equipe 1

# Função para alternar o time que está sacando
def toggle_serving_team():
    global serving_team
    serving_team = 2 if serving_team == 1 else 1  # Alterna entre 1 e 2
    update_serve_icon()

# Função para atualizar o label do set atual
def update_current_set_label():
    labelCurrentSet.config(text=f"Set atual: {current_set_display}")

# Função para alterar o set atual com base no número escolhido
def set_current_set(set_number):
    global current_set_display
    current_set_display = set_number
    update_current_set_label()

# Função para atualizar os nomes das equipes
def update_team_names():
    team1_name = entryTeam1.get()  # Captura o nome da equipe 1
    team2_name = entryTeam2.get()  # Captura o nome da equipe 2

    labelTeam1.config(text=team1_name)  # Atualiza o label da Equipe 1 na janela principal
    labelTeam2.config(text=team2_name)  # Atualiza o label da Equipe 2 na janela principal
# Funções para aumentar o número de substituições
def increaseSubsTeam1():
    global subsTeam1
    subsTeam1 += 1
    update_score()

def increaseSubsTeam2():
    global subsTeam2
    subsTeam2 += 1
    update_score()    

# Funções para aumentar o número de substituições
def increaseTimeTeam1():
    global timeTeam1
    timeTeam1 += 1
    update_score()

def increaseTimeTeam2():
    global timeTeam2
    timeTeam2 += 1
    update_score()  

###############################################################
# Criar a janela principal
root = tk.Tk()
root.title("Placar e Cronômetro")
root.geometry("768x384")
root.configure(bg=colorBackground)  # Fundo preto

# Brasão times
team1 = PhotoImage(file="team1.png")
small_team1 = team1.subsample(2,2)
team2 = PhotoImage(file="team2.png")
small_team2 = team2.subsample(2,2)

# Imagem para o time que está sacando
serve_icon = PhotoImage(file="white_ball.png")
small_serve_icon = serve_icon.subsample(15, 15)  # Reduz o tamanho da imagem

# Labels do placar
labelTeam1 = tk.Label(root, text="Equipe 1", font=("Arial", 30), bg=colorBackground, fg=colorFont)
labelScore1 = tk.Label(root, text=str(scoreTeam1), font=("Arial", 60), bg=colorBackground, fg=colorFont)

labelTeam2 = tk.Label(root, text="Equipe 2", font=("Arial", 30), bg=colorBackground, fg=colorFont)
labelScore2 = tk.Label(root, text=str(scoreTeam2), font=("Arial", 60), bg=colorBackground, fg=colorFont)

# Labels dos sets
labelSet1 = tk.Label(root, text=f"Sets: {setTeam1}", font=("Arial", 25), bg=colorBackground, fg=colorFont)
labelSet2 = tk.Label(root, text=f"Sets: {setTeam2}", font=("Arial", 25), bg=colorBackground, fg=colorFont)

# label do brasão dos times
labelBrazaoTime1 = tk.Label(root, image=small_team1, bg=colorBackground)
labelBrazaoTime2 = tk.Label(root, image=small_team2,  bg=colorBackground)

# Posicionando label brasão dos times
# label do brasão dos times (centralizados)
labelBrazaoTime1.place(relx=0.2, rely=0.25, relwidth=0.1, relheight=0.3)
labelBrazaoTime2.place(relx=0.8, rely=0.25, relwidth=0.1, relheight=0.3, anchor="ne")

# Posicionar os labels do placar e sets
# Labels do placar (centralizados)
labelTeam1.place(relx=0.25, rely=0.20, relwidth=0.2, relheight=0.2, anchor="center")
labelScore1.place(relx=0.4, rely=0.4, relwidth=0.3, relheight=0.2, anchor="center")
labelSet1.place(relx=0.25, rely=0.6, relwidth=0.2, relheight=0.2, anchor="center")


labelTeam2.place(relx=0.75, rely=0.20, relwidth=0.2, relheight=0.2, anchor="center")
labelScore2.place(relx=0.6, rely=0.4, relwidth=0.2, relheight=0.2, anchor="center")
labelSet2.place(relx=0.75, rely=0.6, relwidth=0.2, relheight=0.2, anchor="center")

#labelScore = Label(root, text="0 x 0", font=("Helvetica", 80), bg=colorBackground, fg=colorFont)
#labelScore.place(relx=0.5, rely=0.4, relwidth=0.3, relheight=0.2, anchor="center")

# Label do cronômetro
timer_label = tk.Label(root, text="00:00", font=("Arial", 40), bg=colorBackground, fg=colorFont)
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

# Adicionar o label do set atual na janela principal
labelCurrentSet = tk.Label(root, text=f"Set atual: {current_set_display}", font=("Arial", 20), bg=colorBackground, fg=colorFont)
labelCurrentSet.place(relx=0.5, rely=0.55, relwidth=0.25, relheight=0.1, anchor="center")  # Posicionamento centralizado abaixo do placar    

# Labels para o ícone de saque
labelServe1 = tk.Label(root, image=small_serve_icon, bg=colorBackground)
labelServe2 = tk.Label(root, image=small_serve_icon, bg=colorBackground)    

# Labels para mostrar número de substituições de cada time
labelSubs1 = tk.Label(root, text=f"Substituições: {subsTeam1}", font=("Arial", 25), bg=colorBackground, fg=colorFont)
labelSubs2 = tk.Label(root, text=f"Substituições: {subsTeam2}", font=("Arial", 25), bg=colorBackground, fg=colorFont)

# Posicionar os labels das substituições ao lado dos nomes das equipes
labelSubs1.place(relx=0.07, rely=0.65, relwidth=0.2, relheight=0.1)
labelSubs2.place(relx=0.93, rely=0.65, relwidth=0.2, relheight=0.1, anchor="ne")

# Labels para mostrar número de substituições de cada time
labelTime1 = tk.Label(root, text=f"Tempos: {timeTeam1}", font=("Arial", 25), bg=colorBackground, fg=colorFont)
labelTime2 = tk.Label(root, text=f"Tempos: {timeTeam2}", font=("Arial", 25), bg=colorBackground, fg=colorFont)

# Posicionar os labels das substituições ao lado dos nomes das equipes
labelTime1.place(relx=0.07, rely=0.75, relwidth=0.2, relheight=0.1)
labelTime2.place(relx=0.93, rely=0.75, relwidth=0.2, relheight=0.1, anchor="ne")


###############################################################
# Criar a janela de controle
controlWindow = tk.Toplevel(root)
controlWindow.title("Controles")
controlWindow.geometry("700x600")

# Caixas de texto para entrada de nome das equipes
entryTeam1 = tk.Entry(controlWindow, font=("Arial", 15))
entryTeam1.place(relx=0.2, rely=0.5, relwidth=0.2, relheight=0.05, anchor="center")

entryTeam2 = tk.Entry(controlWindow, font=("Arial", 15))
entryTeam2.place(relx=0.8, rely=0.5, relwidth=0.2, relheight=0.05, anchor="center")

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
    global setTeam1, setTeam2, scoreTeam1, scoreTeam2, current_set, current_set_display
    setTeam1 = 0
    setTeam2 = 0
    scoreTeam1 = 0
    scoreTeam2 = 0
    current_set = 0
    current_set_display = 1
    update_score()
    update_current_set_control_label()
    update_current_set_label()



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

# Funções dos botões para selecionar manualmente o set atual
buttonSet1 = tk.Button(controlWindow, text="1", command=lambda: set_current_set(1))
buttonSet2 = tk.Button(controlWindow, text="2", command=lambda: set_current_set(2))
buttonSet3 = tk.Button(controlWindow, text="3", command=lambda: set_current_set(3))
buttonSet4 = tk.Button(controlWindow, text="4", command=lambda: set_current_set(4))
buttonSet5 = tk.Button(controlWindow, text="5", command=lambda: set_current_set(5))

# Botão para atualizar os nomes das equipes
buttonUpdateNames = tk.Button(controlWindow, text="Atualizar Nomes", command=lambda: update_team_names())
buttonUpdateNames.place(relx=0.5, rely=0.5, relwidth=0.2, relheight=0.05, anchor="center")

# Botão para controlar SETS
buttonNextSet = tk.Button(controlWindow, text="Próximo Set", command=next_set)
buttonPrevSet = tk.Button(controlWindow, text="Set Anterior", command=prev_set)
buttonResetSets = tk.Button(controlWindow, text="Zerar Sets", command=reset_sets)


#### Textos para a janela de controle ###################
title_label = tk.Label(controlWindow, text="Cronômetro", font=("Arial", 15), bg="lightgray", fg="black")
title_label.place(relx=0.5, rely=0.05, relwidth=0.2, relheight=0.05, anchor="center")  # Posiciona no topo centralizado

title_label = tk.Label(controlWindow, text="Set atual", font=("Arial", 15), bg="lightgray", fg="black")
title_label.place(relx=0.5, rely=0.27, relwidth=0.2, relheight=0.05, anchor="center")  # Posiciona no topo centralizado

labelCurrentSetControl = tk.Label(controlWindow, text=current_set_display, font=("Arial", 40), bg="lightgray", fg="black")
labelCurrentSetControl.place(relx=0.5, rely=0.35, relwidth=0.1, relheight=0.1, anchor="center")  # Posiciona entre os botões de set

# Label do cronômetro na janela de controle
timer_label_control = tk.Label(controlWindow, text="00:00", font=("Arial", 40), bg="lightgray", fg="black")
timer_label_control.place(relx=0.4, rely=0.08, relwidth=0.2, relheight=0.1, anchor="nw")

#-----------------------------------#

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

# Adicionar o botão no painel de controle para alternar o saque
buttonToggleServe = tk.Button(controlWindow, text="Alternar Saque", command=toggle_serving_team)
buttonToggleServe.place(relx=0.4, rely=0.6, relwidth=0.2, relheight=0.1)

# Posicionar os botões do cronômetro
buttonStartTimer.place(relx=0.6, rely=0.08, relwidth=0.1, relheight=0.1, anchor="nw")
buttonStopTimer.place(relx=0.4, rely=0.08, relwidth=0.1, relheight=0.1, anchor="ne")
buttonResetTimer.place(relx=0.5, rely=0.2, relwidth=0.2, relheight=0.05, anchor="center")

# Posicionar o botão de avançar set
buttonNextSet.place(relx=0.6, rely=0.30, relwidth=0.1, relheight=0.1, anchor="nw")
buttonPrevSet.place(relx=0.4, rely=0.30, relwidth=0.1, relheight=0.1, anchor="ne")
buttonResetSets.place(relx=0.5, rely=0.42, relwidth=0.2, relheight=0.05, anchor="center")

#Desenhando linhas para separar as áreas nas telas
#Janela de comando
separator1 = tk.Frame(controlWindow, bg="black", width=2)  # Defina a altura como 2 para uma linha fina
separator1.place(relx=0.3, rely=0, relheight=1)
separator2 = tk.Frame(controlWindow, bg="black", width=2)  # Defina a altura como 2 para uma linha fina
separator2.place(relx=0.7, rely=0, relheight=1)
# Começar o ícone na Equipe 1
update_serve_icon()

# Iniciar o loop principal
root.mainloop()
