# ============================================================
# MapTheSoul - Árvore de Decisão
# Recomendação de filmes baseada em preferências do usuário
# ============================================================

import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import pickle

# ============================================================
# 1. CARREGAMENTO DOS DADOS
# ============================================================

def load_data():
    """Carrega e exibe informações básicas do dataset"""
    df = pd.read_csv("data/imdb_top_1000.csv")
    print("### Dataset carregado com sucesso ###")
    print(f"Shape: {df.shape}")
    return df

# ============================================================
# 2. LIMPEZA E PREPARAÇÃO DOS DADOS
# ============================================================

def prepare_data(df):
    """Limpa e prepara os dados para o treinamento"""

    df = df[["Genre", "IMDB_Rating", "Runtime", "Meta_score", "No_of_Votes", "Released_Year"]].copy()

    df.dropna(inplace=True)

    # Separa todos os gêneros do filme em uma lista
    df["Genre"] = df["Genre"].apply(lambda x: [g.strip() for g in x.split(",")])

    df = df.explode("Genre").reset_index(drop=True)

    df["Runtime"] = df["Runtime"].apply(lambda x: int(x.replace(" min", "").strip()))

    df["Released_Year"] = pd.to_numeric(df["Released_Year"], errors="coerce")
    df.dropna(inplace=True)
    df["Released_Year"] = df["Released_Year"].astype(int)

    # ============================================================
    # CRIAÇÃO DO RÓTULO (target)
    # Filmes com nota IMDB >= 8.0 são classificados como "Recomendado"
    # ============================================================
    df["Recomendado"] = df["IMDB_Rating"].apply(lambda x: 1 if x >= 8.0 else 0)

    return df

# ============================================================
# 3. CODIFICAÇÃO DAS VARIÁVEIS CATEGÓRICAS
# ============================================================

def encode_data(df):
    """Converte variáveis categóricas em numéricas"""
    le = LabelEncoder()
    df["Genre_encoded"] = le.fit_transform(df["Genre"])

    # Salva o encoder para uso posterior no Streamlit
    with open("data/label_encoder.pkl", "wb") as f:
        pickle.dump(le, f)

    return df, le

# ============================================================
# 4. MAPEAMENTOS DE DURAÇÃO E DÉCADA
# ============================================================

DURACAO_PARA_MINUTOS = {
    "Curto (até 90min)": (0, 90),
    "Médio (90-120min)": (90, 120),
    "Longo (120min+)": (120, 9999)
}

DECADA_PARA_ANOS = {
    "Qualquer época": None,
    "Clássico (antes de 2000)": (0, 1999),
    "Anos 2000": (2000, 2009),
    "Recente (após 2010)": (2010, 9999)
}

def save_maps(le):
    """Salva os mapeamentos e lista de gêneros para uso no Streamlit"""
    maps = {
        "generos": list(le.classes_),
        "duracao": DURACAO_PARA_MINUTOS,
        "decada": DECADA_PARA_ANOS
    }
    with open("data/maps.pkl", "wb") as f:
        pickle.dump(maps, f)

# ============================================================
# 5. TREINAMENTO DA ÁRVORE DE DECISÃO
# ============================================================

def train_model(df):
    """Treina a Árvore de Decisão"""

    # Define as features (entradas) e o target (saída)
    features = ["Genre_encoded", "Runtime", "Meta_score", "No_of_Votes"]
    target = "Recomendado"

    X = df[features]
    y = df[target]

    # Divide os dados em treino (80%) e teste (20%)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ============================================================
    # ÁRVORE DE DECISÃO
    # max_depth=5 evita overfitting
    # criterion="gini" usa o índice Gini para divisão dos nós
    # ============================================================
    model = DecisionTreeClassifier(max_depth=5, criterion="gini", random_state=42)
    model.fit(X_train, y_train)

    # Avalia o modelo
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    cm = confusion_matrix(y_test, y_pred)

    print(f"\n### Modelo treinado ###")
    print(f"Acurácia: {acc:.2%}")
    print(f"Matriz de Confusão:\n{cm}")

    return model, features

# ============================================================
# 6. VISUALIZAÇÃO DA ÁRVORE
# ============================================================

def visualize_tree(model, features):
    """Gera e salva a visualização da árvore de decisão"""
    plt.figure(figsize=(20, 10))
    plot_tree(
        model,
        feature_names=features,
        class_names=["Não Recomendado", "Recomendado"],
        filled=True,
        rounded=True,
        fontsize=10
    )
    plt.title("MapTheSoul - Árvore de Decisão")
    plt.savefig("data/decision_tree.png", dpi=150, bbox_inches="tight")
    print("\n### Árvore salva em data/decision_tree.png ###")

# ============================================================
# 7. SALVA O MODELO TREINADO
# ============================================================

def save_model(model):
    """Salva o modelo treinado para uso posterior no Streamlit"""
    with open("data/model.pkl", "wb") as f:
        pickle.dump(model, f)
    print("### Modelo salvo em data/model.pkl ###")

# ============================================================
# EXECUÇÃO PRINCIPAL
# ============================================================

if __name__ == "__main__":
    df = load_data()
    df = prepare_data(df)
    df, le = encode_data(df)
    save_maps(le)
    model, features = train_model(df)
    visualize_tree(model, features)
    save_model(model)
    print("\n✅ Pipeline completo; modelo pronto para uso.")