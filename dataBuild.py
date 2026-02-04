from tkinter import Tk, simpledialog, messagebox, Label
from tkinter.filedialog import askopenfilename
from numpy import False_
from utils import obter_data_limite, abrir_gmail
from excel_process import processar_arquivo_excel, salvar_arquivo_excel, limpar_pasta_csv
from otm_process_new import processar_registros_ntrbr_otm_completo
from playwright.sync_api import sync_playwright
import csv_writer as csv_writer
import time
import pandas as pd
import os
from tabulate import tabulate
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import webbrowser


def selecionar_arquivo():
    root = Tk()
    root.withdraw()
    
    arquivo_selecionado = askopenfilename(
        title="Escolha o arquivo Excel",
        filetypes=[("Excel files", "*.xlsx *.xls")],
        initialdir=r'C:\Temp\Cadastro de Tabela'
    )

    root.destroy()

    if not arquivo_selecionado:
        print("Nenhum arquivo foi selecionado.")
        return None

    print(f"Arquivo selecionado: {arquivo_selecionado}")
    return arquivo_selecionado


def main():
    # print('A T E N Ç Ã O: *** ESTE É UM AMBIENTE HML DE TESTE ***')    
    data_limite = None
    caminho_arquivo_excel = None
    
    def submenu(etapa, funcao):
        def processar_opcao():
            if opcao == "1":
                funcao()
            elif opcao == "2":
                print(f"Retornando ao menu principal da Etapa {etapa}.")
            else:
                messagebox.showerror("Erro", "Opção inválida! Tente novamente.")
                submenu(etapa, funcao)

        root = Tk()
        root.withdraw()
        opcao = simpledialog.askstring(
            f"Submenu Etapa {etapa}",
            f"Escolha uma opção:\n\n"
            f"1 - Iniciar a Etapa {etapa}.\n\n"
            f"2 - Voltar ao menu principal.\n\n"
            f"Digite o número da opção desejada:"
        )
        root.destroy()

        if opcao:
            processar_opcao()

    registros = None
    
    def etapa2():
        nonlocal data_limite, registros, caminho_arquivo_excel
        
        print("\nExecutando Etapa 2: Processar o Excel e salvar arquivos...")
        print('------------------------------------------------------------------------------------')
        if not caminho_arquivo_excel:
            caminho_arquivo_excel = selecionar_arquivo()
            if not caminho_arquivo_excel:
                print("Operação cancelada. Nenhum arquivo selecionado.")
                return
        
        if not data_limite:  # Solicita a data apenas se ainda não foi dn,efinida
            data_limite = obter_data_limite()
            
        print("\nRealizando tratamento...")
        print('------------------------------------------------------------------------------------')
        
        # folder_path = r'C:\Temp\Cadastro de Tabela' 
        print()
        print("Criando csv para upload...")
        df, registros = processar_arquivo_excel(caminho_arquivo_excel)
        limpar_pasta_csv()
        print('------------------------------------------------------------------------------------')
        # print(df)
        if df is None or registros is None:
            print("Falha ao processar o arquivo Excel. Retornando ao menu inicial.")
            return
        time.sleep(1)
        for i in range(1, 23):
            method_name = f"create_csv_0{i:02}"
            getattr(csv_writer, method_name)(df)
            # csv_writer.create_csv_00X(df, i)
        # csv_writer.create_csv_001(df)
 
        
        salvar_arquivo_excel(df)
        print("Processamento do arquivo concluído!")
        print()
        retornar_menu()


    def etapa3():
        nonlocal data_limite, registros
        print("\nExecutando Etapa 3: Processar registros NTR/BR OTM PRD...")
        print('------------------------------------------------------------------------------------')
        if not data_limite:
            data_limite = obter_data_limite()
        # folder_path = r'C:\Temp\Cadastro de Tabela'
        # _, registros = processar_arquivo_excel(folder_path)
        
        if registros is None:
            print("Registros não encontrados. Por favor, processe a Etapa 1 primeiro.")
            return
    
        with sync_playwright() as p:
            browser = p.chromium.launch(
                channel="chrome", # Especifica explicitamente o uso do Chrome
                headless=True
            )
            page = browser.new_page()
            processar_registros_ntrbr_otm_completo(page, registros, data_limite, retornar_menu, mostrar_menu)
            browser.close()
        # print("vencimento dos prazos concluído!")
        retornar_menu()

    def enviar_email():
        print("Não é permitido enviar e-mail no aplicativo teste...")
        print("\nPreparando para enviar um e-mail...")
        print('------------------------------------------------------------------------------------')
        
           
        # Defina os destinatários, assunto e corpo do e-mail
        destinatarios = ["cpslatam@natura.net", "widson.oliveira@natura.net", 
                         "centraldetrafego@natura.net", "ALEXPEREIRA@natura.net", 
                         "Danielepoiani@natura.net"
        ]
        copia = ["marciosousa@natura.net", "israel.nascimento@natura.net"]
        assunto = "Nova Tabela Frete Cadastrada no OTM"
        
        # Inicializa a variável `conteudo` com uma mensagem padrão
        conteudo = "Erro ao processar o conteúdo da tabela. Verifique os dados e tente novamente."
    
        # Adicionar conteúdo do arquivo processado ao corpo
        try:
            folder_path = r'C:\Temp\Cadastro de Tabela'
        
            # Processar o Excel para obter o DataFrame
            df, registros = processar_arquivo_excel(folder_path)
            
            
            if df is None or registros is None:
                raise ValueError("Arquivo Excel não processado corretamente.")

            # Seleciona apenas as colunas desejadas 
            colunas_desejadas = ['COD_TRANSPORTADORA', 'NOME_TRANSPORTADORA', 'TIPO_DE_TARIFA', 'DESCRICAO_ZONA_DE_TRANSPORTE_ORIGEM', 'DESCRICAO_ZONA_DE_TRANSPORTE_DESTINO', 
                                 'DESCRICAO_GRUPO_DE_EQUIPAMENTO', 'CUSTO_BASE / CUSTO_VARIAVEL']
            df_selecionado = df[colunas_desejadas]  # Filtra as colunas escolhidas
            
            # Renomeia as colunas
            df_selecionado = df_selecionado.rename(columns={
                'COD_TRANSPORTADORA': 'Cód Transp',
                'NOME_TRANSPORTADORA': 'Nome Transp',
                'TIPO_DE_TARIFA': 'Tipo Tarifa',
                'DESCRICAO_ZONA_DE_TRANSPORTE_ORIGEM': 'Origem',
                'DESCRICAO_ZONA_DE_TRANSPORTE_DESTINO': 'Destino',
                'DESCRICAO_GRUPO_DE_EQUIPAMENTO': 'Equipamento',
                'CUSTO_BASE / CUSTO_VARIAVEL': 'Valor Frete'
                # 'DATA_INICIO_VIGENCIA': 'Data Início',
                # 'DATA_EXPIRACAO_VIGENCIA': 'Data Vencimento'
            })
       
            # Formata a coluna 'Data Início' para DD/MM/YYYY
            # df_selecionado['Data Início'] = pd.to_datetime(df_selecionado['Data Início'], errors='coerce').dt.strftime('%d/%m/%Y')
            df_selecionado['Cód Transp'] = df_selecionado['Cód Transp'].astype(str)
  
            # Filtra os 5 primeiros registros
            df_top5 = df_selecionado.head(5)
            print(df_top5)    
            # print("ok") 
            # Total de linhas na tabela
            total_linhas = len(df_selecionado)
            df_top5 = tabulate(df_top5, headers='keys', tablefmt='plain',
                                   stralign='left', numalign='left', showindex=False)
            # Gera o conteúdo da tabela formatada
            # conteudo = tabulate(df_top5, headers='keys', tablefmt='grid', numalign="center", stralign="center", showindex=False)
            conteudo = f"\nTotal de registros: {total_linhas}"  # Adiciona o total de linhas
            # print(conteudo)  # Verifica a tabela gerada antes de enviar
            
        except Exception as e:
            print(f"Erro ao processar e enviar o e-mail: {e}")
        
        corpo = (
            "** Mensagem de envio automático. Favor não responder este e-mail **\n\n"
            "Prezados(as),\n\n"
            "Os dados da tabela foram atualizados e podem ser acessados no Relatório de Tarifas - Rodoviário e Cabotagem\n\n"
            f"{df_top5}\n\n"
            f"{conteudo}\n\n"
            "Atenciosamente."
        )

        # # Move arquivos para o histórico somente se não houver erros
        # mover_arquivos_para_historico(folder_path)

        # Chama a função para abrir o Gmail
        abrir_gmail(destinatarios, assunto, corpo, copia)

        print("E-mail preparado! Verifique no navegador.")
        retornar_menu()


    def janela_ajuda():
        help_window = Tk()
        help_window.title("Ajuda")
        ajuda_texto = """Data Build: Gerenciador de Cadastros de Frete OTM
        
        Este aplicativo foi desenvolvido para automatizar e simplificar o tratamento 
        de arquivos e o cadastro da tabela frete no sistema OTM (Oracle Transportation Management). 
        
        Projetado para reduzir erros manuais, economizar tempo e melhorar a produtividade, 
        o aplicativo executa as seguintes funções principais:

        1. Processamento de Arquivos.
                       
        2. Cadastro Automático de Fretes.
                   
        3. Integração com OTM.
                   
        Para mais informações, suporte ou dúvidas técnicas, entre em contato com:
               
        - Israel Nascimento
        - israel.nascimento@natura.net
        
        
        
                                            Desenvolvido por Israel Nascimento
        """
        label_ajuda = Label(help_window, text=ajuda_texto, anchor='w', justify='left')
        label_ajuda.pack(padx=10, pady=10)
        help_window.mainloop()
    

    def retornar_menu():
        root = Tk()
        root.withdraw()
        retornar = messagebox.askyesno("Menu Inicial", "Deseja voltar ao menu inicial?")
        root.destroy()  # Certifique-se de destruir a janela
        if not retornar:
            print("Encerrando o programa. Até mais!")
            exit()

    def mostrar_menu():
        root = Tk()
        root.withdraw()
        
        opcao = simpledialog.askstring(
            "Menu Interativo",
            "Escolha uma opção:\n"
            '-----------------------------------------------\n\n'
            "1 - Selecionar um Arquivo Excel.\n\n"  # Nova opção para selecionar arquivo
            "2 - Processar e Salvar Arquivo.\n\n"
            "3 - Processamento do OTM.\n\n"
            "4 - Enviar e-mail.\n\n"  
            "5 - Ajuda.\n\n"
            "6 - Sair.\n\n"
            "Digite o número da opção desejada:"
        )
        
        root.destroy()
        return opcao

    while True:
        opcao = mostrar_menu()
        if opcao == "1":
            caminho_arquivo_excel = selecionar_arquivo()
        elif opcao == "2":
            submenu(2, etapa2)
        elif opcao == "3":
            submenu(3, etapa3)
        elif opcao == "4":
            enviar_email()
        elif opcao == "5":
            janela_ajuda()
        elif opcao == "6":
            print("Encerrando o programa. Até mais!")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == '__main__':
    main()
