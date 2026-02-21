# 🎬 MapTheSoul

> *every soul has a story. every story has a film. map yours.*

Aplicativo de recomendação de filmes baseado em Árvore de Decisão, desenvolvido como trabalho acadêmico para a disciplina de Inteligência Artificial.

---

## 👥 Integrantes

- FLAVIO DA SILVA INACIO DOS SANTOS
- THYFANNY DA CRUZ SILVA

---

##  Requisitos

- Python 3.8+
- Conta no [Kaggle](https://www.kaggle.com) para baixar o dataset
- Conta no [TMDB](https://www.themoviedb.org) para obter a chave da API



---

##  Instalação das Dependências

```bash
pip install pandas scikit-learn matplotlib streamlit requests python-dotenv
```

Ou gere o `requirements.txt` com:

```bash
pip freeze > requirements.txt
```

---

##  Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/thyfanny/MapTheSoul.git
cd MapTheSoul
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Baixe o dataset

Acesse o link abaixo e baixe o arquivo `imdb_top_1000.csv`:

🔗 https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows

Coloque o arquivo dentro da pasta `data/`.

### 5. Configure a chave da API do TMDB

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
TMDB_API_KEY=chave
```

Para obter a chave, crie uma conta em [themoviedb.org](https://www.themoviedb.org) e acesse **Settings → API**.

### 6. Treine o modelo

```bash
python model.py
```

### 7. Execute o aplicativo

```bash
streamlit run app.py
```

Acesse no navegador: `http://localhost:8501`

---

## 🎬 Como Usar

1. **Gênero** — escolha o gênero do filme que deseja assistir
2. **Duração** — selecione quanto tempo você tem disponível
3. **Época** — filtre por período (opcional)
4. **Nota mínima** — defina a qualidade mínima desejada no IMDB
5. Clique em **✦ revelar filmes ✦** e descubra suas recomendações

---

##  Tecnologias Utilizadas

| Biblioteca | Finalidade |
|---|---|
| `pandas` | Carregamento e manipulação do dataset |
| `scikit-learn` | Árvore de Decisão, LabelEncoder e métricas de avaliação |
| `matplotlib` | Visualização gráfica da árvore de decisão |
| `streamlit` | Interface web do aplicativo |
| `requests` | Requisições à API do TMDB |
| `python-dotenv` | Carregamento seguro da chave da API |
| `pickle` | Salvamento e carregamento do modelo treinado |
