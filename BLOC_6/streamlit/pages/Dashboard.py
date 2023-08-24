import streamlit as st
import pandas as pd
import plotly.express as px


data = st.session_state['data']

## ----------- DASHBOARD PAGE ------------

# Titre de la page
st.markdown(
    "<h1 style='text-align: center;'>Data Jobs Dashboard</h1>",
    unsafe_allow_html=True
)
    
# Texte
st.markdown(
    "<h3 style='text-align: center;'>Visualisation du marché de l'emploi français dans les métiers de la data</h3>",
    unsafe_allow_html=True
)
# Sélection d'options de filtrage par cluster
cluster_options = ["Tout voir"] + data["cluster"].unique().tolist()
cluster_filter = st.selectbox("Type d'emploi", cluster_options)
    
if cluster_filter == "Tout voir":
    filtered_data = data
else:
    filtered_data = data[data["cluster"] == cluster_filter]
    
# Sélection d'option de filtrage par skills
skills_options = ["Tout voir"] + data['skills'].str.split(', ', expand=True).stack().unique().tolist()
skills_filter = st.selectbox("Skills", skills_options)
    
if skills_filter == "Tout voir":
    filtered_data = filtered_data
else:
    filtered_data = filtered_data[filtered_data["skills"] == skills_filter]
    
# Création d'une carte pour visualiser les offres d'emploi
def createmapbox(data):
    fig = px.scatter_mapbox(data, lat='lat', lon='lon', hover_name="job_title", hover_data="skills", color="job_class", height=600, color_discrete_sequence=px.colors.qualitative.Prism)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(mapbox=dict(center=dict(lat=46.603354, lon=1.888334), zoom=5))
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.update_traces(marker=dict(size=10))
    return fig

mapbox = createmapbox(filtered_data)
st.plotly_chart(mapbox,use_container_width = True)

# Séparation
st.markdown("----------------")

# Histogramme pour visualiser le nombres d'offres / type d'emploi recherché
fig = px.histogram(
    data,
    x="job_class",
    color="job_class",
    title="Offre d'emploi / types de poste",
    labels={'job_class' : "Types de poste",
            "count": "Nombre d'offres"}
    )
fig.update_layout(showlegend=False, title_text="Offre d'emploi / types de poste", yaxis_title="Nombre d'offres", title_x=0.4)
st.plotly_chart(fig, use_container_width = True)

# Séparation
st.markdown('--------------')

# Sélection d'options de filtrage par cluster
cluster = ["Tout voir"] + data["cluster"].unique().tolist()
cluster_filter2 = st.selectbox("Type de poste", cluster, key="cluster_filter2")

# Création d'un masque pour récupérer seulement le top 10 des skills / clusters
if cluster_filter2 == "Tout voir":
    filtered_data2 = data['skills'].str.split(', ', expand=True).stack().value_counts()
    top_skills = data['skills'].str.split(', ', expand=True).stack().value_counts()
    filtered_data2 = top_skills.head(10).to_frame('count')
    filtered_data2 = filtered_data2.rename_axis('skills').reset_index()
else:
    mask =data['cluster']==cluster_filter2
    new_data = data.where(mask)
    top_skills = new_data['skills'].str.split(', ', expand=True).stack().value_counts()
    filtered_data2 = top_skills.head(10).to_frame('count')
    filtered_data2 = filtered_data2.rename_axis('skills').reset_index()

# Histogramme pour visualiser le top 10 des skills
fig2 = px.histogram(
    filtered_data2,
    x="skills",
    y="count",
    color="skills",
    color_discrete_sequence=px.colors.qualitative.Prism
)
fig2.update_layout(showlegend=False, title_text="Top 10 des compétences les plus mentionnées",
                   yaxis_title="Nombre d'offres", title_x=0.4)
st.plotly_chart(fig2, use_container_width = True)

# Histogramme pour visualiser le top 10 des compagnies qui recrutent le plus
company = data['job_company'].value_counts().head(10)
top_company = pd.DataFrame({"Société" : company.index, "Nombre d'offre": company.values})
fig3 = px.histogram(
    top_company,
    x="Société",
    y="Nombre d'offre",
    color="Société",
    color_discrete_sequence=px.colors.qualitative.Dark2
)
fig3.update_layout(showlegend=False, title_text="Top 10 des entreprises qui recrutent le plus",
                   yaxis_title="Nombre d'offres", title_x=0.4)
st.plotly_chart(fig3, use_container_width = True)