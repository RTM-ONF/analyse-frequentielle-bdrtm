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
    Les données utilisées dans cette application sont issues d'une extraction de la BDRTM en date du **17 août 2026**.
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

st.dataframe(df, hide_index=True)

st.write(f"{len(df)} événements.")

df = df.groupby(["Année", "Phénomène"]).size().reset_index(name="Nombre d'événements")

mapping ={
    "A": "Avalanche",
    "E": "Ravinement/Ruissellement",
    "G": "Mouvement de terrain",
    "I": "Inondation",
    "P": "Chute de bloc",
    "T": "Crue torrentielle"
}

df["Phénomène"] = df["Phénomène"].map(mapping)

fig = px.bar(
    df,
    x="Année",
    y="Nombre d'événements",
    color="Phénomène",
    barmode="stack",
    color_discrete_sequence=px.colors.qualitative.Pastel
)

fig.update_layout(
    title="Evolution du nombre d'événements observés au cours du temps",
    xaxis_title="Année",
    yaxis_title="Nombre d'événements"
)
st.plotly_chart(fig, use_container_width=True)

# st.header("Analyse fréquentielle")

# st.subheader("Analyse locale par phénomène")

# if st.session_state.phenomenes == []:
#     all_pheno = "_".join(["A", "E", "G", "I", "P", "T"])
# elif len(st.session_state.phenomenes) > 1:
#     all_pheno = "_".join([phenomene[0] for phenomene in st.session_state.phenomenes])

# table_1 = df.groupby([st.session_state.echelle, "Phénomène"]).size().reset_index(name="Nombre d'événements")

# if len(st.session_state.phenomenes) > 1 or st.session_state.phenomenes == []:
#     table_2 = df.groupby(st.session_state.echelle).size().reset_index(name="Nombre d'événements")
#     table_2["Phénomène"] = all_pheno
#     df = pd.concat([table_1, table_2])
#     df.reset_index(drop=True)
# else:
#     df = table_1
#     df.reset_index(drop=True)

# T = st.session_state.annee_max - st.session_state.annee_min

# df["Début"] = st.session_state.annee_min
# df["Fin"] = st.session_state.annee_max
# df["Durée"] = T
# df["Fréquence moyenne annuelle"] = df["Nombre d'événements"] / T
# df["Probabilité d'occurrence annuelle"] = 1. - np.exp(-df["Fréquence moyenne annuelle"])
# df["Période de retour"] = 1. / df["Fréquence moyenne annuelle"]
# df["Ecart type"] = np.sqrt(df["Nombre d'événements"]) / T

# alpha = 0.05

# df["Intervalle de confiance à 95% inférieur"] = chi2.ppf(alpha / 2., 2. * df["Nombre d'événements"]) / (2. * T)
# df["Intervalle de confiance à 95% supérieur"] = chi2.ppf(1. - alpha / 2., 2. * (df["Nombre d'événements"] + 1)) / (2. * T)

# df["Indicateur qualitatif de fiabilité"] = np.select(
#     [
#         df["Nombre d'événements"] < 3,
#         df["Nombre d'événements"].between(3, 10, inclusive="both"),
#         df["Nombre d'événements"] > 10
#     ],
#     [1, 2, 3]
# )
# df["Indicateur qualitatif de fiabilité"] = df["Indicateur qualitatif de fiabilité"].map({
#     1: "Faible",
#     2: "Moyenne",
#     3: "Élevée"
# })

# st.dataframe(df, hide_index=True)

# st.write(f"{len(df)} entrées.")

# st.subheader("Analyse globale par phénomène")

# df = (
#     df.groupby("Phénomène")["Nombre d'événements"]
#       .sum()
#       .reset_index()
# )

# df["Début"] = st.session_state.annee_min
# df["Fin"] = st.session_state.annee_max
# df["Durée"] = T
# df["Fréquence moyenne annuelle"] = df["Nombre d'événements"] / T
# df["Probabilité d'occurrence annuelle"] = 1. - np.exp(-df["Fréquence moyenne annuelle"])
# df["Période de retour"] = 1. / df["Fréquence moyenne annuelle"]
# df["Ecart type"] = np.sqrt(df["Nombre d'événements"]) / T

# alpha = 0.05

# df["Intervalle de confiance à 95% inférieur"] = chi2.ppf(alpha / 2., 2. * df["Nombre d'événements"]) / (2. * T)
# df["Intervalle de confiance à 95% supérieur"] = chi2.ppf(1. - alpha / 2., 2. * (df["Nombre d'événements"] + 1)) / (2. * T)

# df["Indicateur qualitatif de fiabilité"] = np.select(
#     [
#         df["Nombre d'événements"] < 3,
#         df["Nombre d'événements"].between(3, 10, inclusive="both"),
#         df["Nombre d'événements"] > 10
#     ],
#     [1, 2, 3]
# )
# df["Indicateur qualitatif de fiabilité"] = df["Indicateur qualitatif de fiabilité"].map({
#     1: "Faible",
#     2: "Moyenne",
#     3: "Élevée"
# })

# st.dataframe(df, hide_index=True)

# st.write(f"{len(df)} phénomènes.")