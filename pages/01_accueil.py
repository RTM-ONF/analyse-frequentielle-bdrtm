import streamlit as st

st.title("Analyse fréquentielle de la BDRTM")

col1, col2, col3 = st.columns([3,2,3])

st.write(
    """
    Placer ici un texte d'introduction / présentation / limites de l'outil...
    """
)

df = st.session_state.df
if st.session_state.departements != []:
    departements = [int(departement[:2]) for departement in st.session_state.departements]
    df = df[df["Dept"].isin(departements)]

df = df[df["an_evt"].between(st.session_state.annee_min, st.session_state.anne_max)]

if st.session_state.phenomenes != []:
    phenomenes = [phenomene[0] for phenomene in st.session_state.phenomenes]
    df = df[df["EV_pheno"].isin(phenomenes)]

st.write(df)

st.write(f"{len(df)} entrées.")

with col2:
    st.image("images/onf.png", width="stretch")

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