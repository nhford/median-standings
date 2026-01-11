# Fantasy Football League Median Standings

_Created by Noah Ford_

My fantasy football league's platform, ESPN, includes the feature of "Bonus Wins", meaning every week you earn up to 1 win for beating your opponent, and you can earn a bonus win for scoring in the top half of your league. This "bonus win" is also called considered a win against the median in other platforms.

The use of this site comes from ESPN only indicating your percent chance to beat your current opponent, and not your chance to finish in the 50% of teams.

Additionally, the same percentile math can be applied to figure out one's percent chance of being the top scoring team which is relevant for our league because said top scoring team earns part of the league buy-in pool.

The workbook median-np.py does simulations where it employs a gamma distribution to project each player's points individually based on each player's "projected points" determined by ESPN. Then the sum of random variables for each team and compared against each other team to determine each team's relative position amongst the league in total points scored.

This methodology is highly flawed because the Gamma distribution inaptly characterizes each player's projected points. Individually, a team's simulated total exhibits much greater variability than witnessed in observed experience. However, because some large N number of simulations is run, this variance is quelled. Additionally, the distribution may be biased as a player's ESPN "projected points" is not always its mean projection.
