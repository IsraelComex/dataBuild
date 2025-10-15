from curses import color_content
import os
from weakref import ref
import pandas as pd
import datetime
from pyparsing import col
# from build.backupRomaker.lib.numpy.testing._private.utils import clear_and_catch_warnings
from numpy.testing._private.utils import clear_and_catch_warnings
import listas as lst
import sys




# Definindo os nomes dos arquivos CSV de saída
csv_filenames = [
    "001_X_LANE_IU.csv",
    "002_CAPACITY_GROUP_IU.csv",
    "003_CAPACITY_LIMIT_IU.csv",
    "004_CAPACITY_USAGE_IU.csv",
    "005_CAPACITY_COMMITMENT_ALLOC_IU.csv",
    "006_CAPACITY_COMMITMENT_ALLOC_D_IU.csv",
    "007_RATE_UNIT_BREAK_PROFILE_IU.csv",
    "008_RATE_UNIT_BREAK_IU.csv",
    "009_RATE_OFFERING_IU.csv",
    "010_CM_RULE_IU.csv",
    "011_RATE_GEO_I.csv",
    "012_RATE_GEO_REFNUM_I.csv",
    "013_RG_SPECIAL_SERVICE_I.csv",
    "014_RATE_GEO_COST_GROUP_I.csv",
    "015_RATE_GEO_COST_I.csv",
    "016_RATE_GEO_COST_UNIT_BREAK_I.csv",
    "017_ACCESSORIAL_COST_IU.csv",
    "018_ACCESSORIAL_COST_UNIT_BREAK_IU.csv",
    "019_RATE_GEO_ACCESSORIAL_I.csv",
    "020_RATE_PREFERENCE_IU.csv",
    "021_RATE_PREFERENCE_DETAIL_IU.csv",
    "YADP.csv"
]

col_idx = {
        'COD_TRANSPORTADORA': 0,
        'NOME_TRANSPORTADORA': 1,
        'TIPO_DE_TARIFA': 2,
        'TIPO_DE_DEDICADA': 3,
        '%_DO_TRAJETO_DA_FD': 4,
        'OPERACAO': 5,
        'ID_ORIGEM': 6,
        'ZONA_DE_TRANSPORTE_ORIGEM': 7,
        'DESCRICAO_ZONA_DE_TRANSPORTE_ORIGEM': 8,
        'ID_DESTINO': 9,
        'ZONA_DE_TRANSPORTE_DESTINO': 10,
        'DESCRICAO_ZONA_DE_TRANSPORTE_DESTINO': 11,
        'PERFIL_GRUPO_DE_EQUIPAMENTO': 12,
        'DESCRICAO_GRUPO_DE_EQUIPAMENTO': 13,
        'CUSTO_BASE': 14,
        'ABASTECIMENTO_CDS': 15,
        'REDESPACHO': 16,
        'REVISTA': 17,
        'AJUDANTE': 18,
        'PEDAGIO': 19,
        'PORCENTAGEM_AD_VALOREM': 20,
        'VALOR_DE_CONTRATO': 21,
        'NRO_DE_VEICULOS': 22,
        'TARIFA_PREFERENCIAL': 23,
        'DATA_DE_INICIO': 24,
        'DATA_DE_EXPIRACAO': 25,
        'NRO_COLETAS': 26,
        'NRO_ENTREGAS': 27
    }

def convert_date_format(date_str):
    
    # Verificar se date_str é NaT ou None
    if pd.isna(date_str):
        return None  # Retorna None ou um valor padrão para casos de valores nulos
        
    # Verificar se date_str é um Timestamp
    if isinstance(date_str, pd.Timestamp):
        date_str = date_str.strftime("%d/%m/%Y")  # Converte para string no formato desejado
    # Converter para objeto datetime
    date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y")  # Agora funciona
    return date_obj.strftime("%Y%m%d")

# Caminho da pasta onde os arquivos CSV serão salvos
output_folder_path = r'C:\Temp\Cadastro de Tabela\templates_csv'

def create_csv_001(df): #001_X_LANE_IU
    global zone
    output_path = os.path.join(output_folder_path, "001_X_LANE_IU.csv")

    # Criar as linhas padrão
    lines = [
        "X_LANE",
        "X_LANE_GID,X_LANE_XID,SOURCE_GEO_HIERARCHY_GID,SOURCE_ZONE1,DEST_GEO_HIERARCHY_GID,DEST_ZONE1,DOMAIN_NAME",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
    
    unique_lines = set()

    # Adicionar as linhas formatadas com base no df
    for index, row in df.iterrows():
        # Extraindo os valores das colunas usando iloc para acessos posicionais
        code_trp = row.iloc[col_idx['COD_TRANSPORTADORA']]
        nome_trp = row.iloc[col_idx['NOME_TRANSPORTADORA']]
        tipo_tarifa = row.iloc[col_idx['TIPO_DE_TARIFA']]
        tipo_dedicada = row.iloc[col_idx['TIPO_DE_DEDICADA']]
        percent_ida = row.iloc[col_idx['%_DO_TRAJETO_DA_FD']]
        operacao = row.iloc[col_idx['OPERACAO']]
        origem = row.iloc[col_idx['ZONA_DE_TRANSPORTE_ORIGEM']]
        destino = row.iloc[col_idx['ZONA_DE_TRANSPORTE_DESTINO']]
        equipamento = row.iloc[col_idx['PERFIL_GRUPO_DE_EQUIPAMENTO']]
        desc_equipamento = row.iloc[col_idx['DESCRICAO_GRUPO_DE_EQUIPAMENTO']]
        nro_coletas = row.iloc[col_idx['NRO_COLETAS']]
        nro_entregas = row.iloc[col_idx['NRO_ENTREGAS']] 
        
        domain1 = lst.domain[0]  # "NTR/BR"
        domain2 = lst.domain[1]  # "NTR/BR."
        zone_value = lst.zone[0]
        subzone_value = lst.zone[1]
        
        if pd.notna(origem) and origem != "" and pd.notna(destino) and destino != "":
            formatted_line = f"{domain2}{subzone_value}_{origem}_{subzone_value}_{destino},{subzone_value}_{origem}_{subzone_value}_{destino},{zone_value},{origem},{zone_value},{destino},{domain1}"
            unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto

    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')

    print(f"Arquivo 001_X_LANE_IU.csv salvo com sucesso.")
    return 

def create_csv_002(df): #002_CAPACITY_GROUP_IU
    global zone
    output_path = os.path.join(output_folder_path, "002_CAPACITY_GROUP_IU.csv")
        
    # Criar as linhas padrão
    lines = [
        "CAPACITY_GROUP",
        "CAPACITY_GROUP_GID,CAPACITY_GROUP_XID,CAPACITY_GROUP_NAME,SERVPROV_GID,DOMAIN_NAME",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
    
    unique_lines = set()
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
        
        
        code_trp = row.iloc[col_idx['COD_TRANSPORTADORA']]
        tipo_tarifa = row.iloc[col_idx['TIPO_DE_TARIFA']]
        tipo_dedicada = row.iloc[col_idx['TIPO_DE_DEDICADA']]
        nro_veiculos = row.iloc[col_idx['NRO_DE_VEICULOS']]
    
    domain1 = lst.domain[0]  # "NTR/BR"
    domain2 = lst.domain[1]  # "NTR/BR."
    domain3 = lst.domain[2]  # "NTR."
    
    modald_code = ''
    type_modald = ''
    
    for modal_dedicada in lst.modalDedicado:
        if isinstance(modal_dedicada, dict) and modal_dedicada["TIPO_MODAL"] == tipo_dedicada:
            modald_code = modal_dedicada["R_C_D"]
            type_modald = modal_dedicada["TIPO_MODAL"]
            break 
    
    if type_modald == tipo_dedicada and pd.notna(tipo_dedicada) and tipo_dedicada != "" and pd.notna(nro_veiculos) and nro_veiculos != "":
        formatted_line = f"{domain2}{modald_code}{code_trp},{modald_code}{code_trp},{tipo_dedicada},{domain3}{code_trp},{domain1}"
        unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto

    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')

    print(f"Arquivo 002_CAPACITY_GROUP_IU.csv salvo com sucesso.")
    return 

def create_csv_003(df): #003_CAPACITY_LIMIT_IU
    global zone 
    output_path = os.path.join(output_folder_path, "003_CAPACITY_LIMIT_IU.csv")

    # Criar as linhas padrão
    lines = [
        "CAPACITY_LIMIT",
        "CAPACITY_LIMIT_GID,CAPACITY_LIMIT_XID,CAPACITY_GROUP_GID,EQUIPMENT_TYPE_GID,X_LANE_GID,TIME_PERIOD_TYPE_GID,EFFECTIVE_DATE,EXPIRATION_DATE,LIMIT,DOMAIN_NAME",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
    
    unique_lines = set()
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
        code_trp = row.iloc[col_idx['COD_TRANSPORTADORA']]
        tipo_tarifa = row.iloc[col_idx['TIPO_DE_TARIFA']]
        tipo_dedicada = row.iloc[col_idx['TIPO_DE_DEDICADA']]
        origem = row.iloc[col_idx['ZONA_DE_TRANSPORTE_ORIGEM']]
        destino = row.iloc[col_idx['ZONA_DE_TRANSPORTE_DESTINO']]
        nro_veiculos = row.iloc[col_idx['NRO_DE_VEICULOS']]
        tarifa_preferencial = row.iloc[col_idx['TARIFA_PREFERENCIAL']]
        data_criacao = convert_date_format(row.iloc[col_idx['DATA_DE_INICIO']])
        data_expiracao = convert_date_format(row.iloc[col_idx['DATA_DE_EXPIRACAO']])


        domain1 = lst.domain[0]  # "NTR/BR"
        domain2 = lst.domain[1]  # "NTR/BR."

        subzone_value = lst.zone[1] # Z1
        
        modald_code = ''
        
        for modal_dedicada in lst.modalDedicado:
            if isinstance(modal_dedicada, dict) and modal_dedicada["TIPO_MODAL"] == tipo_dedicada:
                modald_code = modal_dedicada["R_C_D"]
                break 
        
        infos_dict = lst.infos[0]  # Acessando o único dicionário na lista
        infos19 = infos_dict.get("EQUIPMENT_TYPE") 
        infos18 = infos_dict.get("DAILY")
        
        if pd.notna(tipo_dedicada) and tipo_dedicada != "" and pd.notna(nro_veiculos) and nro_veiculos != "":
            formatted_line = f"{domain2}{origem}_{destino}_{modald_code}{code_trp},{origem}_{destino}_{modald_code}{code_trp},{domain2}{modald_code}{code_trp},{domain2}{infos19},"\
                             f"{domain2}{subzone_value}_{origem}_{subzone_value}_{destino},{infos18},{data_criacao},{data_expiracao},{nro_veiculos},{domain1}"
            unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto

    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')

    print(f"Arquivo 003_CAPACITY_LIMIT_IU.csv salvo com sucesso.")
    return 

def create_csv_004(df): #004_CAPACITY_USAGE_IU
    global zone
    output_path = os.path.join(output_folder_path, "004_CAPACITY_USAGE_IU.csv")
    
    # Criar as linhas padrão
    lines = [
        "CAPACITY_USAGE",
        "CAPACITY_USAGE_GID,CAPACITY_USAGE_XID,CAPACITY_LIMIT_GID,CAPACITY_GROUP_GID,EQUIPMENT_TYPE_GID,X_LANE_GID,START_DATE,END_DATE,LIMIT,DOMAIN_NAME",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
    
    unique_lines = set()
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
        code_trp = row.iloc[col_idx['COD_TRANSPORTADORA']]
        tipo_tarifa = row.iloc[col_idx['TIPO_DE_TARIFA']]
        tipo_dedicada = row.iloc[col_idx['TIPO_DE_DEDICADA']]
        origem = row.iloc[col_idx['ZONA_DE_TRANSPORTE_ORIGEM']]
        destino = row.iloc[col_idx['ZONA_DE_TRANSPORTE_DESTINO']]
        nro_veiculos = row.iloc[col_idx['NRO_DE_VEICULOS']]
        data_criacao = convert_date_format(row.iloc[col_idx['DATA_DE_INICIO']])
        data_expiracao = convert_date_format(row.iloc[col_idx['DATA_DE_EXPIRACAO']])


        
        domain1 = lst.domain[0]  # "NTR/BR"
        domain2 = lst.domain[1]  # "NTR/BR."
  
        subzone_value = lst.zone[1] # Z1
        modald_code = ""
        
        for modal_dedicada in lst.modalDedicado:
            if isinstance(modal_dedicada, dict) and modal_dedicada["TIPO_MODAL"] == tipo_dedicada:
                modald_code = modal_dedicada["R_C_D"]
                break 
        
        infos_dict = lst.infos[0]  # Acessando o único dicionário na lista
        infos19 = infos_dict.get("EQUIPMENT_TYPE") 
        infos18 = infos_dict.get("DAILY")
        
        if pd.notna(tipo_dedicada) and tipo_dedicada != "" and pd.notna(nro_veiculos) and nro_veiculos != "":
            formatted_line = f"{domain2}{origem}_{destino}_{modald_code}{code_trp},{origem}_{destino}_{modald_code}{code_trp},{domain2}{origem}_{destino}_{modald_code}{code_trp},"\
                             f"{domain2}{modald_code}{code_trp},{domain2}{infos19},{domain2}{subzone_value}_{origem}_{subzone_value}_{destino},{data_criacao},{data_expiracao},{nro_veiculos},{domain1}"
            unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto

    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')

    print(f"Arquivo 004_CAPACITY_USAGE_IU.csv salvo com sucesso.")
    return 

def create_csv_005(df):     #df_commitment
    global zone
    output_path = os.path.join(output_folder_path, "005_CAPACITY_COMMITMENT_ALLOC_IU.csv")

    # Criar as linhas padrão
    lines = [
        "CAPACITY_COMMITMENT_ALLOC",
        "CAPACITY_COMMITMENT_ALLOC_GID,CAPACITY_COMMITMENT_ALLOC_XID,EFFECTIVE_DATE,EXPIRATION_DATE,X_LANE_GID,COMMITMENT_LANE_OBJECT_TYPE,ALLOCATION_TYPE,TIME_PERIOD_TYPE_GID,IS_RECURRING,DOMAIN_NAME",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
    unique_lines = set()
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
        
    #     # cod_seq = row[col_idx['SEQ']]      
    #     # origem = row[col_idx['ZONA_DE_TRANSPORTE_ORIGEM']]
    #     # descricao_origem = row[col_idx['DESCRICAO_ZONA_DE_TRANSPORTE_ORIGEM']]
    #     # destino = row[col_idx['ZONA_DE_TRANSPORTE_DESTINO']]
    #     # descricao_destino = row[col_idx['DESCRICAO_ZONA_DE_TRANSPORTE_DESTINO']]
    #     # data_criacao = convert_date_format(row[col_idx['DATA_DE_INICIO']])
    #     # data_expiracao = convert_date_format(row[col_idx['DATA_DE_EXPIRACAO']])
    #     # cod_transp = row[col_idx['TRANSPORTADORA']]
    #     # nro_entregas = row[col_idx['NRO_ENTREGAS']]
    #     # vlr_porcentagem = row[col_idx['PORCENTAGEM']]
      
    #     domain1 = lst.domain[0]  # "NTR/BR."
    #     domain2 = lst.domain[1]  # "NTR/BR" 

    #     subzone_value = lst.zone[1] # Z1
    #     commitment = "CMT_"
             
    #     infos_dict = lst.infos[0]  # Acessando o único dicionário na lista
    #     infos19 = infos_dict.get("EQUIPMENT_TYPE") 
    #     infos18 = infos_dict.get("DAILY")
    #     infos14 = infos_dict.get("SHIPMENT")
    #     infos14 = infos_dict.get("SHIPMENT")
    #     infos20 = infos_dict.get("MONTHLY")
        
        
        formatted_line ='' #f"{domain2}{commitment}{subzone_value}_{origem}_{subzone_value}_{destino},{commitment}{subzone_value}_{origem}_{subzone_value}_{destino},{data_criacao},{data_expiracao}"\
    #                       #  f"{domain2}{subzone_value}_{origem}_{subzone_value}_{destino},{infos14},{infos14},{infos20},Y,{domain1}"
        unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto

    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')

    print(f"Arquivo 005_CAPACITY_COMMITMENT_ALLOC_IU.csv salvo com sucesso.")
    return 

def create_csv_006(df):     #df_commitment#
    global zone
    output_path = os.path.join(output_folder_path, "006_CAPACITY_COMMITMENT_ALLOC_D_IU.csv")

    # Criar as linhas padrão
    lines = [
        "CAPACITY_COMMITMENT_ALLOC_D",
        "CAPACITY_COMMITMENT_ALLOC_GID,SERVPROV_GID,CAPACITY_COMMIT_ALLOC_D_SEQ,COMMIT_PERC,DOMAIN_NAME",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
    unique_lines = set()
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
    #     cod_seq = row['SEQ']       
    #     origem = row['ZONA_DE_TRANSPORTE_ORIGEM']
    #     descricao_origem = row['DESCRICAO_ZONA_DE_TRANSPORTE_ORIGEM']
    #     destino = row['ZONA_DE_TRANSPORTE_DESTINO']
    #     descricao_destino = row['DESCRICAO_ZONA_DE_TRANSPORTE_DESTINO']
    #     data_criacao = convert_date_format(row['DATA_DE_INICIO'])
    #     data_expiracao = convert_date_format(row['DATA_DE_EXPIRACAO'])
    #     cod_transp = row['TRANSPORTADORA']
    #     nro_entregas = row['NRO_ENTREGAS']
    #     vlr_porcentagem = row['PORCENTAGEM']
   
        
    #     domain1 = lst.domain[0]  # "NTR/BR."
    #     domain2 = lst.domain[1]  # "NTR/BR"
    #     domain3 = lst.domain[2]  # "NTR/BR"  
    #     zone_value = lst.zone[0] # zone_value1
    #     subzone_value = lst.zone[1] # Z1
    #     commitment = "CMT_"
              

        formatted_line = '' #f"{domain1}{commitment}{subzone_value}_{origem}_{subzone_value}_{destino},{domain3}{cod_transp},{cod_seq},{vlr_porcentagem},{domain2}" 
        unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto

    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')

    print(f"Arquivo 006_CAPACITY_COMMITMENT_ALLOC_D_IU.csv salvo com sucesso.")
    return 

def create_csv_007(df): #007_RATE_UNIT_BREAK_PROFILE_IU
    output_path = os.path.join(output_folder_path, "007_RATE_UNIT_BREAK_PROFILE_IU.csv")

    # Criar as linhas padrão
    lines = [
        "RATE_UNIT_BREAK_PROFILE",
        "RATE_UNIT_BREAK_PROFILE_GID,RATE_UNIT_BREAK_PROFILE_XID,RATE_UNIT_BREAK_PROFILE_NAME,DATA_TYPE,LOOKUP_TYPE,UOM_TYPE,DOMAIN_NAME",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
    unique_lines = set()
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
        code_trp = row.iloc[col_idx['COD_TRANSPORTADORA']]
        tipo_tarifa = row.iloc[col_idx['TIPO_DE_TARIFA']]
        rede_farma = ""
        
        domain1 = lst.domain[0]  # "NTR/BR"
        domain2 = lst.domain[1]  # "NTR/BR."
 
        unit_dict = lst.unit[0] 
        unit_cod = unit_dict.get("UNIDADE")
        unit_type = unit_dict.get("UOM_TYPE")
        
 
        farma_dict = lst.farma[0] 
        cod_farma = farma_dict.get("REDE_FARMA")  
        cod_transp = farma_dict.get("COD_TRANSPORTADORA")  

        
        if (tipo_tarifa in ["RODOVIARIO", "CONSOLIDADO", "DIRETO", "REDESPACHO"] and unit_cod == rede_farma and rede_farma == cod_farma and code_trp == cod_transp ):
            formatted_line = f"{domain2}{code_trp}_{rede_farma},{code_trp}_{rede_farma},{rede_farma},N,M,{unit_type},{domain1}"
            unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto

    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')

    print(f"Arquivo 007_RATE_UNIT_BREAK_PROFILE_IU.csv salvo com sucesso.")
    return 

def create_csv_008(df): #008_RATE_UNIT_BREAK_IU.csv
    global zone
    output_path = os.path.join(output_folder_path, "008_RATE_UNIT_BREAK_IU.csv")

    # Criar as linhas padrão
    lines = [
        "RATE_UNIT_BREAK",
        "RATE_UNIT_BREAK_GID,RATE_UNIT_BREAK_XID,RATE_UNIT_BREAK_PROFILE_GID,RATE_UNIT_BREAK_MAX,DOMAIN_NAME",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
    
    unique_lines = set()
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
        code_trp = row.iloc[col_idx['COD_TRANSPORTADORA']]
        tipo_tarifa = row.iloc[col_idx['TIPO_DE_TARIFA']]
        rede_farma = ""
        
        domain1 = lst.domain[0]  # "NTR/BR"
        domain2 = lst.domain[1]  # "NTR/BR."
 
        unit_dict = lst.unit[0] 
        unit_cod = unit_dict.get("UNIDADE")
        unit_type = unit_dict.get("UOM_TYPE")
        unit_sigla = unit_dict.get("SIGLAS_UNIDADE")
        
 
        farma_dict = lst.farma[0] 
        cod_farma = farma_dict.get("REDE_FARMA")  
        cod_transp = farma_dict.get("COD_TRANSPORTADORA") 
        qtd_min = farma_dict.get("QTD_MINIMA") 
        qtd_max = farma_dict.get("QTD_MAXIMA")

        
        if (tipo_tarifa in ["RODOVIARIO", "CONSOLIDADO", "DIRETO", "REDESPACHO"] and unit_cod == rede_farma and rede_farma == cod_farma and code_trp == cod_transp ):
            formatted_line = f"{domain2}{code_trp}_{rede_farma}_{qtd_min}-{qtd_max},{rede_farma},{code_trp}_{rede_farma}_{qtd_min}-{qtd_max},"\
                            f"{domain2}{code_trp}_{rede_farma},{qtd_min},,{unit_sigla},{domain1}"
            unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto

    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')

    print(f"Arquivo 008_RATE_UNIT_BREAK_UI.csv salvo com sucesso.")
    return 

def create_csv_009(df): #009_RATE_OFFERING_IU
    global modal
    output_path = os.path.join(output_folder_path, "009_RATE_OFFERING_IU.csv")

    # Criar as linhas padrão
    lines = [
        "RATE_OFFERING",
        "RATE_OFFERING_GID,RATE_OFFERING_XID,RATE_OFFERING_TYPE_GID,SERVPROV_GID,CURRENCY_GID,TRANSPORT_MODE_GID,RATE_SERVICE_GID,RATE_VERSION_GID,RATE_DISTANCE_GID,PERSPECTIVE,CAPACITY_GROUP_GID,IS_ACTIVE,DOMAIN_NAME,ATTRIBUTE1,ATTRIBUTE_NUMBER1,CM_MAX_NUM_SHIPMENTS",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
    
    unique_lines = set()
    
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
    # Extraindo os valores das colunas usando iloc para acesso posicional
        code_trp = row.iloc[col_idx['COD_TRANSPORTADORA']]
        tipo_tarifa = row.iloc[col_idx['TIPO_DE_TARIFA']]
        tipo_dedicada = row.iloc[col_idx['TIPO_DE_DEDICADA']]
        vlr_contrato = str(row.iloc[col_idx['VALOR_DE_CONTRATO']]).replace(",", ".") if pd.notna(row.iloc[col_idx['VALOR_DE_CONTRATO']]) else ""
        # vlr_contrato = row.iloc[col_idx['VALOR_DE_CONTRATO']]
        nro_veiculos = row.iloc[col_idx['NRO_DE_VEICULOS']]

     
        
        domain1 = lst.domain[0]  # "NTR/BR"
        domain2 = lst.domain[1]  # "NTR/BR."
        domain3 = lst.domain[2]  # "NTR."  
        zone_value = lst.zone[0] # ZONE1
   
        
        modal_code = ''
        otype = ''
        type_modal = ''
        modal_trp = ''
        
        for modal_entry in lst.modal:
            if isinstance(modal_entry, dict) and modal_entry["TIPO_MODAL"] == tipo_tarifa:
                modal_code = modal_entry["R_C_D"]
                type_modal = modal_entry["TIPO_MODAL"]
                otype = modal_entry["OFERRING_TYPE"]
                modal_trp = modal_entry["TRANSPORT_MODE"]
                break 
        
        modald_code = ''
        type_modald = ''
        modald_otype = ''
        transp_mode = ''
        
        for modal_dedicada in lst.modalDedicado:
            if isinstance(modal_dedicada, dict) and modal_dedicada["TIPO_MODAL"] == tipo_dedicada:
                modald_code = modal_dedicada["R_C_D"]
                type_modald = modal_dedicada["TIPO_MODAL"]
                modald_otype = modal_dedicada["OFERRING_TYPE"]
                transp_mode = modal_dedicada["TRANSPORT_MODE"]
                break 
            
        infos_dict = lst.infos[0]  # Acessando o único dicionário na lista
        infos7 = infos_dict.get("BRL") 
        infos11 = infos_dict.get("INTERVALO") 
        
        service_modal=''
        rate_service = ''
        rate_distance =''
        
        for service_entry in lst.distanceService:
            if service_entry["MODAL"] == tipo_tarifa:
                service_modal =  service_entry["MODAL"]
                rate_service = service_entry["RATE_SERVICE"]
                rate_distance= service_entry["RATE_DISTANCE"]
                break
        
        service_modald=''
        rate_serviced = ''
        rate_distanced =''
        
        for serviced_entry in lst.distanceService:
            if serviced_entry["MODAL"] == tipo_dedicada:
                service_modald =  serviced_entry["MODAL"]
                rate_serviced = serviced_entry["RATE_SERVICE"]
                rate_distanced= serviced_entry["RATE_DISTANCE"]
                break
        
        if code_trp != '' and tipo_tarifa == type_modal and service_modal == tipo_tarifa:
            # Verifica se rate_distance e rate_service não são vazios
            if rate_distance not in ["", None] and rate_service not in ["", None]:
                formatted_line = f"{domain2}{modal_code}{code_trp},{modal_code}{code_trp},{otype},{domain3}{code_trp},{infos7},{modal_trp},{domain2}{rate_service},"\
                                f"{domain2}{infos11},{domain2}{rate_distance},B,{(domain2 + modal_code + code_trp) if tipo_tarifa == 'FROTA DEDICADA' else ''},Y,{domain1},"\
                                f"{tipo_dedicada},,"           
                unique_lines.add(formatted_line)
            
        if code_trp != '' and tipo_dedicada == type_modald and service_modald == tipo_dedicada:
            # Verifica se rate_distance e rate_service não são vazios
            if rate_distanced not in ["", None] and rate_serviced not in ["", None]:
                formatted_line = f"{domain2}{modald_code}{code_trp},{modald_code}{code_trp},{modald_otype},{domain3}{code_trp},{infos7},{transp_mode},{domain2}{rate_serviced},"\
                                f"{domain2}{infos11},{domain2}{rate_distanced},B,{(domain2 + modald_code + code_trp) if nro_veiculos != '' and tipo_dedicada in ['ANCRA', 'ESTETICO', 'DINAMICO', 'DUNORTE', 'FORTA'] else ''},Y,{domain1},"\
                                f"{tipo_dedicada},{vlr_contrato},"
                unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto

    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')

    print(f"Arquivo 009_RATE_OFFERING_IU.csv salvo com sucesso.")
    return 

def create_csv_010(df): #010_CM_RULE_IU
    global zone
    output_path = os.path.join(output_folder_path, "010_CM_RULE_IU.csv")
    
    # Criar as linhas padrão
    lines = [
        "CM_RULE",
        "RATE_OFFERING_GID,X_LANE_GID,DOMAIN_NAME",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
    
    unique_lines = set()
    
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
        # Extraindo os valores das colunas usando iloc para acessos posicionais
        code_trp = row.iloc[col_idx['COD_TRANSPORTADORA']]
        tipo_tarifa = row.iloc[col_idx['TIPO_DE_TARIFA']]
        tipo_dedicada = row.iloc[col_idx['TIPO_DE_DEDICADA']]
   
        domain1 = lst.domain[0]  # "NTR/BR"
        domain2 = lst.domain[1]  # "NTR/BR."
        
        modal_code = ""
        type_modal = '' 
        modal_sigla=""   
        
        for modal_entry in lst.modal:
            if isinstance(modal_entry, dict) and modal_entry["TIPO_MODAL"] == tipo_tarifa:
                modal_code = modal_entry["R_C_D"]
                type_modal = modal_entry["TIPO_MODAL"]
                modal_sigla = modal_entry["SIGLA_MODAL"]
                break 
            
        type_modald = ''
        modald_code = ''
        
        for modal_dedicada in lst.modalDedicado:
            if isinstance(modal_dedicada, dict) and modal_dedicada["TIPO_MODAL"] == tipo_dedicada:
                modald_code = modal_dedicada["R_C_D"]
                type_modald = modal_dedicada["TIPO_MODAL"]
                break  
            
        if tipo_tarifa == type_modal:  
            if modal_code: 
                formatted_line = f"{domain2}{modal_code}{code_trp},{domain2}{"BR-BR"},{domain1}"
                unique_lines.add(formatted_line)
            
        if tipo_dedicada == type_modald and tipo_dedicada != '': 
            if modald_code:
                formatted_line = f"{domain2}{modald_code}{code_trp},{domain2}{"BR-BR"},{domain1}"
                unique_lines.add(formatted_line) 
    
    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')

    print(f"Arquivo 010_CM_RULE_IU.csv salvo com sucesso.")
    return 

def create_csv_011(df): #011_RATE_GEO_I
    global zone
    output_path = os.path.join(output_folder_path, "011_RATE_GEO_I.csv")

    # Criar as linhas padrão
    lines = [
        "RATE_GEO",
        "RATE_GEO_GID,RATE_GEO_XID,RATE_OFFERING_GID,X_LANE_GID,EQUIPMENT_GROUP_PROFILE_GID,MIN_COST,MIN_COST_GID,PICKUP_STOPS_CONSTRAINT,DELIVERY_STOPS_CONSTRAINT,EFFECTIVE_DATE,EXPIRATION_DATE,DOMAIN_NAME,IS_ACTIVE,ATTRIBUTE_NUMBER1,RATE_SERVICE_GID,ATTRIBUTE1,ATTRIBUTE2,ATTRIBUTE3,ATTRIBUTE4,ATTRIBUTE5,ATTRIBUTE6",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
    
    unique_lines = set()
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
        # Extraindo os valores das colunas usando iloc para acessos posicionais
        code_trp = row.iloc[col_idx['COD_TRANSPORTADORA']]
        nome_trp = row.iloc[col_idx['NOME_TRANSPORTADORA']]
        tipo_tarifa = row.iloc[col_idx['TIPO_DE_TARIFA']]
        tipo_dedicada = row.iloc[col_idx['TIPO_DE_DEDICADA']]
        percent_ida = row.iloc[col_idx['%_DO_TRAJETO_DA_FD']]
        operacao = row.iloc[col_idx['OPERACAO']]
        origem = row.iloc[col_idx['ZONA_DE_TRANSPORTE_ORIGEM']]
        destino = row.iloc[col_idx['ZONA_DE_TRANSPORTE_DESTINO']]
        equipamento = row.iloc[col_idx['PERFIL_GRUPO_DE_EQUIPAMENTO']]
        desc_equipamento = row.iloc[col_idx['DESCRICAO_GRUPO_DE_EQUIPAMENTO']]
        nro_coletas = row.iloc[col_idx['NRO_COLETAS']]
        nro_entregas = row.iloc[col_idx['NRO_ENTREGAS']]

        # Convertendo as datas e concatenando
        data_criacao = convert_date_format(row.iloc[col_idx['DATA_DE_INICIO']])
        data_expiracao = convert_date_format(row.iloc[col_idx['DATA_DE_EXPIRACAO']])

        # Ajustando effective_data e expiration_data para evitar duplicação e lógica contraditória
        if data_criacao is not None and data_expiracao is not None:
            effective_data = data_criacao + "000000"
            expiration_data = data_expiracao + "000000"
        else:
            effective_data = "00000000"
            expiration_data = "00000000"
             
        domain1 = lst.domain[0]  # Isso retorna "NTR/BR"
        domain2 = lst.domain[1]  # Isso retorna "NTR/BR."
        subzone_value = lst.zone[1] # zone_value
        
        modal_code = ""
        type_modal = '' 
        modal_sigla=""   
        
        for modal_entry in lst.modal:
            if isinstance(modal_entry, dict) and modal_entry["TIPO_MODAL"] == tipo_tarifa:
                modal_code = modal_entry["R_C_D"]
                type_modal = modal_entry["TIPO_MODAL"]
                modal_sigla = modal_entry["SIGLA_MODAL"]
                break 
        
        modald_code = ''
        type_modald = ''
        modald_sigla = ''
        
        for modal_dedicada in lst.modalDedicado:
            if isinstance(modal_dedicada, dict) and modal_dedicada["TIPO_MODAL"] == tipo_dedicada:
                modald_code = modal_dedicada["R_C_D"]
                type_modald = modal_dedicada["TIPO_MODAL"]
                modald_sigla = modal_dedicada["SIGLA_MODAL"]
                break 
            
        infos_dict = lst.infos[0]  # Acessando o único dicionário na lista
        infos7 = infos_dict.get("BRL") 
                  
        stops = ''
        pickup = ''
        type_tarifa =''
         
        for tarifa_entry in lst.delivery_stop_constraint:
            if tarifa_entry["TIPO_DE_TARIFA"] == tipo_tarifa:
                type_tarifa = tarifa_entry["TIPO_DE_TARIFA"]
                stops = tarifa_entry["STOPS"]
                pickup = tarifa_entry["PICKUP_STOPS_CONSTRAINT"]
                break
        
        stopsd = ''
        pickupd = ''
        type_tarifad =''
         
        for dedicada_entry in lst.delivery_stop_constraint:
            if dedicada_entry["TIPO_DE_TARIFA"] == tipo_dedicada:
                type_tarifad = dedicada_entry["TIPO_DE_TARIFA"]
                stopsd = dedicada_entry["STOPS"]
                pickupd = dedicada_entry["PICKUP_STOPS_CONSTRAINT"]
                break
        
        def determinar_rate_service(equipamento):
            """Determina o RATE_SERVICE com base no nome do equipamento."""
            if 'ALH30' in equipamento or 'CLH16' in equipamento or 'RLH16' in equipamento or 'RLH14' in equipamento or 'VLH04' in equipamento or  'VAN04' in equipamento or 'ALH16' in equipamento or 'ALH14' in equipamento or 'RL224' in equipamento or 'RLH30' in equipamento or 'VUC04' in equipamento or 'FRG02' in equipamento:
                return 'NTR/BR.TMS_RS_TL_LHC'
            elif 'LE' in equipamento:
                return 'NTR/BR.TMS_RS_TL_LHE'
            elif 'CMT' in equipamento or 'RBT30' in equipamento or 'ALE30' in equipamento or 'RBT28' in equipamento or 'AMT16' in equipamento or 'CTC' in equipamento or 'RTR30' in equipamento or 'RBC30' in equipamento or 'RSP30' in equipamento or 'ABC30' in equipamento or 'ARG02' in equipamento or 'ABT30' in equipamento or 'AVU' in equipamento or 'ARG' in equipamento or 'ATC' in equipamento or 'ATP24' in equipamento:
                return 'NTR/BR.TMS_RS_TL_OBC'
            elif 'RT224' in equipamento or 'AT224' in equipamento or '226' in equipamento:
                return 'NTR/BR.TMS_RS_TL_OBR'
            elif 'BE' in equipamento:
                return 'NTR/BR.TMS_RS_TL_OBE'
            elif 'CBC40' in equipamento:
                return 'NTR/BR.TMS_RS_TL_OBE'
            #'TMS_RS_VESSEL'

        
        service_rate = determinar_rate_service(equipamento)
        serviced_rate = determinar_rate_service(equipamento)
        
               
        if tipo_tarifa == type_modal and type_tarifa != "CONSOLIDADO":   
            formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},"\
                            f"{domain2}{modal_code}{code_trp},{domain2}{subzone_value}_{origem}_{subzone_value}_{destino},{domain2}{equipamento},,{infos7},{pickup},{stops},{effective_data},{expiration_data},"\
                            f"{domain1},Y,{percent_ida},{service_rate},{operacao},{tipo_tarifa},{tipo_dedicada},,,{desc_equipamento},," 
            unique_lines.add(formatted_line)
        elif tipo_tarifa == type_modal and type_tarifa == "CONSOLIDADO":
            formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},"\
                            f"{domain2}{modal_code}{code_trp},{domain2}{subzone_value}_{origem}_{subzone_value}_{destino},{domain2}{equipamento},,{infos7},{nro_coletas},{nro_entregas},{effective_data},{expiration_data},"\
                            f"{domain1},Y,{percent_ida},{service_rate},{operacao},{tipo_tarifa},{tipo_dedicada},,,{desc_equipamento},," 
            unique_lines.add(formatted_line)
            
        if tipo_tarifa == 'FROTA DEDICADA' and tipo_dedicada == type_modald and tipo_dedicada != '' and type_tarifad == tipo_dedicada:   
            formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},"\
                            f"{domain2}{modald_code}{code_trp},{domain2}{subzone_value}_{origem}_{subzone_value}_{destino},{domain2}{equipamento},,{infos7},{stopsd if tipo_tarifa == "FROTA DEDICADA" else ''},{pickupd if tipo_tarifa == "FROTA DEDICADA" else ''},{effective_data},{expiration_data},"\
                            f"{domain1},Y,{percent_ida},{serviced_rate},{operacao},{tipo_tarifa},{tipo_dedicada},,,{desc_equipamento},,"                     
            unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto
           

    def get_penultimate_field(formatted_line):
        # Divide a string no separador de campo por vírgula e retire o penúltimo campo
        return formatted_line.split(',')[-6].strip()

    sorted_unique_lines = sorted(unique_lines, key=get_penultimate_field)
    
    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + sorted_unique_lines
    # final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')
          
    print(f"Arquivo 011_RATE_GEO_I.csv salvo com sucesso.")
    return 

def create_csv_012(df): #012_RATE_GEO_REFNUM_I
    global zone
    output_path = os.path.join(output_folder_path, "012_RATE_GEO_REFNUM_I.csv")

    # Criar as linhas padrão
    lines = [
        "RATE_GEO_REFNUM",
        "RATE_GEO_GID,RATE_GEO_REFNUM_QUAL_GID,RATE_GEO_REFNUM_VALUE,DOMAIN_NAME",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
        
    unique_lines = set()
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
        # Extraindo os valores das colunas G e I usando iloc
        code_trp = row.iloc[col_idx['COD_TRANSPORTADORA']]
        nome_trp = row.iloc[col_idx['NOME_TRANSPORTADORA']]
        tipo_tarifa = row.iloc[col_idx['TIPO_DE_TARIFA']]
        tipo_dedicada = row.iloc[col_idx['TIPO_DE_DEDICADA']]
        operacao = row.iloc[col_idx['OPERACAO']]
        id_origem = row.iloc[col_idx['ID_ORIGEM']]
        origem = row.iloc[col_idx['ZONA_DE_TRANSPORTE_ORIGEM']]
        id_destino = row.iloc[col_idx['ID_DESTINO']]
        descricao_origem = row.iloc[col_idx['DESCRICAO_ZONA_DE_TRANSPORTE_ORIGEM']]
        destino = row.iloc[col_idx['ZONA_DE_TRANSPORTE_DESTINO']]
        descricao_destino = row.iloc[col_idx['DESCRICAO_ZONA_DE_TRANSPORTE_DESTINO']]
        equipamento = row.iloc[col_idx['PERFIL_GRUPO_DE_EQUIPAMENTO']]
        ad_valorem = row.iloc[col_idx['PORCENTAGEM_AD_VALOREM']]
        descricao_equipamento = row.iloc[col_idx['DESCRICAO_GRUPO_DE_EQUIPAMENTO']]
        data_criacao = convert_date_format(row.iloc[col_idx['DATA_DE_INICIO']])
        data_expiracao = convert_date_format(row.iloc[col_idx['DATA_DE_EXPIRACAO']])


        
        domain1 = lst.domain[0]  # Isso retorna "NTR/BR"
        domain2 = lst.domain[1]  # Isso retorna "NTR/BR."
        domain3 = lst.domain[2]  # Isso retorna "NTR."
   
        type_modal = ""
        modal_code = ""
        otype = ""
        modal_sigla = ""
        
        for modal_entry in lst.modal:
            if isinstance(modal_entry, dict) and modal_entry["TIPO_MODAL"] == tipo_tarifa:
                type_modal = modal_entry["TIPO_MODAL"]
                modal_code = modal_entry["R_C_D"]
                otype = modal_entry["OFERRING_TYPE"]
                modal_sigla = modal_entry["SIGLA_MODAL"]
                break         
        
        modald_code = ''
        type_modald = ''
        modald_sigla = ''
                 
        for modal_dedicada in lst.modalDedicado:
            if isinstance(modal_dedicada, dict) and modal_dedicada["TIPO_MODAL"] == tipo_dedicada:
                modald_code = modal_dedicada["R_C_D"]
                type_modald = modal_dedicada["TIPO_MODAL"]
                modald_sigla = modal_dedicada["SIGLA_MODAL"]
                break 
               
        infos_dict = lst.infos[0]  # Acessando o único dicionário na lista
        infos7 = infos_dict.get("BRL") 
        infos11 = infos_dict.get("INTERVALO") 
        
        
        ref_dict = lst.refnum[0]  # Acessando o único dicionário na lista
        ref_tipo_tarifa = ref_dict.get("TIPO_TARIFA") 
        ref_operacao = ref_dict.get("OPERACAO") 
        ref_transp = ref_dict.get("TRANSPORTADORA")
        ref_id_origem = ref_dict.get("ID_ORIGEM")
        ref_id_destino = ref_dict.get("ID_DESTINO")
        ref_desc_origem = ref_dict.get("DESC_ORIGEM")
        ref_desc_destino = ref_dict.get("DESC_DESTINO")
        ref_tipo_dedicada = ref_dict.get("TIPO_DEDICADA")
        ref_gris = ref_dict.get("PORC_GRIS")
        ref_advalorem = ref_dict.get("PORC_AD_VALOREM")

        

        if (tipo_dedicada == type_modald and id_destino != ''):
            if modald_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},{domain3}{ref_id_destino},{id_destino},{domain1}" 
                unique_lines.add(formatted_line)
            
        if (tipo_tarifa == type_modal and id_destino != ''):
            if modal_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},{domain3}{ref_id_destino},{id_destino},{domain1}"
                unique_lines.add(formatted_line)
        
        if (tipo_dedicada == type_modald and descricao_destino != ''):
            if modald_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},{domain3}{ref_desc_destino},{descricao_destino},{domain1}" 
                unique_lines.add(formatted_line)
            
        if (tipo_tarifa == type_modal and descricao_destino != ''):
            if modal_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},{domain3}{ref_desc_destino},{descricao_destino},{domain1}"
                unique_lines.add(formatted_line)
        
        if (tipo_dedicada == type_modald and id_origem != ''):
            if modald_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},{domain3}{ref_id_origem},{id_origem},{domain1}" 
                unique_lines.add(formatted_line)
            
        if (tipo_tarifa == type_modal and id_origem != ''):
            if modal_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},{domain3}{ref_id_origem},{id_origem},{domain1}"
                unique_lines.add(formatted_line)
            
        if (tipo_dedicada == type_modald and descricao_origem != ''):
            if modald_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},{domain3}{ref_desc_origem},{descricao_origem},{domain1}" 
                unique_lines.add(formatted_line)
            
        if (tipo_tarifa == type_modal and descricao_origem != ''):
            if modal_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},{domain3}{ref_desc_origem},{descricao_origem},{domain1}"      
                unique_lines.add(formatted_line)
            
        if (tipo_dedicada == type_modald and operacao != ''):  
            if modald_sigla:  
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},{domain3}{ref_operacao},{operacao},{domain1}" 
                unique_lines.add(formatted_line)
            
        if (tipo_tarifa == type_modal and operacao != ''):
            if modal_sigla:    
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},{domain3}{ref_operacao},{operacao},{domain1}"   
                unique_lines.add(formatted_line)
            
        if (tipo_dedicada == type_modald and ad_valorem != ''): 
            if modald_sigla:   
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},{domain3}{ref_advalorem},{ad_valorem},{domain1}"     
                unique_lines.add(formatted_line)
            
        if (tipo_tarifa == type_modal and ad_valorem != ''):
            if modal_sigla:    
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},{domain3}{ref_advalorem},{ad_valorem},{domain1}"         
                unique_lines.add(formatted_line)
            
        # if (tipo_dedicada == type_modald and gris not in ['', "0.00", "0"]):    
        #     formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},{domain3}{ref_gris},{porcent_gris},{domain1}"     
        #     unique_lines.add(formatted_line)
            
        # if (tipo_tarifa == type_modal and gris not in ['', "0.00", "0"]):    
        #     formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},{domain3}{ref_gris},{porcent_gris},{domain1}"     
        #     unique_lines.add(formatted_line)
            
        if (tipo_dedicada == type_modald): 
            if modald_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},{domain3}{ref_tipo_tarifa},{tipo_tarifa},{domain1}"     
                unique_lines.add(formatted_line)
            
        if (tipo_tarifa == type_modal):  
            if modal_sigla:  
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},{domain3}{ref_tipo_tarifa},{tipo_tarifa},{domain1}"   
                unique_lines.add(formatted_line)
            
        if (tipo_dedicada == type_modald and tipo_tarifa == "FROTA DEDICADA" and tipo_dedicada != ''):
            if modald_sigla:    
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},{domain3}{ref_tipo_dedicada},{tipo_dedicada},{domain1}"       
                unique_lines.add(formatted_line)
            
        if (tipo_dedicada == type_modald and code_trp not in ['', "0.00", "0"]): 
            if modald_sigla:   
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},{domain3}{ref_transp},{code_trp},{domain1}"     
                unique_lines.add(formatted_line)
            
        if (tipo_tarifa == type_modal and code_trp not in ['', "0.00", "0"]): 
            if modal_sigla:   
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},{domain3}{ref_transp},{code_trp},{domain1}"   
                unique_lines.add(formatted_line) 
        

    # Ordenar as linhas únicas pelo penúltimo campo
    def get_penultimate_field(formatted_line):
        # Divide a string no separador de campo por vírgula e retire o penúltimo campo
        return formatted_line.split(',')[-3].strip()

    sorted_unique_lines = sorted(unique_lines, key=get_penultimate_field)
    
    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + sorted_unique_lines
    # final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')

    print(f"Arquivo 012_RATE_GEO_REFNUM_I.csv salvo com sucesso.")
    return 

def create_csv_013(df): # 013_RG_SPECIAL_SERVICE_I
    global zone
    output_path = os.path.join(output_folder_path, "013_RG_SPECIAL_SERVICE_I.csv")

    # Criar as linhas padrão
    lines = [
        "RG_SPECIAL_SERVICE",
        "RATE_GEO_GID,SPECIAL_SERVICE_GID,DOMAIN_NAME",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
    
    unique_lines = set()
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
        code_trp = row.iloc[col_idx['COD_TRANSPORTADORA']]
        tipo_tarifa = row.iloc[col_idx['TIPO_DE_TARIFA']]
        origem = row.iloc[col_idx['ZONA_DE_TRANSPORTE_ORIGEM']]
        data_criacao = convert_date_format(row.iloc[col_idx['DATA_DE_INICIO']])
        data_expiracao = convert_date_format(row.iloc[col_idx['DATA_DE_EXPIRACAO']])
        destino = row.iloc[col_idx['ZONA_DE_TRANSPORTE_DESTINO']]
        equipamento = row.iloc[col_idx['PERFIL_GRUPO_DE_EQUIPAMENTO']]
 
        domain1 = lst.domain[0]  # "NTR/BR."
        domain2 = lst.domain[1]  # "NTR/BR"
        domain3 = lst.domain[2]  # "NTR/BR"  
  
        valor_expresso = "" # VER TABELA DADOS_RATE_AEREO
                     
        infos_dict = lst.infos[0]  # Acessando o único dicionário na lista
        infos16 = infos_dict.get("EXPRESSO")
        
        
        modal_code = ''
        type_modal = ''
        modal_sigla = ''
                
        for modal_entry in lst.modal:
            if isinstance(modal_entry, dict) and modal_entry["TIPO_MODAL"] == tipo_tarifa:
                modal_code = modal_entry["R_C_D"]
                type_modal = modal_entry["TIPO_MODAL"]
                modal_sigla = modal_entry["SIGLA_MODAL"]
                break

        if tipo_tarifa != "" and valor_expresso != "":
            formatted_line = f"{domain1}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_E_{equipamento},{domain3}{infos16},{domain2}"  
            unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto

    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')

    print(f"Arquivo 013_RG_SPECIAL_SERVICE_I.csv salvo com sucesso.")
    return 

def create_csv_014(df): #014_RATE_GEO_COST_GROUP_I
    output_path = os.path.join(output_folder_path, "014_RATE_GEO_COST_GROUP_I.csv")

    # Criar as linhas padrão
    lines = [
        "RATE_GEO_COST_GROUP",
        "RATE_GEO_COST_GROUP_GID,RATE_GEO_COST_GROUP_XID,RATE_GEO_GID,RATE_GEO_COST_GROUP_SEQ,MULTI_RATES_RULE,DOMAIN_NAME",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
    
    unique_lines = set()
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
        # Extraindo os valores das colunas G e I usando iloc
        code_trp = row.iloc[col_idx['COD_TRANSPORTADORA']]
        tipo_tarifa = row.iloc[col_idx['TIPO_DE_TARIFA']]
        tipo_dedicada = row.iloc[col_idx['TIPO_DE_DEDICADA']]
        origem = row.iloc[col_idx['ZONA_DE_TRANSPORTE_ORIGEM']]
        destino = row.iloc[col_idx['ZONA_DE_TRANSPORTE_DESTINO']]
        equipamento = row.iloc[col_idx['PERFIL_GRUPO_DE_EQUIPAMENTO']]
        data_criacao = convert_date_format(row.iloc[col_idx['DATA_DE_INICIO']])
        data_expiracao = convert_date_format(row.iloc[col_idx['DATA_DE_EXPIRACAO']])

        
        domain1 = lst.domain[0]  # "NTR/BR."
        domain2 = lst.domain[1]  # "NTR/BR"

        
        modal_code = ""
        type_modal = ''
        modal_sigla = ''
        
        for modal_entry in lst.modal:
            if isinstance(modal_entry, dict) and modal_entry["TIPO_MODAL"] == tipo_tarifa:
                modal_code = modal_entry["R_C_D"]
                type_modal = modal_entry["TIPO_MODAL"]
                modal_sigla = modal_entry["SIGLA_MODAL"]
                break 
        
        modald_code = ''
        type_modald = ''
        modald_sigla = ''
            
        for modal_dedicada in lst.modalDedicado:
            if isinstance(modal_dedicada, dict) and modal_dedicada["TIPO_MODAL"] == tipo_dedicada:
                modald_code = modal_dedicada["R_C_D"]
                type_modald = modal_dedicada["TIPO_MODAL"]
                modald_sigla = modal_dedicada["SIGLA_MODAL"]
                break 
            
        
        if (tipo_dedicada == type_modald):
            if modald_sigla: 
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},"\
                                f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},1,,{domain1}"
                unique_lines.add(formatted_line)
            
        if (tipo_tarifa == type_modal):
            if modal_sigla: 
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},"\
                                f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},1,A,{domain1}"    
                unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto

    def get_penultimate_field(formatted_line):
        # Divide a string no separador de campo por vírgula e retire o penúltimo campo
        return formatted_line.split(',')[-4].strip()

    sorted_unique_lines = sorted(unique_lines, key=get_penultimate_field)
    
    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + sorted_unique_lines
    # final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')
    print(f"Arquivo 014_RATE_GEO_COST_GROUP_I.csv salvo com sucesso.")
    return 

def create_csv_015(df): #015_RATE_GEO_COST_I
    output_path = os.path.join(output_folder_path, "015_RATE_GEO_COST_I.csv")

    # Criar as linhas padrão
    lines = [
        "RATE_GEO_COST",
        "RATE_GEO_COST_GROUP_GID,RATE_GEO_COST_SEQ,OPER1_GID,LEFT_OPERAND1,LOW_VALUE1,AND_OR1,OPER2_GID,LEFT_OPERAND2,LOW_VALUE2,AND_OR2,OPER3_GID,LEFT_OPERAND3,LOW_VALUE3,AND_OR3,OPER4_GID,LEFT_OPERAND4,LOW_VALUE4,CHARGE_AMOUNT,CHARGE_MULTIPLIER_SCALAR,CHARGE_ACTION,CHARGE_CURRENCY_GID,CHARGE_UNIT_UOM_CODE,CHARGE_UNIT_COUNT,CHARGE_MULTIPLIER,CHARGE_BREAK_COMPARATOR,COST_TYPE,RATE_UNIT_BREAK_PROFILE_GID,COST_CATEGORY_GID,DOMAIN_NAME",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
    
    unique_lines = set()
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
        # Extraindo os valores das colunas G e I usando iloc
        code_trp = row.iloc[col_idx['COD_TRANSPORTADORA']]
        nome_trp = row.iloc[col_idx['NOME_TRANSPORTADORA']]
        tipo_tarifa = row.iloc[col_idx['TIPO_DE_TARIFA']]
        tipo_dedicada = row.iloc[col_idx['TIPO_DE_DEDICADA']]
        porcentagem_ida = row.iloc[col_idx['%_DO_TRAJETO_DA_FD']]
        operacao = row.iloc[col_idx['OPERACAO']]
        origem = row.iloc[col_idx['ZONA_DE_TRANSPORTE_ORIGEM']]
        descricao_origem = row.iloc[col_idx['DESCRICAO_ZONA_DE_TRANSPORTE_ORIGEM']]
        destino = row.iloc[col_idx['ZONA_DE_TRANSPORTE_DESTINO']]
        descricao_destino = row.iloc[col_idx['DESCRICAO_ZONA_DE_TRANSPORTE_DESTINO']]
        equipamento = row.iloc[col_idx['PERFIL_GRUPO_DE_EQUIPAMENTO']]
        descricao_equipamento = row.iloc[col_idx['DESCRICAO_GRUPO_DE_EQUIPAMENTO']]
        custo_base = row.iloc[col_idx['CUSTO_BASE']]
        abast_cds = row.iloc[col_idx['ABASTECIMENTO_CDS']]
        redespacho = row.iloc[col_idx['REDESPACHO']]
        revista = row.iloc[col_idx['REVISTA']]
        ajudante = row.iloc[col_idx['AJUDANTE']]
        pedagio = str(row.iloc[col_idx['PEDAGIO']]).replace(",", ".") if pd.notna(row.iloc[col_idx['PEDAGIO']]) else ""
        valor_de_contrato = row.iloc[col_idx['VALOR_DE_CONTRATO']]
        nro_veiculos = row.iloc[col_idx['NRO_DE_VEICULOS']]
        tarifa_preferencial = row.iloc[col_idx['TARIFA_PREFERENCIAL']]
        data_criacao = convert_date_format(row.iloc[col_idx['DATA_DE_INICIO']])
        data_expiracao = convert_date_format(row.iloc[col_idx['DATA_DE_EXPIRACAO']])
        nro_coletas = row.iloc[col_idx['NRO_COLETAS']]
        nro_entregas = row.iloc[col_idx['NRO_ENTREGAS']]

        
        domain1 = lst.domain[0]  # Isso retorna "NTR/BR"
        domain2 = lst.domain[1]  # Isso retorna "NTR/BR."
        infos_dict = lst.infos[0]  # Acessando o único dicionário na lista
        infos7 = infos_dict.get("BRL") 
        
        modal_code = ''
        type_modal = ''
        modal_sigla = ''
        
        for modal_entry in lst.modal:
            if isinstance(modal_entry, dict) and modal_entry["TIPO_MODAL"] == tipo_tarifa:
                modal_code = modal_entry["R_C_D"]
                type_modal = modal_entry["TIPO_MODAL"]
                modal_sigla = modal_entry["SIGLA_MODAL"]
                break 
         
        modald_code = ''
        type_modald = ''
        modald_sigla = ''
            
        for modal_dedicada in lst.modalDedicado:
            if isinstance(modal_dedicada, dict) and modal_dedicada["TIPO_MODAL"] == tipo_dedicada:
                modald_code = modal_dedicada["R_C_D"]
                type_modald = modal_dedicada["TIPO_MODAL"]
                modald_sigla = modal_dedicada["SIGLA_MODAL"]
                break 
        
        shipment = ''
        type_tariff = ''
            
        for shipment_entry in lst.tarifas_shipment:
            if shipment_entry["TIPO_DE_TARIFA"] == tipo_tarifa:
                shipment = shipment_entry["SHIPMENT"]
                type_tariff = shipment_entry["TIPO_DE_TARIFA"]
                break 
        
        ajudante_dict = lst.ajudante[0] 
        ajudante_cod = ajudante_dict.get("COD")
        ajudante_nome = ajudante_dict.get("NOME")
        ajudante_oper1 = ajudante_dict.get("OPER1_GID")
        ajudante_left_operand1 = ajudante_dict.get("LEFT_OPERAND1")
        ajudante_low_value1 = ajudante_dict.get("LOW_VALUE1")
        ajudante_por = ajudante_dict.get("POR")
        ajudante_cost = ajudante_dict.get("COST_CATEGORY_GID")
        ajudante_acessorial = ajudante_dict.get("ACCESSORIAL_CODE")
        ajudante_ctype = ajudante_dict.get("COST_TYPE")
        
        costc_dict = lst.aux_geo_cost_c[0]
        costc_op1 = costc_dict.get("OPER1_GID")
        costc_operand1 = costc_dict.get("LEFT_OPERAND1")
        costc_low_value = costc_dict.get("LOW_VALUE1")
        costc_or1 = costc_dict.get("AND_OR1")
        costc_op2 = costc_dict.get("OPER2_GID")
        costc_operand2 = costc_dict.get("LEFT_OPERAND2")
        costc_low_value2 = costc_dict.get("LOW_VALUE2")
        costc_or2 = costc_dict.get("AND_OR2")
        costc_op3 = costc_dict.get("OPER3_GID")
        costc_operand3 = costc_dict.get("LEFT_OPERAND3")
        costc_low_value3 = costc_dict.get("LOW_VALUE3")
        costc_or3 = costc_dict.get("AND_OR3")
        costc_op4 = costc_dict.get("OPER4_GID")
        costc_operand4 = costc_dict.get("LEFT_OPERAND4")
        costc_low_value4 = costc_dict.get("LOW_VALUE4")
        costc_currency = costc_dict.get("CHARGE_CURRENCY_GID")
        costc_unit = costc_dict.get("CHARGE_UNIT_COUNT")
        costc_multiplier = costc_dict.get("CHARGE_MULTIPLIER")
        costc_ctype = costc_dict.get("COST_TYPE")

        coste_dict = lst.aux_geo_cost_e[0]
        coste_op1 = coste_dict.get("OPER1_GID")
        coste_operand1 = coste_dict.get("LEFT_OPERAND1")
        coste_low_value1 = coste_dict.get("LOW_VALUE1")
        coste_or1 = coste_dict.get("AND_OR1")
        coste_op2 = coste_dict.get("OPER2_GID")
        coste_operand2 = coste_dict.get("LEFT_OPERAND2")
        coste_low_value2 = coste_dict.get("LOW_VALUE2")
        coste_or2 = coste_dict.get("AND_OR2")
        coste_op3 = coste_dict.get("OPER3_GID")
        coste_operand3 = coste_dict.get("LEFT_OPERAND3")
        coste_low_value3 = coste_dict.get("LOW_VALUE3")
        coste_or3 = coste_dict.get("AND_OR3")
        coste_op4 = coste_dict.get("OPER4_GID")
        coste_operand4 = coste_dict.get("LEFT_OPERAND4")
        coste_low_value4 = coste_dict.get("LOW_VALUE4")
        coste_currency = coste_dict.get("CHARGE_CURRENCY_GID")
        coste_unit = coste_dict.get("CHARGE_UNIT_COUNT")
        coste_multiplier = coste_dict.get("CHARGE_MULTIPLIER")
        coste_ctype = coste_dict.get("COST_TYPE")
               
        cost_mc_dict = lst.aux_geo_cost_mc[0]
        cost_mc_op1 = cost_mc_dict.get("OPER1_GID")
        cost_mc_operand1 = cost_mc_dict.get("LEFT_OPERAND1")
        cost_mc_low_value1 = cost_mc_dict.get("LOW_VALUE1")
        cost_mc_or1 = cost_mc_dict.get("AND_OR1")
        cost_mc_op2 = cost_mc_dict.get("OPER2_GID")
        cost_mc_operand2 = cost_mc_dict.get("LEFT_OPERAND2")
        cost_mc_low_value2 = cost_mc_dict.get("LOW_VALUE2")
        cost_mc_or2 = cost_mc_dict.get("AND_OR2")
        cost_mc_op3 = cost_mc_dict.get("OPER3_GID")
        cost_mc_operand3 = cost_mc_dict.get("LEFT_OPERAND3")
        cost_mc_low_value3 = cost_mc_dict.get("LOW_VALUE3")
        cost_mc_or3 = cost_mc_dict.get("AND_OR3")
        cost_mc_op4 = cost_mc_dict.get("OPER3_GID")
        cost_mc_operand4 = cost_mc_dict.get("LEFT_OPERAND3")
        cost_mc_low_value4 = cost_mc_dict.get("LOW_VALUE3")
        cost_mc_currency = cost_mc_dict.get("CHARGE_CURRENCY_GID")
        cost_mc_unit = cost_mc_dict.get("CHARGE_UNIT_COUNT")
        cost_mc_multiplier = cost_mc_dict.get("CHARGE_MULTIPLIER")
        cost_mc_ctype = cost_mc_dict.get("COST_TYPE")
        cost_mc_action = cost_mc_dict.get("CHARGE_ACTION")
        cost_mc_category = cost_mc_dict.get("COST_CATEGORY_GID")
        
        aux_desc_entrega = lst.aux_geo_cost_desc_entrega[0]
        desc_seq1 = aux_desc_entrega.get("SEQ1")
        desc_seq2 = aux_desc_entrega.get("SEQ2")
        desc_seq3 = aux_desc_entrega.get("SEQ3")
        desc_seq4 = aux_desc_entrega.get("SEQ4")
        desc_op1 = aux_desc_entrega.get("OPER1_GID")
        desc_operand1 = aux_desc_entrega.get("LEFT_OPERAND1")
        desc_low_value1 = aux_desc_entrega.get("LOW_VALUE1")
        desc_or1 = aux_desc_entrega.get("AND_OR1")
        desc_op2 = aux_desc_entrega.get("OPER2_GID")
        desc_operand2 = aux_desc_entrega.get("LEFT_OPERAND2")
        desc_low_value2 = aux_desc_entrega.get("LOW_VALUE2")
        desc_or2 = aux_desc_entrega.get("AND_OR2")
        desc_op3 = aux_desc_entrega.get("OPER3_GID")
        desc_operand3 = aux_desc_entrega.get("LEFT_OPERAND3")
        desc_low_value3 = aux_desc_entrega.get("LOW_VALUE3")
        desc_or3 = aux_desc_entrega.get("AND_OR3")
        desc_op4 = aux_desc_entrega.get("OPER4_GID")
        desc_operand4 = aux_desc_entrega.get("LEFT_OPERAND4")
        desc_low_value4 = aux_desc_entrega.get("LOW_VALUE4")
        desc_currency = aux_desc_entrega.get("CHARGE_CURRENCY_GID")
        desc_unit = aux_desc_entrega.get("CHARGE_UNIT_COUNT")
        desc_multiplier = aux_desc_entrega.get("CHARGE_MULTIPLIER")
        desc_ctype = aux_desc_entrega.get("COST_TYPE")

        help_dict = lst.aux_help[0]
        help_op1 = help_dict.get("OPER1_GID")
        help_operand1 = help_dict.get("LEFT_OPERAND1")
        help_low_value1 = help_dict.get("LOW_VALUE1")
        help_or1 = help_dict.get("AND_OR1")
        helpe_op2 = help_dict.get("OPER2_GID")
        help_operand2 = help_dict.get("LEFT_OPERAND2")
        help_low_value2 = help_dict.get("LOW_VALUE2")
        help_or2 = help_dict.get("AND_OR2")
        help_op3 = help_dict.get("OPER3_GID")
        help_operand3 = help_dict.get("LEFT_OPERAND3")
        help_low_value3 = help_dict.get("LOW_VALUE3")
        help_or3 = help_dict.get("AND_OR3")
        help_op4 = help_dict.get("OPER4_GID")
        help_operand4 = help_dict.get("LEFT_OPERAND4")
        help_low_value4 = help_dict.get("LOW_VALUE4")
        help_currency = help_dict.get("CHARGE_CURRENCY_GID")
        help_unit = help_dict.get("CHARGE_UNIT_COUNT")
        help_multiplier = help_dict.get("CHARGE_MULTIPLIER")
        help_ctype = help_dict.get("COST_TYPE")
        
        custo_consol = lst.custo_consolidado[0]
        custo_seq = custo_consol.get("RATE_GEO_COST_SEQ")
        custo_currency = custo_consol.get("CHARGE_CURRENCY_GID")
        custo_unit = custo_consol.get("CHARGE_UNIT_COUNT")
        custo_multiplier = custo_consol.get("CHARGE_MULTIPLIER")
        custo_stop = custo_consol.get("CHARGE_STOP")
        custo_ctype = custo_consol.get("COST_TYPE")
        
        # unit_entry = lst.unit[0]
        # unit_seq = unit_entry.get("SEQ")
        # unit_unit = unit_entry.get("UNIDADE")
        
        for unit_entry in lst.unit:
            if unit_entry["UNIDADE"] == "FIXO":
                unit_seq = unit_entry["SEQ"]
                unit_unit = unit_entry["UNIDADE"]
                break
     
        pares_origem_destino = [
            ("SP0388800", "AL0055005"),
            ("SP0388800", "BA0307005"),
            ("SP0388800", "PA0024005"),
            ("SP0388800", "AM1302606"),
            ("AL0055005", "SP0388800"),
            ("BA0307005", "SP0388800"),
            ("PA0024005", "SP0388800"),
            ("AM1302606", "SP0388800"),
        ]
        
        
        if (tipo_tarifa == type_modal and abast_cds != '' and tipo_tarifa not in ["DIRETO", "CABOTAGEM", "REDESPACHO"] and (origem, destino) not in pares_origem_destino):
            if modal_sigla:
                if nro_coletas > 1:
                    formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},10,{costc_op1},{costc_operand1},{costc_low_value},{costc_or1},"\
                                    f"{costc_op2},{costc_operand2},{nro_coletas},{costc_or2},{costc_op3},{costc_operand3},{costc_low_value3},{costc_or3},{costc_op4},{costc_operand4},"\
                                    f"ABASTECIMENTO_CDS,{abast_cds},,,{costc_currency},,{costc_unit},{costc_multiplier},,{costc_ctype},,,{domain1}"
                    unique_lines.add(formatted_line)
                elif nro_entregas > 1:
                    formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},20,{coste_op1},{coste_operand1},{nro_entregas},{coste_or1},"\
                                    f"{coste_op2},{coste_operand2},ABASTECIMENTO_CDS,{coste_or2},{coste_op3},{coste_operand3},{coste_low_value3},{coste_or3},{coste_op4},{coste_operand4},"\
                                    f"{coste_low_value4},{abast_cds},,,{coste_currency},,{coste_unit},{coste_multiplier},,{coste_ctype},,,{domain1}"
                    unique_lines.add(formatted_line)
                     
                              
        if (tipo_tarifa == type_modal and tipo_tarifa not in ["DIRETO", "CABOTAGEM", "REDESPACHO"] and custo_base != ''):
            if modal_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},{custo_seq},,,,,,,,,,,,,,,,"\
                                f"{custo_base if tipo_tarifa == "CONSOLIDADO" else ''},,,{custo_currency},,{custo_unit},{custo_multiplier},,{custo_ctype},,,{domain1}"
                unique_lines.add(formatted_line)
       
        if (tipo_dedicada == type_modald and tipo_tarifa == type_tariff and unit_unit == "FIXO"):
            if modald_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},{unit_seq},,,,,,,,,,,,,,,,"\
                                f"{custo_base},,,{infos7},{'KM' if tipo_tarifa == "FROTA DEDICADA" else ''},1,{shipment},,{custo_ctype},,,{domain1}"
                unique_lines.add(formatted_line)
                                                                                             
        if (tipo_tarifa == type_modal and revista != ''):
            if modal_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},12,{costc_op1},{costc_operand1},{costc_low_value},{costc_or1},"\
                                f"{costc_op2},{costc_operand2},{costc_low_value2},{costc_or2},{costc_op3},{costc_operand3},{costc_low_value3},{costc_or3},{costc_op4},{costc_operand4},"\
                                f"REVISTA,{revista},,,{costc_currency},,{costc_unit},{costc_multiplier},,{costc_ctype},,,{domain1}" 
                unique_lines.add(formatted_line)               
              
        if (tipo_tarifa == type_modal and tipo_tarifa in ['CABOTAGEM', 'DIRETO', 'RODOVIARIO', "REDESPACHO"] and tipo_tarifa == type_tariff):
            if modal_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},3,,,,,"\
                                f",,,,,,,,,,,"\
                                f"{custo_base},,,{infos7},{'KM' if tipo_tarifa == "FORTA DEDICADA" else ''},1,{shipment},,C,,,{domain1}"
                unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto
        
        # if (tipo_tarifa == type_modal and desconto_mc != ''):
        #     if modal_sigla:
        #         formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},99,{cost_mc_op1},{cost_mc_operand1},{cost_mc_low_value1},{cost_mc_or1},"\
        #                         f"{cost_mc_op2},{cost_mc_operand2},{cost_mc_low_value2},{cost_mc_or2},{cost_mc_op3},{cost_mc_operand3},{cost_mc_low_value3},{cost_mc_or3},{cost_mc_op4},{cost_mc_operand4},{cost_mc_low_value4},"\
        #                         f",,{desconto_mc},{cost_mc_action},{cost_mc_currency},,{cost_mc_unit},{cost_mc_multiplier},,{cost_mc_ctype},,{cost_mc_category},{domain1}"
        #         unique_lines.add(formatted_line)          

    def get_penultimate_field(formatted_line):
        # Divide a string no separador de campo por vírgula e retire o penúltimo campo
        return formatted_line.split(',')[-6].strip()

    sorted_unique_lines = sorted(unique_lines, key=get_penultimate_field)
    
    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + sorted_unique_lines
    # final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')

    print(f"Arquivo 015_RATE_GEO_COST_I.csv salvo com sucesso.")
    return 

def create_csv_016(df): # 016_RATE_GEO_COST_UNIT_BREAK_I ***** TABELA DADOS_RATE_AEREO ****
    output_path = os.path.join(output_folder_path, "016_RATE_GEO_COST_UNIT_BREAK_I.csv")

    # Criar as linhas padrão
    lines = [
        "RATE_GEO_COST_UNIT_BREAK",
        "RATE_GEO_COST_GROUP_GID,RATE_GEO_COST_SEQ,RATE_UNIT_BREAK_GID,RATE_UNIT_BREAK2_GID,CHARGE_AMOUNT,CHARGE_AMOUNT_GID,DOMAIN_NAME",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
    
    unique_lines = set()
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
        # Extraindo os valores das colunas G e I usando iloc
        # code_trp = row.iloc[col_idx['COD_TRANSPORTADORA']]
        # nome_trp = row.iloc[col_idx['NOME_TRANSPORTADORA']]
        tipo_tarifa = row.iloc[col_idx['TIPO_DE_TARIFA']]
        # tipo_dedicada = row.iloc[col_idx['TIPO_DE_DEDICADA']]
        # porcentagem_ida = row.iloc[col_idx['%_DO_TRAJETO_DA_FD']]
        # operacao = row.iloc[col_idx['OPERACAO']]
        # origem = row.iloc[col_idx['ZONA_DE_TRANSPORTE_ORIGEM']]
        # descricao_origem = row.iloc[col_idx['DESCRICAO_ZONA_DE_TRANSPORTE_ORIGEM']]
        # destino = row.iloc[col_idx['ZONA_DE_TRANSPORTE_DESTINO']]
        # descricao_destino = row.iloc[col_idx['DESCRICAO_ZONA_DE_TRANSPORTE_DESTINO']]
        # equipamento = row.iloc[col_idx['PERFIL_GRUPO_DE_EQUIPAMENTO']]
        # descricao_equipamento = row.iloc[col_idx['DESCRICAO_GRUPO_DE_EQUIPAMENTO']]
        # custo_base = row.iloc[col_idx['CUSTO_BASE']]
        # abast_cds = row.iloc[col_idx['ABASTECIMENTO_CDS']]
        # revista = row.iloc[col_idx['REVISTA']]
        # ajudante = row.iloc[col_idx['AJUDANTE']]
        # pedagio = str(row.iloc[col_idx['PEDAGIO']]).replace(",", ".") if pd.notna(row.iloc[col_idx['PEDAGIO']]) else ""
        # valor_de_contrato = row.iloc[col_idx['VALOR_DE_CONTRATO']]
        # nro_veiculos = row.iloc[col_idx['NRO_DE_VEICULOS']]
        # tarifa_preferencial = row.iloc[col_idx['TARIFA_PREFERENCIAL']]
        # data_criacao = convert_date_format(row.iloc[col_idx['DATA_DE_INICIO']])
        # data_expiracao = convert_date_format(row.iloc[col_idx['DATA_DE_EXPIRACAO']])
        # nro_coletas = row.iloc[col_idx['NRO_COLETAS']]
        # nro_entregas = row.iloc[col_idx['NRO_ENTREGAS']]

        
        domain1 = lst.domain[0]  # Isso retorna "NTR/BR"
        domain2 = lst.domain[1]  # Isso retorna "NTR/BR."
        
        infos_dict = lst.infos[0]  # Acessando o único dicionário na lista
        infos7 = infos_dict.get("BRL") 
        
        modal_code = ''
        type_modal = ''
        modal_sigla = ''
        
        for modal_entry in lst.modal:
            if isinstance(modal_entry, dict) and modal_entry["TIPO_MODAL"] == tipo_tarifa:
                modal_code = modal_entry["R_C_D"]
                type_modal = modal_entry["TIPO_MODAL"]
                modal_sigla = modal_entry["SIGLA_MODAL"]
                break 
         
        modald_code = ''
        type_modald = ''
        modald_sigla = ''
            
        for modal_dedicada in lst.modalDedicado:
            if isinstance(modal_dedicada, dict) and modal_dedicada["TIPO_MODAL"] == tipo_tarifa:
                modald_code = modal_dedicada["R_C_D"]
                type_modald = modal_dedicada["TIPO_MODAL"]
                modald_sigla = modal_dedicada["SIGLA_MODAL"]
                break 
        
        shipment = ''
        type_tariff = ''
            
        for shipment_entry in lst.tarifas_shipment:
            if shipment_entry["TIPO_DE_TARIFA"] == tipo_tarifa:
                shipment = shipment_entry["SHIPMENT"]
                type_tariff = shipment_entry["TIPO_DE_TARIFA"]
                break 
        
        
        unidade =''
           
        unit_dict = lst.unit[0]  # Acessando o único dicionário na lista
        unidade = unit_dict.get("UNIDADE") 
        
        
        formatted_line = ''
        unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto

    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')

    print(f"Arquivo 016_RATE_GEO_COST_UNIT_BREAK_I.csv salvo com sucesso.")
    return 

def create_csv_017(df): #017_ACCESSORIAL_COST_IU
    output_path = os.path.join(output_folder_path, "017_ACCESSORIAL_COST_IU.csv")

    # Criar as linhas padrão
    lines = [
        "ACCESSORIAL_COST",
        "ACCESSORIAL_COST_GID,ACCESSORIAL_COST_XID,LEFT_OPERAND1,OPER1_GID,LOW_VALUE1,AND_OR1,LEFT_OPERAND2,OPER2_GID,LOW_VALUE2,AND_OR2,LEFT_OPERAND3,OPER3_GID,LOW_VALUE3,CHARGE_MULTIPLIER,CHARGE_AMOUNT,CHARGE_AMOUNT_GID,CHARGE_UNIT_COUNT,CHARGE_BREAK_COMPARATOR,COST_CATEGORY_GID,IS_ACTIVE,RATE_UNIT_BREAK_PROFILE_GID,DOMAIN_NAME,COST_TYPE",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
    
    unique_lines = set()
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
        # Extraindo os valores das colunas G e I usando iloc
        code_trp = row.iloc[col_idx['COD_TRANSPORTADORA']]
        nome_trp = row.iloc[col_idx['NOME_TRANSPORTADORA']]
        tipo_tarifa = row.iloc[col_idx['TIPO_DE_TARIFA']]
        tipo_dedicada = row.iloc[col_idx['TIPO_DE_DEDICADA']]
        porcentagem_ida = row.iloc[col_idx['%_DO_TRAJETO_DA_FD']]
        operacao = row.iloc[col_idx['OPERACAO']]
        origem = row.iloc[col_idx['ZONA_DE_TRANSPORTE_ORIGEM']]
        descricao_origem = row.iloc[col_idx['DESCRICAO_ZONA_DE_TRANSPORTE_ORIGEM']]
        destino = row.iloc[col_idx['ZONA_DE_TRANSPORTE_DESTINO']]
        descricao_destino = row.iloc[col_idx['DESCRICAO_ZONA_DE_TRANSPORTE_DESTINO']]
        equipamento = row.iloc[col_idx['PERFIL_GRUPO_DE_EQUIPAMENTO']]
        descricao_equipamento = row.iloc[col_idx['DESCRICAO_GRUPO_DE_EQUIPAMENTO']]
        custo_base = row.iloc[col_idx['CUSTO_BASE']]
        abastecimento_cds = row.iloc[col_idx['ABASTECIMENTO_CDS']]
        redespacho = row.iloc[col_idx['REDESPACHO']]
        revista = row.iloc[col_idx['REVISTA']]
        ajudante = row.iloc[col_idx['AJUDANTE']]
        ad_valorem = row.iloc[col_idx['PORCENTAGEM_AD_VALOREM']]
        vlr_pedagio = str(row.iloc[col_idx['PEDAGIO']]).replace(",", ".") if pd.notna(row.iloc[col_idx['PEDAGIO']]) else ""
        valor_de_contrato = row.iloc[col_idx['VALOR_DE_CONTRATO']]
        nro_veiculos = row.iloc[col_idx['NRO_DE_VEICULOS']]
        tarifa_preferencial = row.iloc[col_idx['TARIFA_PREFERENCIAL']]
        data_criacao = convert_date_format(row.iloc[col_idx['DATA_DE_INICIO']])
        data_expiracao = convert_date_format(row.iloc[col_idx['DATA_DE_EXPIRACAO']])
        nro_coletas = row.iloc[col_idx['NRO_COLETAS']]
        nro_entregas = row.iloc[col_idx['NRO_ENTREGAS']]

        
        
        domain1 = lst.domain[0]  # Isso retorna "NTR/BR"
        domain2 = lst.domain[1]  # Isso retorna "NTR/BR."
        domain3 = lst.domain[2]  # Isso retorna "NTR/BR."

        gris_dict = lst.gris[0]
        gris_cod = gris_dict.get("COD")
        gris_por = gris_dict.get("POR")
        gris_category_gid = gris_dict.get("COST_CATEGORY_GID")
        gris_cost_type = gris_dict.get("COST_TYPE")
        
        # advalorem_dict = lst.advalorem[0]
        # advalorem_cod = advalorem_dict.get("COD")
        # advalorem_nome = advalorem_dict.get("NOME")
        # advalorem_por = advalorem_dict.get("POR")
        # advalorem_cost = advalorem_dict.get("COST_CATEGORY_GID")
        # advalorem_acessorial = advalorem_dict.get("ACESSORIAL_CODE")
        # advalorem_ctype = advalorem_dict.get("COST_TYPE")
        
        advalorem_cod = lst.advalorem[0] # "AD"
        advalorem_nome = lst.advalorem[1] #"AD VALOREM"
        advalorem_por = lst.advalorem[2] #"SHIPMENT"
        advalorem_cost = lst.advalorem[3] #"ACCESSORIAL"
        advalorem_acessorial = lst.advalorem[4] #"AD_VALOREM"
        advalorem_ctype = lst.advalorem[5] #"C"
        
        custof_dict = lst.custo_fixo[0] 
        custof_cod = custof_dict.get("COD")
        custof_por = custof_dict.get("POR")
        custof_cost = custof_dict.get("COST_CATEGORY_GID")
        custof_acessorial = custof_dict.get("ACCESSORIAL_CODE")
        custof_ctype = custof_dict.get("COST_TYPE")
        
        ajudante_dict = lst.ajudante[0] 
        ajudante_cod = ajudante_dict.get("COD")
        ajudante_nome = ajudante_dict.get("NOME")
        ajudante_left_operand1 = ajudante_dict.get("LEFT_OPERAND1")
        ajudante_oper1 = ajudante_dict.get("OPER1_GID")
        ajudante_lowvalue1 = ajudante_dict.get("LOW_VALUE1")
        ajudante_por = ajudante_dict.get("POR")
        ajudante_cost = ajudante_dict.get("COST_CATEGORY_GID")
        ajudante_acessorial = ajudante_dict.get("ACCESSORIAL_CODE")
        ajudante_ctype = ajudante_dict.get("COST_TYPE")
        ajudante_shipment = ajudante_dict.get("COD_SHIPMENT")
        
        rep_dict = lst.repaletizacao[0]
        rep_cod = rep_dict.get("COD")
        rep_nome = rep_dict.get("NOME")
        rep_por = rep_dict.get("POR")
        rep_category = rep_dict.get("COST_CATEGORY_GID")
        rep_accessorial = rep_dict.get("ACCESSORIAL_CODE")
        rep_operand1 = rep_dict.get("LEFT_OPERAND1")
        rep_oper1 = rep_dict.get("OPER1_GID")
        rep_low_value1 = rep_dict.get("LOW_VALUE1")
        rep_and_or1 = rep_dict.get("AND_OR1")
        rep_operand2 = rep_dict.get("LEFT_OPERAND2")
        rep_oper2 = rep_dict.get("OPER2_GID")
        rep_low_value2 = rep_dict.get("LOW_VALUE2")
        rep_and_or2 = rep_dict.get("AND_OR2")
        rep_operand3 = rep_dict.get("LEFT_OPERAND3")
        rep_oper3 = rep_dict.get("OPER3_GID")  # Corrigido aqui
        rep_low_value3 = rep_dict.get("LOW_VALUE3")
        rep_c_type = rep_dict.get("COST_TYPE")
        rep_multiplier = rep_dict.get("CHARGE_MULTIPLIER")
        rep_amount = rep_dict.get("CHARGE_AMOUNT_GID")
        rep_unit_count = rep_dict.get("CHARGE_UNIT_COUNT")
        rep_action = rep_dict.get("CHARGE_ACTION")
        rep_type = rep_dict.get("CHARGE_TYPE")
        rep_use_defaults = rep_dict.get("USE_DEFAULTS")
        rep_mult_option = rep_dict.get("CHARGE_MULTIPLIER_OPTION")
        rep_filed_tariff = rep_dict.get("IS_FILED_AS_TARIFF")
        rep_is_active = rep_dict.get("IS_ACTIVE")
        
        eixo_dict = lst.eixo[0]
        nome_eixo = eixo_dict.get("NOME")
        eixo_oper1_gid = eixo_dict.get("OPER1_GID")
        eixo_cod = eixo_dict.get("COD")
        eixo_por = eixo_dict.get("POR")
        eixo_left_operand1 = eixo_dict.get("LEFT_OPERAND1")
        eixo_low_value1 = eixo_dict.get("LOW_VALUE1")
        eixo_and_or1 = eixo_dict.get("AND_OR1")
        eixo_left_operand2 = eixo_dict.get("LEFT_OPERAND2")
        eixo_oper2_gid = eixo_dict.get("OPER2_GID")
        eixo_low_value2 = eixo_dict.get("LOW_VALUE2")
        eixo_and_or2 = eixo_dict.get("AND_OR2")
        eixo_left_operand3 = eixo_dict.get("LEFT_OPERAND3")
        eixo_opr3_gid = eixo_dict.get("OPR3_GID")
        eixo_low_value3 = eixo_dict.get("LOW_VALUE3")
        eixo_cost_category = eixo_dict.get("COST_CATEGORY_GID")
        eixo_acessorial_code = eixo_dict.get("ACESSORIAL_CODE")
        eixo_c_type = eixo_dict.get("COST_TYPE")
                
        infos_dict = lst.infos[0]  # Acessando o único dicionário na lista
        infos7 = infos_dict.get("BRL") 
        
        cost_category = lst.pedagio[3]
        
        modal_code = ""
        type_modal = ""
        modal_sigla = ""
        
        for modal_entry in lst.modal:
            if isinstance(modal_entry, dict) and modal_entry["TIPO_MODAL"] == tipo_tarifa:
                modal_code = modal_entry["R_C_D"]
                type_modal = modal_entry["TIPO_MODAL"]
                modal_sigla = modal_entry["SIGLA_MODAL"]
                break 
            
        modald_code =""
        type_modald = ""
        modald_sigla = ""
        
        for modal_dedicada in lst.modalDedicado:
            if isinstance(modal_dedicada, dict) and modal_dedicada["TIPO_MODAL"] == tipo_dedicada:
                modald_code = modal_dedicada["R_C_D"]
                type_modald = modal_dedicada["TIPO_MODAL"]
                modald_sigla = modal_dedicada["SIGLA_MODAL"]
                break 
        
        shipment= ""
           
        for shipment_entry in lst.tarifas_shipment:
            if shipment_entry["TIPO_DE_TARIFA"] == tipo_tarifa:
                shipment = shipment_entry["SHIPMENT"]
                break 
        
        
        cod_pedagio = lst.pedagio[0] # "PDG"
        cod_pedagio2 = lst.pedagio[2] # "SHIPMENT"
        cod_pedagio3 = lst.pedagio[3] # "ACCESSORIAL"
        cod_pedagio5 = lst.pedagio[5] # "C" 
        
        
        cod_parada = lst.parada[0] # "STP"
        cod_parada2 = lst.parada[2] # "SHIPMENT"
        cod_parada3 = lst.parada[3] # "ACCESSORIAL"
        cod_parada5 = lst.parada[5] # "C" 
 
        pares_origem_destino = [
            ("SP0388800", "AL0055005"),
            ("SP0388800", "BA0307005"),
            ("SP0388800", "PA0024005"),
            ("SP0388800", "AM1302606"),
            ("AL0055005", "SP0388800"),
            ("BA0307005", "SP0388800"),
            ("PA0024005", "SP0388800"),
            ("AM1302606", "SP0388800"),
        ]
        
        if tipo_tarifa == "CONSOLIDADO" and tipo_tarifa == type_modal and (origem, destino) in pares_origem_destino:
            if modal_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento}_{cod_parada},"\
                                f"{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento}_{cod_parada},"\
                                f",,,,,,,,,,,{cod_parada2},{abastecimento_cds},{infos7},1,,{domain2}{cod_parada3},Y,,{domain1},{cod_parada5}"
                unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto
               
        if tipo_tarifa == "CABOTAGEM" and tipo_tarifa == type_modal and redespacho not in ["", "0.00", "0", "0.0", 0.00, 0, 0.0]:
            if modal_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento}_{cod_parada},"\
                                f"{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento}_{cod_parada},"\
                                f",,,,,,,,,,,{cod_parada2},{redespacho},{infos7},1,,{domain2}{cod_parada3},Y,,{domain1},{cod_parada5}"
                unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto
           
        if tipo_dedicada == type_modald and vlr_pedagio not in ["", "0.00", "0", "0.0", 0.00, 0, 0.0]:                                       
            if modald_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento}_{cod_pedagio},"\
                                f"{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento}_{cod_pedagio},"\
                                f",,,,,,,,,,,{cod_pedagio2},{vlr_pedagio},{infos7},1,,{domain2}{cod_pedagio3},Y,,{domain1},{cod_pedagio5}"           
                unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto
        
        if tipo_tarifa in ["RODOVIARIO", "CONSOLIDADO", "CABOTAGEM", "DIRETO", "REDESPACHO"] and tipo_tarifa == type_modal and vlr_pedagio not in ["", "0.00", "0", "0.0", 0.00, 0, 0.0]:
            if modal_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento}_{cod_pedagio},"\
                                f"{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento}_{cod_pedagio},"\
                                f",,,,,,,,,,,{cod_pedagio2},{vlr_pedagio},{infos7},1,,{domain2}{cod_pedagio3},Y,,{domain1},{cod_pedagio5}"
                unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto
           
        if tipo_dedicada == type_modald and vlr_pedagio not in ["", "0.00", "0", "0.0", 0.00, 0, 0.0]:                                       
            if modald_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento}_{cod_pedagio},"\
                                f"{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento}_{cod_pedagio},"\
                                f",,,,,,,,,,,{cod_pedagio2},{vlr_pedagio},{infos7},1,,{domain2}{cod_pedagio3},Y,,{domain1},{cod_pedagio5}"           
                unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto
                                        
        if tipo_dedicada == type_modald and valor_de_contrato not in ["", "0.00", "0", "0.0", 0.00, 0, 0.0]:
            if modald_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento}_{custof_cod},"\
                                f"{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento}_{custof_cod},"\
                                f",,,,,,,,,,,{custof_por},,{infos7},1,,{domain2}{custof_cost},Y,,{domain1},{custof_ctype}"          
                unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto 
                
        if tipo_tarifa in ["RODOVIARIO", "CONSOLIDADO", "CABOTAGEM", "DIRETO", "REDESPACHO"] and tipo_tarifa  == type_modal and pd.notna(ajudante) and ajudante not in ["", "0.00", "0", "0.0", 0.00, 0, 0.0]:
            if modal_sigla:
                formatted_line = f"{domain2}{code_trp}_{ajudante_nome}_{modal_sigla},{code_trp}_{ajudante_nome}_{modal_sigla},"\
                                f"{ajudante_left_operand1},{ajudante_oper1},{ajudante_lowvalue1},,,,,,,,,{ajudante_por},{ajudante},{infos7},1,,{domain2}{ajudante_cost},"\
                                f"Y,,{domain1},{ajudante_ctype}"           
                unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto 
        
        if tipo_tarifa == type_modal and pd.notna(ad_valorem) and ad_valorem not in ["", "0.00", "0", "0.0", 0.00, 0, 0.0]:
            if modal_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento}_{advalorem_cod},"\
                                f"{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento}_{advalorem_cod},"\
                                f",,,,,,,,,,,{advalorem_por},{ad_valorem},{infos7},1,,{domain2}{advalorem_cost},N,,{domain1},{advalorem_ctype}"       
                unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto 
                          
        if tipo_dedicada == type_modald and ad_valorem not in ["", "0.00", "0", "0.0", 0.00, 0, 0.0]:
            if modald_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento}_{advalorem_cod},"\
                                f"{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento}_{advalorem_cod},"\
                                f",,,,,,,,,,,{advalorem_por},{ad_valorem},{infos7},1,,{domain2}{advalorem_cost},N,,{domain1},{advalorem_ctype}"         
                unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto 
                           
        def extract_relevant_field(formatted_line, identifiers):
            # Divide a string no separador de campo por vírgula
            fields = formatted_line.split('_')
            # Percorre os campos para encontrar o desejado, usando uma lista de possíveis identificadores
            for field in fields:
                for identifier in identifiers:
                    if identifier in field:
                        return field.strip()
            return ""

    # Identificadores que você está procurando
    identifiers = ["CTF", "PDG", "ADV", "AD", "STP", "PD", "CF", "SPO"]

    # Use a função de ordenação com os identificadores
    sorted_unique_lines = sorted(unique_lines, key=lambda line: extract_relevant_field(line, identifiers))
    
    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + sorted_unique_lines
    # final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')

    print(f"Arquivo 017_ACCESSORIAL_COST_IU.csv salvo com sucesso.")
    return 

def create_csv_018(df): #018_ACCESSORIAL_COST_UNIT_BREAK_IU
    output_path = os.path.join(output_folder_path, "018_ACCESSORIAL_COST_UNIT_BREAK_IU.csv")

    # Criar as linhas padrão
    lines = [
        "ACCESSORIAL_COST_UNIT_BREAK",
        "ACCESSORIAL_COST_GID,RATE_UNIT_BREAK_GID,RATE_UNIT_BREAK2_GID,CHARGE_AMOUNT,CHARGE_AMOUNT_GID,DOMAIN_NAME",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
    
    unique_lines = set()
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
    #     # Extraindo os valores das colunas G e I usando iloc
    #     data_criacao = row.iloc[32]
    #     data_expiracao = row.iloc[33] 
    #     data_criacao = convert_date_format(row['DATA_DE_INICIO'])
    #     data_expiracao = convert_date_format(row['DATA_DE_EXPIRACAO'])
        code_trp = row.iloc[0] # trp 
    #     origem = row.iloc[6] # Origem
    #     destino = row.iloc[8] # destino
    #     equipa = row.iloc[10]# Gruo Equipamento
        tarifa = row.iloc[2] # Tipo de Tarifa 
    #     custo = row.iloc[12] # Custo

        
    #     domain1 = lst.domain[0]  # Isso retorna "NTR/BR"
    #     domain2 = lst.domain[1]  # Isso retorna "NTR/BR."
    #     infos_dict = lst.infos[0]  # Acessando o único dicionário na lista
    #     infos7 = infos_dict.get("BRL") 
        
    #     modal_code = ""
    #     shipment= ""
    #     farma=""
        
        
    #     for modal_entry in lst.modal:
    #         if isinstance(modal_entry, dict) and modal_entry["TIPO_MODAL"] == tarifa:
    #             modal_code = modal_entry["R_C_D"]
    #             break 
            
    #     for shipment_entry in lst.tarifas_shipment:
    #         if shipment_entry["TIPO_DE_TARIFA"] == tarifa:
    #             shipment = shipment_entry["SHIPMENT"]
    #             break 
         
    #     rede = ""
        cod_trp = ""
    #     qtd_min = ""
    #     qtd_max = ""
    #     vlr_farma = ""
            
    if tarifa in ["RODOVIARIO", "CONSOLIDADO", "DIRETO", "REDESPACHO"] and  code_trp == cod_trp:
            formatted_line = '' #f"{domain2}{code_trp}_{rede},{domain2}{code_trp}_{rede}_{qtd_min}-{qtd_max},"\
                                #f"{domain2}{code_trp}_{rede}_{qtd_min}-{qtd_max},,{infos7},{domain1}"
            unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto
    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')

    print(f"Arquivo 018_ACCESSORIAL_COST_UNIT_BREAK_ UI.csv salvo com sucesso.")
    return 

def create_csv_019(df): #019_RATE_GEO_ACCESSORIAL_I
    output_path = os.path.join(output_folder_path, "019_RATE_GEO_ACCESSORIAL_I.csv")

    # Criar as linhas padrão
    lines = [
        "RATE_GEO_ACCESSORIAL",
        "ACCESSORIAL_COST_GID,RATE_GEO_GID,ACCESSORIAL_CODE_GID,DOMAIN_NAME",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
    
    unique_lines = set()
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
        # Extraindo os valores das colunas G e I usando iloc
        code_trp = row.iloc[col_idx['COD_TRANSPORTADORA']]
        nome_trp = row.iloc[col_idx['NOME_TRANSPORTADORA']]
        tipo_tarifa = row.iloc[col_idx['TIPO_DE_TARIFA']]
        tipo_dedicada = row.iloc[col_idx['TIPO_DE_DEDICADA']]
        porcentagem_ida = row.iloc[col_idx['%_DO_TRAJETO_DA_FD']]
        operacao = row.iloc[col_idx['OPERACAO']]
        origem = row.iloc[col_idx['ZONA_DE_TRANSPORTE_ORIGEM']]
        descricao_origem = row.iloc[col_idx['DESCRICAO_ZONA_DE_TRANSPORTE_ORIGEM']]
        destino = row.iloc[col_idx['ZONA_DE_TRANSPORTE_DESTINO']]
        descricao_destino = row.iloc[col_idx['DESCRICAO_ZONA_DE_TRANSPORTE_DESTINO']]
        equipamento = row.iloc[col_idx['PERFIL_GRUPO_DE_EQUIPAMENTO']]
        descricao_equipamento = row.iloc[col_idx['DESCRICAO_GRUPO_DE_EQUIPAMENTO']]
        custo_base = row.iloc[col_idx['CUSTO_BASE']]
        abastecimento_cds = row.iloc[col_idx['ABASTECIMENTO_CDS']]
        redespacho = row.iloc[col_idx['REDESPACHO']]
        revista = row.iloc[col_idx['REVISTA']]
        ajudante = row.iloc[col_idx['AJUDANTE']]
        ad_valorem = row.iloc[col_idx['PORCENTAGEM_AD_VALOREM']]
        pedagio = str(row.iloc[col_idx['PEDAGIO']]).replace(",", ".") if pd.notna(row.iloc[col_idx['PEDAGIO']]) else ""
        valor_de_contrato = row.iloc[col_idx['VALOR_DE_CONTRATO']]
        nro_veiculos = row.iloc[col_idx['NRO_DE_VEICULOS']]
        tarifa_preferencial = row.iloc[col_idx['TARIFA_PREFERENCIAL']]
        data_criacao = convert_date_format(row.iloc[col_idx['DATA_DE_INICIO']])
        data_expiracao = convert_date_format(row.iloc[col_idx['DATA_DE_EXPIRACAO']])
        nro_coletas = row.iloc[col_idx['NRO_COLETAS']]
        nro_entregas = row.iloc[col_idx['NRO_ENTREGAS']]



        
        domain1 = lst.domain[0]  # Isso retorna "NTR/BR"
        domain2 = lst.domain[1]  # Isso retorna "NTR/BR."
        domain3 = lst.domain[2]  # Isso retorna "NTR."
        
        infos_dict = lst.infos[0]  # Acessando o único dicionário na lista
        infos7 = infos_dict.get("BRL") 
        
        
        gris_dict = lst.gris[0]
        gris_cod = gris_dict.get("COD")
        gris_por = gris_dict.get("POR")
        gris_category_gid = gris_dict.get("COST_CATEGORY_GID")
        gris_cost_type = gris_dict.get("COST_TYPE")
        
        
        custof_dict = lst.custo_fixo[0] 
        custof_cod = custof_dict.get("COD")
        custof_por = custof_dict.get("POR")
        custof_cost = custof_dict.get("COST_CATEGORY_GID")
        custof_ctype = custof_dict.get("COST_TYPE")
        
        ajudante_dict = lst.ajudante[0] 
        ajudante_cod = ajudante_dict.get("COD")
        ajudante_nome = ajudante_dict.get("NOME")
        ajudante_left_operand1 = ajudante_dict.get("LEFT_OPERAND1")
        ajudante_oper1 = ajudante_dict.get("OPER1_GID")
        ajudante_lowvalue1 = ajudante_dict.get("LOW_VALUE1")
        ajudante_por = ajudante_dict.get("por")
        ajudante_cost = ajudante_dict.get("COST_CATEGORY_GID")
        ajudante_acessorial = ajudante_dict.get("ACCESSORIAL_CODE")
        ajudante_ctype = ajudante_dict.get("COST_TYPE")
        
        prio_h = lst.acessorial[0] # PRIO_H
        prio_l = lst.acessorial[1] # PRIO_L
        priority = lst.acessorial[2] # PRIORITY
        direct = lst.acessorial[3] # DIRECT_W_COST
        triang = lst.acessorial[4] # DIRECT_W_COST_TRIANG
        
        cod_pedagio = lst.pedagio[0]
        cost_category = lst.pedagio[3]
        cod_acessorial = lst.pedagio[4]
        
        parada_cod = lst.parada[0]
        parada_category = lst.parada[3]
        parada_acessorial = lst.parada[4]
        
    
        advalorem_cod = lst.advalorem[0] # "AD"
        # advalorem_nome = lst.advalorem[1] #"AD VALOREM"
        # advalorem_por = lst.advalorem[2] #"SHIPMENT"
        # advalorem_cost = lst.advalorem[3] #"ACCESSORIAL"
        advalorem_acessorial = lst.advalorem[4] #"AD_VALOREM"
        # advalorem_ctype = lst.advalorem[5] #"C"
        
        custof_dict = lst.custo_fixo[0] 
        custof_cod = custof_dict.get("COD")
        custof_por = custof_dict.get("POR")
        custof_cost = custof_dict.get("COST_CATEGORY_GID")  
        custof_acessorial = custof_dict.get("ACCESSORIAL_CODE")
        custof_ctype = custof_dict.get("COST_TYPE")
        
        modal_code = ""
        type_modal = ""
        modal_sigla = ""
        
        for modal_entry in lst.modal:
            if isinstance(modal_entry, dict) and modal_entry["TIPO_MODAL"] == tipo_tarifa:
                modal_code = modal_entry["R_C_D"]
                type_modal = modal_entry["TIPO_MODAL"]
                modal_sigla = modal_entry["SIGLA_MODAL"]
                break 
            
        modald_code =""
        type_modald = ""
        modald_sigla = ""
        
        for modal_dedicada in lst.modalDedicado:
            if isinstance(modal_dedicada, dict) and modal_dedicada["TIPO_MODAL"] == tipo_dedicada:
                modald_code = modal_dedicada["R_C_D"]
                type_modald = modal_dedicada["TIPO_MODAL"]
                modald_sigla = modal_dedicada["SIGLA_MODAL"]
                break 
            
        for shipment_entry in lst.tarifas_shipment:
            if shipment_entry["TIPO_DE_TARIFA"] == tipo_tarifa:
                shipment = shipment_entry["SHIPMENT"]
                break 
        
        pares_origem_destino = [
            ("SP0388800", "AL0055005"),
            ("SP0388800", "BA0307005"),
            ("SP0388800", "PA0024005"),
            ("SP0388800", "AM1302606"),
            ("AL0055005", "SP0388800"),
            ("BA0307005", "SP0388800"),
            ("PA0024005", "SP0388800"),
            ("AM1302606", "SP0388800"),
        ]
        
        if tipo_tarifa == type_modal:
            if modal_sigla:
                formatted_line = f"{domain2}{prio_h},{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},{domain2}{priority},{domain1}"
                unique_lines.add(formatted_line)
            
        if tipo_dedicada == type_modald:
            if modald_sigla:
                formatted_line = f"{domain2}{prio_h},{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},{domain2}{priority},{domain1}"
                unique_lines.add(formatted_line) 
        
        if tipo_tarifa == type_modal:
            if modal_sigla:    
                formatted_line = f"{domain2}{prio_l},{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},{domain2}{priority},{domain1}"
                unique_lines.add(formatted_line)
        
        if tipo_dedicada == type_modald:
            if modald_sigla:    
                formatted_line = f"{domain2}{prio_l},{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},{domain2}{priority},{domain1}"
                unique_lines.add(formatted_line)
        
        if tipo_tarifa == type_modal:
            if modal_sigla:     
                formatted_line = f"{domain2}{direct},{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},{domain2}{direct},{domain1}"
                unique_lines.add(formatted_line)
        
        if tipo_dedicada == type_modald:
            if modald_sigla:     
                formatted_line = f"{domain2}{direct},{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},{domain2}{direct},{domain1}"
                unique_lines.add(formatted_line) 
        
        if tipo_tarifa == type_modal:
            if modal_sigla:     
                formatted_line = f"{domain2}{triang},{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},{domain2}{triang},{domain1}"  
                unique_lines.add(formatted_line)   
        
        if tipo_dedicada== type_modald:
            if modald_sigla:     
                formatted_line = f"{domain2}{triang},{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},{domain2}{triang},{domain1}"  
                unique_lines.add(formatted_line) 
        
        if tipo_tarifa in ["RODOVIARIO", "CONSOLIDADO", "CABOTAGEM", "DIRETO", "REDESPACHO"] and type_modal == tipo_tarifa and pd.notna(pedagio) and pedagio not in ["", "0.00", "0", "0.0", 0.00, 0, 0.0, 0.00, 0, 0.0]:                                       
            if modal_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento}_{cod_pedagio},{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_"\
                                f"{modal_sigla}_{equipamento},{domain2}{cod_acessorial},{domain1}"
                unique_lines.add(formatted_line)
        
        if tipo_dedicada == type_modald and pd.notna(pedagio) and pedagio not in ["", "0.00", "0", "0.0", 0.00, 0, 0.0, 0.00, 0, 0.0]:                                       
            if modald_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento}_{cod_pedagio},{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_"\
                                f"{modald_sigla}_{equipamento},{domain2}{cod_acessorial},{domain1}"
                unique_lines.add(formatted_line) 
        
        if tipo_tarifa == "CABOTAGEM" and type_modal == tipo_tarifa and redespacho not in ["","0.00","0","0.0",0.00,0,0.0]:                                       
            if modal_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento}_{parada_cod},{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_"\
                                f"{modal_sigla}_{equipamento},{domain3}{parada_acessorial},{domain1}"
                unique_lines.add(formatted_line) 
        
        if tipo_tarifa in ["RODOVIARIO", "CONSOLIDADO", "CABOTAGEM", "DIRETO", "REDESPACHO"] and type_modal == tipo_tarifa and pd.notna(ajudante) and ajudante not in ["", "0.00", "0", "0.0", 0.00, 0, 0.0, 0.00, 0, 0.0]:                                       
            if modal_sigla:
                formatted_line = f"{domain2}{code_trp}_{ajudante_nome}_{modal_sigla},{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_"\
                                 f"{modal_sigla}_{equipamento},{domain2}{ajudante_acessorial},{domain1}"
                unique_lines.add(formatted_line)
        
        if tipo_dedicada == type_modald and ajudante and ajudante not in ["", "0.00", "0", "0.0", 0.00, 0, 0.0, 0.00, 0, 0.0]:                                       
            if modald_sigla:
                formatted_line = f"{domain2}{code_trp}_{ajudante_nome}_{modal_sigla},{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_"\
                                 f"{modal_sigla}_{equipamento},{domain2}{ajudante_acessorial},{domain1}"
                unique_lines.add(formatted_line) 
             
        if tipo_tarifa == "FROTA DEDICADA" and tipo_dedicada == type_modald:                                       
            if modald_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento}_{custof_cod},{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_"\
                                f"{modald_sigla}_{equipamento},{domain2}{custof_acessorial},{domain1}"
                unique_lines.add(formatted_line)
        
         
        if tipo_tarifa == "CONSOLIDADO" and type_modal == tipo_tarifa and (origem, destino) in pares_origem_destino:                                        
            if modal_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento}_{parada_cod},{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_"\
                                f"{modal_sigla}_{equipamento},{domain2}{parada_acessorial},{domain1}"
                unique_lines.add(formatted_line)
                
        if tipo_tarifa in ["RODOVIARIO", "CONSOLIDADO", "CABOTAGEM", "DIRETO", "REDESPACHO"] and type_modal == tipo_tarifa and pd.notna(ad_valorem) and ad_valorem not in ["", "0.00", "0", "0.0", 0.00, 0, 0.0, 0.00, 0, 0.0]:                                       
            if modal_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento}_{advalorem_cod},{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_"\
                                f"{modal_sigla}_{equipamento},{domain2}{advalorem_acessorial},{domain1}"
                unique_lines.add(formatted_line)
        
        if tipo_dedicada == type_modald and pd.notna(ad_valorem) and ad_valorem not in ["", "0.00", "0", "0.0", 0.00, 0, 0.0, 0.00, 0, 0.0]:                                       
            if modald_sigla:
                formatted_line = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento}_{advalorem_cod},{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_"\
                                f"{modald_sigla}_{equipamento},{domain2}{advalorem_acessorial},{domain1}"
                unique_lines.add(formatted_line) 

     # Ordenar as linhas únicas pelo penúltimo campo
    def get_penultimate_field(formatted_line):
        # Divide a string no separador de campo por vírgula e retire o penúltimo campo
        return formatted_line.split(',')[-2].strip()

    sorted_unique_lines = sorted(unique_lines, key=get_penultimate_field)
    
    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + sorted_unique_lines
    # final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')

    print(f"Arquivo 019_RATE_GEO_ACCESSORIAL_I.csv salvo com sucesso.")
    return 

def create_csv_020(df): #020_RATE_PREFERENCE_IU
    output_path = os.path.join(output_folder_path, "020_RATE_PREFERENCE_IU.csv")

    # Criar as linhas padrão
    lines = [
        "RATE_PREFERENCE",
        "RATE_PREFERENCE_GID,RATE_PREFERENCE_XID,X_LANE_GID,EFFECTIVE_DATE,EXPIRATION_DATE,PERSPECTIVE,DOMAIN_NAME",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
    
    unique_lines = set()
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
        # Extraindo os valores das colunas G e I usando iloc
        code_trp = row.iloc[col_idx['COD_TRANSPORTADORA']]
        nome_trp = row.iloc[col_idx['NOME_TRANSPORTADORA']]
        tipo_tarifa = row.iloc[col_idx['TIPO_DE_TARIFA']]
        tipo_dedicada = row.iloc[col_idx['TIPO_DE_DEDICADA']]
        percent_ida = row.iloc[col_idx['%_DO_TRAJETO_DA_FD']]
        operacao = row.iloc[col_idx['OPERACAO']]
        origem = row.iloc[col_idx['ZONA_DE_TRANSPORTE_ORIGEM']]
        destino = row.iloc[col_idx['ZONA_DE_TRANSPORTE_DESTINO']]
        equipamento = row.iloc[col_idx['PERFIL_GRUPO_DE_EQUIPAMENTO']]
        data_criacao = convert_date_format(row.iloc[col_idx['DATA_DE_INICIO']])
        data_expiracao = convert_date_format(row.iloc[col_idx['DATA_DE_EXPIRACAO']])
        
        if data_criacao is None:
            data_criacao = "00000000"
        if data_expiracao is None:
            data_expiracao = "00000000"
        
        effective_data = data_criacao + "000000"
        expiration_data = data_expiracao + "000000"
        tarifa_pref = row.iloc[col_idx['TARIFA_PREFERENCIAL']]
        
        domain1 = lst.domain[0]  # Isso retorna "NTR/BR"
        domain2 = lst.domain[1]  # Isso retorna "NTR/BR."
        
        infos_dict = lst.infos[0]  # Acessando o único dicionário na lista
        infos7 = infos_dict.get("BRL") 
        
        cod_pedagio = lst.pedagio[0]
        cost_category = lst.pedagio[3]
        
        zona = lst.zone[1]
        
        modal_code = ""
        shipment= ""
        
        for modal_entry in lst.modal:
            if isinstance(modal_entry, dict) and modal_entry["TIPO_MODAL"] == "RODOVIARIO":
                modal_code = modal_entry["R_C_D"]
                break 
            
        for shipment_entry in lst.tarifas_shipment:
            if shipment_entry["TIPO_DE_TARIFA"] == tipo_tarifa:
                shipment = shipment_entry["SHIPMENT"]
                break 
        
        if tarifa_pref == "SIM":
            formatted_line = f"{domain2}{data_criacao}_{origem}_{destino},{data_criacao}_{origem}_{destino},{domain2}{zona}_{origem}_{zona}_{destino},{effective_data},{expiration_data},"\
                             f"B,{domain1}"
            unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto

    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')

    print(f"Arquivo 020_RATE_PREFERENCE_IU.csv salvo com sucesso.")
    return 

def create_csv_021(df): #021_RATE_PREFERENCE_DETAIL_IU
    output_path = os.path.join(output_folder_path, "021_RATE_PREFERENCE_DETAIL_IU.csv")

    # Criar as linhas padrão
    lines = [
        "RATE_PREFERENCE_DETAIL",
        "RATE_PREFERENCE_GID,RATE_OFFERING_GID,DOMAIN_NAME",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
    
    unique_lines = set()
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
        # Extraindo os valores das colunas G e I usando iloc
        code_trp = row.iloc[col_idx['COD_TRANSPORTADORA']]
        nome_trp = row.iloc[col_idx['NOME_TRANSPORTADORA']]
        tipo_tarifa = row.iloc[col_idx['TIPO_DE_TARIFA']]
        tipo_dedicada = row.iloc[col_idx['TIPO_DE_DEDICADA']]
        percent_ida = row.iloc[col_idx['%_DO_TRAJETO_DA_FD']]
        operacao = row.iloc[col_idx['OPERACAO']]
        origem = row.iloc[col_idx['ZONA_DE_TRANSPORTE_ORIGEM']]
        destino = row.iloc[col_idx['ZONA_DE_TRANSPORTE_DESTINO']]
        equipamento = row.iloc[col_idx['PERFIL_GRUPO_DE_EQUIPAMENTO']]
        data_criacao = convert_date_format(row.iloc[col_idx['DATA_DE_INICIO']])
        data_expiracao = convert_date_format(row.iloc[col_idx['DATA_DE_EXPIRACAO']])
        if data_criacao is None:
            data_criacao = "00000000"
        if data_expiracao is None:
            data_expiracao = "00000000"
        effective_data = data_criacao + "000000"
        expiration_data = data_expiracao + "000000"
        tarifa_pref = row.iloc[col_idx['TARIFA_PREFERENCIAL']]
        
        domain1 = lst.domain[0]  # Isso retorna "NTR/BR"
        domain2 = lst.domain[1]  # Isso retorna "NTR/BR."
        
        infos_dict = lst.infos[0]  # Acessando o único dicionário na lista
        infos7 = infos_dict.get("BRL") 
        
        cod_pedagio = lst.pedagio[0]
        cost_category = lst.pedagio[3]
        
        zona = lst.zone[1]
        
        modal_code = ""
        modal_type = ""
        shipment= ""
        
        for modal_entry in lst.modal:
            if isinstance(modal_entry, dict) and modal_entry["TIPO_MODAL"] == tipo_tarifa:
                modal_code = modal_entry["R_C_D"]
                modal_type = modal_entry["TIPO_MODAL"]
                break 
        
        modald_code = ""
        type_modald = ""

                
        for modal_dedicada in lst.modalDedicado:
            if isinstance(modal_dedicada, dict) and modal_dedicada["TIPO_MODAL"] == tipo_dedicada:
                modald_code = modal_dedicada["R_C_D"]
                type_modald = modal_dedicada["TIPO_MODAL"]
 
                break 
            
        for shipment_entry in lst.tarifas_shipment:
            if shipment_entry["TIPO_DE_TARIFA"] == tipo_tarifa:
                shipment = shipment_entry["SHIPMENT"]
                break 
        
        if tarifa_pref == "SIM" and code_trp != "" and tipo_tarifa == modal_type:
            if modal_code:
                formatted_line = f"{domain2}{data_criacao}_{origem}_{destino},{domain2}{modal_code}{code_trp},{domain1}"
                unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto

        if tarifa_pref == "SIM" and code_trp != "" and tipo_dedicada == type_modald:
            if modald_code:
                formatted_line = f"{domain2}{data_criacao}_{origem}_{destino},{domain2}{modald_code}{code_trp},{domain1}"
                unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto
                
    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')

    print(f"Arquivo 021_RATE_PREFERENCE_DETAIL_UI.csv salvo com sucesso.")
    return 

def create_csv_022(df): #022_RATE_GEO_STOPS_I
    global zone
    output_path = os.path.join(output_folder_path, "022_RATE_GEO_STOPS_I.csv")

    # Criar as linhas padrão
    lines = [
        "RATE_GEO_STOPS",
        "RATE_GEO_GID,LOW_STOP,HIGH_STOP,PER_STOP_COST,PER_STOP_COST_GID,PER_STOP_COST_BASE,DOMAIN_NAME",
        "EXEC SQL ALTER SESSION SET NLS_DATE_FORMAT = 'YYYYMMDDHH24MISS'"
    ]
    
    unique_lines1 = set()
    unique_lines2 = set()
    unique_lines3 = set()
    unique_lines4 = set()
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
        # Extraindo os valores das colunas G e I usando iloc
        code_trp = row.iloc[col_idx['COD_TRANSPORTADORA']]
        tipo_tarifa = row.iloc[col_idx['TIPO_DE_TARIFA']]
        tipo_dedicada = row.iloc[col_idx['TIPO_DE_DEDICADA']]
        percent_ida = row.iloc[col_idx['%_DO_TRAJETO_DA_FD']]
        operacao = row.iloc[col_idx['OPERACAO']]
        origem = row.iloc[col_idx['ZONA_DE_TRANSPORTE_ORIGEM']]
        desc_origem = row.iloc[col_idx['DESCRICAO_ZONA_DE_TRANSPORTE_ORIGEM']]
        destino = row.iloc[col_idx['ZONA_DE_TRANSPORTE_DESTINO']]
        equipamento = row.iloc[col_idx['PERFIL_GRUPO_DE_EQUIPAMENTO']]
        redespacho = row.iloc[col_idx['REDESPACHO']]
        data_criacao = convert_date_format(row.iloc[col_idx['DATA_DE_INICIO']])
        data_expiracao = convert_date_format(row.iloc[col_idx['DATA_DE_EXPIRACAO']])

             
        domain1 = lst.domain[0]  # Isso retorna "NTR/BR"
        domain2 = lst.domain[1]  # Isso retorna "NTR/BR."


        type_modal = '' 
        modal_sigla=""   
        
        for modal_entry in lst.modal:
            if isinstance(modal_entry, dict) and modal_entry["TIPO_MODAL"] == tipo_tarifa:
                type_modal = modal_entry["TIPO_MODAL"]
                modal_sigla = modal_entry["SIGLA_MODAL"]
                break 
        
        type_modald = '' 
        modald_sigla=""
        
        for modal_dedicada in lst.modalDedicado:
            if isinstance(modal_dedicada, dict) and modal_dedicada["TIPO_MODAL"] == tipo_tarifa:
                type_modald = modal_entry["TIPO_MODAL"]
                modald_sigla = modal_entry["SIGLA_MODAL"]
                break 
            
        infos_dict = lst.infos[0]  # Acessando o único dicionário na lista
        infos7 = infos_dict.get("BRL") 

        pares_redespacho = [
        ("SP0388800", "AL0055005"),
        ("SP0388800", "BA0307005"), 
        ("SP0388800", "PA0024005"),
        ("SP0388800", "AM1302606"),
        ("AL0055005", "SP0388800"),
        ("AL0055005", "SP0084005"),
        ("BA0307005", "SP0388800"),
        ("BA0307005", "SP0084005"),
        ("PA0024005", "SP0388800"),
        ("PA0024005", "SP0084005"),
        ("AM1302606", "SP0388800"),
        ("AM1302606", "SP0084005"),
        ("PA0015005", "SP0084005")
    ]

    if tipo_tarifa == type_modal and tipo_tarifa in ["REDESPACHO"] and  redespacho != '' and (origem, destino) in pares_redespacho:
        if modal_sigla:   
            formatted_line1 = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},1,1,{redespacho},{infos7},,{domain1}"
            formatted_line2 = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modal_sigla}_{equipamento},2,4,0.00,{infos7},,{domain1}"  
            unique_lines1.add(formatted_line1)
            unique_lines2.add(formatted_line2)


    if tipo_tarifa == type_modald and tipo_tarifa in ["REDESPACHO"] and  redespacho != '' and (origem, destino) in pares_redespacho:
        if modald_sigla:   
                formatted_line3 = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},1,1,{redespacho},{infos7},,{domain1}"
                formatted_line4 = f"{domain2}{data_criacao}_{code_trp}_{origem}_{destino}_{modald_sigla}_{equipamento},2,4,0.00,{infos7},,{domain1}"                    
                unique_lines3.add(formatted_line3) 
                unique_lines4.add(formatted_line4)      
        

    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + list(unique_lines1) + list(unique_lines2) + list(unique_lines3) + list(unique_lines4) 
    
    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')
          
    print(f"Arquivo 022_RATE_GEO_STOPS_I.csv salvo com sucesso.")
    return 


# def create_csv_YADP(df): # ***** DENIFIR REGRAS ****
    output_path = os.path.join(output_folder_path, "YADP.csv")

    # Criar as linhas padrão
    lines = [
        "NÃ£o Modificar esta linha;KSCHL;DATAB;DATBI;KBETR;KONWA;KOSTKZ;MANDT;TDLNR"
    ]
    unique_lines = set()
    # Adicionar as linhas formatadas com base no df 
    for index, row in df.iterrows():
        # Extraindo os valores das colunas G e I usando iloc
        data_criacao = row.iloc[32]
        data_expiracao = row.iloc[33] 
        data_criacao= convert_date_format(data_criacao)
        data_expiracao = convert_date_format(data_expiracao)
        effective_data = data_criacao + "000000"
        expiration_data = data_expiracao + "000000"
        code_trp = row.iloc[0] # trp 
        origem = row.iloc[6] # Origem
        destino = row.iloc[8] # destino
        equipa = row.iloc[10]# Gruo Equipamento
        tarifa = row.iloc[2] # Tipo de Tarifa 
        custo = row.iloc[12] # Custo
        pedagio = row.iloc[24] #Valor pedágio
        tarifa_pref = row.iloc[31]
        domain1 = lst.domain[0]  # Isso retorna "NTR/BR"
        domain2 = lst.domain[1]  # Isso retorna "NTR/BR."
        
        infos_dict = lst.infos[0]  # Acessando o único dicionário na lista
        infos7 = infos_dict.get("BRL") 
        
        cod_pedagio = lst.pedagio[0]
        cost_category = lst.pedagio[3]
        
        zona = lst.zone[1]
        
        modal_code = ""
        shipment= ""
        
        for modal_entry in lst.modal:
            if isinstance(modal_entry, dict) and modal_entry["TIPO_MODAL"] == "RODOVIARIO":
                modal_code = modal_entry["R_C_D"]
                break 
            
        for shipment_entry in lst.tarifas_shipment:
            if shipment_entry["TIPO_DE_TARIFA"] == tarifa:
                shipment = shipment_entry["SHIPMENT"]
                break 
        
        if tarifa_pref == "SIM":
            formatted_line = ""
            unique_lines.add(formatted_line)  # Adiciona a linha ao conjunto

    # Combinar as linhas padrão com as linhas geradas
    final_lines = lines + list(unique_lines)

    # Salvar as linhas no arquivo CSV
    with open(output_path, 'w') as f:
        for line in final_lines:
            f.write(line + '\n')

    print(f"Arquivo YADP.csv salvo com sucesso.")
    return 