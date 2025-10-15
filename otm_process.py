# Função para processar registros no NTR OTM
from datetime import datetime
import time
from credentials import get_credentials_governance, get_credentials_supply
from playwright.sync_api import TimeoutError, Page
import os
from bs4 import BeautifulSoup
import pyperclip
import listas as lst

def delay(time_in_seconds):
    time.sleep(time_in_seconds)

def aguardar_elemento(page: Page, selector: str, timeout: int = 60000):
    """Aguarda um elemento específico aparecer na página."""
    try:
        page.wait_for_selector(selector, state='visible', timeout=timeout)
        return True
    except TimeoutError:
        return False

def clicar_com_retentativa(element, max_tentativas=3):
    """Tenta clicar em um elemento múltiplas vezes em caso de falha."""
    tentativas = 0
    while tentativas < max_tentativas:
        try:
            element.click()
            return True
        except Exception:
            time.sleep(2)
            tentativas += 1
    return False

def aguardar_decisao_usuario(retornar_menu, mostrar_menu, mensagem=""):
    """Função que aguarda a decisão do usuário para continuar ou retornar ao menu."""
    while True:
        decisao = input(f"{mensagem} Deseja retornar ao menu (M) ou continuar (C)? ").strip().lower()
        if decisao == 'm':
            retornar_menu()
            mostrar_menu()
            return 'menu'
        elif decisao == 'c':
            return 'continue'
        else:
            print("Entrada inválida. Digite 'M' para retornar ao menu ou 'C' para continuar.")

def processar_registros_ntr_otm(page, registros, data_limite, retornar_menu, mostrar_menu):
    try:

        print("Preparando domínio NTR no OTM...")

        #link PROD
        page.goto('https://otmgtm-natura01.otmgtm.us-phoenix-1.ocs.oraclecloud.com/')
        
        #link TEST
        # page.goto('https://otmgtm-test-natura01.otmgtm.us-phoenix-1.ocs.oraclecloud.com/GC3/glog.webserver.home.HomeServlet?ojr=maincontent')
        
        #link DEV
        # page.goto('https://otmgtm-dev1-natura01.otmgtm.us-phoenix-1.ocs.oraclecloud.com/')
        
        while True:
            username, password = get_credentials_governance()
            page.fill('#idcs-signin-basic-signin-form-username', username)
            page.evaluate(f"document.querySelector('#idcs-signin-basic-signin-form-password').value = '{password}';")
            page.click('span#ui-id-4')
            time.sleep(6)
            page.wait_for_load_state('networkidle', timeout=60000)
            if aguardar_elemento(page, '#idcs-signin-basic-signin-form-username', timeout=10000):
                print("Login ou senha incorretos, tente novamente!")
            else:
                print("Login efetuado com sucesso...")
                if aguardar_elemento(page, '#globalBody', timeout=120000):
                    print("Página carregada com sucesso...")
                else:
                    if aguardar_decisao_usuario(retornar_menu, mostrar_menu, "Timeout: Elemento #globalBody não encontrado após 120 segundos") == 'menu':
                        return
                time.sleep(2)
                break
            
        page.wait_for_load_state('networkidle')
        try:
            email_element = page.locator("div[slot='value']").first.inner_text()
            user_name = email_element.split('@')[0]
        except Exception as e:
            print(f"Erro ao extrair o nome de usuário: {str(e)}")
            if aguardar_decisao_usuario(retornar_menu, mostrar_menu, "Erro ao extrair nome de usuário") == 'menu':
                return
        print(f"Nome do usuário registrado: {user_name}")
        print('Processando vigencia tarifária...\n')
        # Tenta encontrar e clicar no primeiro locator possível: "Settings and Actions"
        try:
            # print("Acessando 'Settings and Actions'...")
            settings_actions_locator = page.get_by_label("Settings and Actions")
            # Espera que o elemento esteja visível/interagível
            settings_actions_locator.wait_for(timeout=10000)
            settings_actions_locator.click()
            # print("'Settings and Actions' acessado com sucesso...")

        # Se o primeiro falhou (elemento não encontrado, timeout, etc.), tenta o segundo: "Configurações e Ações"
        except Exception:
            try:
                # print("Falhou em encontrar 'Settings and Actions'. Acessando 'Configurações e Ações'...")
                settings_actions_locator = page.get_by_label("Configurações e Ações")
                # Espera que o elemento esteja visível/interagível
                settings_actions_locator.wait_for(timeout=10000)
                settings_actions_locator.click()
                # print("'Configurações e Ações' acessado com sucesso...")

            # Se o segundo também falhou, tenta o terceiro: "SettingsandActions"
            except Exception:
                try:
                    # print("Falhou em encontrar 'Configurações e Ações'. Acessando 'SettingsandActions'...")
                    settings_actions_locator = page.get_by_label("SettingsandActions")
                    # Espera que o elemento esteja visível/interagível
                    settings_actions_locator.wait_for(timeout=10000)
                    settings_actions_locator.click()
                    # print("'SettingsandActions' acessado com sucesso...")

                # Se todas as tentativas falharam
                except Exception:
                    # print("Erro: Não foi possível encontrar nenhum dos locators para Settings/Actions.")
                    # Aqui você adiciona a lógica de tratamento de erro, similar ao seu exemplo GOVERNANCA.
                    # Por exemplo, chamar uma função para decidir o que fazer:
                    mensagem_erro = "Não foi possível encontrar nenhuma das opções: Settings and Actions, Configurações e Ações ou SettingsandActions."
                settings_actions_locator.wait_for(timeout=10000)
                settings_actions_locator.click()
    
        # page.get_by_label("Settings and Actions").wait_for(timeout=160000)
        # page.get_by_label("Settings and Actions").click()
        # page.wait_for_load_state('networkidle')
        # page.locator('#userRoleSS\\|input').click()
        # # Aguarde explicitamente que o elemento esteja visível
        # page.wait_for_selector("#lovDropdown_userRoleSS", state='visible', timeout=30000)
        
        
        # try:
        #     # Tente clicar diretamente na opção "GOVERNANCA"
        #     try:
        #         governanca_option = page.locator("text=GOVERNANCA")
        #         governanca_option.click()
        #     except Exception:
        #         # Se não encontrar "GOVERNANCA", tente "GOVERNANCA ( Padrão )"
        #         governanca_padrao_option = page.locator("text=GOVERNANCA ( Padrão )")
        #         governanca_padrao_option.click()
        #     valor_funcao_atual = page.locator('#userRoleSS\\|input').input_value()
        #     if "GOVERNANCA" in valor_funcao_atual.upper():
        #         print("Função encontrada...")
        #     else:
        #         page.locator('#userRoleSS\\|input').click()
        #         try:
        #             governanca_option = page.get_by_role("row", name="GOVERNANCA")
        #             governanca_option.wait_for(timeout=10000)
        #             governanca_option.click()
        #         except Exception:
        #             try:
        #                 governanca_padrao_option = page.get_by_role("row", name="GOVERNANCA ( Padrão )")
        #                 governanca_padrao_option.wait_for(timeout=10000)
        #                 governanca_padrao_option.click()
        #             except Exception:
        #                 if aguardar_decisao_usuario(retornar_menu, mostrar_menu, "Não foi possível encontrar a Função GOVERNANCA.") == 'menu':
        #                     return
        #         try:
        #             save_close_button_en_us = page.get_by_label("Save and Close")
        #             save_close_button_en_us.wait_for(timeout=10000)
        #             save_close_button_en_us.click()
        #         except Exception:
        #             try:
        #                 save_close_button_pt_br = page.get_by_label("Salvar e Fechar")
        #                 save_close_button_pt_br.wait_for(timeout=10000)
        #                 save_close_button_pt_br.click()
        #             except Exception:
        #                 if aguardar_decisao_usuario(retornar_menu, mostrar_menu, "Não foi possível encontrar o comando para Salvar.") == 'menu':
        #                     return
        # except Exception as e:
        #     if aguardar_decisao_usuario(retornar_menu, mostrar_menu, f"Erro ao verificar/trocar função de usuário: {str(e)}") == 'menu':
        #         return
        page.wait_for_load_state('networkidle')
        page.locator('#userRoleSS\\|input').click()

        # Aguarde explicitamente que o dropdown esteja visível
        page.wait_for_selector("#lovDropdown_userRoleSS", state='visible', timeout=30000)

        try:
            # Tente clicar diretamente na opção "GOVERNANCA"
            try:
                governanca_option = page.locator("text=GOVERNANCA")
                governanca_option.click()
            except Exception:
                # Se não encontrar "GOVERNANCA", tente "GOVERNANCA ( Padrão )"
                governanca_padrao_option = page.locator("text=GOVERNANCA ( Padrão )")
                governanca_padrao_option.click()

            # Verifique o valor atual
            valor_funcao_atual = page.locator('#userRoleSS\\|input').input_value()
            if "GOVERNANCA" in valor_funcao_atual.upper():
                print("Função GOVERNANCA selecionada com sucesso.")

            # Salva as configurações
            try:
                save_close_button_en_us = page.get_by_label("Save and Close")
                save_close_button_en_us.wait_for(timeout=10000)
                save_close_button_en_us.click()
            except Exception:
                try:
                    save_close_button_pt_br = page.get_by_label("Salvar e Fechar")
                    save_close_button_pt_br.wait_for(timeout=10000)
                    save_close_button_pt_br.click()
                except Exception:
                    if aguardar_decisao_usuario(retornar_menu, mostrar_menu, "Não foi possível encontrar o comando para Salvar.") == 'menu':
                        return

        except Exception as e:
            if aguardar_decisao_usuario(retornar_menu, mostrar_menu, f"Erro ao verificar/trocar função de usuário: {str(e)}") == 'menu':
                return
        # Processamento de tarifas
        try:
            clicar_com_retentativa(page.get_by_title("Menu Icon"))
            page.wait_for_load_state('networkidle')
            clicar_com_retentativa(page.get_by_title("Tarifas", exact=True))
            page.wait_for_load_state('networkidle')
            clicar_com_retentativa(page.get_by_text("Tarifas - Natura"))
            page.wait_for_load_state('networkidle')
        except Exception as e:
            if aguardar_decisao_usuario(retornar_menu, mostrar_menu, f"Erro ao acessar o menu de tarifas: {str(e)}") == 'menu':
                return

        for idx, registro in enumerate(registros, start=1):
            Origem = registro['Origem']
            Destino = registro['Destino']
            Transportadora = registro['Transportadora']
            Equipamento = registro['Equipamento']
            print(f"Processando registro {idx}: {registro}")
            try:
                iframe = page.locator("#mainIFrame").content_frame
                iframe.get_by_label("Zona de Origem 1", exact=True).fill(Origem)
                iframe.get_by_label("Zona de Destino 1", exact=True).fill(Destino)
                data_atual = datetime.now().strftime("%d/%m/%Y")
                iframe.get_by_role("textbox", name="Data de Vencimento").fill(data_atual)
                iframe.get_by_label("Data de Vencimento Operador").select_option("gt")
                iframe.get_by_label("ID do Prestador de Serviço", exact=True).fill(Transportadora)
                iframe.get_by_label("ID do Prestador de Serviço Operador").select_option("contains")
                iframe.get_by_label("ID do Perfil do Grupo de Equipamentos", exact=True).fill(Equipamento)
                iframe.get_by_label("ID do Perfil do Grupo de Equipamentos Operador").select_option("contains")
                iframe.get_by_role("button", name="Pesquisar").click()
                time.sleep(4)
            except Exception as e:
                if aguardar_decisao_usuario(retornar_menu, mostrar_menu, f"Erro ao preencher o registro {idx}: {str(e)}") == 'menu':
                    return

            try:
                iframe = page.locator("#mainIFrame").content_frame
                marcar_elemento = iframe.get_by_label("Marcar/Desmarcar todas as")
                if marcar_elemento.is_visible():
                    marcar_elemento.click()
                    time.sleep(4)
                else:
                    print(f"Nenhum dado disponível no OTM para o registro {idx}. Continuando para o próximo registro...\n")
                    page.get_by_label("Home").click()
                    time.sleep(1)
                    page.get_by_text("Tarifas - Natura").click()
                    time.sleep(1)
                    continue
            except Exception as e:
                if aguardar_decisao_usuario(retornar_menu, mostrar_menu, f"Erro ao processar o registro {idx}: {str(e)}") == 'menu':
                    return

            try:
                with page.expect_popup() as page1_info:
                    iframe = page.frame_locator("#mainIFrame")
                    iframe.locator("button:has-text('Registro de Tarifa de Expiração')").click()
                time.sleep(1)
                page1 = page1_info.value
                iframe_popup = page1.frame_locator("iframe[name='mainBody']")
                data_limite_formatted = data_limite.strftime("%d/%m/%Y")
                iframe_popup.get_by_placeholder("DD/MM/YYYY").fill(data_limite_formatted)
                iframe_popup.get_by_label("ID de Marca de Vencimento").fill(user_name)
                iframe_popup.get_by_role("button", name="OK").click()
                page1.close()
                iframe.get_by_role("button", name="Nova Consulta").click()
                print(f"Registro {idx} processado com sucesso.\n")
            except Exception as e:
                if aguardar_decisao_usuario(retornar_menu, mostrar_menu, f"Erro ao expirar a tarifa do registro {idx}: {str(e)}") == 'menu':
                    return
        
        # # New section for processing "Preferência de Tarifas"
        # try:
        #     print("Acessando 'Preferência de Tarifas'...")
        #     clicar_com_retentativa(page.get_by_title("Menu Icon"))
        #     page.wait_for_load_state('networkidle')
        #     clicar_com_retentativa(page.get_by_title("Tarifas", exact=True))
        #     page.wait_for_load_state('networkidle')
        #     clicar_com_retentativa(page.get_by_text("Preferencia de tarifas"))
        #     page.wait_for_load_state('networkidle')
        #     print("Preferência de Tarifas acessada com sucesso.")
        # except Exception as e:
        #     if aguardar_decisao_usuario(retornar_menu, mostrar_menu, f"Erro ao acessar 'Preferência de Tarifas': {str(e)}") == 'menu':
        #         return
        
        try:
            page.get_by_label("Configurações e Ações").click()
            page.get_by_label("Sair").click()
            time.sleep(5)
            print("Operação concluída com sucesso...")
        except Exception as e:
            if aguardar_decisao_usuario(retornar_menu, mostrar_menu, f"Erro ao sair da aplicação: {str(e)}") == 'menu':
                return

    except Exception as e:
        if aguardar_decisao_usuario(retornar_menu, mostrar_menu, f"Erro geral no processamento de registros NTR OTM: {str(e)}") == 'menu':
            return

def processar_registros_ntrbr_otm(page: Page, retornar_menu, mostrar_menu):
    csv_folder = r'C:\Temp\Cadastro de Tabela\templates_csv'
    csv_option_map = {
        "001_X_LANE_IU.csv": "iu",
        "002_CAPACITY_GROUP_IU.csv": "iu",
        "003_CAPACITY_LIMIT_IU.csv": "iu",
        "004_CAPACITY_USAGE_IU.csv": "iu",
        "005_CAPACITY_COMMITMENT_ALLOC_IU.csv": "iu",
        "006_CAPACITY_COMMITMENT_ALLOC_D_IU.csv": "iu",
        "007_RATE_UNIT_BREAK_PROFILE_IU.csv": "iu",
        "008_RATE_UNIT_BREAK_IU.csv": "iu",
        "009_RATE_OFFERING_IU.csv": "iu",
        "010_CM_RULE_IU.csv": "iu",
        "011_RATE_GEO_I.csv": "i",
        "012_RATE_GEO_REFNUM_I.csv": "i",
        "013_RG_SPECIAL_SERVICE_I.csv": "i",
        "014_RATE_GEO_COST_GROUP_I.csv": "i",
        "015_RATE_GEO_COST_I.csv": "i",
        "016_RATE_GEO_COST_UNIT_BREAK_I.csv": "i",
        "017_ACCESSORIAL_COST_IU.csv": "iu",
        "018_ACCESSORIAL_COST_UNIT_BREAK_IU.csv": "iu",
        "019_RATE_GEO_ACCESSORIAL_I.csv": "i",
        "020_RATE_PREFERENCE_IU.csv": "iu",
        "021_RATE_PREFERENCE_DETAIL_IU.csv": "iu",
        "022_RATE_GEO_STOPS_I.csv": "i"
    }
    try:
        
        print("\nAcessando domínio NTR/BR no OTM...")
        #Link PRD
        page.goto('https://otmgtm-natura01.otmgtm.us-phoenix-1.ocs.oraclecloud.com/')
        
        #link TEST
        # page.goto('https://otmgtm-test-natura01.otmgtm.us-phoenix-1.ocs.oraclecloud.com/GC3/glog.webserver.home.HomeServlet?ojr=maincontent ')

        #link DEV
        # page.goto('https://otmgtm-dev1-natura01.otmgtm.us-phoenix-1.ocs.oraclecloud.com/')
        
        while True:
            username, password = get_credentials_supply()
            page.fill('#idcs-signin-basic-signin-form-username', username)
            page.evaluate(f"document.querySelector('#idcs-signin-basic-signin-form-password').value = '{password}';")
            page.click('span#ui-id-4')
            time.sleep(5)
            page.wait_for_load_state('networkidle', timeout=60000)
            if aguardar_elemento(page, '#idcs-signin-basic-signin-form-username', timeout=10000):
                print("Login ou senha incorretos, tente novamente.")
            else:
                print("Login efetuado com sucesso...")
                if not aguardar_elemento(page, '#globalBody', timeout=120000):
                    if aguardar_decisao_usuario(retornar_menu, mostrar_menu, "Timeout: Elemento #globalBody não encontrado após 120 segundos") == 'menu':
                        return
                break
        
        print("Iniciando Processo de Upload...")
        page.wait_for_load_state('networkidle', timeout=160000)
        time.sleep(3)
        page.get_by_label("Configurações e Ações").wait_for(timeout=160000)
        time.sleep(3)
        page.get_by_label("Configurações e Ações").click()
        time.sleep(3)
        page.get_by_role("combobox", name="Função do Usuário").wait_for()
        time.sleep(3)
        page.get_by_role("combobox", name="Função do Usuário").click()
        page.wait_for_load_state('networkidle', timeout=160000)
        time.sleep(3)

        try:
            suprimentos_option = page.get_by_role("row", name="SUPRIMENTOS")
            suprimentos_option.wait_for(timeout=10000)
            suprimentos_option.click()
        except Exception:
            try:
                suprimentos_padrao_option = page.get_by_role("row", name="SUPRIMENTOS ( Padrão )")
                suprimentos_padrao_option.wait_for(timeout=10000)
                suprimentos_padrao_option.click()
            except Exception:
                if aguardar_decisao_usuario(retornar_menu, mostrar_menu, "Não foi possível encontrar nenhuma das opções: SUPRIMENTOS ou SUPRIMENTOS (Padrão).") == 'menu':
                    return

        page.get_by_label("Salvar e Fechar").wait_for()
        page.get_by_label("Salvar e Fechar").click()
        page.wait_for_load_state('networkidle')

        page.get_by_role("treeitem", name="Integração").locator("span").click()
        page.locator("span.oj-treeview-item-text[title='Gerenciamento de Integração']").click()
        print('Enviando csv...')
        csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]
        iframe = page.locator("#mainIFrame").content_frame
        
        for csv_file in csv_files:
            # print(f"\nProcessando arquivo: {csv_file}")
            resposta_usuario = None
            try:
                csv_path = os.path.join(csv_folder, csv_file)
                iframe.get_by_role("link", name="Carregar uma Transmissão XML/").wait_for()
                iframe.get_by_role("link", name="Carregar uma Transmissão XML/").click()
                time.sleep(2)
                iframe.locator("#file").set_input_files(csv_path)
                time.sleep(2)
                iframe.get_by_role("button", name="Carregar").click()
                time.sleep(1)

                option_value = csv_option_map.get(csv_file, None)
                if option_value:
                    iframe.locator("select[name=\"command\"]").wait_for(state="visible")
                    iframe.locator("select[name=\"command\"]").select_option(option_value)
                iframe.get_by_role("button", name="Executar").click()

                output_locator = iframe.locator("#output")
                output_locator.wait_for(state="visible", timeout=180000)

                print('-----------------------x-------------------------')
                print(f"Arquivo {csv_file}")
                time.sleep(1)
                xml_text = iframe.locator("#output").evaluate("element => element.value")
                pyperclip.copy(xml_text)
                xml_text = pyperclip.paste()
                soup = BeautifulSoup(xml_text, 'lxml-xml')
                error_count_element = soup.find('ErrorCount')

                if error_count_element is not None:
                    error_count = int(error_count_element.text)
                    if error_count > 0:
                        error_element = soup.find('Error')
                        error_message = error_element.text if error_element is not None else "Erro desconhecido."
                        print(f"<ErrorCount>{error_count}</ErrorCount>")
                        print(f"Erro encontrado: {error_message}")
                        resposta = aguardar_decisao_usuario(retornar_menu, mostrar_menu, f"Erro no arquivo {csv_file}")
                        if resposta_usuario == 'menu':
                            return
                    else:
                        print(f"Número de erros encontrado: {error_count}")
                        print("Upload bem-sucedido.")
                else:
                    resposta = aguardar_decisao_usuario(retornar_menu, mostrar_menu, "Elemento <ErrorCount> não encontrado no XML.")
                    if resposta_usuario == 'menu':
                        return

            except Exception as e:
                # --- Lógica de Tratamento de Exceção Inesperada ---
                print(f"Erro inesperado durante o processamento do arquivo {csv_file}: {str(e)}")
                # Chama a função e armazena a resposta
                resposta_usuario = aguardar_decisao_usuario(retornar_menu, mostrar_menu, f"Erro inesperado no arquivo {csv_file}")
                if resposta_usuario == 'menu':
                    return # Sai da função principal de processamento

            # print(f"Navegando de volta para preparar o próximo arquivo...")
            
            try:
                page.get_by_label("Home").click()
                time.sleep(1) # Considere substituir por waits Playwright
                page.get_by_title("Gerenciamento de Integração").click()
                time.sleep(1) # Considere substituir por waits Playwright

            except Exception as nav_e:
                print(f"Erro durante a navegação após processamento/erro tratado do arquivo {csv_file}: {str(nav_e)}")
                print("Aviso: A navegação falhou. O próximo arquivo pode não ser processado corretamente.")

        print("\nProcessamento de todos os arquivos concluído.") # Adicionado para debug

        print('Upload finalizado...')
        retornar_menu()

    except Exception as e:
        if aguardar_decisao_usuario(retornar_menu, mostrar_menu, f"Erro durante o processamento: {str(e)}") == 'menu':
            return
        

