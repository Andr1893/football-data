from connect import Connect


"""
    Get APi KEY https://www.football-data.org/
"""



con = Connect('Input APIKEY')

print(con.getCompetitions('TIER_ONE'))
print(con.getMatches())
