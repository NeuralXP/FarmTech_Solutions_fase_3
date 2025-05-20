# 🌍 FarmTech Dashboard - Monitoramento Agrícola com Previsão Climática

Bem-vindo ao **FarmTech Dashboard**, um painel interativo desenvolvido com **Streamlit** para monitoramento agrícola. Este projeto combina dados simulados de sensores agrícolas com integração à API meteorológica do **OpenWeatherMap**, permitindo decisões inteligentes sobre irrigação com base em condições climáticas.

---

## 📋 Funcionalidades

- **Monitoramento de Sensores Agrícolas**:
  - Umidade do solo (%)
  - pH do solo
  - Presença de nutrientes (Fósforo e Potássio)
  - Status da bomba de irrigação (Ligada ou Desligada)

- **Gráficos Interativos**:
  - Tendências de umidade e pH ao longo do tempo
  - Ativação da bomba de irrigação
  - Presença de nutrientes no solo

- **Integração com API Meteorológica**:
  - Previsão do tempo para as próximas 24 horas
  - Análise de chuva nas próximas 6 horas
  - Decisão automatizada sobre irrigação com base na previsão climática

- **Simulação de Dados**:
  - Geração de dados fictícios para sensores agrícolas, ideal para demonstração e testes.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Python 3.8 ou superior
- Bibliotecas listadas no arquivo `requirements.txt`

### Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/farmtech-dashboard.git
   cd farmtech-dashboard
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate # Linux/Mac
   venv\Scripts\activate    # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Obtenha uma chave de API do OpenWeatherMap:
   - Acesse [OpenWeatherMap](https://openweathermap.org/api) e crie uma conta.
   - Gere uma chave de API gratuita.

5. Atualize o código com sua chave de API:
   - No arquivo `painel_monitoramento.py`, substitua o valor da variável `API_KEY` pela sua chave:
     ```python
     API_KEY = "sua_chave_api_aqui"
     ```

### Executando o Dashboard

1. Inicie o Streamlit:
   ```bash
   streamlit run painel_monitoramento.py
   ```

2. Acesse o painel no navegador:
   - O Streamlit abrirá automaticamente no endereço: `http://localhost:8501`

---

## 📊 Estrutura do Projeto

```plaintext
.
├── painel_monitoramento.py   # Código principal do dashboard
├── requirements.txt          # Dependências do projeto
├── README.md                 # Documentação do projeto
```

---

## 🛠 Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/)**: Framework para criação de dashboards interativos.
- **[Pandas](https://pandas.pydata.org/)**: Manipulação e análise de dados.
- **[NumPy](https://numpy.org/)**: Operações matemáticas e geração de dados simulados.
- **[OpenWeatherMap API](https://openweathermap.org/api)**: Integração para previsão do tempo.
- **[Requests](https://docs.python-requests.org/)**: Requisições HTTP para consumir a API.

---

## 🌟 Funcionalidades Futuras

- Adicionar filtros interativos para análise de dados históricos.
- Integração com sensores reais para coleta de dados em tempo real.
- Exportação de relatórios em PDF ou Excel.
- Notificações automáticas para alertas climáticos.

---

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

---

## 💡 Sobre

Este projeto foi desenvolvido como parte do curso da **FIAP** para demonstrar conceitos de IoT, análise de dados e integração com APIs externas. 

Desenvolvido com ❤️
