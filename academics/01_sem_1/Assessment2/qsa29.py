#Cricket Match Result
# Two cricket teams A and B have played a match. The result is decided based on the
# following rules:
# The team with higher runs is declared the winner.
# If the runs are the same, the team with fewer wickets lost is the winner.
# If both runs and wickets lost are also the same, the match is declared a Draw.
#Input Format
# First line: two integers → runs scored by Team A and wickets lost by Team A.
# Second line: two integers → runs scored by Team B and wickets lost by Team B.
# output Format
# Print one of the following:
#  "Team A Wins"
# "Team B Wins"
# "Team A Wins by wickets"
# "Team B Wins by wickets"
# "Match Drawn"
runs_A=int(input("Enter run of team A"))
wickets_A=int(input("Enter wicket of team A"))
runs_B=int(input("Enter run of team b"))
wickets_B=int(input("Enter wicket of team A"))
if runs_A > runs_B:
    print("Team A Wins")
elif runs_B > runs_A:
    print("Team B Wins")
else:  
    if wickets_A < wickets_B:
        print("Team A Wins by wickets")
    elif wickets_B < wickets_A:
        print("Team B Wins by wickets")
    else:
        print("Match Drawn")
