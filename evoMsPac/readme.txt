Author: Michael Kammeyer
evoMsPac

This program will simulate Ms. Pacman using an evolving controller and the Three Ghosts using random controllers.

To Execute: python evoMsPac.py path/to/config/file

If you run without a config file, it will automatically default to config/1.cfg

After running, you will have a solution file showing the controller that yielded the best overall results, a log file showing the average and best fitnesses after every generation for every run, and a world file that tracks Ms. Pacman, the ghosts, the score, and the time throughout the game that yielded the best fitness.

Config File
-----------
Enter all values without any quotes or brackets. Be sure to leave a space between the identifier and your value. 

example
indentifier: value

width: an integer, specifies the width of the grid
height: integer, specifies the height of the grid
pDensity: integer, specifies the percentage chance that any cell has a pill
seed?: random seed, number value, seeds with the current time when set to 0
population_size: integer, size of population
generation_size: integer, size for every generation
max_tree_depth: integer, maximum depth for the trees that represent controllers
overselection_or_fitness_proportional: Set to OVERSELECTION to run with overselection. Anything else will default to fitness proportional selection
k_tournament_value: size of tournaments for survival selection, set to 0 to use truncation.
parsimony_pressure_coeffiecient: integer, determines how harshly to penalize bloated trees, set to 0 to turn off pressure
evaluations: integer, specifies number of evaluations per run
runs: integer, specifies total number of runs
n_convergence: integer, a run will terminate if the best fitness does not change for n generations. Set to 0 to turn off this criteria
log_file: path/to/log/file output
world_file: path/to/world/file output
solution_file: path/to/solution/file output

width: 10
height: 15
pDensity: 50
seed?: 0
population_size: 200
genereation_size: 50
max_tree_depth: 3
overselection_or_fitness_proportional: OVERSELECTION 
k_tournament_value: 100
parsimony_pressure_coefficient: 1
evaluations: 2000
runs: 30
n_convergence: 0
log_file: log/1.log 
world_file: world/1.world
solution_file: sol/1.sol