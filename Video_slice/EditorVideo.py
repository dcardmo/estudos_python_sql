#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
from tkinter import Tk, filedialog, Label, Button, StringVar, IntVar, Entry, Frame
from tkinter.messagebox import showerror, showinfo
from moviepy.video.io.VideoFileClip import VideoFileClip


# In[ ]:


def dividir_video_com_intervalos(arquivo_entrada, intervalos, pasta_destino, status_label, root):
    """Divide um vídeo em partes com base em intervalos personalizados."""
    try:
        video = VideoFileClip(arquivo_entrada)
        if video.duration is None:
            raise ValueError("Não foi possível obter a duração do vídeo. Verifique o arquivo.")
        status_label.set(f"Duração do vídeo: {video.duration:.2f} segundos")
        root.update_idletasks()

        for i, (inicio, fim) in enumerate(intervalos):
            if inicio < 0 or fim > video.duration or inicio >= fim:
                raise ValueError(f"Intervalo inválido: ({inicio}, {fim}).")
            
            trecho = video.subclip(inicio, fim)
            nome_saida = os.path.join(pasta_destino, f"trecho_{i + 1}.mp4")
            trecho.write_videofile(nome_saida, codec="libx264")
            status_label.set(f"Trecho {i + 1} salvo como: {nome_saida}")
            root.update_idletasks()

        video.close()
        status_label.set("Divisão concluída!")
        showinfo("Sucesso", "Vídeo dividido com sucesso!")

    except Exception as e:
        showerror("Erro", f"Ocorreu um erro: {e}")


# In[ ]:


def converter_tempo_para_segundos(tempo):
    """    Converte uma string no formato hh:mm:ss para o total em segundos.    
    :param tempo: Tempo no formato hh:mm:ss
    :return: Tempo em segundos (int)
    """
    try:
        partes = tempo.split(":")
        if len(partes) == 3:  # hh:mm:ss
            horas, minutos, segundos = map(int, partes)
        elif len(partes) == 2:  # mm:ss
            horas = 0
            minutos, segundos = map(int, partes)
        else:  # ss
            horas = 0
            minutos = 0
            segundos = int(partes[0])
        return horas * 3600 + minutos * 60 + segundos
    except ValueError:
        raise ValueError(f"Formato de tempo inválido: {tempo}. Use hh:mm:ss, mm:ss ou ss.")


# In[ ]:


def selecionar_arquivo(entry):
    """Permite ao usuário selecionar um arquivo de vídeo."""
    arquivo = filedialog.askopenfilename(filetypes=[("Arquivos de vídeo", "*.mp4;*.avi;*.mkv")])
    if arquivo:
        entry.set(arquivo)


# In[ ]:


def selecionar_pasta(entry):
    """Permite ao usuário selecionar uma pasta para salvar os vídeos."""
    pasta = filedialog.askdirectory()
    if pasta:
        entry.set(pasta)


# In[ ]:


def adicionar_campos_intervalos(frame, num_trechos, intervalos):
    """Adiciona dinamicamente campos de entrada para intervalos."""
    for widget in frame.winfo_children():
        widget.destroy()
    
    for i in range(num_trechos.get()):
        Label(frame, text=f"Trecho {i + 1} - Início (hh:mm:ss):").grid(row=i, column=0, padx=5, pady=2)
        inicio = Entry(frame, width=10)
        inicio.grid(row=i, column=1, padx=5, pady=2)

        Label(frame, text="Fim (hh:mm:ss):").grid(row=i, column=2, padx=5, pady=2)
        fim = Entry(frame, width=10)
        fim.grid(row=i, column=3, padx=5, pady=2)

        intervalos.append((inicio, fim))


# In[ ]:


def obter_intervalos(intervalos):
    """    Coleta os valores inseridos nos campos de intervalo e converte para segundos.    
    :param intervalos: Lista de tuplas de Entry para início e fim
    :return: Lista de intervalos em segundos
    """
    valores = []
    for inicio, fim in intervalos:
        try:
            inicio_segundos = converter_tempo_para_segundos(inicio.get())
            fim_segundos = converter_tempo_para_segundos(fim.get())
            valores.append((inicio_segundos, fim_segundos))
        except ValueError as e:
            raise ValueError(f"Erro no intervalo: {e}")
    return valores


# In[ ]:


def iniciar_divisao(entry_video, entry_pasta, intervalos, status_label, root):
    """Inicia o processo de divisão do vídeo."""
    arquivo = entry_video.get()
    pasta = entry_pasta.get()
    
    if not arquivo or not os.path.exists(arquivo):
        showerror("Erro", "Por favor, selecione um arquivo de vídeo válido.")
        return
    
    if not pasta or not os.path.isdir(pasta):
        showerror("Erro", "Por favor, selecione uma pasta válida.")
        return
    
    try:
        intervalos_valores = obter_intervalos(intervalos)
        dividir_video_com_intervalos(arquivo, intervalos_valores, pasta, status_label, root)
    except Exception as e:
        showerror("Erro", f"Ocorreu um erro ao processar os intervalos: {e}")


# In[ ]:


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


# In[ ]:


# Função principal para a interface gráfica
def main():
    root = Tk()
    root.title("Divisor de Vídeos")

    entry_video = StringVar()
    entry_pasta = StringVar()
    num_trechos = IntVar(value=1)
    intervalos = []
    status_label = StringVar(value="Selecione um arquivo de vídeo e configure os intervalos.")

    # Seção de seleção de arquivo
    Label(
        root,
        text="Arquivo de vídeo:").grid(row=0, column=0, padx=5, pady=5)
    Button(
        root,
        text="Selecionar",
        command=lambda: selecionar_arquivo(entry_video)
    ).grid(row=0, column=2, padx=5, pady=5)
    Label(
        root,
        textvariable=entry_video, width=50, anchor="w").grid(row=0, column=1, padx=5, pady=5)

    # Seção de seleção de pasta de destino
    Label(
        root,
        text="Pasta de destino:").grid(row=1, column=0, padx=5, pady=5)
    Button(
        root,
        text="Selecionar",
        command=lambda: selecionar_pasta(entry_pasta)
    ).grid(row=1, column=2, padx=5, pady=5)
    Label(
        root,
        textvariable=entry_pasta,
        width=50, anchor="w").grid(row=1, column=1, padx=5, pady=5)

    # Seção de configuração de trechos
    Label(
        root,
        text="Número de trechos:").grid(row=2, column=0, padx=5, pady=5)
    Entry(
        root,
        textvariable=num_trechos,
        width=5).grid(row=2, column=1, padx=5, pady=5, sticky="w")

    intervalos_frame = Frame(root)
    intervalos_frame.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="w")
    Button(
        root,
        text="Configurar trechos",
        command=lambda: adicionar_campos_intervalos(intervalos_frame, num_trechos, intervalos)
    ).grid(row=2, column=2, padx=5, pady=5)

    
    # Botão para iniciar a divisão
    Button(
        root,
        text="Dividir Vídeo",
        command=lambda: iniciar_divisao(entry_video, entry_pasta, intervalos, status_label, root)
    ).grid(row=4, column=0, columnspan=2, pady=10)


    # Botão para abrir pasta de arquivos com os trechos
    Button(
        root,
        text="Abrir Pasta",
        command=lambda: abrir_pasta_destino(entry_pasta.get(), status_label)
    ).grid(row=4, column=2, pady=10)
    
    # Status
    Label(root, textvariable=status_label, fg="blue").grid(row=5, column=0, columnspan=3, padx=5, pady=5)

    # Inicia a interface
    root.mainloop()


# In[ ]:


# Executa a interface gráfica
if __name__ == "__main__":
    main()


# In[ ]:




