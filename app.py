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
    "A (Avalanche)",
    "E (Ravinement/Ruissellement)",
    "G (Glissement de terrain)",
    "I (Inondation)",
    "P (Chute de bloc)",
    "T (Crue torrentielle)"
    ]

fiabilites = [
    "Élevée",
    "Moyenne",
    "Faible"
]
####################################

@st.cache_data
def load_data():
    return pd.read_feather("data/2026_08_17.feather")

st.set_page_config(
    page_title="Analyse fréquentielle de la BDRTM",
    layout="wide"
)

pages = [
    st.Page("pages/01_accueil.py", title="Accueil"),
    st.Page("pages/02_analyse_locale.py", title="Analyse fréquentielle locale"),
    st.Page("pages/03_analyse_globale.py", title="Analyse fréquentielle globale"),
]

pg = st.navigation(pages, position="hidden")

# Widgets communs dans la sidebar
with st.sidebar:
    col1, col2, col3 = st.columns([1, 5, 1])

    with col2:
        st.image("./images/onf.png")

    st.divider()

    st.page_link(pages[0], label="Accueil")
    st.page_link(pages[1], label="Analyse fréquentielle locale")
    st.page_link(pages[2], label="Analyse fréquentielle globale")

    st.divider()

    # st.header("Echelle d'analyse")

    st.session_state.echelle = st.selectbox("Echelle d'analyse",
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

    st.session_state.fiabilites = st.multiselect("Indicateurs qualitatifs de fiabilité",
                                                 fiabilites,
                                                 help="""
                                                L'effet de ce filtre est visible dans les onglets d'analyse fréquentielle locale et gloable.
                                                """
                                    )

    # st.markdown(
    #     """
    #     <div style="text-align: center; margin-top: 20px;">
    #         <a href="www.onf.fr" target="_blank">
    #             www.onf.fr
    #         </a>
    #     </div>
    #     """,
    #     unsafe_allow_html=True
    # )

st.session_state.df = load_data()

pg.run()
