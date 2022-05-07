from Models import *
from Simulation import Simulator
from DataProcessing import aggregate_wins


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
