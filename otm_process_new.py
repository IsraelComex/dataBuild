from datetime import datetime
import time
from credentials import get_credentials_governance
from playwright.sync_api import TimeoutError, Page
import os
from bs4 import BeautifulSoup
import pyperclip

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
            print("Entrada inválida. Digite 'M' para retornar ao menu ou 'C' para.")

def aguardar_escolha_menu_ntrbr(retornar_menu, mostrar_menu):
    """Função para escolher o que executar no NTR/BR."""
    while True:
        print("\n" + "="*50)
        print("DOMÍNIO NTR/BR - OTM PRD")
        print("="*50)
        print("1 - Governança (Inativar Tarifas)")
        print("2 - Suprimentos (Atualizar Tarifas)")
        print("3 - Voltar ao menu")
        print("-"*50)
        escolha = input("Digite sua opção (1,2 ou 3): ").strip()
        if escolha == '1':
            return 'governanca'
        elif escolha == '2':
            return 'suprimentos'
        elif escolha == '3':
            print("Retornando ao menu principal...")
            retornar_menu()
            mostrar_menu()
            return 'menu'
        else:
            print("Opção inválida! Digite 1, 2 ou 3.")

def processar_registros_ntrbr_otm_completo(page: Page, registros, data_limite, retornar_menu, mostrar_menu):
    """
    Função unificada para o domínio NTR/BR:
    - Login único
    - Menu de escolha: 1=Governança, 2=Suprimentos, 3=Voltar
    - Se escolher Governança, pergunta se quer continuar para Suprimentos
    - Logout no final
    """
    # ========== CONFIGURAÇÕES ==========
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

    # ========== FUNÇÕES AUXILIARES ==========
    def _clicar_settings_actions():
        """Clica em Settings and Actions em qualquer idioma."""
        settings_labels = ["Settings and Actions", "Configurações e Ações", "SettingsandActions"]
        
        time.sleep(2)
        page.wait_for_load_state('networkidle')

        for label in settings_labels:
            locator = page.get_by_label(label)
            if locator.count() > 0:
                try:
                    locator.click()
                    time.sleep(2)
                    return True
                except Exception as e:
                    print(f"Erro ao clicar em {label}: {str(e)}")
                    continue
        msg = "Não foi possível encontrar Settings and Actions em nenhum idioma."
        if aguardar_decisao_usuario(retornar_menu, mostrar_menu, msg) == 'menu':
            return False
        return False

    def _selecionar_funcao_usuario(funcao_nome):
        """Seleciona uma função do usuário (GOVERNANCA ou SUPRIMENTOS)."""
        try:
            print(f"\n{'='*60}")
            print(f"🔄 SELECIONANDO FUNÇÃO: {funcao_nome}")
            print('='*60)
            # ✅ PASSO 1: Abrir o combobox
            page.get_by_role("combobox", name="Função do Usuário").wait_for(timeout=10000)
            page.get_by_role("combobox", name="Função do Usuário").click()
        except Exception:
            try:
                page.locator('#userRoleSS\\|input').wait_for(timeout=10000)
                page.locator('#userRoleSS\\|input').click()
            except Exception as e:
                if aguardar_decisao_usuario(retornar_menu, mostrar_menu,
                                            f"Erro ao acessar seleção de função: {str(e)}") == 'menu':
                    return False
        # ✅ PASSO 2: Aguardar dropdown aparecer
        time.sleep(2)
        try:
            funcao_option = page.get_by_role("row").filter(has_text=funcao_nome).first
            funcao_option.wait_for(timeout=10000)
            funcao_option.click()
            print(f"Função {funcao_nome} selecionada com sucesso.")
            return True
        except Exception:
            if aguardar_decisao_usuario(retornar_menu, mostrar_menu,
                                        f"Não foi possível encontrar a Função {funcao_nome}.") == 'menu':
                return False

    def _salvar_e_fechar():
        """Clica em Salvar e Fechar em qualquer idioma."""
        save_labels = ["Salvar e Fechar", "Save and Close"]
        for label in save_labels:
            try:
                page.get_by_label(label).wait_for(timeout=10000)
                page.get_by_label(label).click()
                return True
            except Exception:
                continue
        if aguardar_decisao_usuario(retornar_menu, mostrar_menu,
                                    "Não foi possível encontrar o comando para Salvar.") == 'menu':
            return False
        return False

    def _fazer_logout():
        """Faz logout em qualquer idioma."""
        logout_pairs = [
            ("Configurações e Ações", "Sair"),
            ("Settings and Actions", "Sign Out")
        ]
        for settings, signout in logout_pairs:
            try:
                page.get_by_label(settings).click()
                page.get_by_label(signout).click()
                time.sleep(5)
                print("✓ Logout realizado com sucesso.")
                return True
            except Exception:
                continue
        print("⚠️  Erro ao fazer logout.")
        return False

    def _voltar_ao_menu(menu_nome):
        """Volta para o menu inicial (Tarifas ou Gerenciamento de Integração)."""
        try:
            page.get_by_label("Home").click()
            time.sleep(1)
            page.get_by_title(menu_nome).click()
            time.sleep(1)
            return True
        except Exception as e:
            print(f"⚠️  Erro ao navegar para {menu_nome}: {str(e)}")
            return False

    # ========== MAPEAMENTO DE TIPOS DE TARIFA ==========
    TIPO_TARIFA_MAP = {
        "DIRETO": "RO",
        "CONSOLIDADO": "CO",
        "REDESPACHO": "RE",
        "CABOTAGEM": "CB",
        "SPOT": "SP",
        "DEDICADO": "DI"
    }

    # ========== PROCESSAMENTO DE GOVERNANÇA ==========
    def _processar_governanca(user_name_local: str):
        print('\n' + "="*60)
        print("INICIANDO PROCESSAMENTO DE GOVERNANÇA (NTR/BR)")
        print("="*60)
        print('Processando vigência tarifária...\n')

        # Abrir Settings and Actions
        if not _clicar_settings_actions():
            return False
        page.wait_for_load_state('networkidle')

        # Selecionar função GOVERNANÇA
        if not _selecionar_funcao_usuario("GOVERNANCA"):
            return False

        # Salvar função
        if not _salvar_e_fechar():
            return False
        print("Função GOVERNANÇA salva e aplicada.")

        # Abrir menu Tarifas → Tarifas - Natura
        try:
            print("Acessando menu de Tarifas...")
            clicar_com_retentativa(page.get_by_title("Menu Icon"))
            page.wait_for_load_state('networkidle')
            clicar_com_retentativa(page.get_by_title("Tarifas", exact=True))
            page.wait_for_load_state('networkidle')
            clicar_com_retentativa(page.get_by_text("Tarifas - Natura"))
            page.wait_for_load_state('networkidle')
            print("Menu Tarifas - Natura acessado.")
        except Exception as e:
            if aguardar_decisao_usuario(retornar_menu, mostrar_menu,
                                        f"Erro ao acessar o menu de tarifas: {str(e)}") == 'menu':
                return False

        # Loop de registros de tarifas
        total_registros = len(registros)
        print(f"\nProcessando {total_registros} registro(s) de tarifas...\n")

        for idx, registro in enumerate(registros, start=1):
            Origem = registro['Origem']
            Destino = registro['Destino']
            Transportadora = registro['Transportadora']
            Equipamento = registro['Equipamento']
            Tarifa = registro.get('Tarifa', '').strip().upper()

            print(f"[{idx}/{total_registros}] Processando: Origem: {Origem} | Destino: {Destino} | Tipo: {Tarifa} ({Tarifa}) | Equipamento: {Equipamento}")

            # ✅ CRIAR CHAVE ÚNICA (Rate Record ID)
            Tarifa = TIPO_TARIFA_MAP[Tarifa]
            rate_record_id = f"{Transportadora}_{Origem}_{Destino}_{Tarifa}_{Equipamento}"

            # Preencher filtros e pesquisar
            try:
                iframe = page.locator("#mainIFrame").content_frame
                # ✅ FILTRAR PELO RATE RECORD ID (chave única)
                # iframe.get_by_label("ID do Registro de Tarifa", exact=True).fill(rate_record_id)
                # iframe.get_by_label("ID do Registro de Tarifa Operador").select_option("contains")

                iframe.locator("[name='rate_geo/xid']").fill(rate_record_id) 
                iframe.locator("[name='rate_geo/xid_operator']").select_option("contains")              

                # ✅ FILTRAR POR DATA DE EXPIRAÇÃO (maior que hoje)
                data_atual = datetime.now().strftime("%d/%m/%Y")
                # iframe.get_by_role("textbox", name="Expiration Date").fill(data_atual)
                # iframe.get_by_label("Data de Vencimentor").select_option("gt")
                iframe.locator("[name='rate_geo/expiration_date']").fill(data_atual)
                iframe.locator("[name='rate_geo/expiration_date_operator']").select_option("gt")

                # iframe.get_by_role("button", name="OK").click()
                iframe.locator("button[name='search_button']").click()
                time.sleep(2)
            except Exception as e:
                if aguardar_decisao_usuario(retornar_menu, mostrar_menu,
                                            f"Erro ao preencher o registro {idx}: {str(e)}") == 'menu':
                    return False

            # Marcar resultados
            try:
                iframe = page.locator("#mainIFrame").content_frame
                # marcar_elemento = iframe.get_by_label("Marcar/Desmarcar todas as linhas")
                marcar_elemento = iframe.locator("input.sgHeadCheck[type='checkbox']")
                if marcar_elemento.is_visible():
                    marcar_elemento.click()
                    time.sleep(2)
                else:
                    print(f"Nenhum dado disponível no OTM para o registro {idx}. Continuando para o próximo registro...\n")
                    if not _voltar_ao_menu("Tarifas - Natura"):
                        return False
                    continue
            except Exception as e:
                if aguardar_decisao_usuario(retornar_menu, mostrar_menu,
                                            f"Erro ao processar o registro {idx}: {str(e)}") == 'menu':
                    return False

            # Abrir popup "Registro de Tarifa de Expiração" e aplicar data_limite
            try:
                with page.expect_popup() as page1_info:
                    iframe = page.frame_locator("#mainIFrame")
                    # iframe.locator("button:has-text('Registro de Tarifa de Expiração')").click()
                    iframe.locator("button[onclick*='rate_geo_set_expire_date']").click()
                    time.sleep(1)
                page1 = page1_info.value
                iframe_popup = page1.frame_locator("iframe[name='mainBody']")
                # data_limite_formatted = data_limite.strftime("d/%m/%Y")
                # iframe_popup.get_by_placeholder("DD/MM/YYYY").fill(data_limite_formatted)
                # iframe_popup.get_by_label("ID de Marca de Vencimento").fill(user_name_local)
                # iframe_popup.get_by_role("button", name="OK").click()

                data_limite_formatted = data_limite.strftime("%Y-%m-%d")  # YYYY-MM-DD
                iframe_popup.locator("[name='expire_date']").fill(data_limite_formatted)
                iframe_popup.locator("[name='expire_mark_id']").fill(user_name_local)
                iframe_popup.locator("button.enButton:has-text('OK')").click()

                page1.close()
                # iframe.get_by_role("button", name="Nova Consulta").click()
                iframe.locator("button[onclick*='newSearch()']").click()
                print(f"    ✓ Registro {idx} expirado com sucesso (data limite: {data_limite_formatted}).\n")
            except Exception as e:
                if aguardar_decisao_usuario(retornar_menu, mostrar_menu,
                                            f"Erro ao expirar a tarifa do registro {idx}: {str(e)}") == 'menu':
                    return False

        print("\n" + "="*60)
        print("PROCESSAMENTO DE GOVERNANÇA CONCLUÍDO COM SUCESSO!")
        print("="*60)
        return True

    # ========== PROCESSAMENTO DE SUPRIMENTOS ==========
    def _processar_suprimentos():
        print('\n' + "="*60)
        print("INICIANDO PROCESSAMENTO DE SUPRIMENTOS (NTR/BR)")
        print("="*60)
        print("Alterando função para SUPRIMENTOS...")


        # ✅ CORREÇÃO: Voltar para Home antes de abrir Settings
        try:
            print("Retornando à página inicial...")
            page.get_by_label("Home").click()
            time.sleep(2)
            page.wait_for_load_state('networkidle')
        except Exception as e:
            print(f"⚠️  Aviso ao navegar para Home: {str(e)}")
            print("Tentando continuar mesmo assim...")


        # Abrir Settings and Actions
        if not _clicar_settings_actions():
            return False
        page.wait_for_load_state('networkidle')

        # Selecionar função SUPRIMENTOS
        if not _selecionar_funcao_usuario("SUPRIMENTOS"):
            return False

        # Salvar função
        if not _salvar_e_fechar():
            return False
        print("Função SUPRIMENTOS salva e aplicada.")
        page.wait_for_load_state('networkidle')

        # Acessar Gerenciamento de Integração
        try:
            print("Acessando Gerenciamento de Integração...")
            page.get_by_role("treeitem", name="Integração").locator("span").click()
            page.locator("span.oj-treeview-item-text[title='Gerenciamento de Integração']").click()
            print("Gerenciamento de Integração acessado.")
        except Exception as e:
            if aguardar_decisao_usuario(retornar_menu, mostrar_menu,
                                        f"Erro ao acessar Gerenciamento de Integração: {str(e)}") == 'menu':
                return False

        print('\nEnviando arquivos CSV...')
        try:
            csv_files = [f for f in os.listdir(csv_folder) if f.endswith('.csv')]
            total_arquivos = len(csv_files)
            print(f"Encontrados {total_arquivos} arquivo(s) CSV para upload.\n")

            iframe = page.locator("#mainIFrame").content_frame

            for idx, csv_file in enumerate(csv_files, start=1):
                print(f"[{idx}/{total_arquivos}] Processando: {csv_file}")

                try:
                    csv_path = os.path.join(csv_folder, csv_file)
                    iframe.get_by_role("link", name="Carregar uma Transmissão XML/").wait_for()
                    iframe.get_by_role("link", name="Carregar uma Transmissão XML/").click()
                    time.sleep(2)
                    iframe.locator("#file").set_input_files(csv_path)
                    time.sleep(2)
                    iframe.get_by_role("button", name="Carregar").click()
                    time.sleep(1)

                    option_value = csv_option_map.get(csv_file)
                    if option_value:
                        iframe.locator("select[name='command']").wait_for(state="visible")
                        iframe.locator("select[name='command']").select_option(option_value)

                    iframe.get_by_role("button", name="Executar").click()
                    output_locator = iframe.locator("#output")
                    output_locator.wait_for(state="visible", timeout=180000)
                    print('    Executando upload...')
                    time.sleep(2)

                    xml_text = iframe.locator("#output").evaluate("element => element.value")
                    pyperclip.copy(xml_text)
                    xml_text = pyperclip.paste()
                    soup = BeautifulSoup(xml_text, 'lxml-xml')
                    error_count_element = soup.find('ErrorCount')

                    if error_count_element is not None:
                        error_count = int(error_count_element.text)
                        if error_count > 0:
                            error_element = soup.find('Error')
                            error_message = error_element.text if error_element else "Erro desconhecido."
                            print(f"    ⚠️  <ErrorCount>{error_count}</ErrorCount>")
                            print(f"    ⚠️  Erro encontrado:")
                            for line in error_message.strip().splitlines():
                                print(f"        {line}")

                            resp = aguardar_decisao_usuario(retornar_menu, mostrar_menu,
                                                            f"        Erro no arquivo {csv_file}")
                            if resp == 'menu':
                                return False
                        else:
                            print(f"    ✓ Upload bem-sucedido! (0 erros)")
                    else:
                        resp = aguardar_decisao_usuario(retornar_menu, mostrar_menu,
                                                        f"Elemento <ErrorCount> não encontrado no XML do arquivo {csv_file}.")
                        if resp == 'menu':
                            return False
                    print()
                    
                except Exception as e:
                    print(f"    ❌ Erro inesperado durante o processamento do arquivo {csv_file}: {str(e)}")
                    resp = aguardar_decisao_usuario(retornar_menu, mostrar_menu,
                                                    f"Erro inesperado no arquivo {csv_file}")
                    if resp == 'menu':
                        return False

                # ✅ Voltar ao menu SEMPRE, exceto no último arquivo
                if idx < total_arquivos:
                    try:
                        page.get_by_label("Home").click()
                        time.sleep(1)
                        page.get_by_title("Gerenciamento de Integração").click()
                        time.sleep(1)
                    except Exception as nav_e:
                        print(f"    ⚠️  Erro ao navegar após o arquivo {csv_file}: {str(nav_e)}")
                        print("    Tentando continuar mesmo assim...")

            print(f"\nTodos os {total_arquivos} arquivos foram processados.")

        except Exception as e:
            print(f"Erro ao listar arquivos CSV: {str(e)}")
            if aguardar_decisao_usuario(retornar_menu, mostrar_menu,
                                        "Erro ao acessar pasta de CSVs.") == 'menu':
                return False

        print("\n" + "="*60)
        print("PROCESSAMENTO DE SUPRIMENTOS CONCLUÍDO COM SUCESSO!")
        print("="*60)
        return True

    # ========== FLUXO PRINCIPAL ==========
    try:
        print("Preparando domínio NTR/BR no OTM PRD...")

        # ✅ CORREÇÃO: Navegar para a URL ANTES de qualquer processamento
        page.goto('https://otmgtm-natura01.otmgtm.us-phoenix-1.ocs.oraclecloud.com/')

        # Login
        while True:
            username, password = get_credentials_governance()
            page.fill('#idcs-signin-basic-signin-form-username', username)
            page.evaluate(f"document.querySelector('#idcs-signin-basic-signin-form-password').value = '{password}';")
             # ✅ Tenta clicar pelo texto em PT/EN
            try:
                # Tenta primeiroAcessar" (PT)
                page.get_by_role("button", name="Acessar").click(timeout=15000)
            except Exception:
                try:
                    # Se não achar "Acessar", "Sign In" (EN)
                    page.get_by_role("button", name="Sign In").click(timeout=15000)
                except Exception:
                    # Como fallback, tenta qualquer coisa com esse texto
                    try:
                        page.click("text=Acessar", timeout=15000)
                    except Exception:
                        page.click("text=Sign In", timeout=15000)

            time.sleep(6)
            page.wait_for_load_state('networkidle', timeout=60000)

            if aguardar_elemento(page, '#idcs-signin-basic-signin-form-username', timeout=10000):
                print("Login ou senha incorretos, tente novamente!")
            else:
                print("✓ Login efetuado com sucesso no domínio NTR/BR...")
                if aguardar_elemento(page, '#globalBody', timeout=120000):
                    print("✓ Página carregada com sucesso...")
                else:
                    if aguardar_decisao_usuario(retornar_menu, mostrar_menu,
                                                "Timeout: Elemento #globalBody não encontrado após 120 segundos") == 'menu':
                        return
                time.sleep(2)
                break

        page.wait_for_load_state('networkidle')

        # Extrair nome do usuário
        try:
            email_element = page.locator("div[slot='value']").first.inner_text()
            user_name = email_element.split('@')[0]
        except Exception as e:
            print(f"Erro ao extrair o nome de usuário: {str(e)}")
            if aguardar_decisao_usuario(retornar_menu, mostrar_menu, "Erro ao extrair nome de usuário") == 'menu':
                return

        print(f"✓ Nome do usuário registrado: {user_name}")

        # Menu principal NTR/BR
        escolha = aguardar_escolha_menu_ntrbr(retornar_menu, mostrar_menu)

        if escolha == 'menu':
            # Logout e voltar ao menu
            print("\nEncerrando sessão e retornando ao menu principal...")
            _fazer_logout()
            return

        # ----- Opção 1: Governança -----
        if escolha == 'governanca':
            ok = _processar_governanca(user_name)
            if ok:
                decisao = aguardar_decisao_usuario(
                    retornar_menu, mostrar_menu,
                    "Executar função SUPRIMENTOS (upload CSV) para atualização agora."
                )
                if decisao == 'continue':
                    _processar_suprimentos()

        # ----- Opção 2: Suprimentos -----
        elif escolha == 'suprimentos':
            _processar_suprimentos()

        # Logout final
        print("\n" + "="*60)
        print("REALIZANDO LOGOUT DO DOMÍNIO NTR/BR")
        print("="*60)
        _fazer_logout()

        print("\n" + "="*60)
        print("OPERAÇÃO CONCLUÍDA COM SUCESSO NO OTM!")
        print("="*60)
        print("Retornando ao menu principal...")
        time.sleep(2)
        retornar_menu()

    except Exception as e:
        if aguardar_decisao_usuario(retornar_menu, mostrar_menu,
                                    f"Erro geral no processamento: {str(e)}") == 'menu':
            return
