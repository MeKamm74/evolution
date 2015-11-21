import sys
import Ghost
import MsPac
import State
import time
import datetime
import random

def main():
	if len(sys.argv) > 1:
		config = open(sys.argv[1], 'r')
	else:
		config = open('config/1.cfg', 'r')

	#read in config values
	width = int(config.readline().split()[1])
	height = int(config.readline().split()[1])
	pDensity = int(config.readline().split()[1])
	seed = int(config.readline().split()[1])
	evals = int(config.readline().split()[1])
	runs = int(config.readline().split()[1])
	logFile = config.readline().split()[1]
	worldFile = config.readline().split()[1]

	#seed Random
	current_time = time.mktime(datetime.datetime.now().timetuple())
	if seed == 0:
		seed = current_time
	random.seed(seed)

	#open files
	log = open(logFile, 'w')


	#log headers
	log.write("Number of Runs: " + str(runs))
	log.write("\nNumber of Evals: " + str(evals))
	log.write("\nWorld height: " + str(height))
	log.write("\nWorld width: " + str(width))
	log.write("\nPill Density: " + str(pDensity))
	log.write("\nRandom Seed " + str(seed))
	log.write("\n\nResults Log")
	log.write("\n---------------\n\n")

	#begin runs
	bestOverallScore = 0
	for i in range(0, runs):
		log.write("Run " + str(i+1) + "\n")
		bestScore = 0
		for j in range(0, evals):

			#Initialize ghosts and Ms. Pacman
			ghosts = []
			for i in range(0, 3):
				ghosts.append(Ghost.Ghost())
			msPac = MsPac.MsPac()

			#Initialize State
			state = State.State(width, height, ghosts, msPac, pDensity)
			#Generate the pills
			state.generateGrid(pDensity)

			#Initial World Log
			tempWorld = ""
			tempWorld += str(state.width) + "\n"
			tempWorld += str(state.height) + "\n"
			tempWorld += "m" + " " + str(state.msPac.locationX) + " " + str(state.msPac.locationY) + "\n"
			for k in range(0, len(state.ghosts)):
				tempWorld += str(k+1) + " " + str(state.ghosts[k].locationX) + " " + str(state.ghosts[k].locationY) + "\n"
			for k in range(0, len(state.pills)):
				tempWorld += "p" + " " + str(state.pills[k].x) + " " + str(state.pills[k].y) + "\n"
			tempWorld += "t" + " " + str(state.time) + " " + str(state.score) + "\n"

			#Run the game
			gameOver = False
			while not gameOver:
				#Update the board
				state.step()

				#World Log
				tempWorld += "m" + " " + str(state.msPac.locationX) + " " + str(state.msPac.locationY) + "\n"
				for k in range(0, len(state.ghosts)):
					tempWorld += str(k+1) + " " + str(state.ghosts[k].locationX) + " " + str(state.ghosts[k].locationY) + "\n"
				tempWorld += "t" + " " + str(state.time) + " " + str(state.score) + "\n"
				
				#Check if game is over
				gameOver = state.isGameOver()

			if state.score > bestScore:
				#Log if improved score
				bestScore = state.score
				log.write(str(j) + "\t" + str(state.score) + "\n")

			if state.score > bestOverallScore:
				#Log the world file if best overall
				bestOverallScore = state.score
				world = open(worldFile, 'w')
				world.write(tempWorld)
				world.close() 

		log.write("\n")
	log.close()


if __name__ == "__main__":
	main()