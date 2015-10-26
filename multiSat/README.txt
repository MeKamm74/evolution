Author: Michael Kammeyer

To run with a specified configuration file:
    python evoSat.py path/to/file.cfg
Example:
    python evoSat.py config/2.cfg 

The configuration file works as follows:
-----------------------------------------
Each entry takes the form -  "attribute": <value>
Do not wrap the values with quotes or brackets, just leave them plain.

Attributes:
-----------
"cnf_file" - points to a cnf file, enter a path/to/file.cnf 
"random_seed" - gives a random seed, leave as null if you don't want to use a specific seed
"runs" - number of runs
"log_file" - file to log results in
"solution_file" - file to log solution in
"analysis_file" - file to log extra analysis data in 
"seed_file" - file containing solutions to seed population with. See seed/seed.txt for format.

"population_size" - size of the population, enter an integer
"lamda" - the number of children per generation, integer

"comma_or_plus" - "plus" uses the plus strategy, "comma" uses comma strategy

"Tournament?" - mark as True if you want to use k-tournament parent selection, anything else will use fitness proportionate selection
"tournament_size_k" - only applicable if above is True, denotes the size of each tournament. MUST BE LARGER THAN LAMBDA. integer
"Fitness?" - mark as True if you want to use fitness proportional selection
"Random?" - mark as True if you want to use random selection

"Tournament?" - same as above, but for survival selection. When not true, truncation is used.
"tournament_size_k" - same as above
"Truncation?" - mark as true to use truncation survival selection.
"Random?" - mark as True if you want to use random selection
"Fitness?" - mark as True if you want to use fitness proportional selection

"num_evals" - total number of evaluations to run
"n_convergence" - the number of generations at which the program terminates without changes to average or best. If you don't want to use this and run the full number of evaluations, leave this at 0.