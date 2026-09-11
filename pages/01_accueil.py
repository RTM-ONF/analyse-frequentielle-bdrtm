import numpy as np
import pandas as pd
from scipy.stats import chi2
import streamlit as st

def convert_for_download(d):
    csv = pd.DataFrame(d).to_csv(index=False, sep=";")
    return csv.encode("utf-8-sig")

st.title("Analyse fréquentielle de la BDRTM")

st.header("Données")

df = st.session_state.df
if st.session_state.departements != []:
    departements = [departement[:2] for departement in st.session_state.departements]
    df = df[df["Dept"].isin(departements)]

df = df[df["an_evt"].between(st.session_state.annee_min, st.session_state.annee_max)]

if st.session_state.phenomenes != []:
    phenomenes = [phenomene[0] for phenomene in st.session_state.phenomenes]
    df = df[df["EV_pheno"].isin(phenomenes)]

if st.session_state.echelle == "Département":
    df = df[["Dept", "an_evt", "EV_pheno"]]

if st.session_state.echelle == "EPCI":
    df["epci"] = df["epci"].str.split(",")
    df = df.explode("epci")
    df = df[["Dept", "an_evt", "epci", "EV_pheno"]]

if st.session_state.echelle == "Commune":
    df["SI_communes"] = df["SI_communes"].str.split(";")
    df = df.explode("SI_communes")
    df = df[["Dept", "an_evt", "SI_communes", "EV_pheno"]]

if st.session_state.echelle == "Site":
    df = df[["Dept", "an_evt", "SI_code", "EV_pheno"]]

st.write(df)

st.write(f"{len(df)} événements.")

st.header("Analyse fréquentielle")

echelles = {
    "Département": "Dept",
    "EPCI": "epci",
    "Commune": "SI_communes",
    "Site": "SI_code"
}

if st.session_state.phenomenes == []:
    all_pheno = "_".join(["A", "E", "G", "I", "P", "T"])
elif len(st.session_state.phenomenes) > 1:
    all_pheno = "_".join([phenomene[0] for phenomene in st.session_state.phenomenes])

table_1 = df.groupby([echelles[st.session_state.echelle], "EV_pheno"]).size().reset_index(name="nb_evt")

if len(st.session_state.phenomenes) > 1 or st.session_state.phenomenes == []:
    table_2 = df.groupby(echelles[st.session_state.echelle]).size().reset_index(name="nb_evt")
    table_2["EV_pheno"] = all_pheno
    df = pd.concat([table_1, table_2])
    df.reset_index(drop=True)
else:
    df = table_1
    df.reset_index(drop=True)

T = st.session_state.annee_max - st.session_state.annee_min

df["lambda"] = df["nb_evt"] / T
df["proba_occ"] = 1. - np.exp(-df["lambda"])
df["T_retour"] = 1. / df["lambda"]
df["sigma"] = np.sqrt(df["nb_evt"]) / T

alpha = 0.05

df["IC_inf"] = chi2.ppf(alpha / 2., 2. * df["nb_evt"]) / (2. * T)
df["IC_sup"] = chi2.ppf(1. - alpha / 2., 2. * (df["nb_evt"] + 1)) / (2. * T)

df["fiabilite"] = np.select(
    [
        df["nb_evt"] < 3,
        df["nb_evt"].between(3, 10, inclusive="both"),
        df["nb_evt"] > 10
    ],
    [1, 2, 3]
)

fiabilite_table = df["fiabilite"].map({ 1: "faible", 2: "moyenne", 3: "élevée"})

st.write(df)

st.table(fiabilite_table.value_counts())

csv = convert_for_download(df)
st.download_button(label="Télécharger l'analyse fréquentielle dans un fichier .csv",
                    data=csv,
                    file_name="analyse_frequentielle_bdrtm.csv"
                    )

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