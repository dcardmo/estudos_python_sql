import os
from tkinter import Tk, filedialog, Label, Button, StringVar
from moviepy.video.io.VideoFileClip import VideoFileClip

def dividir_video_com_intervalos(arquivo_entrada, intervalos, pasta_destino, status_label,root):
    """
    Divide um vídeo em partes com base em intervalos personalizados.

    :param arquivo_entrada: Caminho do arquivo de vídeo original.
    :param intervalos: Lista de tuplas contendo os tempos de início e fim para cada parte (em segundos).
    """
    try:
        # Carrega o vídeo
        video = VideoFileClip(arquivo_entrada)
        # Verifica a duração do vídeo
        if video.duration is None:
            raise ValueError("Não foi possível obter a duração do vídeo. Verifique o arquivo.")
        print(f"Duração total do vídeo: {video.duration:.2f} segundos")

        status_label.set(f"Duração do vídeo: {video.duration:.2f} segundos")
        root.update_idletasks()
        for i, (inicio, fim) in enumerate(intervalos):
            # Valida e ajusta os intervalos
            if fim is None:
                fim = video.duration
            if inicio < 0 or fim > video.duration or inicio >= fim:
                status_label.set(f"Intervalo inválido na posição {i+1}: início={inicio}, fim={fim}. Ignorando...")
                root.update_idletasks()
                continue

            # Divide o vídeo com base no intervalo
            trecho = video.subclip(inicio, fim)

            # Define o nome do arquivo de saída
            nome_arquivo = f"trecho_{i+1}.mp4"
            caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)
            status_label.set(f"Processando: Trecho {i+1} ({inicio}s a {fim}s)        ")
            root.update_idletasks()

            # Adiciona o callback para o progresso
            trecho.write_videofile(
                caminho_arquivo,
                codec="libx264",
                audio_codec="aac"                
            )
            
            status_label.set(f"Trecho {i+1} salvo como '{caminho_arquivo}'")
            root.update_idletasks()

        status_label.set("Divisão concluída!")
        root.update_idletasks()
        video.close()
    except Exception as e:
        status_label.set(f"Erro inesperado ao processar o vídeo: {e}")
        root.update_idletasks()

# Funções para selecionar arquivos e pastas
def selecionar_arquivo_video():
    return filedialog.askopenfilename(
        title="Selecione o arquivo de vídeo",
        filetypes=[("Arquivos de vídeo", "*.mp4 *.avi *.mkv")]
    )

def selecionar_pasta_destino():
    return filedialog.askdirectory(title="Selecione a pasta de destino dos trechos")

# Função para abrir a pasta de destino
def abrir_pasta_destino(pasta_destino, status_label):
    if pasta_destino:
        try:
            os.startfile(pasta_destino)  # No Windows
            status_label.set(f"Abrindo pasta: {pasta_destino}")
        except Exception as e:
            status_label.set(f"Erro ao abrir a pasta: {e}")
    else:
        status_label.set("Erro: Nenhuma pasta de destino foi selecionada!")

# Função principal para a interface gráfica
def criar_interface():
    # Janela principal
    root = Tk()
    root.title("Video Slice")
    root.geometry("600x350")

    # Variáveis para armazenar os caminhos
    arquivo_video = StringVar()
    pasta_destino = StringVar()
    status_label = StringVar()

    # Função para atualizar os caminhos
    def selecionar_video():
        caminho = selecionar_arquivo_video()
        if caminho:
            arquivo_video.set(caminho)
            status_label.set(f"Vídeo selecionado: {os.path.basename(caminho)}")
            root.update_idletasks()

    def selecionar_destino():
        caminho = selecionar_pasta_destino()
        if caminho:
            pasta_destino.set(caminho)
            status_label.set(f"Pasta de destino: {caminho}")
            root.update_idletasks()

    def executar_divisao():
        if not arquivo_video.get():
            status_label.set("Erro: Nenhum vídeo selecionado!")
            root.update_idletasks()
            return
        if not pasta_destino.get():
            status_label.set("Erro: Nenhuma pasta de destino selecionada!")
            root.update_idletasks()
            return

        # Intervalos personalizados (em segundos)
        intervalos = [
            (0, 60),   # Primeiro trecho: de 0 a 60 segundos
            #(70, None), # Segundo trecho: de 70 a 150 segundos
        ]

        # Chama a função de divisão
        status_label.set("Processando...")
        root.update_idletasks()
        dividir_video_com_intervalos(arquivo_video.get(), intervalos, pasta_destino.get(), status_label, root)

    # Botões e etiquetas na interface
    Label(root, text="Divisor de Vídeos", font=("Helvetica", 16)).pack(pady=10)

    Button(root, text="Selecionar Vídeo a ser Dividido", command=selecionar_video).pack(pady=5)
    Label(root, textvariable=arquivo_video, wraplength=400, fg="blue").pack()

    Button(root, text="Selecionar Pasta de Destino dos Trechos do Vídeo", command=selecionar_destino).pack(pady=5)
    Label(root, textvariable=pasta_destino, wraplength=400, fg="blue").pack()

    Button(root, text="Dividir Vídeo", command=executar_divisao).pack(pady=20)
    Label(root, text="Status:", font=("Helvetica", 12)).pack(pady=5)
    Label(root, textvariable=status_label, wraplength=400, fg="green").pack()
    
    Button(root, text="Abrir Pasta com os Trechos do Vídeo", command=lambda: abrir_pasta_destino(pasta_destino.get(), status_label)).pack(pady=10)
 

    # Inicia a interface
    root.mainloop()

# Executa a interface gráfica
if __name__ == "__main__":
    criar_interface()