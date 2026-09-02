# 🗂️ Organizador de Arquivos

> Projeto de monitoramento e organização automática de arquivos em ambiente corporativo.

---

## 📋 Sobre o projeto

O Organizador de Arquivos é um sistema desenvolvido em Python que monitora pastas em computadores, organiza arquivos automaticamente por categoria, detecta duplicatas e registra todas as movimentações em banco de dados e logs diários.

### Funcionalidades

- Organização automática de arquivos por extensão, com base em regras configuráveis
- Detecção e isolamento de arquivos duplicados via hash SHA-256
- Registro de todas as movimentações em banco de dados SQLite
- Logs diários com rotação automática
- Remoção de pastas vazias após organização
- Relatório de movimentações por categoria

---

## 🗂️ Estrutura do projeto

```
organizador-de-arquivos/
├── main.py                         # Ponto de entrada da aplicação
├── config.json                     # Regras de organização por extensão
├── conftest.py                     # Configuração do pytest
│
├── core/
│   ├── __init__.py
│   └── constants.py                # Constantes compartilhadas
│
├── services/
│   ├── __init__.py
│   ├── organizador.py              # Lógica principal de organização
│   ├── duplicate_service.py        # Detecção e movimentação de duplicatas
│   ├── cleanup_service.py          # Remoção de pastas vazias
│   ├── database.py                 # Persistência em SQLite
│   ├── hash_service.py             # Geração de hash SHA-256
│   └── logger.py                   # Configuração de logs
│
├── utils/
│   ├── __init__.py
│   └── gerador_de_caminho_unico.py # Helper para evitar sobrescrita de arquivos
│
├── database/
│   └── organizador.db              # Banco de dados (gerado automaticamente)
│
├── logs/                           # Logs diários (gerado automaticamente)
│   └── log-organizacao.log
│
└── tests/
    ├── __init__.py
    ├── test_organizador.py
    ├── test_duplicate_service.py
    ├── test_cleanup_service.py
    ├── test_database.py
    ├── test_hash_service.py
    ├── test_logger.py
    └── test_gerar_caminho_unico.py
```

---

## ⚙️ Pré-requisitos

- Python 3.10 ou superior
- pip

Para verificar sua versão do Python:

```bash
python --version
```

---

## 🚀 Instalação

**1. Clone o repositório**

```bash
git clone https://github.com/seu-usuario/organizador-de-arquivos.git
cd organizador-de-arquivos
```

**2. Crie e ative um ambiente virtual**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python -m venv venv
source venv/bin/activate
```

**3. Instale as dependências**

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuração

Edite o arquivo `config.json` na raiz do projeto para definir as regras de organização. Cada chave é o nome da pasta de destino, e o valor é a lista de extensões que devem ser movidas para ela:

```json
{
    "Documentos": [".pdf", ".docx", ".txt", ".xlsx"],
    "Imagens":    [".jpg", ".jpeg", ".png", ".gif"],
    "Videos":     [".mp4", ".mov", ".avi"],
    "Audio":      [".mp3", ".wav", ".flac"],
    "Compactados":[".zip", ".rar", ".7z"]
}
```

Em seguida, defina a pasta a ser monitorada em `main.py`:

```python
PASTA_ALVO = r"C:\Users\seu-usuario\Downloads"
```

---

## ▶️ Uso

Com o ambiente virtual ativo, execute:

```bash
python main.py
```

O sistema irá:
1. Detectar e mover arquivos duplicados para a pasta `Duplicados/`
2. Organizar os arquivos restantes nas pastas definidas em `config.json`
3. Remover pastas vazias geradas após a organização
4. Registrar tudo no banco de dados e no log do dia

---

## 🧪 Testes

Para rodar a suíte de testes:

```bash
pytest tests/ -v
```

Para rodar um módulo específico:

```bash
pytest tests/test_organizador.py -v
```

---

## 📦 Dependências

| Pacote   | Uso                        |
|----------|----------------------------|
| `pytest` | Execução dos testes        |

> As demais funcionalidades utilizam apenas bibliotecas da biblioteca padrão do Python (`os`, `shutil`, `hashlib`, `sqlite3`, `logging`).

---

## 🗺️ Roadmap

- [x] Organização de arquivos por extensão
- [x] Detecção de duplicatas via SHA-256
- [x] Registro em banco de dados SQLite
- [x] Logs diários com rotação automática
- [x] Remoção de pastas vazias
- [x] Testes automatizados
- [ ] Monitoramento em tempo real com `watchdog`
- [ ] Execução como serviço do Windows
- [ ] Interface gráfica

---

## 📄 Licença

Projeto desenvolvido para fins acadêmicos.
