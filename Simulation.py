from typing import Type

from Models import Team, FixtureFormat


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
