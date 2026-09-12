import streamlit as st
import pandas as pd

##### A MODIFIER EN CAS DE MAJ #####
min_year = 1900

max_year = 2026

echelles = [
    "Département",
    "EPCI",
    "Commune",
    "Site"
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
    "E (Ravinement/Ruissellement)",
    "G (Glissements de terrain)",
    "I (Inondations)",
    "P (Chutes de bloc)",
    "T (Crues torrentielles)"
    ]
####################################

@st.cache_data
def load_data():
    return pd.read_feather("data/2026_08_17.feather")

st.set_page_config(
    page_title="Analyse fréquentielle de la BDRTM",
    layout="wide"
)

# Widgets communs dans la sidebar
with st.sidebar:
    st.header("Echelle d'analyse")

    st.session_state.echelle = st.selectbox("Echelle",
                                            echelles,
                                    )

    if st.session_state.echelle != "Département":
        st.session_state.selection = st.text_input(
            "Sélection",
            help="""
            Indiquer les valeurs à sélectionner. Utiliser la virgule comme séparateur.\n
            Exemple avec une échelle d'analyse communale :\n
                Grenoble, Gières, La Tronche, Claix
            """
            )

    st.header("Filtres")

    st.session_state.departements = st.multiselect("Départements",
                                                    departements,
                                    )

    st.session_state.annee_min, st.session_state.annee_max = st.slider("Période",
                                                                       min_value=min_year,
                                                                       max_value=max_year,
                                                                       value=(2000, max_year)
                                                            )

    st.session_state.phenomenes = st.multiselect("Phénomènes",
                                                 phenomenes,
                                    )


# Définition des pages
pg = st.navigation([
    st.Page("pages/01_accueil.py", title="Accueil")
])

st.session_state.df = load_data()

pg.run()
