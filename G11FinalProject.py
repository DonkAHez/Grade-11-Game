import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(375, 80)
import random
from pygame import * 
init()
#size of the screen
WIDTH, HEIGHT = 800,700
SIZE = (WIDTH, HEIGHT)
screen = display.set_mode(SIZE)
#variable for the mousebutton
button = 0
#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255, 0, 0)
ORANGE = (255, 140, 0)
YELLOW = (255, 255, 51)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
GREY = (128,128,128)
#fonts
menuFont = font.SysFont("Times New Roman",60)
helpFont = font.SysFont("Times New Roman",20)
pauseFont = font.SysFont("Times new roman",45)
#game loop variable
running = True

myClock = time.Clock()


lives = 5
#counter for if a shot from the player needs to be deleted from reaching the top of the screen
c = 0
#player's starting coordinates
cx = 400
cy = 450

#loading pictures
backgroundPic = image.load("Background1.png")
backgroundPic = transform.scale(backgroundPic,(800,600))
jetpackPic = image.load("Jetpack.png")
jetpackPic = transform.scale(jetpackPic,(40,40))

jetpackExhaust = image.load("JetpackExhaust.png")
jetpackExhaust1 = transform.scale(jetpackExhaust,(10,40))
jetpackExhaustShort1 = transform.scale(jetpackExhaust,(10,20))
jetpackExhaust2 = image.load("JetpackExhaust2.png")
jetpackExhaust2 = transform.scale(jetpackExhaust2,(10,40))
jetpackExhaustShort2 = transform.scale(jetpackExhaust2,(10,20))
jetpackExhaust3 = image.load("JetpackExhaust3.png")
jetpackExhaust3 = transform.scale(jetpackExhaust3,(10,40))
jetpackExhaustShort3 = transform.scale(jetpackExhaust3,(10,20))
jetpackExhaustList = [jetpackExhaust1,jetpackExhaust2,jetpackExhaust3]
jetpackExhaustShortList = [jetpackExhaustShort1,jetpackExhaustShort2,jetpackExhaustShort3]

emptyHeart = image.load("EmptyHeart.png")
emptyHeart = transform.scale(emptyHeart,(50,50))
fullHeart = image.load("FullHeart.png")
fullHeart = transform.scale(fullHeart,(50,50))

attackCoordinates = [] #player's shots coordinates list
collisionList = [] #list of player shots that hit the enemies
enemiesOnScreen = [[20,-290],[120,-80],[260,-170],[310,-190],[380,-120],[440,-40],[530,-130],[580,-100],[660,0]] #list that contains the coordinates of the enemies in the first wave

enemyHP = []
enemyAttackList = [] 
enemyAttackDelete = [] #list that gets the position of the shots that hit the edge of the screen
enemyAttackCollision = [] #list that gets the position of the shots that hit the player

wave = 0 #sets the variable for the enemy wave

for i in range (len(enemiesOnScreen)):
    enemyHP+=[100] 

#keys variables
KEY_RIGHT = False
KEY_LEFT = False
KEY_SHIFT = False
KEY_UP  = False
KEY_DOWN = False
KEY_ESCAPE = False
KEY_Z = False

#main states
STATE_MENU = 0
STATE_GAME = 1
STATE_HELP = 2
STATE_QUIT = 3
state = STATE_MENU

#game states
STATE_PLAY = 4
STATE_PAUSE = 5
STATE_GAMEOVER = 6
STATE_VICTORY = 7
gState = STATE_PLAY

#enemy attack timer/frequency variables
frequency = 750
previousShotTime = 0
shotTimer = 0


retry = False #boolean that checks if you will be immediately sent back into the game after returning to the main menu
Reset = False #boolean that checks if the variables need to be reset

def reset():
    #all the variables that need to be reset:
    global lives,c,cx,cy,attackCoordinates,collisionList,enemiesOnScreen,enemyHP,enemyAttackList,enemyAttackDelete,enemyAttackCollision,state,gState,shotTimer,previousShotTime, wave, frequency
    lives = 5 
    c = 0 
    frequency = 750 
    cx = 400
    cy = 450
    attackCoordinates = collisionList = []
    enemiesOnScreen = [[20,-290],[120,-80],[260,-170],[310,-190],[380,-120],[440,-40],[530,-130],[580,-100],[660,0]]
    enemyHP = [] 
    for i in range (len(enemiesOnScreen)): 
        enemyHP+=[100] 
    enemyAttackList = enemyAttackDelete = enemyAttackCollision = [] 
    wave = 0 
    #all the states are reset 
    state = STATE_MENU    
    gState = STATE_PLAY
    previousShotTime = 0
    shotTimer = 0
    Reset = True 
    return Reset


def drawMenu():
    state = 0 
    x = WIDTH//3 
    width = x+1 
    y = 160
    height = 80
    rectList = [Rect(x,y,width,height),Rect(x,y+180,width,height),Rect(x,y+360,width,height)] 
    titleList = ["PLAY","HELP","QUIT"] 
    stateList = [STATE_GAME, STATE_HELP, STATE_QUIT] 
    for i in range(3): 
        rect = rectList[i]
        draw.rect(screen,BLUE,rect) #draws the rectangle
        draw.rect(screen,WHITE,rect,2) #adds an outline to the rectangle
        text = menuFont.render(titleList[i], 1, CYAN) #grabs the text related to the rectangle
        #centers the text on the rectangle
        textWidth, textHeight = menuFont.size(titleList[i])
        textX = 266+((266-textWidth)//2)
        textY = (80-textHeight)//2
        screen.blit(text, Rect(textX,textY+rect[1],textWidth,textHeight)) #writes/draws the rectangle
        if rectList[i].collidepoint(mx, my): #checks if you hover your mouse over a rectangle
            draw.rect(screen,WHITE,rect,5) #highlights the rectangle that you're hovering over
            if button == 1: 
                state = stateList[i] 
    return state 

def gamePause(): 
    gState = STATE_PAUSE
    draw.rect(screen,WHITE,(265,5,270,50))
    text = pauseFont.render("Game Paused",1,GREEN)
    textWidth, textHeight = pauseFont.size("Game Paused")
    textX = 265+((270-textWidth)//2)
    textY = 5+((50-textHeight)//2)
    screen.blit(text, Rect(textX,textY,textWidth,textHeight))
    titleList = ["Continue", "Help", "Main Menu"]
    stateList = [STATE_PLAY, STATE_HELP, STATE_MENU]
    x = 280
    y = 160
    width = 240
    height = 50
    rectList = [Rect(x,y,width,height),Rect(x,y+180,width,height),Rect(x,y+360,width,height)]
    for i in range (3):
        rect = rectList[i]
        draw.rect(screen,WHITE,rect)
        draw.rect(screen,BLUE,rect,2)  
        text = pauseFont.render(titleList[i],1,GREEN)
        textWidth, textHeight = pauseFont.size(titleList[i])
        textX = 280+((240-textWidth)//2)
        textY = (50-textHeight)//2
        screen.blit(text, Rect(textX,textY+rect[1],textWidth,textHeight))        
        if rectList[i].collidepoint(mx, my):
            draw.rect(screen,BLUE,rect,5)
            if button == 1:
                gState = stateList[i]
    return gState    

def drawHelp(state): 
    state = STATE_HELP
    screen.fill(BLUE)
    rect = Rect(5,635,105,50)
    draw.rect(screen,GREY,rect)
    draw.rect(screen,BLACK,rect,2)
    text = helpFont.render("RETURN",1,CYAN)
    textWidth, textHeight = helpFont.size("RETURN")
    textX = 5+((105-textWidth)//2)
    textY = 635+((50-textHeight)//2)
    screen.blit(text, Rect(textX,textY,textWidth,textHeight))
    if rect.collidepoint(mx,my):
        draw.rect(screen,BLACK,rect,5)
        if button == 1:
            state = STATE_MENU
    #the text thats written in the help screen
    text1 = "All the e-waste piled up in the world's largest e-waste dumpster has turned into a horde of" 
    text2 = "e-waste robots that are destroying the environment to grow their numbers. Scientists all around"
    text3 = "the world have worked together to create the recycling gun which is the only weapon capable of"
    text4 = "destroying the e-waste horde by recycling 100% of the e-waste that makes up each robot."
    text5 = "The fate of the world now rests on your shoulders as the only person capable of weilding a"
    text6 = "recycling gun. Do your best to recycle as many e-waste robots as you can to save the world from"
    text7 = "the e-waste horde."
    text8 = "CONTROLS:"
    text9 = "use the arrow keys to move around"
    text10 = "holding down shift will slow down your movement"
    text11 = "press z to shoot the recycling gun, your shots will travel in a straight line in front of you"
    text12 = "press escape to pause the game"
    textList = [text1,text2,text3,text4,text5,text6,text7,text8,text9,text10,text11,text12] 
    for i in range (12): 
        text = helpFont.render(textList[i],1,BLACK)
        screen.blit(text,Rect(10,(15+24*i),750,690))
    
    return state

def drawGameOver():
    gState = STATE_GAMEOVER
    screen.fill(BLACK)
    draw.rect(screen,WHITE,(200,5,400,95))
    draw.rect(screen,YELLOW,(200,5,400,95),2)
    text = menuFont.render("GAME OVER",1,BLUE)
    textWidth, textHeight = menuFont.size("GAME OVER")
    textX = 200+((400-textWidth)//2)
    textY = 5+((95-textHeight)//2)
    screen.blit(text,Rect(textX,textY,textWidth,textHeight))    
    
    titleList = ["RETRY", "MENU"]
    stateList = [STATE_PLAY, STATE_MENU]
    x = 266
    y = 250
    width = 267
    height = 75
    rectList = [Rect(x,y,width,height),Rect(x,y+225,width,height)]
    for i in range (2):
        rect = rectList[i]
        draw.rect(screen,WHITE,(rect))
        draw.rect(screen,YELLOW,(rect),2)
        text = menuFont.render(titleList[i],1,BLUE)
        textWidth, textHeight = menuFont.size(titleList[i])
        textX = 266+((266-textWidth)//2)
        textY = (75-textHeight)//2
        screen.blit(text, Rect(textX,textY+rect[1],textWidth,textHeight))
        if rect.collidepoint(mx, my):
            draw.rect(screen,YELLOW,rect,5)
            if button == 1:
                gState = stateList[i]  
    return gState
        
        
        
def drawVictory(): 
    gState = STATE_VICTORY
    screen.fill(BLACK)
    draw.rect(screen,WHITE,(200,5,400,95))
    draw.rect(screen,YELLOW,(200,5,400,95),2)
    text = menuFont.render("VICTORY",1,BLUE)
    textWidth, textHeight = menuFont.size("VICTORY")
    textX = 200+((400-textWidth)//2)
    textY = 5+((95-textHeight)//2)
    screen.blit(text,Rect(textX,textY,textWidth,textHeight))    
    
    titleList = ["NEW GAME", "MENU"]
    stateList = [STATE_PLAY, STATE_MENU]
    x = 266
    y = 250
    width = 267
    height = 75
    rectList = [Rect(x-35,y,width+70,height),Rect(x,y+225,width,height)]    
    for i in range (2):
        rect = rectList[i]
        draw.rect(screen,WHITE,(rect))
        draw.rect(screen,YELLOW,(rect),2)
        text = menuFont.render(titleList[i],1,BLUE)
        textWidth, textHeight = menuFont.size(titleList[i])
        textX = 266+((266-textWidth)//2)
        textY = (75-textHeight)//2
        screen.blit(text, Rect(textX,textY+rect[1],textWidth,textHeight))
        if rect.collidepoint(mx, my):
            draw.rect(screen,YELLOW,rect,5)
            if button == 1:
                gState = stateList[i]
    return gState
        


def characterMovement():
    global cx,cy
    #if you're holding down one of the arrow keys, you'll move in the direction of the arrow key
    if KEY_SHIFT == False:
        if KEY_LEFT == True:
            cx-=5
        if KEY_RIGHT == True:
            cx+=5
        if KEY_UP == True:
            cy-=5
        if KEY_DOWN == True:
            cy+=5
    #if you're holding down shift while holding down the arrow keys, you move slower than before
    if KEY_SHIFT == True:
        if KEY_LEFT == True:
            cx-=2 
        if KEY_RIGHT == True:
            cx+=2
        if KEY_UP == True:
            cy-=2
        if KEY_DOWN == True:
            cy+=2
    #if you reach the edge of the screen, you're blocked from moving any further
    if cx+5>800-5: 
        cx = 800-10 
    if cx-5<5:
        cx = 10
    if cy+5>600-5:
        cy = 600-10
    if cy-5<5:
        cy = 10    
    
def playerShooting(list1):
    if KEY_Z == True: 
        list1.append([cx,cy]) 
    return list1


def playerAttackCollision(): 
    global attackCoordinates, c, pos, collisionList, enemyHp
    for i in range (len(attackCoordinates)): 
        coordinates = str(attackCoordinates[i])[1:-1] 
        List = coordinates.split(",") 
        
        tx = int(List[0]) #the first element is the x value
        ty = int(List[1]) #the second element is the y value
        draw.circle(screen,GREEN,(tx,ty),10) 
        ty-=15 
        attackCoordinates[i] = [tx,ty] 
        if ty<=0: #checks if the bullet hits the top of the screen
            c = 1 
            pos = i 
        for l in range (len(enemiesOnScreen)): #checks if the shot hits any of the enemies on the screen
            coordinates = str(enemiesOnScreen[l])[1:-1] 
            List = coordinates.split(",")
            ex = int(List[0])
            ey = int(List[1])                   
            
            distance = ((tx-ex)**2)+((ty-ey)**2)
            distance = distance**(1/2)
            if distance < 30: #if the shot hits an enemy
                collisionList += [i] 
                enemyHP[l] = int(enemyHP[l])-4 


#deleting bullets that hit the enemy
def playerAttackDelete():
    global attackCoordinates, collisionList, pos, c
    for i in range (len(collisionList)): 
        cPos = collisionList[-(i+1)]
        del attackCoordinates[cPos] 
    collisionList = [] 
    
    if c == 1: 
        del attackCoordinates[pos] 
        c = 0 


def deleteEnemies():
    global enemiesOnScreen, enemyHP
    i = 0 
    while i<len(enemiesOnScreen):
        coordinates = str(enemiesOnScreen[i])[1:-1]
        List = coordinates.split(",")
        ex = int(List[0])
        ey = int(List[1])                
        HP = int(enemyHP[i]) 
        if HP<=0 or ey>=620: #checks if the enemy is dead or if its exited the screen
            del enemiesOnScreen[i] 
            del enemyHP[i] 
        i+=1 
        
def enemyAttack():
    global previousShotTime, shotTimer, enemiesOnScreen, enemyAttackList,frequency
    timeSinceLastShot = shotTimer-previousShotTime #gets the time since the last shot
    if timeSinceLastShot>=frequency: #checks if enough time has passed which is given by the value of frequency 
        for i in range(len(enemiesOnScreen)): #loops so that every enemy attacks once at the same time

            coordinates = str(enemiesOnScreen[i])[1:-1]
            List = coordinates.split(",")
            ex = int(List[0])
            ey = int(List[1])+20 #ensures the bullet appears infront of the enemy
            enemyAttackList.append([ex,ey])
        previousShotTime = time.get_ticks() #updates the time of the last shot
    shotTimer = time.get_ticks() #updates the timer

def enemyMovementDown(List):
    for i in range (len(List)):
        coordinates = str(List[i])[1:-1]
        List1 = coordinates.split(",")
        ex = int(List1[0])
        ey = int(List1[1])
        ey+=1 #moves the enemy down by 1
        List[i] = [ex,ey] 
    return List  
         

def drawEnemyAttack():
    global enemyAttackList, enemyAttackDelete, enemyAttackCollision, lives
    for i in range (len(enemyAttackList)): 
        draw.circle(screen,ORANGE,(enemyAttackList[i]),5) #draws the bullet
        coordinates = str(enemyAttackList[i])[1:-1]
        List = coordinates.split(",")
        ax = int(List[0])
        ay = int(List[1])+4 #updates the coordinates of the bullet 
        enemyAttackList[i] = [ax,ay] 
        if ay>605 or ay<-5: #checks if the bullets are outside the screen
            enemyAttackDelete.append(i) 
        if (((ax-cx)**2)+((ay-cy)**2))**(1/2) < 10: #checks if the bullet collides with your hitbox
            enemyAttackCollision.append(i)
            lives-=1  

def enemyAttackDel():
    global enemyAttackCollision, enemyAttackDelete, enemyAttackList
    #delets any bullets that hit you
    for i in range (len(enemyAttackCollision)):
        pos = enemyAttackCollision[-(i+1)] 
        del enemyAttackList[pos]                
    enemyAttackCollision = [] 
    
    #deletes any bullets that've reached the edge of the screen
    for i in range (len(enemyAttackDelete)):
        pos = enemyAttackDelete[-(i+1)]
        del enemyAttackList[pos]
    enemyAttackDelete = []
    
def drawEnemyAndPlayer():
    #jetpack exhaust lists each contain 3 different jetpack exhaust pictures which allow for an animation
    global enemiesOnScreen, jetpackPic,cx,cy,jetpackExhaustShortList,jetpackExhaustList
    for i in range(len(enemiesOnScreen)): #draws a black circle for each enemy alive on the screen
        draw.circle(screen,BLACK,(enemiesOnScreen[i]),20)
    
    #draws character as well as the jetpack
    draw.circle(screen, RED, (cx, cy), 10) #draws the player
    screen.blit(jetpackPic, Rect(cx-20,cy-10,40,40)) #draws the jetpack on the player
    #random numbers, one for each end of the jetpack
    r1 = random.randint(0,2)
    r2 = random.randint(0,2)
    #randomly chooses an element form the jetpack exhaust list so that its animated
    if KEY_SHIFT == True: #if you're holding shift, the jetpack's exhaust is shortened
        screen.blit(jetpackExhaustShortList[r1], Rect(cx+1,cy+20,10,40))
        screen.blit(jetpackExhaustShortList[r2], Rect(cx-11,cy+20,20,30))                
        draw.circle(screen,WHITE,(cx,cy),5)
    else:
        screen.blit(jetpackExhaustList[r1], Rect(cx+1,cy+20,10,40))
        screen.blit(jetpackExhaustList[r2], Rect(cx-11,cy+20,20,30))    
        
def drawLives():
    global lives, pauseFont, emptyHeart, fullHeart
    draw.rect(screen,BLACK,(0,600,800,100)) #draws the black background at the bottom of the screen
    #centers the text so that the hearts appear next to it on the same elevation
    text = pauseFont.render("LIVES:",1,RED)
    textWidth, textHeight = pauseFont.size("LIVES:")
    screen.blit(text, Rect(5,625,textWidth,textHeight))            
    for i in range(5): #draws all 5 empty hearts first
        screen.blit(emptyHeart, Rect(150+(50*i),625,50,50))            
    for i in range(lives): #draws a full heart for each life you have left
        screen.blit(fullHeart, Rect(150+(50*i),625,50,50))    



#game loop
while running:
    button = 0 #resets button so that after clicking, you'll have to click again to register another click 
    screen.fill(BLACK) #resets the screen
    KEY_ESCAPE = False #resets the escape key 
    for e in event.get():
        if e.type == QUIT:
            running = False #stops the game if you click on the x button
        if e.type == MOUSEBUTTONDOWN: #if you click:
            mx, my = e.pos #takes the position of where you clicked
            button = e.button #finds what mouse button you pressed
        if e.type == MOUSEMOTION: 
            mx, my = e.pos #grabs the position of your mouse when you move it
        if e.type == KEYDOWN: #checks if you're holding down one of the arrow keys, left shift button, and/or the z key
            if e.key == K_LEFT:
                KEY_LEFT = True
            if e.key == K_RIGHT:
                KEY_RIGHT = True
            if e.key == K_LSHIFT:
                KEY_SHIFT = True
            if e.key == K_UP:
                KEY_UP = True
            if e.key == K_DOWN:
                KEY_DOWN = True
            if e.key == K_ESCAPE:
                KEY_ESCAPE = True
            if e.key == K_z:
                KEY_Z = True
        if e.type == KEYUP: #checks if you've stopped pressing one of the arrow keys, left shift button, and/or the z key
            if e.key == K_LEFT:
                KEY_LEFT = False
            if e.key == K_RIGHT:
                KEY_RIGHT = False
            if e.key == K_LSHIFT:
                KEY_SHIFT = False
            if e.key == K_UP:
                KEY_UP = False
            if e.key == K_DOWN:
                KEY_DOWN = False
            if e.key == K_z:
                KEY_Z = False
    if state == STATE_MENU:
        if Reset == False: 
            Reset = reset() #resets all the variables so that if you quit to the main menu and click play again, you'll start a new game
        if retry == False: #if you're just visiting the main menu, the game state doesn't update until you click play, help, or quit
            state = drawMenu()
        else: #if you hit retry after the game over or victory screen, you'll be returned to the main menu so that the variables are reset before being automatically being sent back into the game
            state = STATE_GAME 
            retry = False #retry is set to false so that if you go back to the main menu, you won't be automatically sent to the start of a new game 
    elif state == STATE_GAME: #if you click play
        Reset = False #reset is set to false so that when you quit to the main menu, the variables will be reset
        if KEY_ESCAPE == True: #if you press escape, you will pause the game
            gState = STATE_PAUSE #game state is now set to pause
        if gState == STATE_PLAY:#if you're playing the game
            screen.blit(backgroundPic, Rect(0,0,800,600)) #draws the background
            
            characterMovement() 
            
            attackCoordinates = playerShooting(attackCoordinates) 
            
            playerAttackCollision() 
            
            playerAttackDelete()

            deleteEnemies() 
            
            
            if wave == 1:
                frequency = 500
            if wave == 3:
                frequency = 250
            
            enemiesOnScreen = enemyMovementDown(enemiesOnScreen) 
            
            enemyAttack() 
            
            drawEnemyAttack() 
            
            enemyAttackDel() 
            
            drawEnemyAndPlayer() 
            
            drawLives() 

            display.flip()
            
            if len(enemiesOnScreen) == 0:
                if wave == 0:
                    enemiesOnScreen = [[15,-290],[97,-80],[186,-170],[310,-190],[377,-30],[453,-40],[520,-187],[584,-10],[668,-67],[415,-80]]
                if wave == 1:
                    enemiesOnScreen = [[377,-30],[453,-40],[520,-187],[584,-10],[668,-67],[415,-80],[260,-170],[380,-120],[15,-290],[97,-80],[186,-170],[310,-190]]
                if wave == 2:
                    enemiesOnScreen = [[400,0],[370,-20],[430,-20],[470,-40],[330,-40],[480,0],[320,0],[200,0],[170,-20],[230,-20],[170,-40],[230,-40],[280,0],[120,0],[600,0],[570,-20],[630,-20],[670,-40],[530,-40],[680,0],[520,0]]
                wave+=1 
                enemyHP = [] 
                for i in range (len(enemiesOnScreen)): 
                    enemyHP.append(100)
                if wave == 4: 
                    gState = STATE_VICTORY 
            
            if lives <= 0:
                gState = STATE_GAMEOVER 
        if gState == STATE_PAUSE: 
            gState = gamePause() 
            if gState == STATE_PLAY: 
                KEY_ESCAPE = False 
        if gState == STATE_HELP: 
            gState = drawHelp(gState) 
            if gState == STATE_MENU: 
                gState = STATE_PAUSE
        if gState == STATE_MENU: 
            state = STATE_MENU 

        if gState == STATE_GAMEOVER:
            gState = drawGameOver() 
            if gState == STATE_PLAY:  
                retry = True 
                gState = STATE_MENU
        
        if gState == STATE_VICTORY: 
            gState = drawVictory() 
            if gState == STATE_PLAY:
                retry = True
                gState = STATE_MENU
        
    elif state == STATE_HELP:
        state = drawHelp(state) 
    else: #if the state is STATE_QUIT
        running = False 
    display.flip()
    myClock.tick(60) #60 fps
quit() 