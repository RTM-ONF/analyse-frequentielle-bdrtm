import numpy as np
import pandas as pd
import plotly.express as px
from scipy.stats import chi2
import streamlit as st


st.title("Analyse fréquentielle globale")

with st.expander("Détails des indicateurs statistiques"):
    st.markdown(
        """
        ##### Durée d'observation
        $$T$$

        ##### Nombre d'observations
        $$N$$

        ##### Fréquence moyenne annuelle
        $$\\lambda = \\frac{N}{T}$$

        ##### Probabilité d'occurrence annuelle
        $$P = 1 - e^{-\\lambda}$$

        ##### Période de retour
        $$T_r = \\frac{1}{\\lambda}$$

        ##### Ecart type
        $$\\sigma = \\frac{\\sqrt{N}}{T}$$

        ##### Intervalle de confiance à 95% inférieur
        $$IC_{inf} = \\frac{1}{2T} \\chi^2_{\\left[\\frac{\\alpha}{2}, 2N\\right]}$$

        ##### Intervalle de confiance à 95% supérieur
        $$IC_{sup} = \\frac{1}{2T} \\chi^2_{\\left[1-\\frac{\\alpha}{2}, 2N+1\\right]}$$

        ##### Indicateur qualitatif de fiabilité
        - fiabilité faible : moins de 3 événements
        - fiabilité moyenne : entre 3 et 9 événements
        - fiabilité élevée : 10 événements ou plus
        """
    )

df = st.session_state.df

if st.session_state.departements != []:
    departements = [departement[:2] for departement in st.session_state.departements]
    df = df[df["Département"].isin(departements)]

df = df[df["Année"].between(st.session_state.annee_min, st.session_state.annee_max)]

if st.session_state.phenomenes != []:
    phenomenes = [phenomene[0] for phenomene in st.session_state.phenomenes]
    df = df[df["Phénomène"].isin(phenomenes)]

if st.session_state.echelle == "Département":
    df = df[["Département", "Année", "Phénomène"]]

if st.session_state.echelle == "EPCI":
    df["EPCI"] = df["EPCI"].str.split(",")
    df = df.explode("EPCI")
    if st.session_state.selection != "":
        selection = st.session_state.selection.split(",")
        selection = [epci.strip() for epci in selection]
        df = df[df["EPCI"].isin(selection)]

    df = df[["Département", "Année", "EPCI", "Phénomène"]]

if st.session_state.echelle == "Commune":
    df["Commune"] = df["Commune"].str.split(";")
    df = df.explode("Commune")
    if st.session_state.selection != "":
        selection = st.session_state.selection.split(",")
        selection = [commune.strip() for commune in selection]
        df = df[df["Commune"].isin(selection)]

    df = df[["Département", "Année", "Commune", "Phénomène"]]

if st.session_state.echelle == "Site":
    if st.session_state.selection != "":
        selection = st.session_state.selection.split(",")
        selection = [site.strip() for site in selection]
        df = df[df["Site"].isin(selection)]

    df = df[["Département", "Année", "Site", "Phénomène"]]

if st.session_state.phenomenes == []:
    all_pheno = "_".join(["A", "E", "G", "I", "P", "T"])
elif len(st.session_state.phenomenes) > 1:
    all_pheno = "_".join([phenomene[0] for phenomene in st.session_state.phenomenes])

table_1 = df.groupby([st.session_state.echelle, "Phénomène"]).size().reset_index(name="Nombre d'événements")

if len(st.session_state.phenomenes) > 1 or st.session_state.phenomenes == []:
    table_2 = df.groupby(st.session_state.echelle).size().reset_index(name="Nombre d'événements")
    table_2["Phénomène"] = all_pheno
    df = pd.concat([table_1, table_2])
    df.reset_index(drop=True)
else:
    df = table_1
    df.reset_index(drop=True)

T = st.session_state.annee_max - st.session_state.annee_min

df["Début"] = st.session_state.annee_min
df["Fin"] = st.session_state.annee_max
df["Durée"] = T
df["Fréquence moyenne annuelle"] = df["Nombre d'événements"] / T
df["Probabilité d'occurrence annuelle"] = 1. - np.exp(-df["Fréquence moyenne annuelle"])
df["Période de retour"] = 1. / df["Fréquence moyenne annuelle"]
df["Ecart type"] = np.sqrt(df["Nombre d'événements"]) / T

alpha = 0.05

df["Intervalle de confiance à 95% inférieur"] = chi2.ppf(alpha / 2., 2. * df["Nombre d'événements"]) / (2. * T)
df["Intervalle de confiance à 95% supérieur"] = chi2.ppf(1. - alpha / 2., 2. * (df["Nombre d'événements"] + 1)) / (2. * T)

df["Indicateur qualitatif de fiabilité"] = np.select(
    [
        df["Nombre d'événements"] < 3,
        df["Nombre d'événements"].between(3, 10, inclusive="both"),
        df["Nombre d'événements"] > 10
    ],
    [1, 2, 3]
)
df["Indicateur qualitatif de fiabilité"] = df["Indicateur qualitatif de fiabilité"].map({
    1: "Faible",
    2: "Moyenne",
    3: "Élevée"
})

df = (
    df.groupby("Phénomène")["Nombre d'événements"]
      .sum()
      .reset_index()
)

df["Début"] = st.session_state.annee_min
df["Fin"] = st.session_state.annee_max
df["Durée"] = T
df["Fréquence moyenne annuelle"] = df["Nombre d'événements"] / T
df["Probabilité d'occurrence annuelle"] = 1. - np.exp(-df["Fréquence moyenne annuelle"])
df["Période de retour"] = 1. / df["Fréquence moyenne annuelle"]
df["Ecart type"] = np.sqrt(df["Nombre d'événements"]) / T

alpha = 0.05

df["Intervalle de confiance à 95% inférieur"] = chi2.ppf(alpha / 2., 2. * df["Nombre d'événements"]) / (2. * T)
df["Intervalle de confiance à 95% supérieur"] = chi2.ppf(1. - alpha / 2., 2. * (df["Nombre d'événements"] + 1)) / (2. * T)

df["Indicateur qualitatif de fiabilité"] = np.select(
    [
        df["Nombre d'événements"] < 3,
        df["Nombre d'événements"].between(3, 10, inclusive="both"),
        df["Nombre d'événements"] > 10
    ],
    [1, 2, 3]
)
df["Indicateur qualitatif de fiabilité"] = df["Indicateur qualitatif de fiabilité"].map({
    1: "Faible",
    2: "Moyenne",
    3: "Élevée"
})

st.dataframe(df, hide_index=True)

mapping ={
    "A": "Avalanche (A)",
    "E": "Ravinement/Ruissellement (E)",
    "G": "Mouvement de terrain (G)",
    "I": "Inondation (I)",
    "P": "Chute de bloc (P)",
    "T": "Crue torrentielle (T)"
}

df = df[df["Phénomène"].isin(["A", "E", "G", "I", "P", "T"])]
df["Phénomène"] = df["Phénomène"].map(mapping)

st.write(f"{len(df)} phénomènes observés.")

color_map = {
    "Avalanche (A)" : "#66C5CC",
    "Ravinement/Ruissellement (E)" : "#F6CF71",
    "Mouvement de terrain (G)" : "#F89C74",
    "Inondation (I)": "#DCB0F2",
    "Chute de bloc (P)": "#87C55F",
    "Crue torrentielle (T)": "#9EB9F3"
}

fig = px.pie(
    df,
    title="Répartition globale du nombre d'événements observés",
    names="Phénomène",
    values="Nombre d'événements",
    color="Phénomène",
    color_discrete_map=color_map,
)

fig.update_traces(
    textinfo="percent+label",
    marker=dict(
        line=dict(width=1)
    ),
)

fig.update_layout(
    legend=dict(
        title="Phénomène",
    ),
)

st.plotly_chart(fig, use_container_width=True)

#######################################################
df["erreur_sup"] = (
    df["Intervalle de confiance à 95% supérieur"]
    - df["Fréquence moyenne annuelle"]
)

df["erreur_inf"] = (
    df["Fréquence moyenne annuelle"]
    - df["Intervalle de confiance à 95% inférieur"]
)

fig = px.bar(
    df,
    title="Répartition globale de la fréquence moyenne annuelle",
    x="Phénomène",
    y="Fréquence moyenne annuelle",
    color="Phénomène",
    color_discrete_map=color_map,
)

fig.update_traces(
    error_y=dict(
        type="data",
        symmetric=False,
        array=df["erreur_sup"],
        arrayminus=df["erreur_inf"]
    )
)

st.plotly_chart(fig, use_container_width=True)
