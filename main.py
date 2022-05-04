from typing import Type

from numpy import random

from DataProcessing import aggregate_wins


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

            if team1_score == self.X//2 + 1:
                return [self.teams[0], self.teams[1]]

            if team2_score == self.X//2 + 1:
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


class Simulator:
    def __init__(
        self,
        fixture_format: Type[FixtureFormat],
        teams: list[Team],
        measurement_error_factor: float = 0.5,
    ):
        self.fixture_format = fixture_format
        self.teams = teams
        self.measurement_error_factor = measurement_error_factor

    def simulate(self, n: int = 1000):
        total_results = []

        for _ in range(n):
            current_fixture = self.fixture_format(self.teams)
            total_results.append(current_fixture.run())

        return total_results


if __name__ == "__main__":
    warwick_angels = Team("Warwick Angels", 2000)
    portsmouth_paladins = Team("Portsmouth Paladins", 2200)
    teams = [warwick_angels, portsmouth_paladins]

    print(f"{warwick_angels} elo: {warwick_angels.measured_skill}")
    print(f"{portsmouth_paladins} elo: {portsmouth_paladins.measured_skill}")
    
    print("=================================")

    measurement_error_std = 200

    bo1 = Simulator(Bo1Finals, teams, measurement_error_std)
    bo3 = Simulator(Bo3Finals, teams, measurement_error_std)
    bo5 = Simulator(Bo5Finals, teams, measurement_error_std)
    bo7 = Simulator(Bo7Finals, teams, measurement_error_std)
    bo9 = Simulator(Bo9Finals, teams, measurement_error_std)

    bo1_results = bo1.simulate(10000)
    bo3_results = bo3.simulate(10000)
    bo5_results = bo5.simulate(10000)
    bo7_results = bo7.simulate(10000)
    bo9_results = bo9.simulate(10000)

    bo1_data = aggregate_wins(teams, bo1_results)
    bo3_data = aggregate_wins(teams, bo3_results)
    bo5_data = aggregate_wins(teams, bo5_results)
    bo7_data = aggregate_wins(teams, bo7_results)
    bo9_data = aggregate_wins(teams, bo9_results)

    print("========== BO1 RESULTS ==========")
    print(teams)
    print(bo1_data)
    print("========== BO3 RESULTS ==========")
    print(teams)
    print(bo3_data)
    print("========== BO5 RESULTS ==========")
    print(teams)
    print(bo5_data)
    print("========== BO7 RESULTS ==========")
    print(teams)
    print(bo7_data)
    print("========== BO9 RESULTS ==========")
    print(teams)
    print(bo9_data)
