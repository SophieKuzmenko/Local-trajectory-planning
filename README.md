# Local trajectory planning with static obstacle avoidance
*University project*<br>
<mark>To view the simulation please run the colored_simulation.py file, not main.py</mark><br>
Implementation of a local trajectory planning algorithm for a self-driven vehicle with static obstacles avoidance described in [1] <br><br>
The breakdown of the algorithm:
1. Generating a set of candidate paths
2. Eliminating non-executable candidate paths ( due to steering limitations or potential collisions with the obstacles)
3. Choosing the most optimal path
<br><br>*In the simulation, the most optimal path has been marked as dark green, non-executable ones as red and the paths that are excutable but not most cost-efficient as light green*<br>

References: <br>
[1] A. Said, R. Talj, C. Francis and H. Shraim, "Local trajectory planning for autonomous vehicle with static and dynamic obstacles avoidance," 2021 IEEE International Intelligent Transportation Systems Conference (ITSC), Indianapolis, IN, USA, 2021, pp. 410-416, doi: 10.1109/ITSC48978.2021.9565109.
keywords: {Trajectory planning;Trajectory tracking;Heuristic algorithms;Roads;Cost function;Trajectory;Planning},
