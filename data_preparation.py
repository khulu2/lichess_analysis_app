# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 02:12:48 2023

@author: user
"""

import chess.pgn
import pandas as pd
import re
import gc

def count_moves_and_checkmate(moves):
    move_pattern = re.compile(r'\d+\.\s+(\S+)')

    # Extract moves using the pattern
    extracted_moves = move_pattern.findall(moves)

    # Count the number of extracted moves
    num_moves = len(extracted_moves)
    checkmate = moves.endswith("#")  # Check if the last move ends with '#', indicating checkmate
    return num_moves, checkmate

for year in range(2013, 2014):
    for month in range(1,13):
        if month < 10:
            string_month = "0" + str(month)
        else:
            string_month = str(month)

        file_name = f"f:/lichess_data/original_data/lichess_db_standard_rated_{year}-{string_month}.pgn"

        

        pgn = open(file_name)
        games = []
        j = 0
        while True:
            print(f"Converting to list | {year} | {string_month} | {j}")
            game= chess.pgn.read_game(pgn)
            if game is not None:
                games.append(game)
                j += 1
            else: 
                break

        
        list_of_games = []
        i = 0
        for game in games:
            try:
                print(f"Converting to dict | {year} | {string_month} | {i} / {len(games)}")
                moves = str(game.mainline_moves())
                num_moves, checkmate = count_moves_and_checkmate(moves)
                
                individual_game = {
                "Event": game.headers["Event"], 
                "Site": game.headers["Site"], 
                "White": game.headers["White"], 
                "Black": game.headers["Black"], 
                "Result": game.headers["Result"], 
                "UTCDate": game.headers["UTCDate"], 
                "UTCTime": game.headers["UTCTime"],
                "WhiteElo": game.headers["WhiteElo"], 
                "BlackElo": game.headers["BlackElo"], 
                "WhiteRatingDiff": game.headers["WhiteRatingDiff"], 
                "BlackRatingDiff": game.headers["BlackRatingDiff"], 
                "ECO": game.headers["ECO"],
                "Opening": game.headers["Opening"], 
                "TimeControl": game.headers["TimeControl"], 
                "Termination": game.headers["Termination"], 
                "Moves": moves,
                "NumMoves": num_moves,
                "Checkmate": checkmate}
                
                list_of_games.append(individual_game)
                i += 1
            except KeyError:
                pass  # skip the incomplete entries

        print(f"Saving for... {year}_{month}")
        pd.DataFrame(list_of_games).to_csv(f"f:/lichess_data/csv_data/{year}_{month}.csv")
        gc.collect()
                    
    