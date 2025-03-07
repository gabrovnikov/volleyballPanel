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

team1_name = "TIME DA CASA"
team2_name = "TIME VISITANTE"

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
    canvas = tk.Canvas(root, width=1920, height=1080, bg="white")  # Criar o Canvas
    canvas.pack(fill="both", expand=True)  # Adicionar o Canvas à janela

    # Criar e configurar a segunda janela no monitor secundário
    controlWindow = tk.Toplevel(root)  # Usando Toplevel para manter a hierarquia
    configure_window_primary(controlWindow, primary_monitor)



# Atualizar o placar e os quarters
    def update_score():
        #labelScore_control.config(text= str(scoreTeam1_control)+" x "+ str(scoreTeam2_control))
        labelscore1Controlwindow.config(text=str(scoreTeam1))
        #labelscore2Controlwindow.config(text=str(scoreTeam1))
        canvas.itemconfig(canvasscoreTeam1, text=f"{scoreTeam1}")
        canvas.itemconfig(canvasfaltas1, text=str(faltasTeam1))
        canvas.itemconfig(canvasscoreTeam2, text=f"{scoreTeam2}")
        canvas.itemconfig(canvasfaltas2, text=str(faltasTeam2))

    # Funções para aumentar o número de faltas
    def increasefaltasTeam1():
        global faltasTeam1
        faltasTeam1 += 1
        update_score()
    def decreasefaltasTeam1():
        global faltasTeam1
        faltasTeam1 -= 1
        update_score()

    def increasefaltasTeam2():
        global faltasTeam2
        faltasTeam2 += 1
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
        update_current_quarter()  # Atualiza o label na janela principal
        
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
        update_current_quarter()  # Atualiza o label na janela principal

    # Função para atualizar o label do quarter atual
    def update_current_quarter():
        canvascurrentQuarter.config(text=f"Quarter atual: {current_quarter_display}")
    # Função para atualizar os nomes das equipes
    def update_team_names():
        global team1_name, team2_name
        team1_name = entryTeam1.get()  # Captura o nome da equipe 1
        canvas.itemconfig(canvasTeam1, text=str(team1_name))
        team2_name = entryTeam2.get()  # Captura o nome da equipe 2
        canvas.itemconfig(canvasTeam2, text=str(team2_name))

    #Função para selecionar imagem do time
    def selecionar_equipe1():
        global equipe1_tk_ref
        # Abre a janela do sistema para selecionar a imagem
        caminho_equipe1 = filedialog.askopenfilename(parent = controlWindow, initialdir="./Equipes",title="Selecione uma imagem",filetypes=[("Arquivos de Imagem", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if caminho_equipe1:  # Se um arquivo for selecionado
            # Carregar e exibir a imagem usando PIL
            equipe1 = Image.open(caminho_equipe1)
            equipe1 = equipe1.resize((800, 400))  # Redimensiona para ajustar ao Label
            equipe1_controlWindow = equipe1.resize((500, 250))  # Redimensiona para ajustar ao Label
            equipe1_tk_ref = ImageTk.PhotoImage(equipe1)
            equipe1_tk_controlWindow = ImageTk.PhotoImage(equipe1_controlWindow)
            canvas.create_image((secondary_monitor.width)/10, 385, image=equipe1_tk_ref, anchor=CENTER)
            label_equipe1_controlWindow.config(image=equipe1_tk_controlWindow)
            label_equipe1_controlWindow.image = equipe1_tk_controlWindow  # Manter a referência da imagem para não ser coletada pelo garbage collector         

    def selecionar_equipe2():
        global equipe2_tk_ref
        # Abre a janela do sistema para selecionar a imagem
        caminho_equipe2 = filedialog.askopenfilename(parent = controlWindow, initialdir="./Equipes", title="Selecione uma imagem", filetypes=[("Arquivos de Imagem", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
        if caminho_equipe2:  # Se um arquivo for selecionado
            # Carregar e exibir a imagem usando PIL
            equipe2 = Image.open(caminho_equipe2)
            equipe2 = equipe2.resize((800, 400))  # Redimensiona para ajustar ao Label
            equipe2_controlWindow = equipe2.resize((500, 250))  # Redimensiona para ajustar ao Label
            equipe2_tk_ref = ImageTk.PhotoImage(equipe2)
            equipe2_tk_controlWindow = ImageTk.PhotoImage(equipe2_controlWindow)
            canvas.create_image(9*(secondary_monitor.width)/10, 385, image=equipe2_tk_ref, anchor=CENTER)
            label_equipe2_controlWindow.config(image=equipe2_tk_controlWindow)
            label_equipe2_controlWindow.image = equipe2_tk_controlWindow  # Manter a referência da imagem para não ser coletada pelo garbage collector

    # Labels para exibir o placar de cada set
    quarter_score_labels = []
    for i in range(5):
        x_quarter_label = 0.36 + i * 0.55
        x_score_label = 0.36 + i * 0.55
        y_quarter_label = 1.5
        y_score_label = 1.67
        if i < 4:  # Apenas os 4 primeiros sets aparecem na tela
            quarter_label = canvas.create_text(x_quarter_label * 800, y_quarter_label * 600, text=f"QUARTER {i + 1}", font=("Anton", 60), fill=colorFont, anchor="center")
            score_label = canvas.create_text(x_score_label * 800, y_score_label * 600, text="0x0", font=("Anton", 55), fill=colorFont, anchor="center")
        else:
            quarter_label = None
            score_label = None
        quarter_score_labels.append((quarter_label, score_label))


    canvasTeam1 = canvas.create_text(18*(secondary_monitor.width)/100, 90, text=f"{team1_name}", font=("Anton", 55), fill=colorFont, anchor="center" )
    canvasscoreTeam1 = canvas.create_text(48*(secondary_monitor.width)/100, 37*(secondary_monitor.height)/100, text=f"{scoreTeam1}", font=("Anton", 200), fill=colorFont, anchor="e" )
    canvas.create_text(5*(secondary_monitor.width)/100, 70*(secondary_monitor.height)/100, text=f"FALTAS: ", font=("Anton", 60), fill=colorFont, anchor="w" )
    canvasfaltas1 = canvas.create_text(25*(secondary_monitor.width)/100, 70*(secondary_monitor.height)/100, text=f"{faltasTeam1}", font=("Anton", 60), fill=colorFont, anchor="w" )
    
    canvasCross = canvas.create_text(50*(secondary_monitor.width)/100, 39*(secondary_monitor.height)/100, text = "X", font=("Anton", 80), fill=colorFont, anchor="center")

    canvasTeam2 = canvas.create_text(82*(secondary_monitor.width)/100, 90, text=f"{team2_name}", font=("Anton", 55), fill=colorFont, anchor="center" )
    canvasscoreTeam2 = canvas.create_text(52*(secondary_monitor.width)/100, 37*(secondary_monitor.height)/100, text=f"{scoreTeam2}", font=("Anton", 200), fill=colorFont, anchor="w" )
    canvas.create_text(72*(secondary_monitor.width)/100, 70*(secondary_monitor.height)/100, text=f"FALTAS: ", font=("Anton", 60), fill=colorFont, anchor="w" )
    canvasfaltas2 = canvas.create_text(92*(secondary_monitor.width)/100, 70*(secondary_monitor.height)/100, text=f"{faltasTeam2}", font=("Anton", 60), fill=colorFont, anchor="w" )

    
    canvascurrentQuarter = canvas.create_text(50*(secondary_monitor.width)/100, 70*(secondary_monitor.height)/100, text=f"QUARTER ATUAL: {current_quarter_display}", font=("Anton", 60), fill=colorFont, anchor="center" )
    
# Labels do placar

    #Cronômetro
    timer_label = tk.Label(root, text="10:00:00", font=("Anton", 90), relief="solid", bg=colorBackground, fg=colorFont)
    timer_label.place(relx=0.5, rely=0, relwidth=0.28, relheight=0.15, anchor="n")

    #Separadores
    separator_inferior_timer = tk.Frame(root, bg="black", height=4)  # Defina a altura como 2 para uma linha fina
    separator_inferior_timer.place(relx=0, rely=0.15, relwidth=4)

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
        update_current_quarter()

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
    def atualizar_timer():
        global newTime
        newTime = entryTimer.get()
        timer_label.config(text=f"{newTime}")
        
    def update_team_names():
        global team1_name, team2_name
        team1_name = entryTeam1.get()  # Captura o nome da equipe 1
        canvas.itemconfig(canvasTeam1, text=str(team1_name))
        team2_name = entryTeam2.get()  # Captura o nome da equipe 2
        canvas.itemconfig(canvasTeam2, text=str(team2_name))

    label_equipe1_controlWindow = tk.Label(controlWindow,  bg=colorBackground)
    label_equipe1_controlWindow.place(relx=0.15, rely=0.05, relwidth=0.3, relheight=0.3, anchor="n")

    label_equipe2_controlWindow = tk.Label(controlWindow,  bg=colorBackground)
    label_equipe2_controlWindow.place(relx=0.85, rely=0.05, relwidth=0.3, relheight=0.3, anchor="n")

    labelscore1Controlwindow=tk.Label(controlWindow, text=scoreTeam1_control, font=("Anton", 70), bg=colorBackground, fg=colorFont)

    # Botões para controle do placar
    buttonTeam1Up = tk.Button(controlWindow, text="+1", font=("Montserrat Bold", 10), command=increaseTeam1)
    buttonTeam1_by_2 = tk.Button(controlWindow, text="+2", font=("Montserrat Bold", 10), command=increaseTeam1_by_2)
    buttonTeam1_by_3 = tk.Button(controlWindow, text="+3", font=("Montserrat Bold", 10), command=increaseTeam1_by_3)
    buttonTeam1Down = tk.Button(controlWindow, text="-", font=("Montserrat Bold", 10), command=decreaseTeam1)


    buttonTeam2Up = tk.Button(controlWindow, text="+1", font=("Montserrat Bold", 10), command=increaseTeam2)
    buttonTeam2_by_2 = tk.Button(controlWindow, text="+2", font=("Montserrat Bold", 10), command=increaseTeam2_by_2)
    buttonTeam2_by_3 = tk.Button(controlWindow, text="+3", font=("Montserrat Bold", 10), command=increaseTeam2_by_3)
    buttonTeam2Down = tk.Button(controlWindow, text="-", font=("Montserrat Bold", 10), command=decreaseTeam2)

    # Botões para controle dos sets
    buttonQuarter1Up = tk.Button(controlWindow, text="+ Período Time 1", command=increaseQuarter1)
    buttonQuarter1Down = tk.Button(controlWindow, text="- Período Time 1", command=decreaseQuarter1)
    buttonQuarter2Up = tk.Button(controlWindow, text="+ Período Time 2", command=increaseQuarter2)
    buttonQuarter2Down = tk.Button(controlWindow, text="- Período Time 2", command=decreaseQuarter2)

    # Botões para controle de substituição
    buttonFalta1Up = tk.Button(controlWindow, text="+", command=increasefaltasTeam1)
    buttonFalta1Down = tk.Button(controlWindow, text="-", command=decreasefaltasTeam1)
    buttonFalta2Up = tk.Button(controlWindow, text="+", command=increasefaltasTeam2)
    buttonFalta2Down = tk.Button(controlWindow, text="-", command=decreasefaltasTeam2)




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
    botao_equipe1.place(relx=0.15, rely=0, relwidth=0.3, relheight=0.05, anchor="n")

    botao_equipe2 = tk.Button(controlWindow, text="Logo Equipe 2", font=("Montserrat SemiBold", 10), command=selecionar_equipe2)
    botao_equipe2.place(relx=0.85, rely=0, relwidth=0.3, relheight=0.05, anchor="n")

    entryTeam1 = tk.Entry(controlWindow, font=("Arial", 15), bg="orange")
    entryTeam1.place(relx=0.15, rely=0.35, relwidth=0.3, relheight=0.05, anchor="n")

    entryTeam2 = tk.Entry(controlWindow, font=("Arial", 15), bg="orange")
    entryTeam2.place(relx=0.85, rely=0.35, relwidth=0.3, relheight=0.05, anchor="n")

    # SEÇÃO PARA DECLARAR E POSICIONAR CRONOMETRO E FUNCOES
    title_label = tk.Label(controlWindow, text="Cronômetro", font=("Arial", 25), bg="lightgray", fg="black")
    title_label.place(relx=0.5, rely=0, relwidth=0.4, relheight=0.05, anchor="n")  # Posiciona no topo centralizado
    # Label do cronômetro na janela de controle
    timer_label_control = tk.Label(controlWindow, text="10:00:00", font=("Montserrat SemiBold", 50), bg=colorBackground, fg=colorFont)
    timer_label_control.place(relx=0.5, rely=0.05, relwidth=0.2, relheight=0.1, anchor="n")

    entryTimer=tk.Entry(controlWindow, font=("Arial", 15))
    entryTimer.place(relx=0.5, rely=0.15, relwidth=0.2, relheight=0.1, anchor="n")
    entryTimerButton=tk.Button(controlWindow, text="Atualizar Timer", font=("Arial", 15), command=atualizar_timer)
    entryTimerButton.place(relx=0.5, rely=0.25, relwidth=0.2, relheight=0.05, anchor="n")
    # Criando botões de controle do cronômetro
    buttonStartTimer = tk.Button(controlWindow, text="Iniciar \nCronômetro", font=("Montserrat SemiBold", 20), command=start_timer)
    #buttonStopTimer = tk.Button(controlWindow, text="Parar \nCronômetro", font=("Montserrat SemiBold", 20), command=stop_timer)
    buttonResetTimer = tk.Button(controlWindow, text="Reiniciar\nCronômetro", font=("Montserrat SemiBold", 20), command=reset_timer)
    #start_button = tk.Button(controlWindow, text="Play\nPause", command=start_timer, font=("Montserrat SemiBold", 20))
    #start_button.place(relx=0.65, rely=0.05, relwidth=0.1, relheight=0.1, anchor="n")
    # Botão para parar o cronômetro
    #stop_button = tk.Button(controlWindow, text="Parar", command=stop_timer, font=("Montserrat SemiBold", 20))
    #stop_button.place(relx=0.5, rely=0.7, anchor="n")
    # Botão para resetar o cronômetro

    # Posicionar os botões do cronômetro
    buttonStartTimer.place(relx=0.65, rely=0.05, relwidth=0.1, relheight=0.1, anchor="n")
    #buttonStopTimer.place(relx=0.4, rely=0.8, relwidth=0.1, relheight=0.15, anchor="ne")

    buttonResetTimer.place(relx=0.35, rely=0.05, relwidth=0.1, relheight=0.1, anchor="n")
    #-----------------------------------#

    # Posicionar os botões do placar

    buttonTeam1Up.place(relx=0.3, rely=0.4, relwidth=0.05, relheight=0.05, anchor="ne")
    buttonTeam1_by_2.place(relx=0.3, rely=0.45, relwidth=0.05, relheight=0.05, anchor="ne")
    buttonTeam1_by_3.place(relx=0.3, rely=0.5, relwidth=0.05, relheight=0.05, anchor="ne")
    buttonTeam1Down.place(relx=0, rely=0.4, relwidth=0.05, relheight=0.15, anchor="nw")
    labelscore1Controlwindow.place(relx=0.15, rely=0.4, relwidth=0.2, relheight=0.15, anchor="n")


    buttonTeam2Up.place(relx=1, rely=0.4, relwidth=0.05, relheight=0.05, anchor="ne")
    buttonTeam2_by_2.place(relx=1, rely=0.45, relwidth=0.05, relheight=0.05, anchor="ne")
    buttonTeam2_by_3.place(relx=1, rely=0.5, relwidth=0.05, relheight=0.05, anchor="ne")
    buttonTeam2Down.place(relx=0.7, rely=0.4, relwidth=0.05, relheight=0.15, anchor="nw")

    # Posicionar os botões dos sets
    #buttonQuarter1Up.place(relx=0.15, rely=0.45, relwidth=0.1, relheight=0.05, anchor="nw")
    #buttonQuarter2Up.place(relx=0.85, rely=0.45, relwidth=0.1, relheight=0.05, anchor="nw")
    #buttonQuarter1Down.place(relx=0.15, rely=0.45, relwidth=0.1, relheight=0.05, anchor="ne")
    #buttonQuarter2Down.place(relx=0.85, rely=0.45, relwidth=0.1, relheight=0.05, anchor="ne")

    # Posicionar os botões dos tempos
    buttonFalta1Up.place(relx=0.3, rely=0.55, relwidth=0.05, relheight=0.05, anchor="ne")
    buttonFalta2Up.place(relx=1, rely=0.55, relwidth=0.05, relheight=0.05, anchor="ne")
    buttonFalta1Down.place(relx=0, rely=0.55, relwidth=0.05, relheight=0.05, anchor="nw")
    buttonFalta2Down.place(relx=0.7, rely=0.55, relwidth=0.05, relheight=0.05, anchor="nw")

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
