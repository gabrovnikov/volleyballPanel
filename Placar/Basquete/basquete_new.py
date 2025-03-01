import tkinter as tk
from tkinter import *
from tkinter import font
from tkinter import filedialog
from PIL import Image, ImageTk
from screeninfo import get_monitors
import os
import subprocess

# Variáveis globais do cronômetro
timer_running = False
time_seconds = 600  # 10 minutos em segundos
time_milliseconds = 0  # Começando com 0 milissegundos
timer_label_control = None  # Label para o cronômetro na janela de controle
labelScore_control = None

# Variáveis do placar e quarters
scoreTeam1 = 0
scoreTeam2 = 0
scoreTeam1_control = 0
scoreTeam2_control = 0
quarterTeam1 = 0
quarterTeam2 = 0
current_quarter = 0  # Para saber qual quarter está rodando

quarter_scores = [[0, 0] for _ in range(10)]  # Armazena os placares de cada quarter
current_quarter_display = 1  # quarter atual, começa no 1

# Variáveis para contagem de substituições
subsTeam1 = 0
subsTeam2 = 0

# Variáveis para contagem de tempos
faltasTeam1 = 0
faltasTeam2 = 0

# Variáveis de desafio
challengeTeam1 = 0
challengeTeam2 = 0

# variáveis de cor
colorFont = "black"
colorBackground = "white"

#definir o time que está sacando 
serving_team = 1  # Começa com a Equipe 1 

timer_running = False
time_seconds = 600  # 10 minutos em segundos
time_milliseconds = 0  # Começando com 0 milissegundos




# Função que configura a primeira janela
def configure_window_primary(controlWindow, primary_monitor):
    controlWindow.title("Controles")
    controlWindow.geometry(f"700x600")

# Função que configura a segunda janela
def configure_window_secondary(root, secondary_monitor):
    root.title("Placar e Cronômetro")
    
    root.geometry(f"768x384+{secondary_monitor.x}+{secondary_monitor.y}")

    root.configure(bg=colorBackground)
    
    # Função para alternar o modo fullscreen
    def toggle_fullscreen(event=None):
        is_fullscreen = root.attributes('-fullscreen')
        root.overrideredirect(True)
        
        if not is_fullscreen:
            # Se está entrando em fullscreen, fixa as coordenadas no monitor secundário
            root.overrideredirect(True)
            root.geometry(f"{secondary_monitor.width}x{secondary_monitor.height}+{secondary_monitor.x}+{secondary_monitor.y}")

    # Função para sair do modo fullscreen
    def exit_fullscreen(event=None):
        root.overrideredirect(False)
        
        
        # Reposiciona a janela no monitor secundário
        root.geometry(f"{secondary_monitor.width}x{secondary_monitor.height}+{secondary_monitor.x}+{secondary_monitor.y}")

    # Bind das teclas F11 e ESC para alternar fullscreen
    root.bind("<F11>", toggle_fullscreen)
    root.bind("<Escape>", exit_fullscreen)





# Função para abrir as janelas em monitores diferentes
def open_windows_on_monitors():
    # Obter informações dos monitores conectados
    monitors = get_monitors()
    
    # Verifica se há mais de um monitor disponível
    if len(monitors) < 2:
        print("Segundo Monitor não conectado.")
    primary_monitor = monitors[0]
    secondary_monitor = monitors[1]
    # Criar e configurar a primeira janela no monitor secundário
    root = tk.Tk()
    configure_window_secondary(root, secondary_monitor)
    # Criar e configurar a segunda janela no monitor secundário
    controlWindow = tk.Toplevel(root)  # Usando Toplevel para manter a hierarquia
    configure_window_primary(controlWindow, primary_monitor)

# Atualizar o placar e os quarters
    def update_score():
        labelScore1.config(text=str(scoreTeam1))
        labelScore2.config(text=str(scoreTeam2))
        labelScore_control.config(text= str(scoreTeam1_control)+" x "+ str(scoreTeam2_control))
        # Atualizar o label com o número total de quarters
        labelfaltas1.config(text=str(faltasTeam1))
        labelfaltas2.config(text=str(faltasTeam2))
        
    # Funções para aumentar o número de substituições
    def increasefaltasTeam1():
        global faltasTeam1
        faltasTeam1 += 1
        update_score()
    def increasefaltasTeam2():
        global faltasTeam2
        faltasTeam2 += 1
        update_score()  
    def decreasefaltasTeam1():
        global faltasTeam1
        faltasTeam1 -= 1
        update_score()   
    def decreasefaltasTeam2():
        global faltasTeam2
        faltasTeam2 -= 1
        update_score() 
    # Update visualização quarter atual na janela de comando
    def update_current_quarter_control_label():
        labelCurrentQuarterControl.config(text=current_quarter_display)
    # Função para armazenar o placar do quarter atual
    def store_quarter_score():
        global quarter_scores, current_quarter
        quarter_scores[current_quarter][0] = scoreTeam1
        quarter_scores[current_quarter][1] = scoreTeam2
        quarter_score_labels[current_quarter][1].config(text=f"{scoreTeam1} x {scoreTeam2}")
    # Função para mudar o quarter
    def next_quarter():
        global scoreTeam1, scoreTeam2, scoreTeam1_control, scoreTeam2_control, current_quarter, current_quarter_display
        # Armazenar o placar do quarter atual
        store_quarter_score()
        # Passar para o próximo quarter
        current_quarter += 1
        current_quarter_display += 1
        scoreTeam1, scoreTeam2 = 0, 0
        scoreTeam1_control, scoreTeam2_control = 0, 0
        update_score()
        update_current_quarter_control_label()  # Atualiza o label na janela de controle
        update_current_quarter_label()  # Atualiza o label na janela principal
        
    def prev_quarter():
        global scoreTeam1, scoreTeam2, current_quarter, current_quarter_display
        # Armazenar o placar do quarter atual
        store_quarter_score()
        # Voltar para o quarter anterior
        if current_quarter > 0:
            current_quarter -= 1
            current_quarter_display -= 1
        scoreTeam1, scoreTeam2 = 0, 0
        update_score()
        update_current_quarter_control_label()  # Atualiza o label na janela de controle
        update_current_quarter_label()  # Atualiza o label na janela principal

    # Função para atualizar o label do quarter atual
    def update_current_quarter_label():
        labelCurrentQuarter.config(text=f"Quarter atual: {current_quarter_display}")
    # Função para atualizar os nomes das equipes
    def update_team_names():
        
        team1_name = entryTeam1.get()  # Captura o nome da equipe 1
        team2_name = entryTeam2.get()  # Captura o nome da equipe 2

        labelTeam1.config(text=team1_name)  # Atualiza o label da Equipe 1 na janela principal
        labelTeam2.config(text=team2_name)  # Atualiza o label da Equipe 2 na janela principal

    #Função para selecionar imagem do time
    def selecionar_equipe1():
        # Abre a janela do sistema para selecionar a imagem
        caminho_equipe1 = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Arquivos de Imagem", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        
        if caminho_equipe1:  # Se um arquivo for selecionado
            # Carregar e exibir a imagem usando PIL
            equipe1 = Image.open(caminho_equipe1)
            equipe1 = equipe1.resize((800, 400))  # Redimensiona para ajustar ao Label
            equipe1_controlWindow = equipe1.resize((500, 250))  # Redimensiona para ajustar ao Label
            equipe1_tk = ImageTk.PhotoImage(equipe1)
            equipe1_tk_controlWindow = ImageTk.PhotoImage(equipe1_controlWindow)
            # Atualizar o Label com a imagem selecionada
            label_equipe1.config(image=equipe1_tk)
            label_equipe1.image = equipe1_tk  # Manter a referência da imagem para não ser coletada pelo garbage collector
            
            label_equipe1_controlWindow.config(image=equipe1_tk_controlWindow)
            label_equipe1_controlWindow.image = equipe1_tk_controlWindow  # Manter a referência da imagem para não ser coletada pelo garbage collector         

    def selecionar_equipe2():
        # Abre a janela do sistema para selecionar a imagem
        caminho_equipe2 = filedialog.askopenfilename(
            title="Selecione uma imagem",
            filetypes=[("Arquivos de Imagem", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        
        if caminho_equipe2:  # Se um arquivo for selecionado
            # Carregar e exibir a imagem usando PIL
            equipe2 = Image.open(caminho_equipe2)
            equipe2 = equipe2.resize((350, 350))  # Redimensiona para ajustar ao Label
            equipe2_controlWindow = equipe2.resize((250, 250))  # Redimensiona para ajustar ao Label
            equipe2_tk = ImageTk.PhotoImage(equipe2)
            equipe2_tk_controlWindow = ImageTk.PhotoImage(equipe2_controlWindow)
            # Atualizar o Label com a imagem selecionada

            label_equipe2.config(image=equipe2_tk)
            label_equipe2.image = equipe2_tk  # Manter a referência da imagem para não ser coletada pelo garbage collector
            
            label_equipe2_controlWindow.config(image=equipe2_tk_controlWindow)
            label_equipe2_controlWindow.image = equipe2_tk_controlWindow  # Manter a referência da imagem para não ser coletada pelo garbage collector

    
# Brasão times
    label_equipe1 = tk.Label(root,  bg=colorBackground)
    label_equipe1.place(relx=0.05, rely=0.55, relwidth=0.19, relheight=0.35, anchor="sw")

    label_equipe2 = tk.Label(root, bg=colorBackground)
    label_equipe2.place(relx=0.95, rely=0.55, relwidth=0.19, relheight=0.35, anchor="se")

# Labels do placar

    #Declaração
    labelTeam1 = tk.Label(root, text="Equipe 1", font=("Anton", 40), bg="red", fg=colorFont)
    labelScore1 = tk.Label(root, text=str(scoreTeam1), font=("Anton", 200), bg="red", fg=colorFont)
    labelCross = tk.Label(root, text = "X", font=("Anton", 50), bg="cyan", fg=colorFont)
    labelTeam2 = tk.Label(root, text="Equipe 2", font=("Anton", 40), bg="blue", fg=colorFont)
    labelScore2 = tk.Label(root, text=str(scoreTeam2), font=("Anton", 200), bg="blue", fg=colorFont)
    
    #Posicionamento
    labelTeam1.place(relx=0, rely=0.025, relwidth=0.4, relheight=0.1, anchor="nw")
    labelScore1.place(relx=0.35, rely=0.35, relwidth=0.25, relheight=0.4, anchor="center")
    labelCross.place(relx=0.5, rely=0.35, relwidth=0.05, relheight=0.2, anchor="center")
    labelTeam2.place(relx=1, rely=0.025, relwidth=0.4, relheight=0.1, anchor="ne")
    labelScore2.place(relx=0.65, rely=0.35, relwidth=0.25, relheight=0.4, anchor="center")

    #Cronômetro
    timer_label = tk.Label(root, text="10:00:00", font=("Anton", 90), bg="yellow", fg=colorFont)
    timer_label.place(relx=0.5, rely=0, relwidth=0.3, relheight=0.15, anchor="n")

    #Separadores
    separator_inferior_timer = tk.Frame(root, bg="black", height=4)  # Defina a altura como 2 para uma linha fina
    separator_inferior_timer.place(relx=0, rely=0.15, relwidth=4)
    separator_lateral_esquerda = tk.Frame(root, bg="black", width=4)  # Defina a altura como 2 para uma linha fina
    separator_lateral_esquerda.place(relx=0.3, rely=0, relheight=0.15)
    separator_lateral_direita = tk.Frame(root, bg="black", width=4)  # Defina a altura como 2 para uma linha fina
    separator_lateral_direita.place(relx=0.7, rely=0, relheight=0.15)

    # Labels para exibir o placar de cada quarter
    quarter_score_labels = []
    for i in range(4):
        quarter_label = tk.Label(root, text=f"Quarter {i + 1}", font=("Anton", 55), bg="green", fg=colorFont)
        score_label = tk.Label(root, text="0 x 0", font=("Anton", 50), bg="green", fg=colorFont)
        quarter_label.place(relx=0.04 + i * 0.23, rely=0.675, relwidth=0.25, relheight=0.1)
        score_label.place(relx=0.04 + i * 0.23, rely=0.76, relwidth=0.25, relheight=0.07)
        quarter_score_labels.append((quarter_label, score_label))

    # Adicionar o label do quarter atual na janela principal
    labelCurrentQuarter = tk.Label(root, text=f"Quarter atual: {current_quarter_display}", font=("Anton", 70), bg="green", fg=colorFont)
    labelCurrentQuarter.place(relx=0.5, rely=0.55, relwidth=0.4, relheight=0.12, anchor="n")  # Posicionamento centralizado abaixo do placar

    # Labels para mostrar número de tempos de cada time
    labelwordfaltas1 = tk.Label(root, text=f"Faltas:", font=("Anton", 60), bg="brown", fg=colorFont)
    labelfaltas1 = tk.Label(root, text=f"{faltasTeam1}", font=("Anton", 60), bg="brown", fg=colorFont)
    labelwordfaltas2 = tk.Label(root, text=f"Faltas:", font=("Anton", 60), bg="brown", fg=colorFont)
    labelfaltas2 = tk.Label(root, text=f"{faltasTeam2}", font=("Anton", 60), bg="brown", fg=colorFont)

    # Posicionar os labels das substituições ao lado dos nomes das equipes
    labelwordfaltas1.place(relx=0.05, rely=0.85, relwidth=0.15, relheight=0.1, anchor="nw")
    labelfaltas1.place(relx=0.24, rely=0.85, relwidth=0.03, relheight=0.1, anchor="ne")
    labelwordfaltas2.place(relx=0.76, rely=0.85, relwidth=0.15, relheight=0.1, anchor="nw")
    labelfaltas2.place(relx=0.95, rely=0.85, relwidth=0.03, relheight=0.1, anchor="ne")

    # Funções para aumentar o placar e alternar o saque automaticamente
    def increaseTeam1():
        global scoreTeam1, scoreTeam1_control, serving_team
        scoreTeam1 += 1
        scoreTeam1_control +=1
        serving_team = 1  # Time 1 marcou ponto, logo passa a ser o time sacando
        update_score()
        #update_serve_icon()  # Atualiza a bolinha para o lado do time que marcou


    def increaseTeam1_by_2():
        global scoreTeam1, scoreTeam1_control, serving_team
        scoreTeam1 += 2
        scoreTeam1_control += 2
        serving_team = 1  # Time 1 marcou ponto, logo passa a ser o time sacando
        update_score()

    def increaseTeam1_by_3():
        global scoreTeam1, scoreTeam1_control, serving_team
        scoreTeam1 += 3
        scoreTeam1_control += 3
        serving_team = 1  # Time 1 marcou ponto, logo passa a ser o time sacando
        update_score()

    # Funções para aumentar pontos para o Time 2
    def increaseTeam2():
        global scoreTeam2, scoreTeam2_control, serving_team
        scoreTeam2 += 1
        scoreTeam2_control += 1
        serving_team = 2  # Time 2 marcou ponto, logo passa a ser o time sacando
        update_score()

    def increaseTeam2_by_2():
        global scoreTeam2, scoreTeam2_control, serving_team
        scoreTeam2 += 2
        scoreTeam2_control += 2
        serving_team = 2  # Time 2 marcou ponto, logo passa a ser o time sacando
        update_score()

    def increaseTeam2_by_3():
        global scoreTeam2, scoreTeam2_control, serving_team
        scoreTeam2 += 3
        scoreTeam2_control += 3
        serving_team = 2  # Time 2 marcou ponto, logo passa a ser o time sacando
        update_score()
    def decreaseTeam1():
        global scoreTeam1, scoreTeam1_control
        if scoreTeam1 > 0:
            scoreTeam1 -= 1
            scoreTeam1_control -=1
        update_score()

    def decreaseTeam2():
        global scoreTeam2,scoreTeam2_control
        if scoreTeam2 > 0:
            scoreTeam2 -= 1
            scoreTeam2_control -=1
        update_score()

    # Funções para aumentar/diminuir o número de quarters
    def increaseQuarter1():
        global quarterTeam1
        quarterTeam1 += 1
        update_score()

    def decreaseQuarter1():
        global quarterTeam1
        quarterTeam1 -= 1
        update_score()

    def increaseQuarter2():
        global quarterTeam2
        quarterTeam2 += 1
        update_score()

    def decreaseQuarter2():
        global quarterTeam2
        quarterTeam2 -= 1
        update_score()

    # Zerar os quarters (panic button)
    def reset_quarters():
        global quarterTeam1, quarterTeam2, scoreTeam1, scoreTeam2, current_quarter, current_quarter_display
        quarterTeam1 = 0
        quarterTeam2 = 0
        scoreTeam1 = 0
        scoreTeam2 = 0
        current_quarter = 0
        current_quarter_display = 1
        update_score()
        update_current_quarter_control_label()
        update_current_quarter_label()

    # Função para atualizar o cronômetro
    def update_timer():
        global time_seconds, time_milliseconds
        if timer_running:
            # Verifica se o tempo acabou
            if time_seconds == 0 and time_milliseconds == 0:
                stop_timer()  # O cronômetro terminou, parar de atualizar
                return
            
            # Decrementar os milissegundos a cada 100ms
            if time_milliseconds == 0:
                time_milliseconds = 9  # Agora o ciclo de milissegundos vai de 9 (não 99)
                if time_seconds > 0:
                    time_seconds -= 1
            else:
                time_milliseconds -= 1

            # Converter para minutos, segundos e milissegundos
            minutes, seconds = divmod(time_seconds, 60)
            time_formatted = f"{minutes:02d}:{seconds:02d}:{time_milliseconds:01d}"

            # Atualizar o cronômetro nas duas janelas
            timer_label.config(text=time_formatted)
            timer_label_control.config(text=time_formatted)

            # Atualizar a cada 100ms (milissegundos)
            root.after(100, update_timer)  # 100ms = 0.1 segundo
    # Função para iniciar o cronômetro
    def start_timer():
        global timer_running
        timer_running = not timer_running
        if timer_running:
            update_timer()
    # Função para parar o cronômetro
    def stop_timer():
        global timer_running
        timer_running = False
    # Função para reiniciar o cronômetro
    def reset_timer():
        global time_seconds, time_milliseconds
        time_seconds = 600  # 10 minutos
        time_milliseconds = 0
        timer_label.config(text="10:00:00")
        timer_label_control.config(text="10:00:00")
        stop_timer()

    def toggle_timer():
        global timer_running
        timer_running = not timer_running
        if timer_running:
            update_timer()

    label_equipe1_controlWindow = tk.Label(controlWindow,  bg=colorBackground)
    label_equipe1_controlWindow.place(relx=0.15, rely=0, relwidth=0.2, relheight=0.3, anchor="n")

    label_equipe2_controlWindow = tk.Label(controlWindow,  bg=colorBackground)
    label_equipe2_controlWindow.place(relx=0.85, rely=0, relwidth=0.2, relheight=0.3, anchor="n")

    # Botões para controle do placar
    buttonTeam1Up = tk.Button(controlWindow, text="1 +", font=("Montserrat SemiBold", 10), command=increaseTeam1)
    buttonTeam2Up = tk.Button(controlWindow, text="2 +", font=("Montserrat SemiBold", 10), command=increaseTeam2)
    buttonTeam1Down = tk.Button(controlWindow, text="1 -", font=("Montserrat SemiBold", 10), command=decreaseTeam1)
    buttonTeam2Down = tk.Button(controlWindow, text="2 -", font=("Montserrat SemiBold", 10), command=decreaseTeam2)

    # Botões para controle dos sets
    buttonSet1Up = tk.Button(controlWindow, text="+ Período Time 1", command=increaseQuarter1)
    buttonSet1Down = tk.Button(controlWindow, text="- Período Time 1", command=decreaseQuarter1)
    buttonSet2Up = tk.Button(controlWindow, text="+ Período Time 2", command=increaseQuarter2)
    buttonSet2Down = tk.Button(controlWindow, text="- Período Time 2", command=decreaseQuarter2)


    # Botões para controle de substituição
    buttonTime1Up = tk.Button(controlWindow, text="+ Falta 1", command=increasefaltasTeam1)
    buttonTime1Down = tk.Button(controlWindow, text="- Falta 1", command=decreasefaltasTeam1)
    buttonTime2Up = tk.Button(controlWindow, text="+ Falta 2", command=increasefaltasTeam2)
    buttonTime2Down = tk.Button(controlWindow, text="- Falta 2", command=decreasefaltasTeam2)

    buttonTeam1_by_2 = tk.Button(controlWindow, text="Time 1 +2", command=increaseTeam1_by_2, font=("Arial", 20))
    buttonTeam1_by_2.place(relx=0.1, rely=0.75, anchor="n")

    buttonTeam1_by_3 = tk.Button(controlWindow, text="Time 1 +3", command=increaseTeam1_by_3, font=("Arial", 20))
    buttonTeam1_by_3.place(relx=0.1, rely=0.8, anchor="n")

    buttonTeam2 = tk.Button(controlWindow, text="Time 2 +1", command=increaseTeam2, font=("Arial", 20))
    buttonTeam2.place(relx=0.9, rely=0.7, anchor="n")

    buttonTeam2_by_2 = tk.Button(controlWindow, text="Time 2 +2", command=increaseTeam2_by_2, font=("Arial", 20))
    buttonTeam2_by_2.place(relx=0.9, rely=0.75, anchor="n")

    buttonTeam2_by_3 = tk.Button(controlWindow, text="Time 2 +3", command=increaseTeam2_by_3, font=("Arial", 20))
    buttonTeam2_by_3.place(relx=0.9, rely=0.8, anchor="n")


    # Botão para atualizar os nomes das equipes
    buttonUpdateNames = tk.Button(controlWindow, text="Atualizar Nomes", font=("Montserrat SemiBold", 10), command=lambda: update_team_names())
    buttonUpdateNames.place(relx=0, rely=1, relwidth=0.2, relheight=0.05, anchor="sw")


    title_label = tk.Label(controlWindow, text="Período", font=("Arial", 25), bg="lightgray", fg="black")
    title_label.place(relx=0.5, rely=0.45, relwidth=0.4, relheight=0.05, anchor="n")  # Posiciona no topo centralizado

    labelCurrentQuarterControl = tk.Label(controlWindow, text=current_quarter_display, font=("Montserrat SemiBold", 40), bg="white", fg="black")
    labelCurrentQuarterControl.place(relx=0.5, rely=0.5, relwidth=0.2, relheight=0.1, anchor="n")  # Posiciona entre os botões de set
    
    # Botão para controlar QUARTERS
    buttonNextQuarter = tk.Button(controlWindow, text="Próximo \nPeríodo", font=("Montserrat SemiBold", 18), command=next_quarter)
    buttonPrevQuarter = tk.Button(controlWindow, text="Período \nAnterior", font=("Montserrat SemiBold", 18), command=prev_quarter)
    buttonResetQuarters = tk.Button(controlWindow, text="Zerar Períodos", font=("Montserrat SemiBold", 10), command=reset_quarters)
    
    # Posicionar o botão de avançar Quarter
    buttonNextQuarter.place(relx=0.6, rely=0.5, relwidth=0.1, relheight=0.15, anchor="nw")
    buttonPrevQuarter.place(relx=0.4, rely=0.5, relwidth=0.1, relheight=0.15, anchor="ne")
    buttonResetQuarters.place(relx=0.5, rely=0.6, relwidth=0.2, relheight=0.05, anchor="n")

    #Botão para selecionar imagem do time
    botao_equipe1 = tk.Button(controlWindow, text="Logo Equipe 1", font=("Montserrat SemiBold", 10), command=selecionar_equipe1)
    botao_equipe1.place(relx=0.15, rely=0.35, relwidth=0.2, relheight=0.05, anchor="n")

    botao_equipe2 = tk.Button(controlWindow, text="Logo Equipe 2", font=("Montserrat SemiBold", 10), command=selecionar_equipe2)
    botao_equipe2.place(relx=0.85, rely=0.35, relwidth=0.2, relheight=0.05, anchor="n")

    entryTeam1 = tk.Entry(controlWindow, font=("Arial", 15))
    entryTeam1.place(relx=0.15, rely=0.3, relwidth=0.2, relheight=0.05, anchor="n")

    entryTeam2 = tk.Entry(controlWindow, font=("Arial", 15))
    entryTeam2.place(relx=0.85, rely=0.3, relwidth=0.2, relheight=0.05, anchor="n")

    # SEÇÃO PARA DECLARAR E POSICIONAR CRONOMETRO E FUNCOES
    title_label = tk.Label(controlWindow, text="Cronômetro", font=("Arial", 25), bg="lightgray", fg="black")
    title_label.place(relx=0.5, rely=0, relwidth=0.4, relheight=0.05, anchor="n")  # Posiciona no topo centralizado
    # Label do cronômetro na janela de controle
    timer_label_control = tk.Label(controlWindow, text="10:00:00", font=("Montserrat SemiBold", 60), bg=colorBackground, fg=colorFont)
    timer_label_control.place(relx=0.5, rely=0.2, relwidth=0.2, relheight=0.15, anchor="n")
    # Criando botões de controle do cronômetro
    buttonStartTimer = tk.Button(controlWindow, text="Iniciar \nCronômetro", font=("Montserrat SemiBold", 18), command=start_timer)
    buttonStopTimer = tk.Button(controlWindow, text="Parar \nCronômetro", font=("Montserrat SemiBold", 18), command=stop_timer)
    buttonResetTimer = tk.Button(controlWindow, text="Reiniciar Cronômetro", font=("Montserrat SemiBold", 10), command=reset_timer)
    start_button = tk.Button(controlWindow, text="Iniciar/Pauser", command=start_timer, font=("Arial", 20))
    start_button.place(relx=0.5, rely=0.6, anchor="n")
    # Botão para parar o cronômetro
    stop_button = tk.Button(controlWindow, text="Parar", command=stop_timer, font=("Arial", 20))
    stop_button.place(relx=0.5, rely=0.7, anchor="n")
    # Botão para resetar o cronômetro
    reset_button = tk.Button(controlWindow, text="Resetar", command=reset_timer, font=("Arial", 20))
    reset_button.place(relx=0.5, rely=0.8, anchor="center")


    # Posicionar os botões do cronômetro
    buttonStartTimer.place(relx=0.6, rely=0.8, relwidth=0.1, relheight=0.15, anchor="nw")
    buttonStopTimer.place(relx=0.4, rely=0.8, relwidth=0.1, relheight=0.15, anchor="ne")
    
    buttonResetTimer.place(relx=0.5, rely=0.15, relwidth=0.2, relheight=0.05, anchor="n")
    #-----------------------------------#

    # Posicionar os botões do placar
    buttonTeam1Up.place(relx=0.15, rely=0.4, relwidth=0.1, relheight=0.05, anchor="nw")
    buttonTeam2Up.place(relx=0.85, rely=0.4, relwidth=0.1, relheight=0.05, anchor="nw")
    buttonTeam1Down.place(relx=0.15, rely=0.4, relwidth=0.1, relheight=0.05, anchor="ne")
    buttonTeam2Down.place(relx=0.85, rely=0.4, relwidth=0.1, relheight=0.05, anchor="ne")

    # Posicionar os botões dos sets
    buttonSet1Up.place(relx=0.15, rely=0.45, relwidth=0.1, relheight=0.05, anchor="nw")
    buttonSet2Up.place(relx=0.85, rely=0.45, relwidth=0.1, relheight=0.05, anchor="nw")
    buttonSet1Down.place(relx=0.15, rely=0.45, relwidth=0.1, relheight=0.05, anchor="ne")
    buttonSet2Down.place(relx=0.85, rely=0.45, relwidth=0.1, relheight=0.05, anchor="ne")

    # Posicionar os botões dos tempos
    buttonTime1Up.place(relx=0.15, rely=0.6, relwidth=0.1, relheight=0.05, anchor="nw")
    buttonTime2Up.place(relx=0.85, rely=0.6, relwidth=0.1, relheight=0.05, anchor="nw")
    buttonTime1Down.place(relx=0.15, rely=0.6, relwidth=0.1, relheight=0.05, anchor="ne")
    buttonTime2Down.place(relx=0.85, rely=0.6, relwidth=0.1, relheight=0.05, anchor="ne")

    separator1 = tk.Frame(controlWindow, bg="black", width=2)  # Defina a altura como 2 para uma linha fina
    separator1.place(relx=0.3, rely=0, relheight=0.8)
    separator2 = tk.Frame(controlWindow, bg="black", width=2)  # Defina a altura como 2 para uma linha fina
    separator2.place(relx=0.7, rely=0, relheight=0.8)
    separator3 = tk.Frame(controlWindow, bg="black", height=2)  # Defina a altura como 2 para uma linha fina
    separator3.place(relx=0, rely=0.8, relwidth=1)

        # Executar as duas janelas Tkinter
    root.mainloop()

# Chamar a função para abrir as janelas
open_windows_on_monitors()