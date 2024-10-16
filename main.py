import tkinter as tk

# Variáveis globais do cronômetro
timer_running = False
time_seconds = 0

# Variáveis do placar e sets
scoreTeam1 = 0
scoreTeam2 = 0
setTeam1 = 0
setTeam2 = 0
timers_running = [False] * 5
times_seconds = [0] * 5  # Tempo de cada set em segundos
current_set = 0  # Para saber qual set está rodando
# Labels para exibir o tempo final de cada set
final_time_labels = [None] * 5

# variaveis de cor

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

# Função para converter segundos em minutos:segundos
def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"

# Função para atualizar o cronômetro de um set específico
def update_set_timer(set_index):
    if timers_running[set_index]:
        times_seconds[set_index] += 1
        minutes, seconds = divmod(times_seconds[set_index], 60)
        set_timer_labels[set_index].config(text=f"{minutes:02d}:{seconds:02d}")
        root.after(1000, update_set_timer, set_index)
 
 # Função para iniciar o cronômetro de um set
def start_set_timer(set_index):
    global current_set
    # Parar o cronômetro do set anterior se estiver rodando
    if timers_running[current_set]:
        timers_running[current_set] = False
        final_time_labels[current_set].config(text=f"Tempo set {current_set + 1}: {format_time(times_seconds[current_set])}")

    # Iniciar o cronômetro do novo set
    current_set = set_index
    if not timers_running[set_index]:
        timers_running[set_index] = True
        update_set_timer(set_index)

# Função para zerar os tempos e reiniciar os cronômetros
def reset_all_timers():
    global times_seconds
    global timers_running
    times_seconds = [0] * 5
    timers_running = [False] * 5
    for i in range(5):
        set_timer_labels[i].config(text="00:00")
        final_time_labels[i].config(text=f"Tempo do set {i + 1}: 00:00")
        
###############################################################
# Criar a janela principal
root = tk.Tk()
root.title("Placar e Cronômetro")
root.geometry("768x384")
root.configure(bg=colorBackground) # Fundo preto

# Labels do placar
labelTeam1 = tk.Label(root, text="Equipe 1", font=("Arial", 15), bg=colorBackground, fg=colorFont)
labelScore1 = tk.Label(root, text=str(scoreTeam1), font=("Arial", 60), bg=colorBackground, fg=colorFont)

labelTeam2 = tk.Label(root, text="Equipe 2", font=("Arial", 15), bg=colorBackground, fg=colorFont)
labelScore2 = tk.Label(root, text=str(scoreTeam2), font=("Arial", 60), bg=colorBackground, fg=colorFont)

# Labels dos sets
labelSet1 = tk.Label(root, text=f"Sets: {setTeam1}", font=("Arial", 15), bg=colorBackground, fg=colorFont)
labelSet2 = tk.Label(root, text=f"Sets: {setTeam2}", font=("Arial", 15), bg=colorBackground, fg=colorFont)

# Posicionar os labels do placar e sets
labelTeam1.place(relx=0.1, rely=0.1, relwidth=0.2, relheight=0.2)
labelScore1.place(relx=0.1, rely=0.3, relwidth=0.2, relheight=0.2)
labelSet1.place(relx=0.1, rely=0.5, relwidth=0.2, relheight=0.2)
labelTeam2.place(relx=0.8, rely=0.1, relwidth=0.2, relheight=0.2)
labelScore2.place(relx=0.8, rely=0.3, relwidth=0.2, relheight=0.2)
labelSet2.place(relx=0.8, rely=0.5, relwidth=0.2, relheight=0.2)

# Label do cronômetro
timer_label = tk.Label(root, text="00:00", font=("Arial", 20), bg=colorBackground, fg=colorFont)
timer_label.pack(pady=20)

# Label do número de sets no placar
labelTotalSets = tk.Label(root, text=f"Número de sets: {setTeam1 + setTeam2}", font=("Arial", 15), bg="red", fg=colorFont)
labelTotalSets.place(relx=0.4, rely=0.6, relwidth=0.25, relheight=0.1)

# Labels para exibir o tempo de cada set embaixo do placar
set_timer_labels = []
for i in range(5):
    label = tk.Label(root, text="00:00", font=("Arial", 15), bg="black", fg="white")
    label.place(relx=0.1 + i*0.15, rely=0.9, relwidth=0.12, relheight=0.1)
    set_timer_labels.append(label)

# Labels para exibir o tempo final de cada set embaixo de cada cronômetro
for i in range(5):
    final_label = tk.Label(root, text=f"Set {i + 1}: 00:00", font=("Arial", 12), bg="green", fg="white")
    final_label.place(relx=0.1 + i*0.15, rely=0.85, relwidth=0.15, relheight=0.05)
    final_time_labels[i] = final_label


###############################################################

# Criar a janela de controle
controlWindow = tk.Toplevel(root)
controlWindow.title("Controles")
controlWindow.geometry("600x600")

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
    scoreTeam1 -= 1
    update_score()

def decreaseTeam2():
    global scoreTeam2
    scoreTeam2 -= 1
    update_score()

# Funções para aumentar o número de sets
def increaseSet1():
    global setTeam1
    setTeam1 += 1
    update_score()

def increaseSet2():
    global setTeam2
    setTeam2 += 1
    update_score()

# Zerar os sets (panic button)
def reset_sets():
    global setTeam1, setTeam2
    setTeam1 = 0
    setTeam2 = 0
    update_score()   

# Botões para controle do placar
buttonTeam1Up = tk.Button(controlWindow, text="1 +", command=increaseTeam1)
buttonTeam2Up = tk.Button(controlWindow, text="2 +", command=increaseTeam2)
buttonTeam1Down = tk.Button(controlWindow, text="1 -", command=decreaseTeam1)
buttonTeam2Down = tk.Button(controlWindow, text="2 -", command=decreaseTeam2)

# Botões para controle dos sets
buttonSet1Up = tk.Button(controlWindow, text="Set 1 +", command=increaseSet1)
buttonSet2Up = tk.Button(controlWindow, text="Set 2 +", command=increaseSet2)

# Botão para zerar os sets
buttonResetSets = tk.Button(controlWindow, text="Zerar Sets", command=reset_sets)

# Posicionar os botões do placar
buttonTeam1Up.place(relx=0.1, rely=0.1, relwidth=0.1, relheight=0.1)
buttonTeam2Up.place(relx=0.55, rely=0.1, relwidth=0.1, relheight=0.1)
buttonTeam1Down.place(relx=0.1, rely=0.4, relwidth=0.1, relheight=0.1)
buttonTeam2Down.place(relx=0.55, rely=0.4, relwidth=0.1, relheight=0.1)

# Posicionar os botões dos sets
buttonSet1Up.place(relx=0.1, rely=0.7, relwidth=0.1, relheight=0.1)
buttonSet2Up.place(relx=0.55, rely=0.7, relwidth=0.1, relheight=0.1)

# Botões de controle do cronômetro
buttonStartTimer = tk.Button(controlWindow, text="Iniciar Cronômetro", command=start_timer)
buttonStopTimer = tk.Button(controlWindow, text="Parar Cronômetro", command=stop_timer)
buttonResetTimer = tk.Button(controlWindow, text="Reiniciar Cronômetro", command=reset_timer)

# Posicionar os botões do cronômetro
buttonStartTimer.place(relx=0.1, rely=0.85, relwidth=0.35, relheight=0.1)
buttonStopTimer.place(relx=0.55, rely=0.85, relwidth=0.35, relheight=0.1)

# Posicionar o botão de zerar sets
buttonResetSets.place(relx=0.3, rely=0.8, relwidth=0.4, relheight=0.1)

# Botões para iniciar os cronômetros dos sets na janela de controle
for i in range(5):
    button = tk.Button(controlWindow, text=f"Set {i + 1}", command=lambda i=i: start_set_timer(i))
    button.place(relx=0.1 + i*0.15, rely=0.2, relwidth=0.05, relheight=0.05)

# Botão para reiniciar todos os cronômetros
reset_button = tk.Button(controlWindow, text="Reset timers", command=reset_all_timers)
reset_button.place(relx=0.35, rely=0.6, relwidth=0.3, relheight=0.1)

# Iniciar o loop principal
root.mainloop()
