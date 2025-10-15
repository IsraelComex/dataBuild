import time
import tkinter as tk
from tkinter import simpledialog, messagebox
from datetime import datetime

def delay(time_in_seconds):
    time.sleep(time_in_seconds)
# Função para solicitar a data de expiração em uma janela
print("Iniciando...")
def solicitar_data_limite():
    root = tk.Tk()
    root.geometry("800x600")
    root.withdraw()  # Esconder a janela principal
    data_limite= simpledialog.askstring("New Date", "Informe a data início de vigência (dd/mm/yyyy):")
    root.destroy()  # Fechar a janela após a entrada
    return data_limite

def validar_data(data_str):
    """Valida o formato da data e retorna um objeto datetime."""
    try:
        data_str = data_str.strip()
        print(f"Data recebida: '{data_str}'")
        data = datetime.strptime(data_str, "%d/%m/%Y")
        return data
    except ValueError:
        return None
    
def obter_data_limite():
    """Função para solicitar e validar a data limite do usuário."""
    data_limite_str = solicitar_data_limite()

    if data_limite_str is None:
        messagebox.showinfo("Entrada Cancelada", "A entrada de data foi cancelada.")
        return None  # Retorna None se a entrada foi cancelada

    # Validar a data informada
    data_limite = validar_data(data_limite_str)

    if data_limite is None:
        messagebox.showerror("Erro", "Formato de data inválido. Por favor, use o formato dd/mm/yyyy.")
        return None  # Retorna None se a data for inválida

    return data_limite

def abrir_gmail(destinatarios, assunto, corpo, copia):
    
    import urllib.parse
    # Constrói a URL do Gmail com os parâmetros
    base_url = "https://mail.google.com/mail/u/0/?view=cm&fs=1&tf=1"
    
    params = {
        "to": ",".join(destinatarios),  # Lista de destinatários
        "cc": ",".join(copia),         # Lista de cópias
        "su": assunto,  # Codifica o assunto corretamente
        "body": corpo                  # Corpo do e-mail
    }
    
    # Codifica os parâmetros para serem usados na URL
    url_completa = f"{base_url}&{urllib.parse.urlencode(params)}"
    import webbrowser
    # Abre a URL no navegador padrão
    webbrowser.open(url_completa)

