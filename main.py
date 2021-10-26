import pygame
import math
import time
import random
from donut import *
from explosion import *
from man import *
from bonusplayer import Player, FlyingDonut

from cleanup import *


pygame.init()
res = (750, 500)
render = pygame.Surface(res)
screen = pygame.display.set_mode(res)
pygame.display.set_caption('LETHAL DONUT')

icon = pygame.image.load('data/donutthing.png')
pygame.display.set_icon(icon)

#FONTS
font = pygame.font.Font('data/Futura-Condensed-Bold.ttf', 50)
smallFont = pygame.font.Font('data/Futura-Condensed-Bold.ttf', 25)
bigFont = pygame.font.Font('data/Futura-Condensed-Bold.ttf', 125)

#SPRITES
vignette = pygame.image.load('data/vignette.png').convert()
vignette = pygame.transform.scale(vignette, res)

sDonut = pygame.image.load('data/donut.png').convert_alpha()
sBoom = pygame.image.load('data/boom.png').convert_alpha()
sBoom = pygame.transform.scale(sBoom, (100, 100))
sDonut = pygame.transform.scale(sDonut, (100, 100))

#EXTRAS
"""t0 = pygame.image.load('data/t0.png').convert_alpha()
t1 = pygame.image.load('data/t1.png').convert_alpha()
ts = [t0, t1]
tindex = 0
tDelay = 0.45"""
t3 = pygame.image.load('data/tBg.png').convert_alpha()

#SOUNDS
titleSong = 'data/music/title.ogg'
boom = pygame.mixer.Sound('data/sounds/boom.wav')
hit = pygame.mixer.Sound('data/sounds/hit.wav')
boom.set_volume(0.1)
hit.set_volume(0.2)
pause = pygame.mixer.Sound('data/sounds/pause.mp3')
pause.set_volume(0.5)
extra = pygame.mixer.Sound('data/sounds/extra.mp3')
extra.set_volume(0.5)

#SCORES (INT)
hiScore = 0
hiCombo = 0
try:
    f = open('data/scores.txt', 'r')
    l = f.read()
    hs, hc = l.split(':')
    hiScore = int(hs)
    hiCombo = int(hc)
    print(f"LOADED DATA - HS:::{hs} HC:::{hc}")
except:
    print("Data file does not exist, creating new blank one")
    f = open('data/scores.txt', 'w')
    f.write('0:0')
    f.close()

    


"""
sWall = pygame.image.load('data/wall.png').convert_alpha()
sSpike = pygame.image.load('data/spike.png').convert_alpha()
sButton = pygame.image.load('data/button.png').convert_alpha()
"""
sMan = pygame.image.load('data/man.png').convert_alpha()
sMan = pygame.transform.scale(sMan, (40, 40))

"""
tileSize = 32
tiles = {1:sWall, 2:sMan, 3:sSpike, 4:sButton}
for i in tiles:
    tiles[i] = pygame.transform.scale(tiles[i], (tileSize, tileSize))
"""
clock = pygame.time.Clock()
run = True



#LEVELS
#lvl = 0
#l = Level((255, 255))
#levels = [l]


def randomSpawn(existingAngle, e):
    global man
    if e:
        explosions.append(Explosion(man.x, man.y, sBoom))
    angle = existingAngle
    while angle == existingAngle:
        ang = random.randint(0, 3)
        angle = ang * 90
    pm = random.randint(1, 100)
    pmm = False
    print(pm)
    if pm == 10:
        print("h")
        pmm = True
    man.angle = angle
    man.determinePosition(res, pmm)
    

dt = 0
prevTime = time.time()
def deltaTime():
    global dt
    global prevTime
    now = time.time()
    dt = now - prevTime
    prevTime = now

pygame.mixer.music.load(titleSong)
musicVol = 1.2
pygame.mixer.music.set_volume(musicVol)
pygame.mixer.music.play(-1)

menu = True
game = False
bonusGame = False

#GAME LOOP PREP###


title = bigFont.render("lethal donut", True, (0, 0, 0))
subtitle = font.render("click to play", True, (0, 0, 0))
g1 = smallFont.render('Take countless lives', True, (99, 99, 99))
g2 = smallFont.render('with this one huge donut', True, (99, 0, 0))
g3 = smallFont.render('Press [M] to mute music', True, (75, 75, 75))
splash = font.render('by Dorbell', True, (252, 92, 101))
sc = font.render(f'Hi {str(hiScore)}, Combo {str(hiCombo)}', True, (128, 128, 128))
splashSpeed = 2
splashed = False
tempScore =  0
tempCombo = 0

def updateScoreFile(scoreu, combou):
    global score
    global maxCombo
    global hiScore
    global hiCombo
    global sc #unnecessary?
    if scoreu:
        hiScore = score
    if combou:
        hiCombo = maxCombo
    sc = font.render(f'Hi {str(hiScore)}, Combo {str(hiCombo)}', True, (128, 128, 128))
    f = open('data/scores.txt', 'w')
    f.write(f'{str(hiScore)}:{str(hiCombo)}')
    f.close()


while run:
    ai = False
    chatter.stop()
    startDelay = time.time() + 2
    sc = font.render(f'Hi {str(hiScore)}, Combo {str(hiCombo)}', True, (128, 128, 128))
    sy = res[1] / 3
    ty = -res[1]
    titleRender = pygame.Surface(res)
    if splashed:
        splash = font.render(f'Results: {tempScore}, {tempCombo} combo', True, (0, 128, 0))
    while menu:
        clock.tick(60)
        deltaTime()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                menu = False
            if event.type == pygame.MOUSEBUTTONDOWN and time.time() >= startDelay + 0.4:
                hit.play()
                game = True
                menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    hit.play()
                    musicVol = -musicVol
                    pygame.mixer.music.set_volume(clamp(musicVol, 0, math.fabs(musicVol)))
                if event.key == pygame.K_SEMICOLON:
                    ai = not ai
                    finish.play()

        
        screen.blit(vignette, (0, 0))
        render.blit(vignette, (0, 0))
        render.blit(splash, (res[0] / 2 - splash.get_width() / 2, sy))
        #I'm sorry for this abomination. Really, I am.
        if time.time() >= startDelay:
            sy += ((res[1] / 2.5) - sy) / 20 * dt * 50
            ty += (0 - ty) / 20 * dt * 50
            tempscore = 0
            tempCombo = 0
            splashed = True
            _title = pygame.transform.rotate(title, sine(2, 2))
            render.blit(sc, (20, 350 - ty / 2))
            render.blit(subtitle, (10, 150 - ty + sine(6, 6)))
            render.blit(g1, (550, 150 + ty))
            render.blit(g2, (500, 325 - ty * 2))
            render.blit(sDonut, (550 - abs(sine(5, 10)), 210 - ty))
            render.blit(sMan, (635 + abs(sine(50, 5)), 240 - ty * 1.5))
            render.blit(_title, (20, 10 - ty))
        render.blit(g3, (res[0] - g3.get_width() - 15, res[1] - 50 - ty))
        screen.blit(render, (sine(2, 5), sine(3, 4)))
        #if not splashed:
        pygame.display.flip()
    
    tl = 10
    timeleft = tl
    eDelay = time.time()
    sinAmp = 0

    score = 0
    combo = 0

    donut = Donut(255, 255, 0, 0, sDonut)
    explosions = []

    tScore = bigFont.render(str(score), True, (128, 128, 128))
    tCombo = font.render(str(combo), True, (100, 100, 100))
    fade = 0

    man = Man(sMan, 40, 0)
    man.enabled = True
    randomSpawn(0, False)
    ttDelay = time.time() + 7

    #SPECIALMODE
    pointsToGather = random.randint(int(int(hiScore) / 2), int(int(hiScore) * 1.2) if hiScore > 2 else 20)
    print(f"GATHER {pointsToGather} POINTS!!!")
    toolTips = ['Launch your donut with your cursor! Hit innocent civilians!', 
    f'Dont forgor to keep control! and don\'t reach {pointsToGather} points pls', 
    'Violently dismiss polygonal planets! (for an extra 5 points)', 
    f"did I mention DON'T reach {pointsToGather} points..? Please don't.",      
    "you're doing GREAT! i think",
    "don't ask who i am,,,,",
    'shoutout to replit...',
    'yes... kill them all... make them suffer.',
    'USE THE DONUT! ITS NOT HARD',
    f'...again, just dont reach {pointsToGather} points bro I swear',
    'subscribe to dorbellprod...',
    'These civilians must die at all costs.',
    'gif caption font']

    aiTips = [
        'You\'ve activated my AI bot.',
        'There\'s no escape. You can\'t save this score...',
        'HA! But at least we\'re getting the job done quickly and efficiently.',
        'Thanks MMG xoxo'
    ]
    tip = {True:aiTips, False:toolTips}
    tti, leng = 0, len(tip[ai])

    paused = False
    maxCombo = 0
    while game:
        clock.tick(60)
        deltaTime()
        screen.blit(vignette, (0, 0))
        render.blit(vignette, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
                bonusGame = False
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    pause.play()
                    if paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.play(-1)
                if event.key == pygame.K_SPACE and paused:
                    bonusGame = False
                    menu = True
                    pygame.mixer.music.play(-1)
                    splashed = False
                    hit.play()
                    game = False
            if event.type == pygame.MOUSEBUTTONDOWN and not ai and not paused:
                if time.time() >= eDelay:
                    eDelay = time.time() +  0.5
                    pos = pygame.mouse.get_pos()
                    donut.addForce(pos, 4000)
                    explosions.append(Explosion(pos[0], pos[1], sBoom))
                    boom.play()
                    sinAmp = 12
        if paused:
            render.blit(bigFont.render("PAUSED", True, (0, 0, 0)), (20, 20))
            render.blit(smallFont.render("press SPACE for menu - press ESC to play", True, (255, 0, 0)), (20 - sine(3, 4), 250 + sine(2, 5)))
            screen.blit(render, (0, 0))
            pygame.display.flip()
            continue
        if time.time() >= ttDelay:
            ttDelay += 4
            tti += 1
        tooltip = smallFont.render(tip[ai][tti % leng], True, (fade, fade, fade))
        fade = math.fabs(sine(1, 0.5)) * 255
        render.blit(tooltip, (res[0] / 2 - tooltip.get_width() / 2, res[1] - 50))
            
           


        if ai and time.time() >= eDelay:
            #<stolen, thanks MMG>
            posRel = ((man.x - donut.x), (man.y - donut.y))
            posM = math.sqrt((posRel[0] * posRel[0]) + (posRel[1] * posRel[1]))
            posN = (-posRel[0] / posM, -posRel[1] / posM)
            posL = (posN[0] * 50, posN[1] * 50)
            pos = (donut.x + posL[0], donut.y + posL[1])
            #</stolen, thanks MMG>
            eDelay += 0.5
            donut.addForce(pos, 4000)
            explosions.append(Explosion(pos[0], pos[1], sBoom))
            boom.play()
            sinAmp = 12
        if timeleft <= 0:
            Man.stopAllSounds()
            hit.play()
            if int(hiScore) < score:
                updateScoreFile(True, False)
            if int(hiCombo) < maxCombo:
                updateScoreFile(False, True)
                hiCombo = maxCombo
            tempScore = score
            tempCombo = maxCombo
            game = False
            menu = True
        timeleft -= dt
        sinAmp -= 20 * dt
        sinAmp = clamp(sinAmp, 2, 999)


        #SCORE AND COMBO STUFF
        if donut.getAvVel() < 35:
            combo = 0
            tCombo = font.render(str(combo), True, (100, 100, 100))
        #levels[lvl].update(render, tiles, level1, donut)
        col = 255 / timeleft
        col = clamp(col, 0, 255)
        render.blit(tScore, (res[0] / 2 - tScore.get_width() / 2, res[1] / 2 - tScore.get_height() / 2))
        render.blit(tCombo, (res[0] / 2 - tCombo.get_width() / 2, res[1] / 2 + 100 - tScore.get_height() / 2))
        render.blit(t3, (7, 7))
        pygame.draw.rect(render, (col, 255 - col, 0), pygame.Rect(12, 12, 155 * (timeleft / tl), 15))
        updateTime, isPm = man.update(render, donut, randomSpawn)
        if updateTime:
            if isPm:
                score += 5
            else:
                score += 1
                
            combo += 1
            if combo > maxCombo:
                maxCombo = combo
            tScore = bigFont.render(str(score), True, (128, 128, 128))
            tCombo = font.render(str(combo), True, (100, 100, 100))
            tl -= 0.1 if tl > 3 else 0
            timeleft = tl
            if score >= pointsToGather:
                bonusGame = True
        for i in explosions:
            if not i.enabled:
                explosions.remove(i)
                continue
            i.update(render, dt)
        donut.update(render, 1000, res, dt)



        screen.blit(render, (sine(5, 1) * sinAmp, sine(12, sinAmp)))
        
        pygame.display.flip()

    bonusTips = [
        "Okay - deep breath. Don't panic. It's the bonus game.",
        "You've switched places - you're a civilian!",
        "Use your arrow keys to try to avoid any incoming donuts!",
        f"Didn't I tell you not to gather {pointsToGather} points??",
        "Oh, well. You'll get a point every 2 seconds. Get set...",
        "GO!",
        "Come on!! Don't you fail me.",
        "Fair enough, you don't even know who I am.",
        "Well, just don't die... or die, since you're a civilian lmao",
        "What? How are you still alive?",
        "DIE DIE DIE DIE DIE"
    ]
    man.kill()
    bonusIndex = 0
    fade = 0
    tipd = 3
    indexDelay = time.time() + tipd
    startOfGame = time.time() + (tipd * 4) + 2.5
    bonusPlayer = Player(res[0] / 2, res[1] / 2, 250, 20)

    donutDelay = time.time()
    collectDelay = time.time()
    donuts = []
    bonusBegin = False

    Man.stopAllSounds()
    chatter.play(-1)
    while bonusGame:
        clock.tick(60)
        deltaTime()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                bonusGame = False
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused
                    pause.play()
                    if paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.play()
                if event.key == pygame.K_SPACE and paused:
                    bonusGame = False
                    menu = True
                    pygame.mixer.music.play()
                    splashed = False
                    hit.play()
                    game = False
        
        screen.blit(vignette, (0, 0))
        render.blit(vignette, (0, 0))
        if paused:
            render.blit(bigFont.render("PAUSED", True, (0, 0, 0)), (20, 20))
            render.blit(smallFont.render("press SPACE for menu - press ESC to play", True, (255, 0, 0)), (20 - sine(3, 4), 250 + sine(2, 5)))
            screen.blit(render, (0, 0))
            pygame.display.flip()
            continue

        fade = math.fabs(sine(1, 0.5)) * 255
        bt = smallFont.render(bonusTips[clamp(bonusIndex, 0, len(bonusTips) - 1)], True, (fade, fade, fade))
        render.blit(tScore, (res[0] / 2 - tScore.get_width() / 2, res[1] / 2 - tScore.get_height() / 2))
        render.blit(bt, (res[0] / 2 - bt.get_width() / 2, res[1] - 50))
        
        if time.time() >= indexDelay:
            if bonusIndex < len(bonusTips) - 1:
                indexDelay += tipd
                bonusIndex += 1
        

        addition = 0
        if bonusIndex >= 5:
            if time.time() >= donutDelay:
                donutDelay = time.time() + 0.5
                donuts.append(FlyingDonut(500 + addition, res))
                addition += 6
            if time.time() >= startOfGame + 2:
                print("Add a point.")
                startOfGame = time.time()
                score += 1
                tScore = bigFont.render(str(score), True, (128, 128, 128))
            for i in donuts:
                c = i.update(render, sDonut, res, dt, bonusPlayer)
                if c:
                    if int(hiScore) < score:
                        updateScoreFile(True, False)
                        hiScore = score
                    chatter.stop()
                    tempScore = score
                    hit.play()
                    menu = True
                    bonusGame = False
        
        
        keys = pygame.key.get_pressed()
        bonusPlayer.update(bonusIndex >= 5, keys, res, sMan, render, dt)
        screen.blit(render, (sine(2, 5), sine(3, 4)))
        pygame.display.flip()
pygame.quit()

#TEAMSEAS