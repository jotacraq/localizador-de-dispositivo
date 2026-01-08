# 🔍 Device Finder - Localizador de Dispositivos

Um aplicativo Python poderoso para coletar, rastrear e gerenciar informações de dispositivos com interface gráfica interativa.

## ✨ Funcionalidades

- 📊 **Coleta Automática de Dados**: Coleta informações completas do dispositivo
- 📋 **Histórico Persistente**: Armazena todos os dados em banco SQLite
- 🔎 **Busca Avançada**: Procure por UUID de hardware
- 🌐 **Dados de Rede**: IP local, IP público, SSID
- 📍 **Localização Geográfica**: Obtém latitude e longitude via API
- 🖥️ **Interface Gráfica Moderna**: Tkinter com design intuitivo
- 💾 **Banco de Dados Robusto**: SQLite com verificação de integridade

## 📦 Dados Coletados

- ✓ UUID do Hardware
- ✓ Nome do Host
- ✓ IP Local
- ✓ IP Público
- ✓ SSID (Rede WiFi conectada)
- ✓ Status da Conexão de Internet
- ✓ Localização (Latitude/Longitude)
- ✓ Data e Hora (Fuso horário: São Paulo)

## 🚀 Instalação

### Requisitos
- Python 3.7+
- Windows (para uso completo)

### Passos

1. **Clone ou baixe o projeto**
```bash
cd DeviceFinder
```

2. **Instale as dependências**
```bash
pip install pytz
```

3. **Execute a aplicação**

#### Modo GUI (Recomendado)
```bash
python __init__.py
```

#### Modo CLI
```bash
python __init__.py --cli
```

## 📚 Uso

### Interface Gráfica (Recomendada)

1. **Aba "Coletar Dados"**
   - Clique em "▶ Coletar e Salvar" para coletar e armazenar dados
   - Clique em "👁️ Visualizar Dados" para ver dados sem salvar

2. **Aba "Histórico"**
   - Clique em "🔄 Atualizar" para carregar todos os pings
   - Clique em "🗑️ Limpar Banco" para limpar base de dados (CUIDADO!)

3. **Aba "Buscar"**
   - Digite um UUID e clique em "🔎 Buscar"
   - Veja todos os pings associados a esse UUID

4. **Aba "Sobre"**
   - Informações sobre o aplicativo e funcionalidades

### Linha de Comando

```bash
# Coletar dados e exibir
python __init__.py --cli
```

## 📁 Estrutura do Projeto

```
DeviceFinder/
├── __init__.py          # Ponto de entrada principal
├── app_gui.py          # Interface gráfica (Tkinter)
├── localPing.py        # Coleta de dados do dispositivo
├── query.py            # Operações de banco de dados
├── banco.db            # Banco de dados SQLite (criado automaticamente)
└── README.md           # Este arquivo
```

## 🔧 Módulos

### localPing.py
Responsável pela coleta de dados:
- `pegar_data_hora()`: Data/hora no fuso de São Paulo
- `pegar_nome_host()`: Nome do computador
- `pegar_uuid_hardware()`: UUID único do hardware
- `pegar_ip_local()`: Endereço IP da rede local
- `pegar_ip_publico()`: Endereço IP público
- `pegar_ssid()`: Nome da rede WiFi
- `pegar_localizacao()`: Latitude e longitude
- `verificar_internet()`: Status da conexão
- `montar_json_completo()`: Retorna todos os dados coletados

### query.py
Operações com banco de dados:
- `inicializar_banco()`: Cria tabela se não existir
- `inserir_ping()`: Insere novo registro
- `obter_todos_pings()`: Retorna todos os pings
- `obter_pings_por_uuid()`: Busca por UUID específico
- `limpar_banco()`: Limpa todos os dados

### app_gui.py
Interface gráfica com 4 abas:
1. **Coletar Dados**: Coleta manual de informações
2. **Histórico**: Visualização de todos os registros
3. **Buscar**: Busca por UUID
4. **Sobre**: Informações do aplicativo

## 🗄️ Banco de Dados

O SQLite armazena:
- ID (chave primária)
- UUID do Hardware
- Data do Ping
- Nome do Host
- IP Local
- IP Público
- SSID
- Status Internet (0/1)
- Latitude
- Longitude

## 🛠️ Desenvolvimento

### Adicionar nova funcionalidade

1. **Coleta de dados**: Edite `localPing.py`
2. **Banco de dados**: Edite `query.py`
3. **Interface**: Edite `app_gui.py`

### Exemplo - Adicionar novo campo

1. Adicione função em `localPing.py`
2. Adicione coluna em `query.inicializar_banco()`
3. Atualize `montar_json_completo()` e `inserir_ping()`
4. Atualize a interface em `app_gui.py`

## ⚠️ Avisos Importantes

- O aplicativo coleta informações de localização. Use responsavelmente.
- Proteja o arquivo `banco.db` com dados sensíveis
- A função "Limpar Banco" é irreversível
- Internet é necessária para localização geográfica

---

**Última atualização**: Janeiro 2026