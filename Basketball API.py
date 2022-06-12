import random

class Person:

    def __init__(self,name,lastname):
        self.name=name
        self.lastname=name
    def get_name(self):
        return self.name + ' ' + self.lastname
    def __str__(self):
        return self.name+" "+self.lastname
    def __lt__(self,other):
        if self.lastname!=other.lastname:
            return self.lastname<other.lastname
        else:
            return self.name<other.name
        
class Player(Person):
    id_count=0
    def __init__(self, name, lastname):
        self.name=name
        self.lastname=lastname
        self.power=random.randint(4,8)
        self.all_points=[]
        Player.id_count+=1
        self.id=Player.id_count
        self.team=""
    def reset(self):
        self.all_points=[]
    def get_id(self):
        return self.id
    def get_power(self):
        return self.power
    def set_team(self, t):
        t.players.append(self)
    def get_team(self):
        return self.team
    def add_to_points(self, x):
        self.all_points.append(x)
    def get_points_detailed(self):
        return self.all_points
    def get_points(self):
        return sum(self.all_points)
    def __lt__(self,other):
        if self.get_points()!=other.get_points():
            return sum(self.all_points)<sum(other.all_points)
        elif self.get_lastname!=other.get_lastname():
            return self.lastname<other.lastname
        else:
            return self.name<other.name
        
class Manager(Person):
    id_count=0
    def __init__(self,name,lastname):
        self.name=name
        self.lastname=lastname
        Manager.id_count+=1
        self.id=Manager.id_count
        self.influence=[]
        self.team=""
    def reset(self):
        self.influence=[]
    def get_id(self):
        return self.id
    def set_team(self,t):
        t.manager=self
    def get_team(self):
        return self.team
    def get_influence_detailed(self):
        return self.influence
    def get_influence(self):
        return sum(self.influence)
    def __lt__(self, other):
        if sum(self.influence)!=sum(other.influence):
            return self.influence<other.influence
        elif self.get_lastname()!=other.get_lastname():
            return self.lastname<other.lastname
        else:
            return self.name<other.name

class Team:
    id_count=0
    def __init__(self,teamname,manager,players):
        self.teamname=teamname
        self.manager=manager
        manager.set_team(self)
        self.players=players
        Team.id_count+=1
        self.id=Team.id_count
        self.fixture=[]
        self.scored=0
        self.conceded=0
        self.wins=0
        self.losses=0
        for i in self.players:
            i.team=self
    def reset(self):
        self.fixture=[]
        self.scored=0
        self.conceded=0
        self.wins=0
        self.losses=0
    def get_id(self):
        return self.id
    def get_name(self):
        return self.teamname
    def get_manager(self):
        return self.manager
    def get_roster(self):
        return self.players
    def add_to_fixture(self,m):
        self.fixture.append(m)
    def get_fixture(self):
        return self.fixture
    def add_result(self, s):
        self.scored+=s[0]
        self.conceded+=s[1]
        if s[0]>s[1]:
            self.wins+=1
        elif s[0]<s[0]:
            self.losses+=1
    def get_scored(self):
        return self.scored
    def get_conceded(self):
        return self.conceded
    def get_wins(self):
        return self.wins
    def get_losses(self):
        return self.losses
    def __str__(self):
        return self.teamname
    def __lt__(self,other):
        difference=(self.scored-self.conceded,other.scored-other.conceded)
        if self.scored!=other.scored:
            return self.scored<other.scored 
        elif difference[0]!=difference[1]:
            return difference[0]<difference[1]
        else:
            return True

class Match:
    def __init__(self,home_team,away_team,week_no):
        self.home=home_team
        self.away=away_team
        self.week=week_no
        self.is_played=False
        self.score_home=0
        self.score_away=0
    def is_played(self):
        return self.is_played
    def play(self):
        home_manager_p=random.randint(-10,10)
        away_manager_p=random.randint(-10,10)
        self.home.get_manager().influence.append(home_manager_p)
        self.away.get_manager().influence.append(away_manager_p)
        self.score_home+=home_manager_p
        self.score_away+=away_manager_p
        for i in range(4):
            mood_home,mood_away=0,0
            for x in self.home.players:
                a=random.randint(-5,5)
                x.add_to_points(a)
                mood_home+=a+x.power
            for p in self.away.players:
                a=random.randint(-5,5)
                p.add_to_points(a)
                mood_away+=a+p.power
            self.score_home+=mood_home
            self.score_away+=mood_away
        
        
        while self.score_home==self.score_away:
            mood_home,mood_away=0,0
            for x in self.home.players:
                a=random.randint(-5,5)
                x.add_to_points(a)
                mood_home+=a
            for i in self.away_players:
                a=random.randint(-5,5)
                i.add_to_points(a)
                mood_away+=a
            self.score_home+=mood_home
            self.score_away+=mood_away
            
        self.is_played=True
    def get_teams(self):
        return self.home,self.away
    def get_home_team(self):
        return self.home
    def get_away_team(self):
        return self.away
    def get_winner(self):
        if self.is_played==False:
            return None
        elif self.score_home>self.score_away:
            return self.home
        else: return self.away 
    def __str__(self):
        if self.is_played==False:
            return self.home + " vs. " + self.away
        else:
            return self.home.teamname + str((self.score_home)) + " vs. " + self.away.teamname + str((self.score_away))
    
class Season:
    def __init__(self,teams,managers,players):
        self.manager_list,self.player_list,self.all_players=[],[],[]
        self.all_managers=[]
        self.week=1
        self.all_teams=[]
        self.t=open(teams,"r")
        self.pw_no=1
        self.is_completed=False
        self.build_fixture()
        m=open(managers,"r")
        p=open(players,"r")
        for i in m:
            self.manager_list.append(i.strip())
        for x in p:
            x.split("\n")
            self.player_list.append(x.strip())
        for j in self.t:
            self.players=[]
            for l in range(5):
                choice=random.choice(self.player_list)
                self.player_list.remove(choice)
                choice=Player(choice.split(" ")[0],choice.split(" ")[1])
                self.players.append(choice)
            manager_choice=random.choice(self.manager_list)
            self.manager_list.remove(manager_choice)
            manager_choice=Manager(manager_choice.split(" ")[0],manager_choice.split(" ")[1])
            self.all_players+=self.players
            self.all_managers.append(manager_choice)
            self.all_teams.append(Team(j.strip(),manager_choice,self.players))
    def reset(self):#sonra bakarsın
        self.manager_list,self.player_list,self.all_players=[],[],[]
        self.all_managers=[]
        self.week=1
        self.all_teams=[]
        self.pw_no=1
        self.is_completed=False
    def build_fixture(self):
            def first(teamlist):
                teamlist1=teamlist
                bos=[]
                for i in range(0,len(teamlist1)):
                    bos.append(0)
                bos[0]=teamlist1[0]
                for i in range(0,len(teamlist1)-1):
                    haftalik=[]
                    for k in range(0,int(len(teamlist1)/2)):
                        match=Match(teamlist1[k],teamlist1[k+int(len(teamlist1)/2)],i+1)
                        haftalik.append(match)
                    self.weeklyMatches.append(haftalik)
                    for j in range(len(teamlist1)):
                        if j==0:
                            pass
                        elif j==len(teamlist1)/2:
                            bos[1]=teamlist1[j]
                        elif j==(len(teamlist1)/2)-1:
                            bos[-1]=teamlist1[j]
                        elif j <=(len(teamlist1)/2)-1:
                            bos[j+1]=teamlist1[j]
                        elif j>(len(teamlist1)/2)-1:
                            bos[j-1]=teamlist1[j]
                    teamlist1=bos.copy()
            def second(teamlist):
                teamlist1=teamlist.copy()
                bos=[]
                for i in range(0,len(teamlist1)):
                    bos.append(0)
                bos[0]=teamlist1[0]
                for i in range(0,len(teamlist1)-1):
                    weekly_play=[]
                    for k in range(0,int(len(teamlist1)/2)):
                        match=Match(teamlist1[k],teamlist1[k+int(len(teamlist1)/2)],i+1)
                        weekly_play.append(match)
                    self.weeklyMatches.append(weekly_play)
                    for j in range(len(teamlist1)):
                        if j==len(teamlist1)/2:
                            pass
                        elif j==0:
                            bos[int(len(teamlist1)/2+1)]=teamlist1[j]
                        elif j==len(teamlist1)-1:
                            bos[int(len(teamlist1)/2-1)]=teamlist1[j]
                        elif j <=(int(len(teamlist1)/2))-1:
                            bos[j-1]=teamlist1[j]
                        elif j>(int(len(teamlist1)/2))-1:
                            bos[j+1]=teamlist1[j]
                    teamlist1=bos.copy()



            coppied=self.TeamList.copy()
            temp1=[]
            temp2=temp1.copy()
            for i in range(0,len(coppied)):
                if i <=(len(coppied)/2)-1:
                    temp2.append(coppied[i])
                else:
                    temp1.append(coppied[i])
            # 1  2   3   4   5   6   7   8   9  10  11
            # 8  9  10  11  12  13  14  15  16  17  18
            
    def get_week_fixture(self,week_no):
        if week_no==0 or week_no>len(self.matches):
            return None
        return self.all_fixture[week_no-1]
        
    
    def return_matches(self):
        return self.matches
    
    def get_week_no(self):
        return self.week
    
    def play_week(self):
        if self.pw_no<=len(self.all_fixture):
            for i in self.all_fixture[self.pw_no-1]:
                i.play()
            self.pw_no+=1
        if self.pw_no==len(self.all_fixture):
            self.is_completed=True
        
        
    def get_players(self):
        return self.all_players
    
    def get_managers(self):
        return self.all_managers
    
    def get_teams(self):
        return self.all_teams
    
    def get_season_length(self):
        return len(self.matches)
    
    def get_best_player(self):
        points=[]
        for i in self.all_players:
            points.append(i.get_points_detailed()[-1])
        a=max(points)
        for x in self.all_players:
            if x.get_points_detalied()[-1]==a:
                return x
    
    def get_best_manager(self):
        points=[]
        for i in self.all_managers:
            points.append(i.get_influence_detailed()[-1])
        a=max(points)
        for x in self.all_managers:
            if x.get_influence_detalied()[-1]==a:
                return x
    
    def most_scoring_team(self):
        points=[]
        for i in self.all_teams:
            points.append(i.get_points_detailed()[-1])
        a=max(points)
        if points.count(a)==1:
            for x in self.all_teams:
                if x.get_points_detalied()[-1]==a:
                    return x
            
    def get_champion(self):
        if self.is_completed:
            a=self.all_teams[:]
            a.sort()
            return max(a)
    
