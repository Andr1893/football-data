import urllib, requests
import json
from enum import Enum
from exceptions import APIErrorException
from headers import Headers

class Connect:

    endpoint= 'http://api.football-data.org'


    Competitions = {
        'Competition': '/v2/competitions/{id}',
        'Team': '/v2/competitions/{id}/teams',
        'Standings': '/v2/competitions/{id}/standings',
        'Match': '/v2/competitions/{id}/matches',
        'Scorers': '/v2/competitions/{id}/scorers'
    }

    Matches = {
        'Match': '/v2/matches/{id}'
    }

    Teams = {
        'Team': '/v2/teams/{id}',
        'Match': '/v2/teams/{id}/matches'
    }

    Players = {
        'Player': '/v2/players/{id}',
        'Match': '/v2/players/{id}/matches'
    }

    Areas = {
        'Area': '/v2/areas/{id}'
    }

    responseHeaders = Headers()


    def __init__(self, APItoken: str):
        self.headers = { 'X-Auth-Token': APItoken }
    

    def getResponse(self, url:str,  params=None):

        req = requests.get(url, headers = self.headers, params = params) if params != None else requests.get(url, headers = self.headers)

        status_code = req.status_code
        print(status_code)
        if status_code == requests.codes.ok:

            try:
                self.responseHeaders.APIVersion = req.headers['X-API-Version']
                self.responseHeaders.Data = req.headers['Date']
                self.responseHeaders.RequestCounterReset = req.headers['X-RequestCounter-Reset']
                self.responseHeaders.RequestsAvailableMinute = req.headers['X-Requests-Available-Minute']
                self.responseHeaders.AuthenticatedClient = req.headers['X-Authenticated-Client']
            except APIErrorException as identifier:
                print(identifier)

       
            return req
        elif status_code == requests.codes.bad:
            raise APIErrorException('Invalid request. Check parameters.')
        elif status_code == requests.codes.forbidden:
            raise APIErrorException('This resource is restricted')
        elif status_code == requests.codes.not_found:
            raise APIErrorException('This resource does not exist. Check parameters')
        elif status_code == requests.codes.too_many_requests:
            raise APIErrorException('You have exceeded your allowed requests per minute/day')

    def getCompetitions(self, Plan = None, Id = None):
        """
            Plan = String /[A-Z]+/ -> [ TIER_ONE | TIER_TWO | TIER_THREE | TIER_FOUR ]

            Id = Integer /[0-9]+/
        """

        resources = self.Competitions['Competition'].replace('{id}','') if Id == None else self.Competitions['Competition'].replace('{id}', str(Id))

        try:
            params = urllib.parse.urlencode({'plan': Plan}) if Plan != None else None

            response = self.getResponse('%s%s'%(self.endpoint, resources),params = params)

            return response.json()
        except APIErrorException as identifier:
            print(identifier)
            

    def getTeamsCompetition(self, Id, Season = ''):
        """
            Season = String /YYYY/ -> The starting year of a season e.g. 2017 or 2016
        """

        resources = self.Competitions['Team'].replace('{id}',str(Id))

        try:
            params = urllib.parse.urlencode({'season': str(Season)})

            response = self.getResponse('%s%s'%(self.endpoint, resources), params=params)

            return response.json()
        except APIErrorException as identifier:
            print(identifier)



    def getStandingsCompetition(self, Id , standingType = None):
        """
            standingType = String /[A-Z]+/ -> [ TOTAL (default) | HOME | AWAY ]
        """

        resources = self.Competitions['Standings'].replace('{id}',str(Id))

        try:

            params = urllib.parse.urlencode({'standingType': standingType}) if standingType != None else None

            response = self.getResponse('%s%s'%(self.endpoint, resources),params= params)

            return response.json()
        except APIErrorException as identifier:
            print(identifier)

    def getMatchCompetition(self, Id, dateFrom = '', dateTo = '', stage = '', status = '', matchday = '', group = '', season = ''):
        """
            dateFrom / dateTo = String /YYYY-MM-dd/ -> e.g. 2018-06-22 or 2018-06-02

            stage = String /[A-Z]+/ -> Check the season node for available stages of a particular competition/season.

            status = String /[A-Z]+/ -> The status of a match. [SCHEDULED | LIVE | IN_PLAY | PAUSED | FINISHED | POSTPONED | SUSPENDED | CANCELED]

            matchday = Integer /[1-4]+[0-9]*/ 

            group = String /[A-Z]+/ -> 	Allows filtering for groupings in a competition.

            season = String /YYYY/ -> The starting year of a season e.g. 2017 or 2016
        """

        resources = self.Competitions['Match'].replace('{id}',str(Id))

       
        try:
            params = urllib.parse.urlencode({
                'dateFrom': dateFrom,
                'dateTo': dateTo,
                'stage': stage,
                'status': status,
                'matchday': matchday,
                'group': group,
                'season': season
            })

            response = self.getResponse('%s%s'%(self.endpoint, resources),params = params)
            
            return response.json() 
        except APIErrorException as identifier:
            print(identifier)  
       
       
       
       

    def getScorersCompetition(self, Id, limit = None):
        """
            limit = Integer /\d+/ -> Limits your result set to the given number. Defaults to 10.
        """

        resources = self.Competitions['Scorers'].replace('{id}',str(Id))

        try:
            params = urllib.parse.urlencode({'limit': limit}) if limit != None else None
            
            response = self.getResponse('%s%s'%(self.endpoint, resources), params=  params)

            return response.json()
        except APIErrorException as identifier:
            print(identifier)


    def getMatches(self, Id = None, competitionIds = '', dateFrom = '', dateTo = '' , status = ''):
        """
            Id = Integer /[0-9]+/ 

            competitionIds = String /\d+,\d+/ -> Comma separated list of competition ids.

            dateFrom / dateTo = String /YYYY-MM-dd/ -> e.g. 2018-06-22 or 2018-06-02

            status = String /[A-Z]+/ -> The status of a match. [SCHEDULED | LIVE | IN_PLAY | PAUSED | FINISHED | POSTPONED | SUSPENDED | CANCELED]
        """

        resources = self.Matches['Match'].replace('{id}','') if Id == None else self.Matches['Match'].replace('{id}', str(Id))

        try:
            params = urllib.parse.urlencode({
                'competitions': competitionIds,
                'dateFrom':dateFrom,
                'dateTo':dateTo,
                'status':status
            }) 

            response = self.getResponse('%s%s'%(self.endpoint, resources), params = params)

            return response.json()
        except APIErrorException as identifier:
            print(APIErrorException)


    def getTeam(self, Id):

        """
            Id = Integer /[0-9]+/
        """
        resources = self.Teams['Team'].replace('{id}',str(Id))

        try:
            response = self.getResponse('%s%s'%(self.endpoint, resources))

            return response.json()
        except APIErrorException as identifier:
            print(APIErrorException)

        return response.json()

    def getTeamMatch(self, Id, dateFrom= '', dateTo = '', status:Enum = '', venue:Enum = '', limit= ''  ):

        """
            Id = Integer /[0-9]+/ 

            dateFrom / dateTo = String /YYYY-MM-dd/ -> e.g. 2018-06-22 or 2018-06-02

            status = String /[A-Z]+/ -> The status of a match. [SCHEDULED | LIVE | IN_PLAY | PAUSED | FINISHED | POSTPONED | SUSPENDED | CANCELED]

            venue = String /[A-Z]+/ -> 	Defines the venue (type). [HOME | AWAY]

            limit = Integer /\d+/ -> Limits your result set to the given number. Defaults to 10.
        """

        resources = self.Teams['Match'].replace('{id}','')

        try:
            params = urllib.parse.urlencode({
                'dateFrom': dateFrom,
                'dateTo':dateTo,
                'status':status,
                'venue':venue,
                'limit':limit
            }) 


            response = self.getResponse('%s%s'%(self.endpoint, resources) , params = params)
            return response.json()
        except APIErrorException as identifier:
            print(APIErrorException)

        

    def getPlayers(self, Id):

        """
            Id = Integer /[0-9]+/ 
        """

        resources = self.Players['Player'].replace('{id}',str(Id))
       
        try:
            response = requests.get('%s%s'%(self.endpoint, resources))

            return response.json()
        except APIErrorException as identifier:
            print(APIErrorException)
        
       
    
    def getPlayersMatch(self, Id, competitionIds = '', dateFrom = '', dateTo = '' , status:Enum = ''):

        """
            Id = Integer /[0-9]+/ 

            competitions = String /\d+,\d+/ ->	Comma separated list of competition ids.

            dateFrom / dateTo = String /YYYY-MM-dd/ -> e.g. 2018-06-22

            status = String /[A-Z]+/  -> The status of a match. [SCHEDULED | LIVE | IN_PLAY | PAUSED | FINISHED | POSTPONED | SUSPENDED | CANCELED]
        """

        resources = self.Players['Match'].replace('{id}',str(Id))

        try:
            params = urllib.parse.urlencode({
                'competitions': competitionIds,
                'dateFrom':dateFrom,
                'dateTo':dateTo,
                'status':status
            }) 

            response = requests.get('%s%s'%(self.endpoint, resources), params = params)
            return response.json()
        except APIErrorException as identifier:
            print(APIErrorException)
        
        

    def getAreas(self, Id = None):

        """
            Id = Integer /[0-9]+/ 
        """

        resources = self.Areas['Area'].replace('{id}','') if Id == None else self.Areas['Area'].replace('{id}', str(Id))

        try:
            response = requests.get('%s%s'%(self.endpoint, resources))

            return response.json()
        except APIErrorException as identifier:
            print(APIErrorException)


      

