import numpy as np
import pandas as pd
from scipy.stats import chi2
import streamlit as st


st.title("Analyse fréquentielle de la BDRTM")

st.header("Données")

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
    df = df[["Département", "Année", "EPCI", "Phénomène"]]

if st.session_state.echelle == "Commune":
    df["Commune"] = df["Commune"].str.split(";")
    df = df.explode("Commune")
    df = df[["Département", "Année", "Commune", "Phénomène"]]

if st.session_state.echelle == "Site":
    df = df[["Département", "Année", "Site", "Phénomène"]]

st.dataframe(df, hide_index=True)

st.write(f"{len(df)} événements.")

st.header("Analyse fréquentielle")

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
df["Période"] = T
df["Lambda"] = df["Nombre d'événements"] / T
df["Probabilité d'occurence"] = 1. - np.exp(-df["Lambda"])
df["Période de retour"] = 1. / df["Lambda"]
df["Sigma"] = np.sqrt(df["Nombre d'événements"]) / T

alpha = 0.05

df["IC inférieur"] = chi2.ppf(alpha / 2., 2. * df["Nombre d'événements"]) / (2. * T)
df["IC supérieur"] = chi2.ppf(1. - alpha / 2., 2. * (df["Nombre d'événements"] + 1)) / (2. * T)

df["Fiabilité"] = np.select(
    [
        df["Nombre d'événements"] < 3,
        df["Nombre d'événements"].between(3, 10, inclusive="both"),
        df["Nombre d'événements"] > 10
    ],
    [1, 2, 3]
)

st.dataframe(df, hide_index=True)

st.write(f"{len(df)} entrées.")

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