import pandas as pd
import streamlit as st
import plotly.express as px

def main():
    st.set_page_config(layout="wide")
    st.title('NBA Lineup Analysis Tool')

    # Upload file via Streamlit
    uploaded_file = st.file_uploader("NBALineup2024.csv", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # User chooses team 
        team = st.selectbox('Choose Your Team:', df['team'].unique())
        
        # Get just the selected team 
        df_team = df[df['team'] == team].reset_index(drop=True)

        # Get players on roster
        df_team['players_list'] = df_team['players_list'].str.replace(r"[\"\' \[\]]", '', regex=True).str.split(',')
        duplicate_roster = df_team['players_list'].apply(pd.Series).stack()
        roster = duplicate_roster.unique()

        players = st.multiselect('Select your players', roster, roster[0:5])

        # Find the right lineup
        df_lineup = df_team[df_team['players_list'].apply(lambda x: set(x) == set(players))]
        df_important = df_lineup[['MIN', 'PLUS_MINUS', 'FG_PCT', 'FG3_PCT']]

        if not df_important.empty:
            st.dataframe(df_important)
        else:
            st.write("No lineup found for the selected players.")

        col1, col2, col3, col4 = st.columns(4)

        if not df_important.empty:
            with col1:
                fig_min = px.histogram(df_team, x="MIN")
                fig_min.add_vline(x=df_important['MIN'].values[0], line_color='red')
                st.plotly_chart(fig_min, use_container_width=True)

            with col2:
                fig_plus_minus = px.histogram(df_team, x="PLUS_MINUS")
                fig_plus_minus.add_vline(x=df_important['PLUS_MINUS'].values[0], line_color='red')
                st.plotly_chart(fig_plus_minus, use_container_width=True)

            with col3:
                fig_fg_pct = px.histogram(df_team, x="FG_PCT")
                fig_fg_pct.add_vline(x=df_important['FG_PCT'].values[0], line_color='red')
                st.plotly_chart(fig_fg_pct, use_container_width=True)

            with col4:
                fig_fg3_pct = px.histogram(df_team, x="FG3_PCT")
                fig_fg3_pct.add_vline(x=df_important['FG3_PCT'].values[0], line_color='red')
                st.plotly_chart(fig_fg3_pct, use_container_width=True)

if __name__ == "__main__":
    main()

