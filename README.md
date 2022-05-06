# SimpleTournamentFormats
Like [TournamentFormats](https://github.com/phosphorescentt/tournamentformats), but simpler.

The idea is the following:
- Model every team as having some *measured skill* (Elo) and assume that that measurement has some *variance*.
- Determine the probability of a given team winning a map (match) using the probability [formula given by the Elo rating system](https://en.wikipedia.org/wiki/Elo_rating_system#Theory)
- Run this for a large number of iterations
- Do some analysis on the outcomes

# Inspiration
In university esports, it felt like some games were getting unfair treatment in the size of their finals. For example, the tournament organisers would only give Overwatch a best of 5 final when most of the players believe it should be a best of 7. The idea for this project is to evaluate the difference between different finals formats and find the best tradeoff between time and fairness.
