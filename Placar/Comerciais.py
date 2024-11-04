import tkinter as tk
import os
import subprocess
from screeninfo import get_monitors

def play_all_videos():
    # Caminho para o diretório onde os arquivos de vídeo estão
    directory = r"C:\Users\Vinic\OneDrive\Documentos\Placar\Patrocinadores"  # Substitua com o caminho do seu diretório de vídeos
    
    # Lista todos os arquivos no diretório com as extensões de vídeo
    video_files = [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(('.mp4', '.avi', '.mkv'))]
    
    # Verifica se há vídeos na pasta
    if not video_files:
        print("Nenhum vídeo encontrado no diretório.")
        return
    
    # Tenta obter informações do segundo monitor
    monitors = get_monitors()
    if len(monitors) < 2:
        print("Monitor secundário não encontrado.")
        return
    
    # Obtenha as coordenadas do monitor secundário
    secondary_monitor = monitors[1]
    secondary_x = secondary_monitor.x
    secondary_y = secondary_monitor.y

    # Usa o VLC para reproduzir todos os vídeos no monitor secundário em fullscreen
    try:
        subprocess.Popen([
            'vlc', '--fullscreen', '--no-embedded-video', '--playlist-autostart',
            '--play-and-exit', f'--video-x={secondary_x}', f'--video-y={secondary_y}'
        ] + video_files)
    except FileNotFoundError:
        print("VLC não encontrado. Certifique-se de que o VLC está instalado e no PATH do sistema.")

# Configuração da janela Tkinter
root = tk.Tk()
root.title("Reprodutor de Vídeos")
root.geometry("300x200")

# Botão para iniciar a reprodução
play_button = tk.Button(root, text="Reproduzir Todos os Vídeos", command=play_all_videos)
play_button.pack(pady=20)

root.mainloop()
