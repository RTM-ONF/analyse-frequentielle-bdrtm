import numpy as np
import pandas as pd
import plotly.express as px
from scipy.stats import chi2
import streamlit as st


st.title("Analyse fréquentielle de la BDRTM")

with st.expander("Avertissement – Clause de non-responsabilité"):
    st.markdown(
        """
        Cette application est fournie à titre informatif et pédagogique. Les calculs, estimations et résultats produits par ce logiciel sont basés sur des modèles, hypothèses et données qui peuvent comporter des approximations ou des simplifications.

        Malgré le soin apporté à son développement et à sa validation, aucune garantie n’est donnée quant à l’exactitude, l’exhaustivité ou l’actualité des informations et résultats fournis.

        En conséquence, les auteurs, développeurs et distributeurs de cette application ne sauraient être tenus responsables des erreurs, omissions ou des conséquences directes ou indirectes résultant de l’utilisation des informations, résultats ou recommandations fournis par ce logiciel.

        L’utilisateur demeure seul responsable de l’interprétation des résultats et de l’usage qu’il en fait. Il lui appartient notamment de vérifier la pertinence des hypothèses, des paramètres d’entrée et des résultats obtenus au regard de son contexte d’utilisation.

        Cette application ne se substitue en aucun cas à une expertise technique, scientifique ou professionnelle. Toute décision fondée sur les résultats fournis par ce logiciel relève de la seule responsabilité de l’utilisateur.

        L’utilisation de cette application implique l’acceptation pleine et entière des présentes conditions.
        """
    )

st.header("Données")

st.markdown(
    """
    Les données utilisées dans cette application sont issues d'une extraction de la BDRTM réalisée le 17 août 2026.

    - Une entrée correspond à un événement.
    - Chaque événement est associé à une année, un site et un phénomène.
    - Un site appartient à un département.
    - Un site peut être rattaché à plusieurs communes.
    - Un site peut être rattaché à plusieurs EPCI.

    **Important :** lorsqu'une analyse est réalisée à l'échelle des communes ou des EPCI, le nombre total d'événements affiché peut être supérieur au nombre d'événements initial. En effet, un même événement est comptabilisé pour chacune des communes ou chacun des EPCI intersectés par le site auquel il est rattaché.
    """
)

st.write(f"Nombre total d'événements : {len(st.session_state.df)}")

df = st.session_state.df

if st.session_state.departements != []:
    departements = [departement[:2] for departement in st.session_state.departements]
    df = df[df["Département"].isin(departements)]

df = df[df["Année"].between(st.session_state.annee_min, st.session_state.annee_max)]

if st.session_state.phenomenes != []:
    phenomenes = [phenomene[0] for phenomene in st.session_state.phenomenes]
    df = df[df["Phénomène"].isin(phenomenes)]

if st.session_state.echelle == "Département":
    df = df[["Département", "Année", "Site", "Phénomène"]]

if st.session_state.echelle == "EPCI":
    df["EPCI"] = df["EPCI"].str.split(",")
    df = df.explode("EPCI")
    if st.session_state.selection != "":
        selection = st.session_state.selection.split(",")
        selection = [epci.strip() for epci in selection]
        df = df[df["EPCI"].isin(selection)]

    df = df[["Département", "Année", "Site", "EPCI", "Phénomène"]]

if st.session_state.echelle == "Commune":
    df["Commune"] = df["Commune"].str.split(";")
    df = df.explode("Commune")
    if st.session_state.selection != "":
        selection = st.session_state.selection.split(",")
        selection = [commune.strip() for commune in selection]
        df = df[df["Commune"].isin(selection)]

    df = df[["Département", "Année", "Site", "Commune", "Phénomène"]]

if st.session_state.echelle == "Site":
    if st.session_state.selection != "":
        selection = st.session_state.selection.split(",")
        selection = [site.strip() for site in selection]
        df = df[df["Site"].isin(selection)]

    df = df[["Département", "Année", "Site", "Phénomène"]]

st.dataframe(df, hide_index=True)

st.write(f"Nombre d'événements sélectionnés : {len(df)}")

df = df.groupby(["Année", "Phénomène"]).size().reset_index(name="Nombre d'événements")

mapping ={
    "A": "Avalanche (A)",
    "E": "Ravinement/Ruissellement (E)",
    "G": "Mouvement de terrain (G)",
    "I": "Inondation (I)",
    "P": "Chute de bloc (P)",
    "T": "Crue torrentielle (T)"
}

df["Phénomène"] = df["Phénomène"].map(mapping)

color_map = {
    "Avalanche (A)" : "#66C5CC",
    "Ravinement/Ruissellement (E)" : "#F6CF71",
    "Mouvement de terrain (G)" : "#F89C74",
    "Inondation (I)": "#DCB0F2",
    "Chute de bloc (P)": "#87C55F",
    "Crue torrentielle (T)": "#9EB9F3"
}

fig = px.bar(
    df,
    title="Evolution du nombre d'événements observés au cours du temps",
    x="Année",
    y="Nombre d'événements",
    color="Phénomène",
    barmode="stack",
    color_discrete_map=color_map
)

fig.update_layout(
    legend=dict(
        title="",
        orientation="h",
        yanchor="bottom",
        y=1.0
    )
)

st.plotly_chart(fig, width="stretch")
