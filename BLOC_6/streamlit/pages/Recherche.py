import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from streamlit_modal import Modal
#https://datanerd.tech/
#docker run -it -p 8501:8501 streamlit pwd
#streamlit run streamlit_r.py --server.port=8501 --server.address=0.0.0.0 pwd
#pip install streamlit-aggrid
### CONFIG

data = st.session_state['data']

st.markdown(
        """
<style>
span[data-baseweb="tag"] {background-color: grey !important;}
</style>
""",
   unsafe_allow_html=True,
)

st.markdown(
        """
<style>
div[data-modal-container='true'] {color: black !important;}
</style>
""",
    unsafe_allow_html=True)

## ------------ RESEARCH PAGE --------------

### Titre et texte
st.title("Recherche Job")

st.markdown("""
    Recherche des offres par cluster 👇
""")

gb = GridOptionsBuilder()
gb.configure_grid_options(tooltipShowDelay=1, )

gb.configure_default_column(
    resizable=True,
    filterable=True,
    sortable=True,
    editable=False,
)

gb.configure_column(field="job_title", header_name="Intitulé", width=300)
gb.configure_column(field="job_description", header_name="Description", width=600)
gb.configure_column(field="job_company", header_name="Entreprise", width=200)
gb.configure_selection('single', use_checkbox=True)

go = gb.build()

#st.markdown("Sélection des mots-clés")
# multi select box

skills = data['skills'].str.split(', ', expand=True).stack().unique().tolist()

# first argument takes the box title
# second argument takes the options to show
to_filter_cluster= st.multiselect("Cluster", data['cluster'].sort_values().unique())
 
# write the selected options
st.write("Vous avez sélectionné", len(to_filter_cluster), 'cluster(s)')

mask =data['cluster'].isin(to_filter_cluster)
new_data = data.where(mask).dropna()


modify = st.checkbox("Ajouter un filtre")
if not modify:
    # dataset with no filter
    if len(to_filter_cluster) == 0 :
       
        tab = AgGrid(data,  gridOptions=go, height=500, theme="alpine", allow_unsafe_jscode=True, GridUpdateMode=GridUpdateMode.MODEL_CHANGED)
        selected_row = tab["selected_rows"]
        st.metric("Nombre d'offres sélectionnées", len(data))
        if not selected_row == []:
            #st.write("Descriptif du poste :", selected_row[0]['job_description'])
            modal = Modal(key="Demo Key",title="Descriptif du poste")
            open_modal = st.button(label="Détail de l'offre")
            if open_modal:
                with modal.container():
                    st.markdown(selected_row[0]['job_description'])
    
    else :
        # dataset with cluster filter
        tab = AgGrid(new_data, gridOptions=go, height=500, theme="alpine", allow_unsafe_jscode=True, GridUpdateMode=GridUpdateMode.MODEL_CHANGED)
        selected_row = tab["selected_rows"]
        st.metric("Nombre d'offres sélectionnées", len(new_data))
        if not selected_row == []:
            #st.write("Descriptif du poste :", selected_row[0]['job_description'])
            modal = Modal(key="Demo Key",title="Descriptif du poste")
            open_modal = st.button(label="Détail de l'offre")
            if open_modal:
                with modal.container():
                    st.markdown(selected_row[0]['job_description'])
        
else :    
    if len(to_filter_cluster) == 0 :
        st.error("🚨 S'il vous plait, veuillez choisir au moins un cluster")
    #### Create columns to add filters
    col1, col2, col3 = st.columns(3)
    with col1:
        modification_container = st.container()
        with modification_container:
            to_filter_platform= st.multiselect("Platform", data['platform'].sort_values().unique())
            st.write("Vous avez sélectionné", len(to_filter_platform), 'platform(s)')
            if not len(to_filter_platform) == 0 :
                mask =data['platform'].isin(to_filter_platform)
                new_data = new_data.where(mask).dropna()

    with col2:
        modification_container = st.container()
        with modification_container:
            to_filter_loc = st.multiselect("Location", data['location'].sort_values().unique())
            st.write("Vous avez sélectionné", len(to_filter_loc), 'location(s)')
            if not len(to_filter_loc ) == 0 :
                mask =data['location'].isin(to_filter_loc)
                new_data = new_data.where(mask).dropna()

    with col3:
        modification_container = st.container()
        with modification_container:
            to_filter_skill= st.multiselect("Skills: ", sorted(skills))
            st.write("Vous avez sélectionné", len(to_filter_skill), 'skill(s)')
            if not len(to_filter_skill) == 0 :
                mask =data['skills'].isin(to_filter_skill)
                new_data = new_data.where(mask).dropna()
    if new_data.empty : 
        st.markdown("<h1 style='text-align: center;'>Pas d'annonces avec les critères souhaités</h1>", unsafe_allow_html=True)  
    else :
        tab_bis = AgGrid(new_data, gridOptions=go, height=500, theme="alpine", allow_unsafe_jscode=True, GridUpdateMode=GridUpdateMode.MODEL_CHANGED )
        selected_row = tab_bis["selected_rows"]
        st.metric("Nombre d'offres sélectionnées", len(new_data))
        if not selected_row == []:
         #st.write("Descriptif du poste :", selected_row[0]['job_description'])
        
            modal = Modal(key="2 Key",title="Descriptif du poste")
            open_modal = st.button(label="Détail de l'offre")
            if open_modal:
                with modal.container():
                    st.markdown(selected_row[0]['job_description'])



