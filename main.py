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


class Bo5Finals(FixtureFormat):
    def __init__(self, teams: list[Team]):
        super().__init__(teams)

    def run(self):
        pass


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
    warwick_angels = Team("Grey Warwick", 2000)
    portsmouth_paladins = Team("Portsmouth Paladins", 2200)

    teams = [warwick_angels, portsmouth_paladins]

    s = Simulator(Bo1Finals, teams, 0.5)
    results = s.simulate(10)
    a_results = aggregate_wins(teams, results)
    print(results)
    print(a_results)

    print("================")

    s2 = Simulator(Bo3Finals, teams, 0.5)
    results2 = s2.simulate(10)
    a_results2 = aggregate_wins(teams, results2)
    print(results2)
    print(a_results2)
