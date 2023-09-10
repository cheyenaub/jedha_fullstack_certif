import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns 
import streamlit as st

#link
#https://my-dashboard-chey-a086f6b143ed.herokuapp.com/

### Configuration
st.set_page_config(
    page_title = "GetAround Dashboard",
    layout = "wide",
    initial_sidebar_state="auto"
)

st.title("GetAround Dashboard Analysis")
st.markdown("""
        Hello ! 👋  
        With this dashboard you will discover some good informations about GetAround app !  
        When people rent a car they have to follow few steps like checkin at the beginning and checkout at the end of the rent. To help users with theses steps,  
        GetAround offers two solutions :   
        Mobile 📱 : when driver and owner meet and sign the rental agreement of the owner's smartphone  
        Connect 🛜 : when the driver doesn't meet the owner, everything is done with the application created by GetAround  
        This dashboard answers two questions :   
        - What threshold should be set to limit the impact of delays?
        - This threshold should be enable on all cars ? Or only Connect cars ?""")

# Data
@st.cache_data()
def load_data():
    data = pd.read_csv('data/get_around_delay_clean.csv')
    return data

data = load_data()

data['delay'] = data['delay_at_checkout_in_minutes'].apply(lambda x: 1 if x>0 else 0)
delay_checkout = []
for delay in data['delay_at_checkout_in_minutes']:
    if delay < 0:
        delay_checkout.append('Early')
    elif delay < 15:
        delay_checkout.append('Late 0-15')
    elif delay < 30:
        delay_checkout.append('Late 15-30')
    elif delay < 60:
        delay_checkout.append('Late 30-60')
    elif delay < 120:
        delay_checkout.append('Late 60-120')
    elif delay >= 120:
        delay_checkout.append('Very late')
    else:
        delay_checkout.append('NA')
    
data['time_delay'] = delay_checkout

st.markdown("Let's see the delays time and the impact of the checkin type on the delays")
col1, col2 = st.columns(2)
with col1:
    fig1 = px.pie(
        data,
        values='delay',
        names = 'checkin_type',
        color_discrete_sequence=px.colors.qualitative.G10
        )

    fig1.update_layout(showlegend=False, title_text="Delays by checkin type", title_x=0.5)
    fig1.update_traces(textinfo='label+percent')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.pie(
        data,
        names = 'time_delay',
        color_discrete_sequence=px.colors.qualitative.G10
        )
    fig2.update_layout(showlegend=False, title_text="Delay time", title_x=0.5)
    fig2.update_traces(textinfo='label+percent')
    st.plotly_chart(fig2, use_container_width=True)
    
st.markdown("As we see, there is lot more delays with Mobile checkin/checkout than with Connect, maybe it is a lot faster to do the checkin and checkout with Connect but it's hard to say because there is a lot more Mobile users than Connect.")
    
st.markdown("-------------------------------------")

st.markdown("The biggest problem with theses delays is that they can create dissatisfaction when the next user can't pick up the car on time.")
st.subheader("How many users are impacted by the delay of previous rentals ?")

data['difference'] = data['delay_at_checkout_in_minutes'] - data['time_delta_with_previous_rental_in_minutes']
impacted_users = data[data['difference'] >= 0]
not_impacted = data[data['difference'] < 0]

fig3 = px.histogram(
    impacted_users,
    x = 'difference',
    color_discrete_sequence = ['purple'],
)
fig3.add_trace(px.histogram(
    not_impacted,
    x='difference',
    color_discrete_sequence=['yellow']).data[0]
    )

fig3.update_layout(title="Impacted and not impacted users by the delays")
st.plotly_chart(fig3, use_container_width=True)
st.markdown("""The yellow part represent the users that are not impacted by the delays while the purple section indicate the users that are impacted. This is what we need to fight in order to resolve users dissatisfaction.  
            Impacted users are the users who cannot collect the car at the chosen time because the previous driver is late.  
            One of the solution can be to introduce a delay between two reservations.'""")

st.markdown("----------------------------------------")

st.subheader("What threshold should be set to limit the number of customers affected by delays?")

def plot_impact_solved_graph(data):
    threshold = np.arange(0, 720, step=15) # 0 à 12 heures avec un pas de 15 minutes
    impacted_mobile = []
    impacted_connect = []
    total_impacted = []
    solved_mobile = []
    solved_connect = []
    solved_total = []

    for delay in threshold:
        impacted = data.dropna(subset=['time_delta_with_previous_rental_in_minutes'])
        impact_connect = impacted[impacted['checkin_type'] == 'connect']
        impact_connect = impact_connect[impact_connect['difference'] > delay]
        impact_mobile = impacted[impacted['checkin_type'] == 'mobile']
        impact_mobile = impact_mobile[impact_mobile['difference'] > delay]
        impacted = impacted[impacted['difference'] > delay]
        impacted_mobile.append(len(impact_mobile))
        impacted_connect.append(len(impact_connect))
        total_impacted.append(len(impacted))

        solved = data.dropna(subset=['time_delta_with_previous_rental_in_minutes'])
        solve_connect = solved[solved['checkin_type'] == 'connect']
        solve_connect = solve_connect[solve_connect['difference'] < delay]
        solve_mobile = solved[solved['checkin_type'] == 'mobile']
        solve_mobile = solve_mobile[solve_mobile['difference'] < delay]
        solved = solved[solved['difference'] < delay]
        solved_mobile.append(len(solve_mobile))
        solved_connect.append(len(solve_connect))
        solved_total.append(len(solved))

    # Créez les graphiques avec Matplotlib
    fig, ax = plt.subplots(1, 2, sharex=True, figsize=(20, 7))
    ax[0].plot(threshold, solved_connect)
    ax[0].plot(threshold, solved_mobile)
    ax[0].plot(threshold, solved_total)
    ax[1].plot(threshold, impacted_connect)
    ax[1].plot(threshold, impacted_mobile)
    ax[1].plot(threshold, total_impacted)
    ax[0].set_xlabel('Threshold (min)')
    ax[0].set_ylabel('Number of impacted cases & cases solved')
    ax[0].legend(['Connect solved', 'Mobile solved', 'Total solved'])
    ax[1].legend(['Connect impacted', 'Mobile impacted', 'Total impacted'])

    # Affichez les graphiques dans Streamlit
    st.pyplot(fig)

plot_impact_solved_graph(data)

st.subheader("Conclusion")
st.markdown("""We can easily observe a great decrease in impacted cases around 100 minutes of delay and inversely for the solved cases. Thanks to this data we can estimate that a threshold between 90 and 120 minutes between two reservations is the best solutions to limit the impact of delays from previous reservation and optimize the flow between owners and drivers.  
            Mobile and Connect checkin seems to have the same behaviour so the feature can be implemented on both checkin type. However, the Connect method has a smaller sample size and may be interesting for initial testing.""")