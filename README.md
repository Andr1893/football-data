# football-data


<ul>
  <li>python Library</li>
  <li><a href="https://www.football-data.org/documentation/quickstart">Documentation</a></li>
  <li><a href="https://www.football-data.org/documentation/quickstart">Documentation</a></li>
</ul>


# Build from source
    $ git clone https://github.com/Andr1893/football-data.git
    $ Run - py main.py
    
You need to get api key to the site 
[football-data](https://www.football-data.org/)
# exemple code
  ```python
     from connect import Connect

     con = Connect('Input APIKEY') 
     
     print(con.getCompetitions('TIER_ONE'))
     print(con.getMatches())
 
