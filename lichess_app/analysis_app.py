# Streamlit dependencies
import streamlit as st
import joblib, os

from streamlit_option_menu import option_menu # need to pip install streamlit-option-menu to use this

# Data dependencies
import pandas as pd
import datetime
import numpy as np

import plotly.express as px
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# Load your raw data
@st.cache_resource  # 👈 Add the caching decorator
def load_data():
	df = pd.read_csv("f:/lichess_data/merged_data/2013_merged_files.csv")
	df["DateTime"] = pd.to_datetime(df["UTCDate"] + ' ' + df["UTCTime"])
	df["DateTime"] = df["DateTime"] + pd.Timedelta(hours=1) # Lichess servers are in France (UTC + 1)
	df = df.drop(["UTCDate", "UTCTime", "Unnamed: 0.1", "Unnamed: 0"], axis=1)
	return df

data = load_data()

@st.cache_resource
def get_top_20_active_users(df):
	white_players = df.groupby(['GameType', 'White']).size().nlargest(20).reset_index(name='GamesPlayed')
	black_players = df.groupby(['GameType', 'Black']).size().nlargest(20).reset_index(name='GamesPlayed')
	return white_players, black_players

white_players, black_players = get_top_20_active_users(data)

# @st.cache_resource
# def get_top_20_rated_users(df):
# 	white_ratings = df.groupby(['GameType', 'White'])['WhiteElo'].max().nlargest(20).reset_index(name='Rating')
# 	black_ratings = df.groupby(['GameType', 'Black'])['BlackElo'].max().nlargest(20).reset_index(name='Rating')
# 	combined_players_ratings = pd.concat([white_ratings, black_ratings], ignore_index=True)
# 	return combined_players_ratings


@st.cache_resource
def filter_game_type(df):
	return list(df["GameType"].unique())

game_type_list = filter_game_type(data)

@st.cache_resource
def filter_opening(df):
	return list(df["Opening"].unique())

opening_list = filter_opening(data)

@st.cache_resource
def filter_white_piece_players(df):
	return list(df["White"].unique())

white_piece_players_list = filter_white_piece_players(data)

@st.cache_resource
def filter_black_piece_players(df):
	return list(df["Black"].unique())

black_piece_players_list = filter_black_piece_players(data)

all_players = white_piece_players_list + black_piece_players_list
all_players_unique = list(set(all_players))
all_players_unique = sorted(all_players_unique, key = str.lower)

def main():
	st.title("Lichess Insights")

	with st.sidebar:
		selection = option_menu(
			menu_title = "Main Menu",
			options = ["Info", "Analysis", "Contact"],
			icons = ["info-square", "bar-chart-line", "envelope"],
			default_index = 1,
			menu_icon = "house",
			styles = {
			"container": {"padding": "0!important", "background-color": "#fafafa"},
			"icon": {"color": "black", "font-size": "25px"}, 
			"nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
			"nav-link-selected": {"background-color": "blue"},
		})

	# Building out the info page
	if selection == "Info":
		st.info("Purpose of the app", icon="🤷‍♂️")
		st.markdown("Something")

		st.info("How to use this app", icon="💡")
		st.markdown("Something")

		st.info("Data description", icon="📚")
		st.markdown(f"""The data was manually downloaded from the [Lichess database](https://database.lichess.org/) website. Only data for 2013 was used.
Future work involves optimising the data to utilise more without slowing down the app. A sample of the raw data looks like this:
		
	[Event "Rated Classical game"]
	[Site "https://lichess.org/j1dkb5dw"]
	[White "BFG9k"]
	[Black "mamalak"]
	[Result "1-0"]
	[UTCDate "2012.12.31"]
	[UTCTime "23:01:03"]
	[WhiteElo "1639"]
	[BlackElo "1403"]
	[WhiteRatingDiff "+5"]
	[BlackRatingDiff "-8"]
	[ECO "C00"]
	[Opening "French Defense: Normal Variation"]
	[TimeControl "600+8"]
	[Termination "Normal"]

	1. e4 e6 2. d4 b6 3. a3 Bb7 4. Nc3 Nh6 5. Bxh6 gxh6 6. Be2 Qg5 7. Bg4 h5 8. Nf3 Qg6 9. Nh4 Qg5 10. Bxh5 Qxh4 11. Qf3 Kd8 12. Qxf7 Nc6 13. Qe8# 1-0""")
		st.markdown("This raw data was then converted to CSV. A sample of the CSV data can be viewed below (To view the raw data, select the checkbox):")

		if st.checkbox("Show raw data"): # data is hidden if box is unchecked
			st.write(data.head(10)) # will write the df to the page

	# Building out the analysis page
	if selection == "Analysis":
		st.info("This page explains information gathered from the data. To expand the image, hover over it and click the expand arrows that appear.", icon = "🕵️‍♂️")
		#-------------------------------------------------------------
		df_game_type = data.groupby(["GameType"]).mean(numeric_only=True)
		st.write(df_game_type)

		game_type_counts = data['GameType'].value_counts().reset_index()
		game_type_counts.columns = ['GameType', 'Count']

		# Plotting the bar graph using Plotly Express
		fig = px.bar(game_type_counts, x='Count', y='GameType', color='GameType',
					labels={'GameType': 'Game Type', 'Count': 'Count'},
					title='Counts of Different Game Types', color_discrete_sequence= px.colors.sequential.Plasma_r[::3])
		fig.update_layout(xaxis={'categoryorder': 'total descending'})
		st.plotly_chart(fig, use_container_width=True)

		# st.write(white_players)
		fig_white_games = px.bar(white_players, x='White', y='GamesPlayed', color='GameType',
                          title='Top 20 White Players by Games Played per GameType', color_discrete_sequence= px.colors.sequential.Plasma_r[::3])
		fig_white_games.update_layout(xaxis={'categoryorder': 'total descending'})
		st.plotly_chart(fig_white_games, use_container_width=True)

		fig_black_games = px.bar(black_players, x='Black', y='GamesPlayed', color='GameType',
                          title='Top 20 Black Players by Games Played per GameType', color_discrete_sequence= px.colors.sequential.Plasma_r[::3])
		fig_black_games.update_layout(xaxis={'categoryorder': 'total descending'})
		st.plotly_chart(fig_black_games, use_container_width=True)

		viz = st.checkbox("Game Type") 
		if viz:
			st.write("""In the dropdown menu below, you can select your favourite director and see how financial 
        		backing (or lack thereof) may have influenced their creations.""")
			event_type = st.selectbox(label = "Choose an event type", options = game_type_list)
			filtered_data = data[data['GameType'] == event_type]
			st.write(f"There are a total of {len(filtered_data)} {event_type} games.")
			st.write(filtered_data.head())

			time_control_counts = filtered_data['TimeControl'].value_counts().reset_index()
			time_control_counts.columns = ['TimeControl', 'Count']

			top_10_time_controls = time_control_counts.head(10)

			fig = px.bar(top_10_time_controls, x='Count', y='TimeControl', color='TimeControl',
					labels={'TimeControl': 'Time Control', 'Count': 'Count'},
					title='Top 10 Time Controls', color_discrete_sequence= px.colors.sequential.Plasma_r[::3])
			fig.update_layout(xaxis={'categoryorder': 'total descending'})
			st.plotly_chart(fig, use_container_width=True)

			opening_counts = filtered_data['Opening'].value_counts().reset_index()
			opening_counts.columns = ['Opening', 'Count']

			top_10_openings = opening_counts.head(10)

			fig = px.bar(top_10_openings, x='Count', y='Opening', color='Opening',
					labels={'Opening': 'Opening', 'Count': 'Count'},
					title='Top 10 Openings', color_discrete_sequence= px.colors.sequential.Plasma_r[::3])
			fig.update_layout(xaxis={'categoryorder': 'total descending'})
			st.plotly_chart(fig, use_container_width=True)

			checkmate_counts = filtered_data['Checkmate'].value_counts().reset_index()
			checkmate_counts.columns = ['Checkmate', 'Count']

			fig = px.pie(checkmate_counts, values='Count', names='Checkmate',
            labels={'Checkmate': 'Checkmate', 'Count': 'Count'},
            title='Counts of Different Checkmate Types', 
            color_discrete_sequence=px.colors.sequential.Plasma_r)
			st.plotly_chart(fig, use_container_width=True)

		viz = st.checkbox("Openings") 
		if viz:
			st.markdown("Openings stuff")

		viz = st.checkbox("Player") 
		if viz:
			st.markdown("Player stuff")
			player_name = st.selectbox(label = "Choose a player", options = all_players_unique)
			filtered_data = data[(data['White'] == player_name) | (data['Black'] == player_name)]
			st.write(f"There are a total of {len(filtered_data)} {player_name} games.")
			st.write(filtered_data.head())

			game_type_counts = filtered_data['GameType'].value_counts().reset_index()
			game_type_counts.columns = ['GameType', 'Count']

			fig = px.bar(game_type_counts, x='Count', y='GameType', color='GameType',
						labels={'GameType': 'Game Type', 'Count': 'Count'},
						title='Counts of Different Game Types', color_discrete_sequence= px.colors.sequential.Plasma_r[::3])
			fig.update_layout(xaxis={'categoryorder': 'total descending'})
			st.plotly_chart(fig, use_container_width=True)

			checkmate_counts = filtered_data['Checkmate'].value_counts().reset_index()
			checkmate_counts.columns = ['Checkmate', 'Count']

			fig = px.pie(checkmate_counts, values='Count', names='Checkmate',
            labels={'Checkmate': 'Checkmate', 'Count': 'Count'},
            title='Counts of Different Checkmate Types', 
            color_discrete_sequence=px.colors.sequential.Plasma_r[::3])
			st.plotly_chart(fig, use_container_width=True)

			opening_counts = filtered_data['Opening'].value_counts().reset_index()
			opening_counts.columns = ['Opening', 'Count']

			top_10_openings = opening_counts.head(10)

			fig = px.bar(top_10_openings, x='Count', y='Opening', color='Opening',
					labels={'Opening': 'Opening', 'Count': 'Count'},
					title=f'Top 10 Openings by {player_name}', color_discrete_sequence= px.colors.sequential.Plasma_r[::3])
			fig.update_layout(xaxis={'categoryorder': 'total descending'})
			st.plotly_chart(fig, use_container_width=True)

			def get_game_results(df):
				wins = df[((df['White'] == player_name) & (df['Result'] == '1-0')) | ((df['Black'] == player_name) & (df['Result'] == '0-1'))].shape[0]
				draws = df[((df['White'] == player_name) | (df['Black'] == player_name)) & (df['Result'] == '1/2-1/2')].shape[0]
				losses = df[((df['Black'] == player_name) & (df['Result'] == '1-0')) | (df['White'] == player_name) & (df['Result'] == '0-1')].shape[0]
				return wins, draws, losses
			
			wins, draws, losses = get_game_results(filtered_data)

			outcomes_df = pd.DataFrame({'Outcomes': ['Wins', 'Draws', 'Losses'], 'Count': [wins, draws, losses]})
			fig = px.pie(outcomes_df, values='Count', names='Outcomes', title=f"{player_name}'s Game Outcomes",
             color_discrete_sequence=px.colors.sequential.Plasma_r[::3])
			st.plotly_chart(fig, use_container_width=True)

			#------------------------------------------------------------------------------------
			col1, col2, col3, col4 = st.columns(4)

			with col1:
				player_classical_games_df = filtered_data[(filtered_data['GameType'] == "Classical")]

				wins, draws, losses = get_game_results(player_classical_games_df)

				outcomes_df = pd.DataFrame({'Outcomes': ['Wins', 'Draws', 'Losses'], 'Count': [wins, draws, losses]})
				fig = px.pie(outcomes_df, values='Count', names='Outcomes', title=f"{player_name}'s Classical Game Results",
				color_discrete_sequence=px.colors.sequential.Plasma_r[::3])
				st.plotly_chart(fig, use_container_width=True)

				total_games = len(player_classical_games_df)
				games_played_text = "game" if total_games == 1 else "games"
				wins_text = "win" if wins == 1 else "wins"
				draws_text = "draw" if draws == 1 else "draws"
				losses_text = "loss" if losses == 1 else "losses"

				st.markdown(f"In {total_games} Classical {games_played_text} played, there were {wins} {wins_text}, {draws} {draws_text}, and {losses} {losses_text}.")

			#------------------------------------------------------------------------------------
			with col2:
				player_blitz_games_df = filtered_data[(filtered_data['GameType'] == "Blitz")]

				wins, draws, losses = get_game_results(player_blitz_games_df)

				outcomes_df = pd.DataFrame({'Outcomes': ['Wins', 'Draws', 'Losses'], 'Count': [wins, draws, losses]})
				fig = px.pie(outcomes_df, values='Count', names='Outcomes', title=f"{player_name}'s Blitz Game Results",
				color_discrete_sequence=px.colors.sequential.Plasma_r[::3])
				st.plotly_chart(fig, use_container_width=True)

				total_games = len(player_blitz_games_df)
				games_played_text = "game" if total_games == 1 else "games"
				wins_text = "win" if wins == 1 else "wins"
				draws_text = "draw" if draws == 1 else "draws"
				losses_text = "loss" if losses == 1 else "losses"

				st.markdown(f"In {total_games} Blitz {games_played_text} played, there were {wins} {wins_text}, {draws} {draws_text}, and {losses} {losses_text}.")

			#------------------------------------------------------------------------------------
			with col3:
				player_bullet_games_df = filtered_data[(filtered_data['GameType'] == "Bullet")]

				wins, draws, losses = get_game_results(player_bullet_games_df)

				outcomes_df = pd.DataFrame({'Outcomes': ['Wins', 'Draws', 'Losses'], 'Count': [wins, draws, losses]})
				fig = px.pie(outcomes_df, values='Count', names='Outcomes', title=f"{player_name}'s Bullet Game Results",
				color_discrete_sequence=px.colors.sequential.Plasma_r[::3])
				st.plotly_chart(fig, use_container_width=True)

				total_games = len(player_bullet_games_df)
				games_played_text = "game" if total_games == 1 else "games"
				wins_text = "win" if wins == 1 else "wins"
				draws_text = "draw" if draws == 1 else "draws"
				losses_text = "loss" if losses == 1 else "losses"

				st.markdown(f"In {total_games} Bullet {games_played_text} played, there were {wins} {wins_text}, {draws} {draws_text}, and {losses} {losses_text}.")
				
			#------------------------------------------------------------------------------------
			with col4:
				player_correspondence_games_df = filtered_data[(filtered_data['GameType'] == "Correspondence")]

				wins, draws, losses = get_game_results(player_correspondence_games_df)

				outcomes_df = pd.DataFrame({'Outcomes': ['Wins', 'Draws', 'Losses'], 'Count': [wins, draws, losses]})
				fig = px.pie(outcomes_df, values='Count', names='Outcomes', title=f"{player_name}'s Correspondence Game Results",
				color_discrete_sequence=px.colors.sequential.Plasma_r[::3])
				st.plotly_chart(fig, use_container_width=True)

				total_games = len(player_correspondence_games_df)
				games_played_text = "game" if total_games == 1 else "games"
				wins_text = "win" if wins == 1 else "wins"
				draws_text = "draw" if draws == 1 else "draws"
				losses_text = "loss" if losses == 1 else "losses"

				st.markdown(f"In {total_games} Correspondence {games_played_text} played, there were {wins} {wins_text}, {draws} {draws_text}, and {losses} {losses_text}.")

	
	if selection == "Contact":
		st.info("This page explains information gathered from the data. To expand the image, hover over it and click the expand arrows that appear.", icon = "🕵️‍♂️")

# Required to let Streamlit instantiate our web app.  
if __name__ == '__main__':
	main()
