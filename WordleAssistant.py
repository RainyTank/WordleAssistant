from wordfreq import zipf_frequency
import pygame

pygame.init()

(width, height) = (1200,650)
screen = pygame.display.set_mode((width,height))

#colours
BLACK = (0,0,0)
WHITE = (255,255,255)
Gainsboro = (220, 220, 220)
LightGray = (211,211,211)
Gray = (128,128,128)
DimGray = (105, 105, 105)
Gold = (255, 215, 0)
MediumSeaGreen = (60,179,113)
Tomato = (255, 99, 71)

COLORLIST = [DimGray,Gold,MediumSeaGreen]
#sizes and locations
BUTTONW = 50
BUTTONH = 50

BUTTONX = 50
BUTTONY = 100

userword = ['?','?','?','?','?']
rightletters = ['?','?','?','?','?']
correctness = ['DimGray','DimGray','DimGray','DimGray','DimGray']
WORKINGROW = [1]

# gotta redraw part of the screen so it looks like it refreshes
def REDRAW(xcoord,ycoord,w,h,color):
    pygame.draw.rect(screen,color,(xcoord,ycoord,w,h))

#font stuff
SMALLFONT= pygame.font.Font("freesansbold.ttf",20)
BIGFONT= pygame.font.Font("freesansbold.ttf",35)

def text_objects(words,font,color):
    textSurface = font.render(words,True,color)
    return textSurface, textSurface.get_rect()
#text appear justified center right or left
def display_textc(words,font,color,xcoord,ycoord):
    textSurf, textRect = text_objects(f'{words}',font,color)
    textRect.center=((xcoord),(ycoord))
    screen.blit(textSurf,textRect)
def display_textl(words,font,color,xcoord,ycoord):
    textSurf, textRect = text_objects(f'{words}',font,color)
    textRect.midleft=((xcoord),(ycoord))
    screen.blit(textSurf,textRect)     

class GenButton: 
    def __init__(self,xcoord,ycoord,width,height,neutral,hover,text):
        self.xcoord=xcoord
        self.ycoord=ycoord
        self.width=width
        self.height=height
        self.neutral=neutral
        self.hover=hover
        self.text=text
        self.rect=pygame.Rect(xcoord,ycoord,width,height)
        #pygame.draw.rect(screen,neutral,(xcoord,ycoord,width,height))
        
    def draw(self):
        mouse=pygame.mouse.get_pos()
        if self.xcoord+self.width> mouse[0] > self.xcoord and self.ycoord+self.height> mouse[1] > self.ycoord:
            pygame.draw.rect(screen,self.hover,(self.xcoord,self.ycoord,self.width,self.height))
            display_textc(f'{self.text}',SMALLFONT,WHITE,(self.xcoord+(self.width/2)),(self.ycoord+(self.height/2)))
        else:
            pygame.draw.rect(screen,self.neutral,(self.xcoord,self.ycoord,self.width,self.height))
            display_textc(f'{self.text}',SMALLFONT,WHITE,(self.xcoord+(self.width/2)),(self.ycoord+(self.height/2)))

### PYGAME FUNCTIONS

def usertyping(xcoord,ycoord,width,height,color):
    usertypes =  True
    userentry=''
    while usertypes: 
        pygame.draw.rect(screen,color,(xcoord,ycoord,width,height))
        display_textl(f'{userentry}',BIGFONT,WHITE,xcoord+10,ycoord+30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                usertypes = False
            pygame.display.update()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and len(userentry) == 5 and userentry.isalpha() == True:
                    userword.clear()
                    for each in userentry:
                        userword.append(each)
                    userentry=''
                    usertypes=False
                elif event.key==pygame.K_BACKSPACE:
                    userentry=userentry[:-1]
                elif event.key==pygame.K_ESCAPE:
                    userentry=''
                    usertypes=False
                else:
                    userentry+=event.unicode

def ButtonRow(dowhat="None", j = 0):
    i=0

    for k in range(len(userword)):
        thisletter=GenButton(BUTTONX+i,BUTTONY+j, BUTTONW, BUTTONH, correctness[k], Gainsboro, userword[k])
        if dowhat=='draw':
            thisletter.draw()
        if dowhat=='clicked':
            mouse=pygame.mouse.get_pos()
            if thisletter.rect.collidepoint(mouse)==True:
                if correctness[k] == 'DimGray':
                    correctness[k] = 'Gold'
                elif correctness[k] == 'Gold':
                    correctness[k] = 'MediumSeaGreen'
                else:
                    correctness[k] = 'DimGray'
        i+=60
    

def WelcomeDisplay():
    display_textl('Welcome to wordle assistant!',SMALLFONT,Gainsboro,BUTTONX,BUTTONY-30)
    display_textl('I recommend starting with the word AROSE',SMALLFONT,Gainsboro,BUTTONX*13,BUTTONY-30)
    display_textl('click the squares to cycle through colors',SMALLFONT,Gainsboro,BUTTONX*13,BUTTONY)
    display_textl('--Gray means letter is not in the word',SMALLFONT,Gainsboro,BUTTONX*13,BUTTONY+30)
    display_textl('--Yellow is correct letter but wrong location',SMALLFONT,Gainsboro,BUTTONX*13,BUTTONY+60)
    display_textl('--Green is correct letter and location',SMALLFONT,Gainsboro,BUTTONX*13,BUTTONY+90)
    display_textl('only click run stats when you are done with the colors',SMALLFONT,Gainsboro,BUTTONX*13,BUTTONY+120)
    
def RunStats(dowhat="None"):
    StatsButton = GenButton(BUTTONX*8,BUTTONY+450,BUTTONW*4,BUTTONH,Tomato,Gainsboro,'Run Stats')
    StatsButton.draw()
    if dowhat=='clicked':
        mouse=pygame.mouse.get_pos()
        if StatsButton.rect.collidepoint(mouse)==True and userword[0] != '?':
            updatedlist()
            REDRAW(BUTTONX*8,BUTTONY+150,550,270,BLACK)
            updatedictionary()
            display_textl('In the words remaining; ',SMALLFONT,Gainsboro,BUTTONX*8,BUTTONY+140)
            WORKINGROW[0] += 1
            userword.clear()
            correctness.clear()
            for i in range(5):
                userword.append('?')
                correctness.append('DimGray')
        else:
            pass
            
def Restart(dowhat="None"):
    RestartButton = GenButton(BUTTONX*14,BUTTONY+450,BUTTONW*4,BUTTONH,Tomato,Gainsboro,'Restart')
    RestartButton.draw()
    if dowhat=='clicked':
        mouse=pygame.mouse.get_pos()
        if RestartButton.rect.collidepoint(mouse)==True:     
            currentlist.clear()
            uploadwords()
            #for the stats
            REDRAW(BUTTONX*8,BUTTONY+150,550,270,BLACK)
            #for the words
            REDRAW(BUTTONX,BUTTONY+60,300,350,BLACK)
            updatedictionary()
            userword.clear()
            rightletters.clear()
            correctness.clear()
            WORKINGROW[0] = 1
            for i in range(5):
                userword.append('?')
                rightletters.append('?')
                correctness.append('DimGray')


        
### THE BRAINS BELOW

firstfrequencydict = {
'a':0,
'b':0,
'c':0,
'd':0,
'e':0,
'f':0,
'g':0,
'h':0,
'i':0,
'j':0,
'k':0,
'l':0,
'm':0,
'n':0,
'o':0,
'p':0,
'q':0,
'r':0,
's':0,
't':0,
'u':0,
'v':0,
'w':0,
'x':0,
'y':0,
'z':0
}

secondfrequencydict = firstfrequencydict.copy()
thirdfrequencydict = firstfrequencydict.copy()
fourthfrequencydict = firstfrequencydict.copy()
fifthfrequencydict = firstfrequencydict.copy()
totalfrequencydict = firstfrequencydict.copy()

uniquedict = firstfrequencydict.copy()
tempdict = {}

wordfrequencydictionary = {}
currentlist = []

def uploadwords():
    textfile = open("words2022.txt", 'r').read().splitlines()
    for line in textfile:
        currentlist.append(line)

def updatedictionary():
    
    for values in firstfrequencydict:
        firstfrequencydict[values]= 0
    for values in secondfrequencydict:
        secondfrequencydict[values]= 0
    for values in thirdfrequencydict:
        thirdfrequencydict[values]= 0
    for values in fourthfrequencydict:
        fourthfrequencydict[values]= 0
    for values in fifthfrequencydict:
        fifthfrequencydict[values]= 0
    for values in totalfrequencydict:
        totalfrequencydict[values]= 0        
    for values in uniquedict:
        uniquedict[values]= 0 
        
    wordfrequencydictionary.clear()

    for word in currentlist:
        firstfrequencydict[word[0]]+=1
        secondfrequencydict[word[1]]+=1
        thirdfrequencydict[word[2]]+=1
        fourthfrequencydict[word[3]]+=1
        fifthfrequencydict[word[4]]+=1
        totalfrequencydict[word[0]]+=1
        totalfrequencydict[word[1]]+=1
        totalfrequencydict[word[2]]+=1
        totalfrequencydict[word[3]]+=1
        totalfrequencydict[word[4]]+=1
        
        tempdict.update({word[0]:1})
        tempdict.update({word[1]:1})
        tempdict.update({word[2]:1})
        tempdict.update({word[3]:1})
        tempdict.update({word[4]:1})
        for each in tempdict:
            uniquedict[each] +=1
        tempdict.clear()

            
            
    
    display_textl(f'the most frequent letter in the: ',SMALLFONT,Gainsboro,BUTTONX*13,BUTTONY+170)
        
    FFIRST=sorted(firstfrequencydict, key=firstfrequencydict.get, reverse=True)[:5]
    display_textl(f'1st position {FFIRST}',SMALLFONT,Gainsboro,BUTTONX*13,BUTTONY+200)
 
    FSECOND=sorted(secondfrequencydict, key=secondfrequencydict.get, reverse=True)[:5]
    display_textl(f'2nd position {FSECOND}',SMALLFONT,Gainsboro,BUTTONX*13,BUTTONY+230)

    FTHIRD=sorted(thirdfrequencydict, key=thirdfrequencydict.get, reverse=True)[:5]
    display_textl(f'3rd position {FTHIRD}',SMALLFONT,Gainsboro,BUTTONX*13,BUTTONY+260)

    FFOURTH=sorted(fourthfrequencydict, key=fourthfrequencydict.get, reverse=True)[:5]
    display_textl(f'4th position {FFOURTH}',SMALLFONT,Gainsboro,BUTTONX*13,BUTTONY+290)

    FFIFTH=sorted(fifthfrequencydict, key=fifthfrequencydict.get, reverse=True)[:5]
    display_textl(f'5th position {FFIFTH}',SMALLFONT,Gainsboro,BUTTONX*13,BUTTONY+320)

    FTOTAL=sorted(totalfrequencydict, key=totalfrequencydict.get, reverse=True)[:5]
    display_textl(f'overall {FTOTAL}',SMALLFONT,Gainsboro,BUTTONX*13,BUTTONY+350)

    FUNIQUE=sorted(uniquedict, key=uniquedict.get, reverse=True)[:5]
    display_textl(f'unique {FUNIQUE}',SMALLFONT,Gainsboro,BUTTONX*13,BUTTONY+380)
    
    for each in currentlist:
        wordfrequencydictionary[each]=zipf_frequency(each, 'en')
    
    display_textl(f'the most frequent words',SMALLFONT,Gainsboro,BUTTONX*8,BUTTONY+170)
    FWORD= dict(sorted(wordfrequencydictionary.items(), key=lambda item: item[1], reverse=True)[:5])
    i = 0
    for k,v in FWORD.items():
        display_textl(f'{k} = {v}',SMALLFONT,Gainsboro,BUTTONX*8,BUTTONY+200+i)
        i += 30
        
    display_textl(f'{len(currentlist)} words remain',SMALLFONT,Gainsboro,BUTTONX*8,BUTTONY+350)

def removewrong(location, letter):
    x = 0
    while x < len(currentlist):
        for i in range(5):
            if letter != rightletters[i] and letter == currentlist[x][i]:
                currentlist.remove(currentlist[x])
                break
            else:
                continue
        else:
            x += 1

def rightspot(location, letter):
    rightletters[location] = letter
    x = 0
    while x < len(currentlist):
        if currentlist[x][location] != letter:
            currentlist.remove(currentlist[x])
        else:
            x += 1

def wrongspot(location, letter):
    x = 0
    while x < len(currentlist):
        #so i want to remove all words that dont contain the letter at all
        if currentlist[x][location] == letter or currentlist[x][0] != letter and currentlist[x][1] != letter and currentlist[x][2] != letter and currentlist[x][3] != letter and currentlist[x][4] != letter:
            currentlist.remove(currentlist[x])
        else:
            x += 1

def updatedlist():
    #had to seperate them because i wanted all the green words in the correct letters before the grey letters get deleted
    for k in range(len(userword)):
        if correctness[k] == 'MediumSeaGreen':
            rightspot(k, userword[k])
        else:
            continue
            
    for k in range(len(userword)):       
        if correctness[k] == 'Gold':
            wrongspot(k, userword[k])
        elif correctness[k] == 'DimGray':
            removewrong(k, userword[k])
        else:
            continue

def wordscontain():
    pass

uploadwords()
updatedictionary()


### THE GAME BELOW
       
pygame.display.flip()



#run program
def main():
    programon = True
    while programon:
        #clock.tick(60)             #clock stuff do i even need lol
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                programon = False
            pygame.display.update()

          
            WelcomeDisplay()
            
            TheGuess=GenButton(BUTTONX*8,BUTTONY,BUTTONW*4,BUTTONH,Tomato,Gainsboro,'enter guess')
            TheGuess.draw()
            
            RunStats()
            Restart()
            
            if WORKINGROW[0] == 1:
                ButtonRow('draw')
            if WORKINGROW[0] == 2:
                ButtonRow('draw', 60)
            if WORKINGROW[0] == 3:
                ButtonRow('draw', 120)
            if WORKINGROW[0] == 4:
                ButtonRow('draw', 180)
            if WORKINGROW[0] == 5:
                ButtonRow('draw', 240)
            if WORKINGROW[0] == 6:
                ButtonRow('draw', 300)
                
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.MOUSEBUTTONUP:
                mouse=pygame.mouse.get_pos()
                
                RunStats('clicked')
                Restart('clicked')
                

                    
                if WORKINGROW[0] == 1:
                    ButtonRow('clicked')
                if WORKINGROW[0] == 2:
                    ButtonRow('clicked', 60)
                if WORKINGROW[0] == 3:
                    ButtonRow('clicked', 120)
                if WORKINGROW[0] == 4:
                    ButtonRow('clicked', 180)
                if WORKINGROW[0] == 5:
                    ButtonRow('clicked', 240)
                if WORKINGROW[0] == 6:
                    ButtonRow('clicked', 300)
                    
                if TheGuess.rect.collidepoint(mouse) == True:
                    usertyping(BUTTONX*8,BUTTONY,BUTTONW*4,BUTTONH,Tomato)

main()
pygame.quit()
quit()