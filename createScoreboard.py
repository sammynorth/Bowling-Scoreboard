import scoreFunctions as sf

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
	frameList = gameString.split('-')
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
	firstBall = f'{frameList[0]} '
	scoreboard+=f'{verticalLine} '
	if(frameList[1] == 'S'):
		firstBall = f'{frameList[0]}S'
		secondBall = f'{frameList[2]} '
	else:
		secondBall = f'{frameList[1]} '
	if(len(frame.replace('S','')) == 3):
		thirdBall = frame.replace('S','')[-1]
		if(frame[-1] == 'S'):
			thirdball = f'{thirdBall}S'
		else:
			thirdBall = f'{thirdBall} '
		scoreboard+=f'{firstBall}{verticalLine} {secondBall}{verticalLine} {thirdBall}{verticalLine}'
	else:
		scoreboard+=f'   {verticalLine}{firstBall}{verticalLine} {secondBall}{verticalLine}'

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
		score+=sf.getFrameScore(i,gameString)  
	return score
