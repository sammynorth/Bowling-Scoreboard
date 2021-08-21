import sqlite3
# function for getting a games score by getting every frame score and 
def getTotalScore(gameString):
	score = 0
	for i in range(0,10):
		score+=getFrameScore(i,gameString)

	return score
# function that gets an individual frames score from a game string
def getFrameScore(frame, gameString):
	tempScore = 0
	stringList = gameString.replace('S','').split('-')
	frameString = stringList[frame]
	frameList = [char for char in frameString]
	if(frame < 8):
		nextFrameString = stringList[frame + 1]
		finalFrameString = stringList[frame + 2]
		nextFrameList = [char for char in nextFrameString]
		finalFrameList = [char for char in finalFrameString]
		if(frameString == 'X'):
			tempScore+=10
			if(nextFrameString == 'X'):
				tempScore+=10
				if(finalFrameString == 'X'):
					tempScore+=10
				else:
					if(finalFrameList[0] == 'X'):
						tempScore+=10
					else:
						tempScore+=int(finalFrameList[0])
			else:
				if(nextFrameList[1] == '/'):
					tempScore+=10
				else:
					tempScore+=(int(nextFrameList[0]))
					tempScore+=(int(nextFrameList[1]))
		elif(frameList[1] == '/'):
			tempScore+=10
			if(nextFrameString == 'X'):
				tempScore+=10
			else:
				tempScore+=int(nextFrameList[0])
		else:
			tempScore+=int(frameList[0])
			tempScore+=int(frameList[1])
	elif(frame == 8): #ninth frame due to indexing
		nextFrameString = stringList[frame + 1][0]
		if(nextFrameString != 'X'):
			nextFrameString = stringList[frame + 1][0:2]
			if('/' not in nextFrameString):
				finalFrameString = '0'
			else:
				finalFrameString = stringList[frame + 1][2]
		else:
			finalFrameString = stringList[frame + 1][1]
		nextFrameList = [char for char in nextFrameString]
		finalFrameList = [char for char in finalFrameString]
		if(frameString == 'X'):
			tempScore+=10
			if(nextFrameString == 'X'):
				tempScore+=10
				if(finalFrameString == 'X'):
					tempScore+=10
				else:
					tempScore+=int(finalFrameList[0])
			else:
				if(nextFrameList[1] == '/'):
					tempScore+=10
				else:
					tempScore+=(int(nextFrameList[0]))
					tempScore+=(int(nextFrameList[1]))
		elif(frameList[1] == '/'):
			tempScore+=10
			if(nextFrameString == 'X'):
				tempScore+=10
			else:
				tempScore+=int(nextFrameList[0])
		else:
			tempScore+=int(frameList[0])
			tempScore+=int(frameList[1])
	elif(frame == 9): #tenth frame
		firstBall = frameList[0]
		secondBall = frameList[1]
		try:
			thirdBall = frameList[2]
		except IndexError:
			thirdBall = '0'
		if(firstBall == 'X'): # first ball struck
			tempScore+=10
			if(secondBall == 'X'):# first and second ball struck
				tempScore+=10
				if(thirdBall == 'X'):# struck out tenth frame
					tempScore+=10
				else: # first two strikes then not strike
					tempScore+=int(thirdBall)
			else:# first ball struck, second ball did not
				if(thirdBall == '/'):
					tempScore+=10
				else:
					tempScore+=(int(secondBall))
					tempScore+=(int(thirdBall))
		elif(secondBall == '/'): # spare on first/second ball
			tempScore+=10
			if(thirdBall == 'X'):
				tempScore+=10
			else:
				tempScore+=int(thirdBall)
		else: # open frame
			tempScore+=int(firstBall)
			tempScore+=int(secondBall)
	
	return tempScore

def botAddGame(score, league, tournament, practice, alley, date, gameNumber, ball, gameString, notes):
	con = sqlite3.connect('G:\\bowling bot\\BowlingDatabase.db')
	cursor = con.cursor()
	cursor.execute('''INSERT INTO BowlingScores (score, league, tournament, practice, "bowling alley", date, "game number", ball, gameString, notes) 
		VALUES (?,?,?,?,?,?,?,?,?,?)''',(score, league, tournament, practice, alley, date, gameNumber, ball, gameString, notes))
	con.commit()
	con.close()	

# named after Joe Slowinksi who wrote the below article on advanced bowling statistics
# http://bowlingknowledge.info/index.php?option=com_content&task=view&id=36&Itemid=1

# gets three 'expert' statistics.  Simplified Bowler Rating, Power Rating, and Advanced Bowler Rating
# SBR is on a scale from 0 to 3
# PR is on a scale from 0 to 3
# ABR is on a scale from 0 to 5
def getSlowimetrics(statistics):
	strikePercentage = statistics['strikePercentage']
	sparePercentage = 1.0 # we assume spare % is 1 because if you never leave spares to pick up you should be rewarded not punished
	# if there are attempted spares then we can change the sparePercentage to the sets spare percentage
	if(statistics['totalSpares'] + statistics['singlePinSparesMissed'] + statistics['multiPinSparesMissed'] > 0):
		sparePercentage = statistics['sparePercentage']
	splitPercentage = 1.0 # we assume split % is 1 because if you never leave splits you should be rewarded not punished
	# if there are attempted splits then we can change the sparePercentage to the sets split percentage
	if((statistics['splitsMade'] + statistics['splitsMissed']) > 0):
		splitPercentage = statistics['splitPercentage']
	ninePinFills = 0
	for game in statistics['gamesList']:
		finalFrame = list(game.replace('S','').split('-')[-1])
		if(len(finalFrame) == 3):
			if(finalFrame[2] == '9'):
				ninePinFills+=1
	# SBR = X % + / % + SPL %
	SimplifiedBowlerRating = strikePercentage + sparePercentage + splitPercentage
	# PR = X % + C % + XX %
	# to get carry percentage we are assuming every shot that either strikes or leaves one pin hit the pocket.
	# this doesnt account for bad shots the struck or left one, or good shots that left 2 or more, but it is a good estimate
	pocketHits = (statistics['totalStrikes'] + statistics['singlePinSparesMissed'] + statistics['singlePinSparesMade'] + ninePinFills)
	if(pocketHits > 0):
		carryPercentage = statistics['totalStrikes'] / pocketHits
	else:
		carryPercentage = 0
	powerRating = strikePercentage + carryPercentage + statistics['strikeAfterStrikeRate']

	# ABR = PR + / % + SPL %
	advancedBowlerRating = powerRating + sparePercentage + splitPercentage

	return(f'SBR: {SimplifiedBowlerRating:.2f}/3.00\nPower Rating: {powerRating:.2f}/3.00\nABR: {advancedBowlerRating:.2f}/5.00')

def getSetStatistics(gameSet):
	# dictionary of stats for easy reference
	statsDictionary = {
	'gamesBowled':0,
	'series':0,
	'average':0.00,
	'framesBowled':0,
	'totalStrikes':0,
	'strikePercentage':0.00,
	'totalSpares':0,
	'sparePercentage':0.00,
	'singlePinSparesMade':0,
	'singlePinSparesMissed':0,
	'singlePinPercentage':0.00,
	'multiPinSparesMade':0,
	'multiPinSparesMissed':0,
	'multiPinPercentage':0.00,
	'splitsMade':0,
	'splitsMissed':0,
	'splitPercentage':0.00,
	'scoresList':[],
	'punchouts':0,
	'firstBallAverage':0.00,
	'strikeAfterStrikeRate':0.00,
	'gamesList':[],
	'lowGame':0,
	'highGame':0,
	'strikesAfterStrikes':0,
	'strikesAfterStrikeAttempts':0,
	}
	totalPinfall = 0
	lastBallStruck = False
	#iterate through each game
	for game in gameSet:
		statsDictionary['gamesBowled'] = statsDictionary['gamesBowled']+1
		frames = game.split('-')
		score = getTotalScore(game)
		if(statsDictionary['gamesBowled'] == 1):
			statsDictionary['lowGame'] = score
			statsDictionary['lowGame'] = score
		elif(score > statsDictionary['highGame']):
			statsDictionary['highGame'] = score
		elif(score < statsDictionary['lowGame']):
			statsDictionary['lowGame'] = score

		statsDictionary['scoresList'].append(score)
		statsDictionary['gamesList'].append(game)
		statsDictionary['series'] = statsDictionary['series'] + score
		lastBallStruck = False
		for i in range(9): # iterate through first nine frames
			frame = frames[i]
			frameList = [x for x in frame]
			# increment frames bowled
			statsDictionary['framesBowled'] = statsDictionary['framesBowled']+1
			# strike
			if(frame == 'X'):
				statsDictionary['totalStrikes'] = statsDictionary['totalStrikes']+1
				totalPinfall+=10

				if(lastBallStruck):
					statsDictionary['strikesAfterStrikes']+=1
					statsDictionary['strikesAfterStrikeAttempts']+=1
				lastBallStruck = True

			# spare 
			elif('/' in frameList):
				# single pin spare
				if(int(frameList[0]) == 9):
					statsDictionary['singlePinSparesMade'] = statsDictionary['singlePinSparesMade']+1
				else:
					# split converted
					if('S' in frameList):
						statsDictionary['splitsMade'] = statsDictionary['splitsMade']+1
					# non split multi pin spare
					else:
						statsDictionary['multiPinSparesMade'] = statsDictionary['multiPinSparesMade']+1
				totalPinfall+=int(frameList[0])

				if(lastBallStruck):
					statsDictionary['strikesAfterStrikeAttempts']+=1
				lastBallStruck = False
			# open frame
			else:
				# single pin spare missed
				if(int(frameList[0]) == 9):
					statsDictionary['singlePinSparesMissed'] = statsDictionary['singlePinSparesMissed']+1
				else:
					# split missed
					if('S' in frameList):
						statsDictionary['splitsMissed'] = statsDictionary['splitsMissed']+1
					# non split multi pin spare missed
					else:
						statsDictionary['multiPinSparesMissed'] = statsDictionary['multiPinSparesMissed']+1
				totalPinfall+=int(frameList[0])

				if(lastBallStruck):
					statsDictionary['strikesAfterStrikeAttempts']+=1
				lastBallStruck = False
		# tenth frame
		frame = frames[9]
		frameList = [x for x in frame]
		statsDictionary['framesBowled'] = statsDictionary['framesBowled']+1
		# first ball strike
		if(frameList[0] == 'X'):
			statsDictionary['totalStrikes'] = statsDictionary['totalStrikes']+1
			totalPinfall+=10

			if(lastBallStruck):
				statsDictionary['strikesAfterStrikeAttempts']+=1
				statsDictionary['strikesAfterStrikes']+=1
			lastBallStruck = True
			# first and second ball strike
			if(frameList[1] == 'X'):
				statsDictionary['framesBowled'] = statsDictionary['framesBowled']+1
				statsDictionary['totalStrikes'] = statsDictionary['totalStrikes']+1
				totalPinfall+=10

				if(lastBallStruck):
					statsDictionary['strikesAfterStrikeAttempts']+=1
					statsDictionary['strikesAfterStrikes']+=1
				lastBallStruck = True
				# all three in tenth
				if(frameList[2] == 'X'):
					statsDictionary['framesBowled'] = statsDictionary['framesBowled']+1
					statsDictionary['totalStrikes'] = statsDictionary['totalStrikes']+1
					statsDictionary['punchouts'] = statsDictionary['punchouts']+1
					totalPinfall+=10
					if(lastBallStruck):
						statsDictionary['strikesAfterStrikeAttempts']+=1
						statsDictionary['strikesAfterStrikes']+=1
					lastBallStruck = True
				# first two strikes then count
				else:
					statsDictionary['framesBowled'] = statsDictionary['framesBowled']+1
					totalPinfall+=int(frameList[2])

					if(lastBallStruck):
						statsDictionary['strikesAfterStrikeAttempts']+=1
					lastBallStruck = False
			# first ball strike, second ball not
			else:
				statsDictionary['framesBowled'] = statsDictionary['framesBowled']+1
				# strike then spare
				if('/' in frameList):
					# single pin spare
					if(int(frameList[1]) == 9):
						statsDictionary['singlePinSparesMade'] = statsDictionary['singlePinSparesMade']+1
					else:
						# split converted
						if('S' in frameList):
							statsDictionary['splitsMade'] = statsDictionary['splitsMade']+1
						# non split multi pin spare
						else:
							statsDictionary['multiPinSparesMade'] = statsDictionary['multiPinSparesMade']+1
					totalPinfall+=int(frameList[1])

					if(lastBallStruck):
						statsDictionary['strikesAfterStrikeAttempts']+=1
					lastBallStruck = False
				else:
					# single pin spare missed
					if(int(frameList[1]) == 9):
						statsDictionary['singlePinSparesMissed'] = statsDictionary['singlePinSparesMissed']+1
					else:
						# split missed
						if('S' in frameList):
							statsDictionary['splitsMissed'] = statsDictionary['splitsMissed']+1
						# non split multi pin spare missed
						else:
							statsDictionary['multiPinSparesMissed'] = statsDictionary['multiPinSparesMissed']+1
					totalPinfall+=int(frameList[1])

					if(lastBallStruck):
						statsDictionary['strikesAfterStrikeAttempts']+=1
					lastBallStruck = False
		# first ball spare
		elif('/' in frameList):
			if(int(frameList[0]) == 9):
				statsDictionary['singlePinSparesMade'] = statsDictionary['singlePinSparesMade']+1

				if(frameList[2] == 'X'):
					statsDictionary['totalStrikes'] = statsDictionary['totalStrikes']+1
					statsDictionary['framesBowled'] = statsDictionary['framesBowled']+1
					totalPinfall+=10
				else:
					statsDictionary['framesBowled'] = statsDictionary['framesBowled']+1
					totalPinfall+=int(frameList[2])

			else:
				# split converted
				if(frameList[1] == 'S'):
					statsDictionary['splitsMade'] = statsDictionary['splitsMade']+1
					if(frameList[3] == 'X'):
						statsDictionary['totalStrikes'] = statsDictionary['totalStrikes']+1
						statsDictionary['framesBowled'] = statsDictionary['framesBowled']+1
						totalPinfall+=10
					else:
						statsDictionary['framesBowled'] = statsDictionary['framesBowled']+1
						totalPinfall+=int(frameList[3])
				# non split multi pin spare
				else:
					statsDictionary['multiPinSparesMade'] = statsDictionary['multiPinSparesMade']+1
					if(frameList[2] == 'X'):
						statsDictionary['totalStrikes'] = statsDictionary['totalStrikes']+1
						statsDictionary['framesBowled'] = statsDictionary['framesBowled']+1
						totalPinfall+=10
					else:
						statsDictionary['framesBowled'] = statsDictionary['framesBowled']+1
						totalPinfall+=int(frameList[2])
			totalPinfall+=int(frameList[0])

			if(lastBallStruck):
				statsDictionary['strikesAfterStrikeAttempts']+=1
			lastBallStruck = False
		# open tenth
		else:
			# missed single pin spare
			if(int(frameList[0]) == 9):
				statsDictionary['singlePinSparesMissed'] = statsDictionary['singlePinSparesMissed']+1
			else:
				# split missed
				if(frameList[1] == 'S'):
					statsDictionary['splitsMissed'] = statsDictionary['splitsMissed']+1
				# non split multi pin miss
				else:
					statsDictionary['multiPinSparesMissed'] = statsDictionary['multiPinSparesMissed']+1

			totalPinfall+=int(frameList[0])

			if(lastBallStruck):
				statsDictionary['strikesAfterStrikeAttempts']+=1
			lastBallStruck = False

	if(statsDictionary['framesBowled'] > 0):
		statsDictionary['strikePercentage'] = statsDictionary['totalStrikes'] / statsDictionary['framesBowled']
		statsDictionary['firstBallAverage'] = totalPinfall / statsDictionary['framesBowled']
		statsDictionary['average'] = statsDictionary['series'] / statsDictionary['gamesBowled'] 
	
	if(statsDictionary['strikesAfterStrikeAttempts'] > 0):
		statsDictionary['strikeAfterStrikeRate'] = statsDictionary['strikesAfterStrikes'] / statsDictionary['strikesAfterStrikeAttempts']
	
	if(statsDictionary['singlePinSparesMade'] + statsDictionary['singlePinSparesMissed'] > 0):
		statsDictionary['singlePinPercentage'] = statsDictionary['singlePinSparesMade'] / (statsDictionary['singlePinSparesMade'] + statsDictionary['singlePinSparesMissed'])
	
	if(statsDictionary['multiPinSparesMade'] + statsDictionary['multiPinSparesMissed'] > 0):
		statsDictionary['multiPinPercentage'] = statsDictionary['multiPinSparesMade'] / (statsDictionary['multiPinSparesMade'] + statsDictionary['multiPinSparesMissed'])
	
	if(statsDictionary['splitsMade'] + statsDictionary['splitsMissed'] > 0):
		statsDictionary['splitPercentage'] = statsDictionary['splitsMade'] / (statsDictionary['splitsMade'] + statsDictionary['splitsMissed'])
	
	statsDictionary['totalSpares'] = (statsDictionary['singlePinSparesMade'] + statsDictionary['multiPinSparesMade'])
	if(statsDictionary['totalSpares'] + statsDictionary['multiPinSparesMissed'] + statsDictionary['singlePinSparesMissed'] > 0):
		statsDictionary['sparePercentage'] = statsDictionary['totalSpares'] / (statsDictionary['multiPinSparesMade'] + statsDictionary['multiPinSparesMissed'] + statsDictionary['singlePinSparesMade'] + statsDictionary['singlePinSparesMissed'])
	statsDictionary['totalSpares'] = statsDictionary['totalSpares'] + statsDictionary['splitsMade']

	return statsDictionary
