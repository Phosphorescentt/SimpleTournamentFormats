def aggregate_wins(teams, results):
    aggregate_results = [0] * len(teams)

    for result in results:
        if result[0] == teams[0]:
            aggregate_results[0] += 1
        if result[0] == teams[1]:
            aggregate_results[1] += 1

    return aggregate_results
