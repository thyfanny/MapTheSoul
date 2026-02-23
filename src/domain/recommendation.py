import pandas as pd

def recomendation(genero: str, duracao, decada, nota_minima, model, encoder, maps, df):
    """Filter and rank movies based on user preferences"""
    df_filtrado = df[df["Genre"].apply(lambda x: genero in [g.strip() for g in x.split(",")])].copy()

    min_dur, max_dur = maps["duracao"][duracao]
    df_filtrado = df_filtrado[(df_filtrado["Runtime"] >= min_dur) & (df_filtrado["Runtime"] <= max_dur)]

    if maps["decada"][decada] is not None:
        min_ano, max_ano = maps["decada"][decada]
        df_filtrado = df_filtrado[(df_filtrado["Released_Year"] >= min_ano) & (df_filtrado["Released_Year"] <= max_ano)]

    df_filtrado = df_filtrado[df_filtrado["IMDB_Rating"] >= nota_minima]

    if df_filtrado.empty:
        return pd.DataFrame()

    df_filtrado["Genre_encoded"] = encoder.transform([genero] * len(df_filtrado))
    features = ["Genre_encoded", "Runtime", "Meta_score", "No_of_Votes"]

    df_filtrado["Recomendado"] = model.predict(df_filtrado[features])

    return df_filtrado[df_filtrado["Recomendado"] == 1][
        ["Series_Title", "Genre", "IMDB_Rating", "Runtime", "Released_Year"]
    ].sample(frac=1).head(10)