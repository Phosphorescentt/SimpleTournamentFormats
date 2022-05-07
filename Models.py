from numpy import random


class TournamentException(Exception):
    pass


class Team:
    def __init__(
        self, name: str, measured_skill: int, measurement_error_factor: float = 0.5
    ):
        self.name = name
        self.measured_skill = measured_skill
        self.measurement_error_factor = measurement_error_factor

    def set_measurement_error_factor(self, measurement_error_factor: float):
        self.measurement_error_factor = measurement_error_factor

    def __repr__(self):
        return self.name


class FixtureFormat:
    def __init__(self, teams: list[Team]):
        self.teams = teams

    def run(self):
        class_name = self.__class__.__name__
        raise TournamentException(f"{class_name} has not implemented run()")

    def simulate(self):
        return self.run()


class Map(FixtureFormat):
    def __init__(self, teams: list[Team]):
        super().__init__(teams)

    def run(self):
        if len(self.teams) > 2:
            raise TournamentException(f"Incorrect number of teams: {len(self.teams)}")

        team1 = self.teams[0]
        team2 = self.teams[1]
        team1_true_skill = (
            team1.measured_skill + team1.measurement_error_factor * random.normal()
        )
        team2_true_skill = (
            team2.measured_skill + team2.measurement_error_factor * random.normal()
        )
        skill_diff = team1_true_skill - team2_true_skill

        prob_team1_win = 1 - 1 / (1 + 10 ** (skill_diff / 400))

        if random.uniform() < prob_team1_win:
            return [team1, team2]
        else:
            return [team2, team1]


class Bo1Finals(FixtureFormat):
    def __init__(self, teams: list[Team]):
        super().__init__(teams)
        self.games = [Map(teams)]

    def run(self):
        results = self.games[0].run()
        return results


class Bo3Finals(FixtureFormat):
    def __init__(self, teams: list[Team]):
        super().__init__(teams)

        self.games = [Map(teams) for _ in range(3)]

    def run(self):
        team1_score = 0
        team2_score = 0

        for game in self.games:
            res = game.run()
            if res[0] == self.teams[0]:
                team1_score += 1
            else:
                team2_score += 1

            if team1_score == 2:
                return [self.teams[0], self.teams[1]]

            if team2_score == 2:
                return [self.teams[1], self.teams[0]]


class BoXFinals(FixtureFormat):
    def __init__(self, teams: list[Team], X: int):
        super().__init__(teams)

        if X % 2 != 1:
            raise TournamentException(f"BoX format not valid for X = {X}")

        self.X = X

        self.games = [Map(teams) for _ in range(X)]

    def run(self):
        team1_score = 0
        team2_score = 0

        for game in self.games:
            res = game.run()
            if res[0] == self.teams[0]:
                team1_score += 1
            else:
                team2_score += 1

            if team1_score == self.X // 2 + 1:
                return [self.teams[0], self.teams[1]]

            if team2_score == self.X // 2 + 1:
                return [self.teams[1], self.teams[0]]


class Bo5Finals(FixtureFormat):
    def __init__(self, teams: list[Team]):
        super().__init__(teams)
        self.BoX = BoXFinals(teams, 5)

    def run(self):
        return self.BoX.run()


class Bo7Finals(FixtureFormat):
    def __init__(self, teams: list[Team]):
        super().__init__(teams)
        self.BoX = BoXFinals(teams, 7)

    def run(self):
        return self.BoX.run()


class Bo9Finals(FixtureFormat):
    def __init__(self, teams: list[Team]):
        super().__init__(teams)
        self.BoX = BoXFinals(teams, 9)

    def run(self):
        return self.BoX.run()
