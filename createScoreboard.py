topLeft = '╔'
topRight = '╗'
bottomLeft = '╚'
bottomRight = '╝'

verticalLine = '║'
horizontalLine = '═'

topTee = '╦'
leftTee = '╠'
rightTee = '╣'
bottomTee = '╩'
intersection = '╬'


def createScoreboard(gameString):
	frameList = gameString.replace('x','X').replace('s','S').split('-')
	# initialize string
	scoreboard = f'{topLeft}'
	scoreboard+=f'{horizontalLine*3}{topTee}'*20
	scoreboard+=f'{horizontalLine*3}{topRight}'
	scoreboard+='\n'

	for i in range(9):
		frame = frameList[i]
		firstBall = frame[0]
		scoreboard+=f'{verticalLine} '
		if(firstBall == 'X'):
			scoreboard+=f'  {verticalLine} X '
		else:
			secondBall = frame[1]
			if(secondBall == 'S'):
				secondBall = frame[2]
				scoreboard+=f'{firstBall}S{verticalLine} {secondBall} '
			else:
				scoreboard+=f'{firstBall} {verticalLine} {secondBall} '
	# tenth frame
	frame = frameList[-1]
	secondBall = ''
	thirdBall = ''
	firstBall = f'{frame[0]} '
	scoreboard+=f'{verticalLine} '
	if(frame[1] == 'S'):
		firstBall = f'{frame[0]}S'
		secondBall = f'{frame[2]} '
	else:
		secondBall = f'{frame[1]} '
	if(len(frame.replace('S','')) == 3):
		thirdBall = frame.replace('S','')[-1]
		if(frame[-1] == 'S'):
			thirdball = f'{thirdBall}S'
		else:
			thirdBall = f'{thirdBall} '
		scoreboard+=f'{firstBall}{verticalLine} {secondBall}{verticalLine} {thirdBall}{verticalLine}'
	else:
		scoreboard+=f'  {verticalLine} {firstBall}{verticalLine} {secondBall}{verticalLine}'

	scoreboard+=f'\n{verticalLine}'
	scoreboard+=f'   {bottomLeft}{horizontalLine*3}{rightTee}'*10
	scoreboard = scoreboard[:-1] + bottomTee + f'{horizontalLine*3}{rightTee}\n'
	scoreboard+=f'{verticalLine}'
	for i in range(9):
		score = getFrameScore(i,gameString)
		if(score > 99):
			scoreboard+=f'  {score}  {verticalLine}'
		else:
			scoreboard+=f'   {score}  {verticalLine}'
	score = getFrameScore(9,gameString)
	if(score > 99):
		scoreboard+=f'    {score}    {verticalLine}'
	else:
		scoreboard+=f'     {score}    {verticalLine}'
	
	scoreboard+=f'\n{bottomLeft}'
	scoreboard+=f'{horizontalLine*7}{bottomTee}'*9
	scoreboard+=f'{horizontalLine*11}{bottomRight}'

	print(scoreboard)

def getFrameScore(frame, gameString):
	score = 0
	for i in range(frame+1):
		score+=getFrameScoreHelper(i,gameString)  
	return score

# function that gets an individual frames score from a game string
def getFrameScoreHelper(frame, gameString):
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

def main():
	gameString = 'X-X-X-X-X-X-X-X-X-XXX'
	createScoreboard(gameString)

if __name__ == '__main__':
	main()