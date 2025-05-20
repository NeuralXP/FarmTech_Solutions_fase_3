import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# --- Configurações da Página ---
st.set_page_config(page_title="FarmTech Dashboard", layout="wide", initial_sidebar_state="expanded")
st.title("💧 FarmTech Solutions - Dashboard de Monitoramento Agrícola")
st.markdown("Visualização dos dados simulados do sistema de irrigação e sensores.")

# --- Geração de Dados Simulados para Sensores ---
# Função para gerar dados simulados ao longo do tempo
def gerar_dados_sensores(n_leituras=20):
    dados = []
    tempo_inicial = datetime.now() - timedelta(minutes=n_leituras * 5) # Simular leituras a cada 5 min
    for i in range(n_leituras):
        tempo_atual = tempo_inicial + timedelta(minutes=i * 5)
        umidade = random.uniform(30, 85) # %
        ph = random.uniform(5.5, 7.5)
        # Sensores P e K (Booleanos: 1 = Presença, 0 = Ausência)
        fosforo_presente = random.choice([0, 1])
        potassio_presente = random.choice([0, 1])
        # Lógica simulada para bomba (ligada se umidade < 50%)
        bomba_ligada = 1 if umidade < 50 else 0
        
        dados.append({
            "Timestamp": tempo_atual,
            "Umidade (%)": umidade,
            "pH": ph,
            "Fósforo (P)": "Presente" if fosforo_presente else "Ausente",
            "Potássio (K)": "Presente" if potassio_presente else "Ausente",
            "Bomba Ligada": "Sim" if bomba_ligada else "Não",
            "fosforo_val": fosforo_presente, # para gráficos
            "potassio_val": potassio_presente, # para gráficos
            "bomba_val": bomba_ligada # para gráficos
        })
    return pd.DataFrame(dados)

# Botão para atualizar/gerar novos dados simulados
if 'sensor_data' not in st.session_state or st.sidebar.button("🔄 Gerar Novos Dados de Sensores"):
    st.session_state.sensor_data = gerar_dados_sensores()

df_sensores = st.session_state.sensor_data

# --- Sidebar para Filtros e Controles (Exemplo) ---
st.sidebar.header("Configurações e Filtros")
st.sidebar.markdown("Aqui você pode adicionar filtros ou controles interativos no futuro.")
# Exemplo de seletor de período (não funcional com dados simulados fixos, mas ilustrativo)
periodo_selecionado = st.sidebar.select_slider(
    "Selecione o período para visualização:",
    options=['Última Hora', 'Últimas 6 Horas', 'Últimas 24 Horas'],
    value='Últimas 6 Horas'
 )

# --- Apresentação dos Dados ---

# KPIs Principais
st.header("📈 Indicadores Chave Atuais")
col1, col2, col3, col4, col5 = st.columns(5)
ultima_leitura = df_sensores.iloc[-1]

col1.metric("Umidade Atual", f"{ultima_leitura['Umidade (%)']:.1f}%")
col2.metric("pH do Solo", f"{ultima_leitura['pH']:.2f}")
col3.metric("Fósforo (P)", ultima_leitura['Fósforo (P)'])
col4.metric("Potássio (K)", ultima_leitura['Potássio (K)'])
col5.metric("Bomba de Irrigação", "Ligada ✅" if ultima_leitura['Bomba Ligada'] == "Sim" else "Desligada ❌")

st.markdown("---")

# Gráficos de Tendências
st.header("📊 Gráficos de Tendências dos Sensores")

# Colunas para organizar os gráficos
g_col1, g_col2 = st.columns(2)

with g_col1:
    st.subheader("Umidade do Solo ao Longo do Tempo")
    st.line_chart(df_sensores.set_index("Timestamp")[["Umidade (%)"]])

    st.subheader("Nível de pH do Solo ao Longo do Tempo")
    st.line_chart(df_sensores.set_index("Timestamp")[["pH"]])

with g_col2:
    st.subheader("Estado da Bomba de Irrigação")
    # Usando um gráfico de área para mostrar ativação da bomba (0 ou 1)
    st.area_chart(df_sensores.set_index("Timestamp")[["bomba_val"]].rename(columns={'bomba_val': 'Bomba Ativa (1=Sim, 0=Não)'}))
    
    st.subheader("Presença de Nutrientes (P e K)")
    # Gráfico de barras para a última leitura de P e K
    # Para simplificar, mostramos o status atual, mas poderia ser um histórico
    nutrientes_status = pd.DataFrame({
        'Nutriente': ['Fósforo (P)', 'Potássio (K)'],
        'Status': [ultima_leitura['fosforo_val'], ultima_leitura['potassio_val']]
    })
    st.bar_chart(nutrientes_status.set_index('Nutriente'))


st.markdown("---")

# Tabela de Dados Detalhados
st.header("📋 Tabela com Dados Históricos dos Sensores")
st.dataframe(df_sensores[["Timestamp", "Umidade (%)", "pH", "Fósforo (P)", "Potássio (K)", "Bomba Ligada"]], height=300)

st.markdown("---")

st.sidebar.info(
    """
    **Sobre este Dashboard:**
    Este painel é uma simulação para o projeto FarmTech Solutions da FIAP.
    Os dados dos sensores são gerados artificialmente para fins de demonstração.
    """
)
st.sidebar.markdown("---")
st.sidebar.markdown("Desenvolvido com ❤️ usando Streamlit.")


import requests
import json
from datetime import datetime

# --- Configurações da API OpenWeatherMap ---
API_KEY = "207d471599cab6f442a27a1ece9643cb" 
# Você pode alterar a cidade e o país conforme necessário
CIDADE = "Sao Paulo"
PAIS_COD = "BR"
UNITS = "metric" # Celsius para temperatura
LANGUAGE = "pt_br" # Para descrição do tempo em português


BASE_URL_FORECAST = "http://api.openweathermap.org/data/2.5/forecast"

def buscar_dados_climaticos(api_key, cidade, pais_cod, units, lang):
    """
    Busca dados de previsão do tempo (próximas horas/dias) para a cidade especificada.
    """
    params = {
        'q': f"{cidade},{pais_cod}",
        'appid': api_key,
        'units': units,
        'lang': lang,
        'cnt': 8 # Número de timestamps de previsão (8 timestamps * 3 horas = 24 horas de previsão)
    }
    try:
        response = requests.get(BASE_URL_FORECAST, params=params)
        response.raise_for_status() # Apresenta um erro para códigos de status HTTP
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP ao buscar dados climáticos: {http_err}")
        if response.status_code == 401:
            print("Verifique sua chave de API. Pode ser inválida ou não autorizada.")
        elif response.status_code == 404:
            print(f"Cidade '{cidade}' não encontrada.")
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"Erro de requisição ao buscar dados climáticos: {req_err}")
        return None

def processar_dados_climaticos(dados_api):
    """
    Processa a resposta da API e extrai informações relevantes.
    Verifica se há previsão de chuva significativa nas próximas horas.
    """
    if not dados_api or 'list' not in dados_api or not dados_api['list']:
        print("Dados climáticos não disponíveis ou em formato inesperado.")
        return None, False # Nenhum dado, assume que não há chuva para segurança

    print("\n--- Previsão do Tempo Detalhada (Próximas Horas) ---")
    chuva_nas_proximas_horas = False
    limite_horas_previsao_chuva = 6 # Verificar chuva nas próximas 6 horas
    count_timestamps_verificar = limite_horas_previsao_chuva // 3 # Cada timestamp é de 3h

    for i, previsao in enumerate(dados_api['list'][:count_timestamps_verificar]):
        timestamp_dt = datetime.fromtimestamp(previsao['dt'])
        temp = previsao['main']['temp']
        feels_like = previsao['main']['feels_like']
        humidity = previsao['main']['humidity']
        weather_desc = previsao['weather'][0]['description']
        pop = previsao.get('pop', 0) * 100 # Probabilidade de precipitação em %
        rain_volume_3h = previsao.get('rain', {}).get('3h', 0) # Volume de chuva nas últimas 3h em mm

        print(f"\nHorário: {timestamp_dt.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Temperatura: {temp}°C (Sensação: {feels_like}°C)")
        print(f"  Umidade: {humidity}%")
        print(f"  Condição: {weather_desc.capitalize()}")
        print(f"  Probabilidade de Precipitação: {pop:.0f}%")
        if rain_volume_3h > 0:
            print(f"  Volume de Chuva (em 3h): {rain_volume_3h} mm")
        
        # Lógica para considerar chuva:
        # Se houver probabilidade de precipitação > 50% OU volume de chuva > 0.5mm
        if pop > 50 or rain_volume_3h > 0.5: # Ajuste estes limiares conforme necessidade
            chuva_nas_proximas_horas = True
            print("  -> ALERTA: Previsão de chuva significativa neste período!")

    # Informação consolidada da cidade
    cidade_info = dados_api.get('city', {})
    nome_cidade = cidade_info.get('name', 'N/A')
    pais = cidade_info.get('country', 'N/A')
    print(f"\nLocalização da Previsão: {nome_cidade}, {pais}")
    
    return dados_api['list'][0], chuva_nas_proximas_horas # Retorna a previsão mais próxima e o flag de chuva

def decidir_irrigacao_com_clima(dados_atuais, ha_previsao_chuva):
    """
    Lógica condicional que relaciona os dados climáticos à irrigação.
    """
    if ha_previsao_chuva:
        print("\n--- Decisão de Irrigação ---")
        print("🚫 Não irrigar: Há previsão de chuva significativa nas próximas horas.")
        return False # Não irrigar
    else:
        print("\n--- Decisão de Irrigação ---")
        print("✅ Sem previsão de chuva significativa. A irrigação pode prosseguir baseada nos sensores de solo.")
        # Aqui, a lógica de irrigação poderia depender dos outros sensores (umidade do solo, etc.)
        # Mas aqui apenas considerei a chuva.
        return True # Irrigar (ou verificar outros sensores)

# --- Função Principal ---
def main():
    st.title("🌍 FarmTech - Integração com API Meteorológica")
    
    # Usar st.secrets para API Key se for implantar no Streamlit Cloud
    api_key_input = st.text_input("Sua Chave API OpenWeatherMap", type="password", value=API_KEY if API_KEY != "SUA_CHAVE_API_AQUI" else "")
    
    # Para rodar localmente e simplificar, usei a constante, mas alertamos sobre a chave
    if API_KEY == "8ab192bb24ed3a21641be3be77d84800": 
        st.error("🚨 Por favor, adicione sua chave da API OpenWeatherMap no código (`API_KEY = \"207d471599cab6f442a27a1ece9643cb\"`)")
        st.markdown("Obtenha sua chave em: [https://openweathermap.org/api](https://openweathermap.org/api)")
        return

    cidade_input = st.text_input("Digite a cidade:", value=CIDADE)
    pais_input = st.text_input("Digite o código do país (ex: BR):", value=PAIS_COD, max_chars=2)

    if st.button("☀️ Buscar Dados Climáticos e Decidir Irrigação"):
        with st.spinner("Buscando dados climáticos..."):
            dados_api = buscar_dados_climaticos(API_KEY, cidade_input, pais_input, UNITS, LANGUAGE)

        if dados_api:
            st.subheader(f"Previsão para {dados_api.get('city', {}).get('name', cidade_input)}")
            
            # Exibir a primeira previsão (mais próxima do tempo atual)
            previsao_atual = dados_api['list'][0]
            temp_atual = previsao_atual['main']['temp']
            umidade_atual = previsao_atual['main']['humidity']
            descricao_atual = previsao_atual['weather'][0]['description']
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Temperatura Atual", f"{temp_atual}°C")
            col2.metric("Umidade do Ar", f"{umidade_atual}%")
            col3.metric("Condição", descricao_atual.capitalize())

            # Processar para decisão de irrigação
            st.markdown("---")
            st.subheader("Análise para Irrigação (próximas 6 horas):")
            
            # Usaremos uma função para printar no terminal, mas para Streamlit, exibimos na interface
            log_output = []
            
            chuva_nas_proximas_horas_flag = False
            limite_horas_previsao_chuva = 6 
            count_timestamps_verificar = limite_horas_previsao_chuva // 3

            log_output.append("--- Previsão Detalhada (Próximas Horas para Irrigação) ---")
            for i, previsao_item in enumerate(dados_api['list'][:count_timestamps_verificar]):
                ts_dt = datetime.fromtimestamp(previsao_item['dt'])
                pop_item = previsao_item.get('pop', 0) * 100
                rain_vol_item = previsao_item.get('rain', {}).get('3h', 0)
                desc_item = previsao_item['weather'][0]['description']

                log_output.append(f"\nHorário: {ts_dt.strftime('%Y-%m-%d %H:%M')}, Condição: {desc_item.capitalize()}, Chuva: {pop_item:.0f}%, Vol: {rain_vol_item}mm")
                
                if pop_item > 50 or rain_vol_item > 0.5:
                    chuva_nas_proximas_horas_flag = True
                    log_output.append("  -> ALERTA: Previsão de chuva significativa neste período!")
            
            st.text_area("Log da Análise de Chuva:", "\n".join(log_output), height=200)

            if decidir_irrigacao_com_clima(previsao_atual, chuva_nas_proximas_horas_flag):
                st.success("✅ Decisão: Irrigar (considerando apenas a ausência de previsão de chuva).")
            else:
                st.warning("🚫 Decisão: Não irrigar devido à previsão de chuva.")
        else:
            st.error("Não foi possível obter os dados climáticos.")

if __name__ == "__main__":
    main() # Função principal para gerar a interface com Streamlit