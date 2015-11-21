Author - Michael Kammeyer
randomMsPac

This program will simulate Ms. Pacman and the Three Ghosts using random controllers.

To Execute: python randomMsPac.py path/to/config/file

If you run without a config file, it will automatically default to config/1.cfg

After running, you will have a log file showing the best fitnesses and a world file that tracks Ms. Pacman, the ghosts, the score, and the time throughout the game that yielded the best fitness.

Config File
-----------
Enter all values without any quotes or brackets. Be sure to leave a space between the identifier and your value. 

example
indentifier: value

width: an integer, specifies the width of the grid
height: integer, specifies the height of the grid
pDensity: integer, specifies the percentage chance that any cell has a pill
seed?: random seed, number value, seeds with the current time when set to 0
evaluations: integer, specifies number of evaluations per run
runs: integer, specifies total number of runs
log_file: path/to/log/file output
world_file: path/to/world/file output
