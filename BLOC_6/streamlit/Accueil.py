import streamlit as st
import pandas as pd
import plotly.express as px 
import matplotlib as plt
from PIL import Image
#https://datanerd.tech/
#docker run -p 8501:8501 streamlit_jobs
#streamlit run streamlit_r.py --server.port=8501 --server.address=0.0.0.0 pwd
#pip install streamlit-aggrid
### CONFIG


# Paramètres de la page
st.set_page_config(
    page_title="DataMatch",
    layout="wide",
    initial_sidebar_state='auto'
)

# Importation des données
@st.cache_data
def load_data():
    data = pd.read_csv('/Users/cheyen/Desktop/jedha_fullstack/BLOC_6/streamlit/data/dataset_finalv13.csv')
    return data


# Stockage des données dans une variable
data = load_data()
st.session_state["data"] = data

st.markdown(
        """
<style>
    
span[data-baseweb="tag"] {
background-color: grey !important;
}
</style>
""",

    unsafe_allow_html=True,
)

# Titre
st.markdown("<h1 style='text-align: center; margin-bottom: 30px;'><span style='font-size: 80px;'>DataMatch</h1>", unsafe_allow_html=True)

# Texte explicatif projet
st.markdown("<p style='text-align: center; padding: 50px; margin-bottom: 10px;'><span style='font-size: 20px;'>Naviguer dans le complexe marché de l'emploi de la data peut être un défi de taille. Les intitulés de poste se multiplient, sont parfois obscurs, sont parfois déconnectés de la réalité des responsabilités qu'ils impliquent.</span></p>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; margin-bottom: 10px; padding: 50px;'><span style='font-size: 20px;'>Notre application, DataMatch, utilise l'intelligence artificielle pour simplifier votre recherche d'emploi en vous permettant une recherche par cluster d'offres similaires en termes de compétences et de responsabilités. Découvrez des opportunités insoupçonnées et maximisez vos chances de succès grâce à notre vue d'ensemble complète du marché du travail de la data.</p>", unsafe_allow_html=True)

# Wordcloud / clusters
image1 = Image.open("/Users/cheyen/Desktop/jedha_fullstack/BLOC_6/streamlit/png/wordcloud1.png")
image2 = Image.open("/Users/cheyen/Desktop/jedha_fullstack/BLOC_6/streamlit/png/wordcloud2_bis.png")
image3 = Image.open("/Users/cheyen/Desktop/jedha_fullstack/BLOC_6/streamlit/png/wordcloud3.png")


def plot_wordcloud_without_background(wordcloud):
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)

st.markdown(
    """
    <style>
    .stImage>div>div>div>img {
        pointer-events: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.subheader("Clusters")

col1, col2, col3 = st.columns(3)

with col1:
    st.write("Engineering, Data Environment")
    st.image(image1, use_column_width=True, clamp=True)

with col2:
    st.write("Data Analsye, Data Science")
    st.image(image2, use_column_width=True, clamp=True)

with col3:
    st.write("Consulting")
    st.image(image3, use_column_width=True, clamp=True)


st.markdown("--------------------")

# Sélection d'options de filtrage par cluster
options_pie = ["Tout voir"] + data["cluster"].unique().tolist()
filtre_pie = st.selectbox("Type de poste", options_pie, key="pie_filter")
    
if filtre_pie == "Tout voir":
    data_pie = data
else:
    data_pie = data[data["cluster"] == filtre_pie]
    
couleurs = ["#131862","#2e4482","#073763","#005073","#107dac","#189ad3","#1ebbd7","#71c7ec", "#76b6c4","#7fcdff",
            "#2986cc","#d0e0e3","#a8d7e0","#60a2af"]
# Camembert pour visualiser le nombres d'offres / clusters et par job_class
fig_pie = px.pie(
    data_pie,
    names = "job_class",
    color="job_class",
    title="Offre d'emploi / clusters",
    height=750,
    width=450,
    color_discrete_sequence=couleurs
    )
fig_pie.update_layout(showlegend=False, title_text="Offre d'emploi / cluster et types d'emploi", title_x=0.4)
fig_pie.update_traces(textinfo='label+percent')

st.plotly_chart(fig_pie, use_container_width = True)

# https://gist.github.com/asehmi/dc26e9e5693f20662979509e472a860b
# https://blog.streamlit.io/auto-generate-a-dataframe-filtering-ui-in-streamlit-with-filter_dataframe/


