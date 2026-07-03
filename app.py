import streamlit as st
import pandas as pd

##### A MODIFIER EN CAS DE MAJ #####
min_year = 1000

max_year = 2026

versions = [
    "avril 2026"
]

departements = [
    "04 (Alpes-de-Haute-Provence)",
    "05 (Hautes-Alpes)",
    "06 (Alpes-Maritimes)",
    "09 (Ariège)",
    "11 (Aude)",
    "31 (Haute-Garonne)",
    "38 (Isère)",
    "64 (Pyrénées-Atlantiques)",
    "65 (Hautes-Pyrénées)",
    "66 (Pyrénées-Orientales)",
    "73 (Savoie)",
    "74 (Haute-Savoie)"
    ]

phenomenes = [
    "A (Avalanches)",
    "G (Glissements de terrain)",
    "P (Chutes de bloc)",
    "T (Crues torrentielles)"
    ]
####################################

@st.cache_data
def load_data():
    return pd.read_feather(f"data/{st.session_state.version.replace(" ", "_")}.feather")

st.set_page_config(
    page_title="Analyse fréquentielle de la BDRTM",
    layout="wide"
)

# Widgets communs dans la sidebar
with st.sidebar:
    st.header("Extraction de la BDRTM")

    st.session_state.version = st.selectbox("Version",
                                            versions,
                                            index=0
                                    )

    st.header("Filtres")

    st.session_state.departements = st.multiselect("Départements",
                                                    departements,
                                    )

    st.session_state.annee_min, st.session_state.anne_max = st.slider("Période",
                                                                      min_value=min_year,
                                                                      max_value=max_year,
                                                                      value=(min_year, max_year)
                                                            )

    st.session_state.phenomenes = st.multiselect("Phénomènes",
                                                 phenomenes,
                                    )


# Définition des pages
pg = st.navigation([
    st.Page("pages/01_accueil.py", title="Accueil"),
    st.Page("pages/02_analyse_departement.py", title="Analyse à l'échelle du département"),
    st.Page("pages/03_analyse_site.py", title="Analyse à l'échelle du site"),
    st.Page("pages/04_analyse_commune.py", title="Analyse à l'échelle de la commune"),
])

st.session_state.df = load_data()

# Exécution de la page sélectionnée
pg.run()