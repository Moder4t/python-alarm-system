#Imports
from alarm2 import *
import pygame 
import math
from datetime import datetime
from pyowm import OWM 
from pyowm.utils.config import get_default_config

#------------------------------------------------------------------------------------------------------------------------------------------
# Constantes Globale
PASSWORD           = "996999"
SCREEN_WIDTH       = 800
SCREEN_HEIGHT      = 500
OPENWEATHERMAP_KEY = "c7f2b9e644081852a58bd13fae3cccf3"
WEATHER_AT_PLACE   = "Montreal,CA"
LANGUAGE           = "fr"

#------------------------------------------------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------------------------------------------------
# Creation de l'ecran principale
class Ecran1:
# Deisgn de l'ecran principale
    APP_BACKGROUND_COLOR = (8,60,72)
    ARM_BTN_COLOR        = (8,21,2)
    ID_ARM_BTN     = 1
    ID_WEATHER_BTN = 2
    BTN_TOP    = 250
    BTN_WIDTH  = 165
    BTN_HEIGHT = 165

    def __init__(self, screen):
# Proprietes et ajout de la barre horizontal du haut et calcul de separation entre les deux boutons
        self.controls = []
        self.screen = screen
        self.statusBar = HorizontalBar(screen)
        self.controls.append(self.statusBar)
        position = (SCREEN_WIDTH - (2 * self.BTN_WIDTH)) / 3
# Calcule la position et ajoute le 1er bouton a l'ecran
        x = position
        self.controls.append(Meteo(self.ID_WEATHER_BTN,screen, pygame.Rect(x, self.BTN_TOP, self.BTN_WIDTH, self.BTN_HEIGHT)))
# Calcule la position et ajoute le 2e bouton a l'ecran
        x = position + self.BTN_WIDTH + position
        self.controls.append(Image(self.ID_ARM_BTN,screen, pygame.Rect(x, self.BTN_TOP, self.BTN_WIDTH, self.BTN_HEIGHT),"images/buttons/arm_button.png"))                                        
        self.draw()

#------------------------------------------------------------------------------------------------------------------------------------------
# Fonction pour dessiner
    def draw(self):
# Effacer le background
        self.screen.fill(self.APP_BACKGROUND_COLOR)
# Dessiner les boutons
        for ctrl in self.controls:
            ctrl.draw()
# Appliquer les changement a l'ecran
        pygame.display.flip()

#------------------------------------------------------------------------------------------------------------------------------------------
# Fonction Idle
    def refresh(self):
        self.statusBar.draw()
        pygame.display.flip()

#------------------------------------------------------------------------------------------------------------------------------------------
# Lecture du touchscreen / souris
    def appEvent(self):
# Loop pour les evenements
        running = True 
        while running: 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
# Click de souris
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    for ctrl in self.controls:
                        if ctrl.rect.collidepoint(pos):
                            self.onCommand(ctrl.id)
            self.refresh()                
        pygame.quit()

#------------------------------------------------------------------------------------------------------------------------------------------
#Fonction qui link le bouton a son action
    def onCommand(self, id):
        if id == self.ID_ARM_BTN:
# Switch entre l'ecran 1 et l'ecran 2
            screen2 = Ecran2(self.screen)
            screen2.appEvent()
# Reformatage de l'ecran 1
            self.draw()
            pygame.display.flip()


#------------------------------------------------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------------------------------------------------
#Class Ecran d'alarme
class Ecran2:
#Designe et formatage du numpad
    APP_BACKGROUND_COLOR = (8,60,72)
#Numeration des elements de la page
    ID_PWD        = 12
    ID_ARM_DESARM = 13
    ID_NUM_1      =  1;     ID_NUM_2 =  2;      ID_NUM_3         =  3;
    ID_NUM_4      =  4;     ID_NUM_5 =  5;      ID_NUM_6         =  6;
    ID_NUM_7      =  7;     ID_NUM_8 =  8;      ID_NUM_9         =  9;
    ID_NUM_CLEAR  = 10;     ID_NUM_0 =  0;      ID_NUM_BACKSPACE = 11;
#Design du gris, colonnes et ranger
    GRID_CX   = 11
    GRID_CY   = 10
    GRID_COLS = 3
    GRID_ROWS = 4
#Dimension des boutons
    TEXTBOX_HEIGHT = 64
    NUM_BTN_WIDTH   = 122
    NUM_BTN_HEIGHT  = 64
#Dimension de l'image    
    ARM_DESARM_BTN_WIDTH  = 165
    ARM_DESARM_BTN_HEIGHT = 165
#Path pour allez chercher les images
    ARM_IMAGE_PATH        = "images/buttons/arm_button.png"
    DESARM_IMAGE_PATH     = "images/buttons/desarm_button.png"

#------------------------------------------------------------------------------------------------------------------------------------------
# Importation du systeme d'alarme
    def __init__(self, screen):
# Creation d'une instance de systeme d'alarme
        self.alarmSystem = AlarmSystem()
# Initialisation des propriete de l'ecran
        self.controls = []
        self.screen = screen
# Ajout de la barre d'etat 
        self.statusBar = HorizontalBar(screen)
        self.controls.append(self.statusBar)
# Ajout de la barre pour le password
        self.password = EcranPassword(self.ID_PWD, screen, pygame.Rect(SCREEN_WIDTH / 2, self.statusBar.rect.height + self.GRID_CY, 
        (SCREEN_WIDTH / 2) - self.GRID_CX, self.NUM_BTN_HEIGHT))
        self.controls.append(self.password)
# Ajout du bouton Armer/Desarmer
        self.img = Image(self.ID_ARM_DESARM, screen, pygame.Rect(((SCREEN_WIDTH / 2) - self.ARM_DESARM_BTN_WIDTH) / 2, 
        (SCREEN_HEIGHT - self.statusBar.rect.height - self.ARM_DESARM_BTN_HEIGHT) / 2, self.ARM_DESARM_BTN_WIDTH, 
        self.ARM_DESARM_BTN_HEIGHT), self.ARM_IMAGE_PATH)
        self.controls.append(self.img)

#------------------------------------------------------------------------------------------------------------------------------------------
#Numpad design / location des boutons
        labels = ['1',      '2',        '3', 
                  '4',      '5',        '6', 
                  '7',      '8',        '9',
                  'Del',    '0',        'Back']
# Liaisons entre les boutons et leur ID                  
        ids = [self.ID_NUM_1,     self.ID_NUM_2,    self.ID_NUM_3,
               self.ID_NUM_4,     self.ID_NUM_5,    self.ID_NUM_6,
               self.ID_NUM_7,     self.ID_NUM_8,    self.ID_NUM_9,
               self.ID_NUM_CLEAR, self.ID_NUM_0,    self.ID_NUM_BACKSPACE]
# Ajout des boutons
        x = SCREEN_WIDTH / 2
        y = self.statusBar.rect.height + self.GRID_CY + self.TEXTBOX_HEIGHT + self.GRID_CY
        for i in range(0, self.GRID_ROWS):
            for j in range(0, self.GRID_COLS):
                self.controls.append(Button(ids[(i*self.GRID_COLS) + j], screen, pygame.Rect(x, y, self.NUM_BTN_WIDTH, self.NUM_BTN_HEIGHT), 
                labels[(i*self.GRID_COLS) + j]))
                x += self.NUM_BTN_WIDTH + self.GRID_CX
            x = SCREEN_WIDTH / 2
            y += self.NUM_BTN_HEIGHT + self.GRID_CY
        self.draw()

#------------------------------------------------------------------------------------------------------------------------------------------
# Dessinateur d'interface
    def draw(self):
# Effaceure de background
        self.screen.fill(self.APP_BACKGROUND_COLOR)
# Dessinateur de bouton
        for ctrl in self.controls:
            ctrl.draw()
        pygame.display.flip()

#------------------------------------------------------------------------------------------------------------------------------------------
# Lecture d'evenements
    def refresh(self):
# Lecture des evenements du GPIO
            event = self.alarmSystem.getEvent()
            if event != Events.No_event:
                self.alarmSystem.doEvent(event)
# Update du temps sur la barre horizontal
            self.statusBar.draw()
            pygame.display.flip()

#------------------------------------------------------------------------------------------------------------------------------------------
# Input convertie en String
    def idToStr(self, id):
        return str(id)

#------------------------------------------------------------------------------------------------------------------------------------------
# Apelle des evenements du systeme d'alarme
    def appEvent(self):
# Boucle principale
            running = True 
            while running: 
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        for ctrl in self.controls:
                            pos = pygame.mouse.get_pos()
                            if ctrl.rect.collidepoint(pos):
                                self.onCommand(ctrl.id)
# Apelle des boutons presser
                    elif event.type == pygame.KEYDOWN:
# retour a l'ecran principale avec la touche escape
                        if event.key == pygame.K_ESCAPE:
                            running = False
                        self.BouttonPress(event.key)
                self.refresh()

#------------------------------------------------------------------------------------------------------------------------------------------
# Armer/ Desarmer le systeme
    def armDesarm(self):
# Verification du password
        if self.password.text == PASSWORD:
# Arm ou desarme le systeme
            self.alarmSystem.doEvent(Events.Bouton)
# Efface le Password
            self.password.toucheDel()
# Affiche l'image approprier selon l'etat du systeme
            if self.img.img_path == self.ARM_IMAGE_PATH:
                self.img.load(self.DESARM_IMAGE_PATH)
            else:
                self.img.load(self.ARM_IMAGE_PATH)
            self.img.draw()
            pygame.display.flip()
#------------------------------------------------------------------------------------------------------------------------------------------
# Etat du password
    def onCommand(self, id):
        if id == self.ID_ARM_DESARM:
# Arm/desarm le systeme
            self.armDesarm()
        elif id == self.ID_NUM_CLEAR:
# Efface le password
            self.password.toucheDel()
        elif id == self.ID_NUM_BACKSPACE:
# Efface avec le backspace
            self.password.toucheBack()
        else:
 # Ajout d'un chiffre au password
            self.password.toucheChiffre(self.idToStr(id))

#------------------------------------------------------------------------------------------------------------------------------------------
# Input au numpad
    def BouttonPress(self, key):
# Input des chiffres 0-9
        if key == pygame.K_0 or key == pygame.K_KP0:
            self.password.toucheChiffre('0')
        elif key == pygame.K_1 or key == pygame.K_KP1:
            self.password.toucheChiffre('1')
        elif key == pygame.K_2 or key == pygame.K_KP2:
            self.password.toucheChiffre('2')
        elif key == pygame.K_3 or key == pygame.K_KP3:
            self.password.toucheChiffre('3')
        elif key == pygame.K_4 or key == pygame.K_KP4:
            self.password.toucheChiffre('4')
        elif key == pygame.K_5 or key == pygame.K_KP5:
            self.password.toucheChiffre('5')
        elif key == pygame.K_6 or key == pygame.K_KP6:
            self.password.toucheChiffre('6')
        elif key == pygame.K_7 or key == pygame.K_KP7:
            self.password.toucheChiffre('7')
        elif key == pygame.K_8 or key == pygame.K_KP8:
            self.password.toucheChiffre('8')
        elif key == pygame.K_9 or key == pygame.K_KP9:
            self.password.toucheChiffre('9')
# Backspace
        elif key == pygame.K_BACKSPACE:
            self.password.toucheBack()
# Delete
        elif key == pygame.K_DELETE:
            self.password.toucheDel()
# Return\ enter
        elif key == pygame.K_RETURN:
            self.armDesarm()

#------------------------------------------------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------------------------------------------------
# Design de la barre horizontal du haut
class HorizontalBar:
    SB_HEIGHT      = 48
    SB_COLOR       = (148,70,0)
    SB_FONT_SIZE   = 24
    SB_TEXT_COLOR  = (255, 255, 255)
    SB_TIME_FORMAT = "%H:%M:%S"
    SB_CX_MARGIN   = 350

#------------------------------------------------------------------------------------------------------------------------------------------
#Initialisation de la barre horizontal
    def __init__(self, screen):
        self.screen = screen
        rect = screen.get_rect()
        self.rect = pygame.Rect(0, 0, rect.width, self.SB_HEIGHT)

#------------------------------------------------------------------------------------------------------------------------------------------
# Import du temps et initialisation au coin haut droit
    def draw(self):
        pygame.draw.rect(self.screen, self.SB_COLOR, self.rect, 0)
        current_time = datetime.now().strftime(self.SB_TIME_FORMAT)
        font = pygame.font.SysFont(None, self.SB_FONT_SIZE)
        img = font.render(current_time, True, self.SB_TEXT_COLOR)
        rect = img.get_rect()
        rect = pygame.Rect((self.rect.width - rect.width) - self.SB_CX_MARGIN,
        (self.rect.height - rect.height) / 2, rect.width, rect.height)
        self.screen.blit(img, rect)


#------------------------------------------------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------------------------------------------------
# Class pour formater et importer les images
class Image:
# Importe et converstion des images   
    def load(self, img_path):
        self.img = pygame.image.load(img_path)
        self.img.convert()  
        self.img_path = img_path      

    def __init__(self, id, screen, rect, img_path):
# Initialisation et configuration / load les images
        self.id = id
        self.screen = screen
        self.rect = rect
        self.img_path = ""
        self.load(img_path)

    def draw(self):
# Formate le rectangle de l'image et centre l'image dans le rectangle 
        rect = self.img.get_rect()
        rect.center = self.rect.center
        self.screen.blit(self.img, rect)


#------------------------------------------------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------------------------------------------------
# Class pour les boutons
class Button:
# Couleurs des boutons
    BTN_COLOR = (148,70,0)
    BTN_FONT_SIZE = 30
    BTN_TEXT_COLOR = (255, 255, 255)

    def __init__(self, id, screen, rect, text):
# initialisation des proprietes de boutons
        self.id = id
        self.screen = screen
        self.rect = rect
        self.text = text

    def draw(self):
# Dessine le bouton rectangle
        pygame.draw.rect(self.screen,self.BTN_COLOR, self.rect, 0)
        font = pygame.font.SysFont(None, self.BTN_FONT_SIZE)
        img = font.render(self.text, True, self.BTN_TEXT_COLOR)
# Formate le rectangle de l'image et centre l'image dans le rectangle 
        rect = img.get_rect()
        rect.center = self.rect.center
        self.screen.blit(img, rect)

        
#------------------------------------------------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------------------------------------------------
# Implimentation du label a password
class EcranPassword:
#design du label pour le password
    PWD_CHAR = '*'
    PWD_LEN  = 6
    LBL_COLOR = (255, 255, 255)
    LBL_FONT_SIZE = 48
    LBL_TEXT_COLOR = (0, 0, 0)

    def __init__(self,id, screen, rect):        
#Proprietes du label
        self.id = id
        self.screen = screen
        self.rect = rect
        self.text = ""
#------------------------------------------------------------------------------------------------------------------------------------------
#Dessinateur du label a password
    def draw(self):
        pygame.draw.rect(self.screen, self.LBL_COLOR, self.rect, 0)    
#Dessinateur du password cacher
        pwd = ""
        for char in range(0, len(self.text)):
            pwd+= self.PWD_CHAR
        font = pygame.font.SysFont(None, self.LBL_FONT_SIZE)
        img = font.render(pwd, True, self.LBL_TEXT_COLOR)
# Formate le rectangle de l'image et centre l'image dans le rectangle 
        rect = img.get_rect()
        rect.center = self.rect.center
        self.screen.blit(img, rect)
#------------------------------------------------------------------------------------------------------------------------------------------
# Insertion du password dans l'ecran blanche
    def toucheChiffre(self, char):
        if len(self.text) < self.PWD_LEN:
            self.text += char
            self.draw()
            pygame.display.flip()
#------------------------------------------------------------------------------------------------------------------------------------------
# Backspace
    def toucheBack(self):
        self.text = self.text[:len(self.text) -1]
        self.draw()
        pygame.display.flip()
#------------------------------------------------------------------------------------------------------------------------------------------
# Clear   
    def toucheDel(self):
        self.text = ""
        self.draw()
        pygame.display.flip()


#------------------------------------------------------------------------------------------------------------------------------------------
##------------------------------------------------------------------------------------------------------------------------------------------
# Station meteo
class Meteo:
#Design pour la meteo
    WEATHER_FONT_SIZE   = 24
    WEATHER_TEXT_COLOR  =  (255, 255, 255)
    WEATHER_IMAGE_SCALE = 1

#------------------------------------------------------------------------------------------------------------------------------------------
# Slecteur d'ecran pour afficher la meteo
    def __init__(self, id, screen, rect):
        self.id = id
        self.screen = screen
        self.rect = rect
#------------------------------------------------------------------------------------------------------------------------------------------
#Importation de la meteo
    def draw(self):
        config_dict = get_default_config() 
        config_dict['language'] = LANGUAGE 
        owm = OWM(OPENWEATHERMAP_KEY, config_dict) 
        mgr = owm.weather_manager() 
        observation = mgr.weather_at_place(WEATHER_AT_PLACE) 
        weather = observation.weather 
# Appliquer l'image relier a la meteo
        img = pygame.image.load("images/weather/large/" + weather.weather_icon_name + ".png")
        img.convert()
        img = pygame.transform.rotozoom(img, 0, self.WEATHER_IMAGE_SCALE) 
# Formate le rectangle de l'image et centre l'image dans le rectangle 
        rect = img.get_rect()
        rect.center = self.rect.center
        self.screen.blit(img, rect)
# Ecriture et formatage de la temperature en degree celcius
        font = pygame.font.SysFont(None, self.WEATHER_FONT_SIZE)
        img = font.render(str(weather.temperature('celsius')['temp']) + "°C", True, self.WEATHER_TEXT_COLOR)
        rect = img.get_rect()
        rect.midbottom = self.rect.midbottom
        self.screen.blit(img, rect)


#------------------------------------------------------------------------------------------------------------------------------------------
# Initialisation du programme
pygame.init()
screen1 = Ecran1(pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT]))
screen1.appEvent()
#------------------------------------------------------------------------------------------------------------------------------------------
#