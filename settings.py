import pygame
pygame.init()

window_width = 700
window_height = 700
FPS = 20

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Warfare')
clock = pygame.time.Clock()

game_background = pygame.transform.scale(pygame.image.load('images/game_background.jpeg'), (700,700))
menu_background = pygame.transform.scale(pygame.image.load('images/menu.jpeg'), (700,700))

player_image = 'images/player.png'
heal_image = 'images/aid.png'
enemy_images = ['images/zombie1.png', 'images/zombie2.png']
bullet_image = 'images/bullet.png'

bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()

boss_list = []

colors = [[205,127,50],[192,192,192],[255,215,0],[185,242,255],[128,128,128]]
arms = []

arm_images = ['images/arm1.png','images/arm2.png','images/arm3.png','images/arm4.png','images/arm5.png']

cost = [200, 500, 1000, 5000, 10000]
damagex = [1, 2, 3, 5, 10]
reload = [10,8,6,4,3]
costs = []
damages = []
reloads = []

tick_image = 'images/tick.png'
lock_image = 'images/lock.png'

pygame.mixer.music.load('sounds/bg_menu.mp3')
choice_sound = pygame.mixer.Sound('sounds/choice.ogg')
fire_sound = pygame.mixer.Sound('sounds/fire.ogg')
fire_sound.set_volume(0.5)
damage_sound = pygame.mixer.Sound('sounds/damage.ogg')
levelup_sound = pygame.mixer.Sound('sounds/levelup.ogg')
levelup_sound.set_volume(5)
coin_sound = pygame.mixer.Sound('sounds/coin.ogg')
coins_sound = pygame.mixer.Sound('sounds/coins.ogg')
heal_sound = pygame.mixer.Sound('sounds/heal.ogg')
heal_sound.set_volume(5)
gameover_sound = pygame.mixer.Sound('sounds/gameover.ogg')

background = (150,150,100)

UI = pygame.Rect(0, 0, window_width, 50)
UI_SHOP = pygame.Rect(20,20, window_width-40, window_height-40)

ui_font = pygame.font.Font(None, 50)

start_btn_text = ui_font.render('Start', True, (100,255,255))
shop_btn_text = ui_font.render('Shop', True, (100,255,255))
settings_btn_text = ui_font.render('Settings', True, (100,255,255))
back_btn_text = ui_font.render('<Back', True, (100,255,255))
exit_btn_text = ui_font.render('Exit', True, (100,255,255))
continue_btn_text = ui_font.render('Continue', True, (100,255,255))
restart_btn_text = ui_font.render('Restart', True, (100,255,255))
menu_btn_text = ui_font.render('Exit to menu', True, (100,255,255))

bought_text = ui_font.render('Bought',True,(50,50,100))