from objects import *

score = 0
level = 1
red_tone = 255

menu = True
shop = False
game = False
finish = True
pause = False
levelup = False

boss_round = False 

pygame.draw.rect(window, background, UI)
pygame.draw.rect(window, background, UI_SHOP)

player = Player(player_image,340,400,50,50,5)
for i in range(15):
    enemy = Enemy(enemy_images[0], 0, 0, 70, 70, 2)
    enemy.spawn()
    enemies.add(enemy)

def start():
    global menu, game, finish, pause, level, levelup, score, boss_round, player, enemies, red_tone

    menu = False
    game = True
    finish = False
    pause = False
    levelup = False
    boss_round = False

    pygame.mixer.music.load('sounds/bg_game.mp3')
    pygame.mixer_music.play(loops=-1)

    score = 0
    level = 1
    red_tone = 255
    player = Player(player_image,340,400,50,50,5)
    enemies.empty()
    for i in range(15):
        enemy = Enemy(enemy_images[0], 0, 0, 70, 70, 2)
        enemy.spawn()
        enemies.add(enemy)

def shop_fc():
    global shop, menu
    shop = True
    menu = False

def arm():
    for arm in arms:
        if arm.pressed:
            if not db.is_bought(arms.index(arm)):
                if db.get_points() >= costs[arms.index(arm)][1]:
                    db.add_weapon(arms.index(arm))
                    db.add_result(-costs[arms.index(arm)][1])
                    db.set_active(arms.index(arm))
            elif db.is_bought(arms.index(arm)):
                if not db.is_active(arms.index(arm)):
                    db.set_active(arms.index(arm))

def back():
    global shop, menu
    menu = True
    shop = False

def exit():
    quit()

def continue_game():
    global pause, finish
    pause = False
    finish = False
    pygame.mixer_music.unpause()

def menu_exit():
    global game, menu
    game = False
    menu = True

    pygame.mixer.music.load('sounds/bg_menu.mp3')
    pygame.mixer_music.play(loops=-1)

def lose():
    lose_text = pygame.font.Font(None,100).render('Game Over', True, (255,0,0))
    lose_rect = lose_text.get_rect(center=(window_width/2,250))
    window.blit(lose_text, lose_rect)
    record_text = ui_font.render(f'Best score: {db.get_record()}', True, (100,100,255))
    record_rect = record_text.get_rect(center=(window_width/2,window_height-30))
    window.blit(record_text, record_rect)

    restart_btn.rect.y = 350
    restart_btn.draw()
    restart_btn.update()
    menu_btn.rect.y = 520
    menu_btn.draw()
    menu_btn.update()

start_btn = Button(350,250,200,100,(50,50,100),start_btn_text, callback=start)
shop_btn = Button(350,400,200,100,(50,50,100),shop_btn_text, callback=shop_fc)
back_btn = Button(100,630,120,60,(50,50,100),back_btn_text, callback=back)
exit_btn = Button(70,50,100,50,(50,50,100),exit_btn_text, callback=exit)
continue_btn = Button(350,300,200,100,(50,50,100),continue_btn_text, callback=continue_game)
restart_btn = Button(350,450,200,100,(50,50,100),restart_btn_text, callback=start)
menu_btn = Button(350,600,200,100,(50,50,100),menu_btn_text, callback=menu_exit)

index = 0
x_coo = 100
for i in range(5):
    img = pygame.transform.scale(pygame.image.load(arm_images[index]), (90,50))
    but = Button(x_coo,130,100,100,(colors[index][0],colors[index][1],colors[index][2]),img, callback=arm)
    arms.append(but)
    costt = ui_font.render(f'{cost[index]}$', True, (100,255,255))
    costs.append([costt,cost[index]])
    damaget = ui_font.render(f'dmg:{damagex[index]}', True, (100,255,255))
    damages.append(damaget)
    reloadt = ui_font.render(f'rsp:{reload[index]}', True, (100,255,255))
    reloads.append(reloadt)
    x_coo += 125
    index += 1

heal = Heal(heal_image, -100, -100, 50, 50)
heal.spawn()

pygame.mixer_music.play(loops=-1)
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            quit()
    if menu:
        window.blit(menu_background, (0,0))
        start_btn.draw()
        start_btn.update()
        shop_btn.draw()
        shop_btn.update()
        exit_btn.draw()
        exit_btn.update()

        points = ui_font.render(f'Balance: {db.get_points()}$', True, (100,100,255))
        points_rect = points.get_rect()
        points_rect.center = (window_width-points_rect.width/2-20,40)
        window.blit(points, points_rect)

    if shop:
        pygame.draw.rect(window, background, UI_SHOP)
        back_btn.draw()
        back_btn.update()
        points = ui_font.render(f'Balance: {db.get_points()}$', True, (255,100,255))
        points_rect = points.get_rect()
        points_rect.center = (window_width-points_rect.width/2-20,40)
        window.blit(points, points_rect)
        for a in arms:
            a.draw()
            a.update()
        x_coo1 = 60
        x_coo2 = 60
        x_coo3 = 60
        for cost in costs:
            if not db.is_bought(costs.index(cost)):
                window.blit(cost[0],(x_coo1, 200))
                if db.get_points() < cost[1]:
                    img = pygame.transform.scale(pygame.image.load(lock_image), (50,50))
                    window.blit(img,(x_coo1+65,150))
            else:
                window.blit(bought_text, (x_coo1-20,200))
                if db.is_active(costs.index(cost)):
                    img = pygame.transform.scale(pygame.image.load(tick_image), (40,40))
                    window.blit(img,(x_coo1+65,150))
            x_coo1 += 120
        for damage in damages:
            if not db.is_bought(damages.index(damage)):
                window.blit(damage,(x_coo2, 250))
            x_coo2 += 120
        for reload in reloads:
            if not db.is_bought(reloads.index(reload)):
                window.blit(reload,(x_coo3, 300))
            x_coo3 += 120

    elif game:
        window.blit(game_background, (0,50))
        for a in arms:
            if db.is_active(arms.index(a)):
                color = colors[arms.index(a)]
        pygame.draw.circle(window, color, player.rect.center, player.width/2+5)
        player.draw()

        if player.hp <= 0:
            lose()
            enemies.empty()
        for enemy in enemies:
            enemy.draw()
        
        pygame.draw.rect(window, background, UI)
        if red_tone < 135.00000000000114:
            red_tone = 135.00000000000114
        health_label = ui_font.render(f'HP: {player.hp}', True, (red_tone,0,0))
        health_rect = health_label.get_rect()
        health_rect.center = (0+health_rect.width/2+20,25)
        window.blit(health_label, health_rect)
        level_label = ui_font.render(f'Level: {level}', True, (150,50,255))
        level_rect = level_label.get_rect(center=(window_width/2,25))
        window.blit(level_label, level_rect)
        score_label = ui_font.render(f'Coins: {score}', True, (150,255,50))
        score_rect = score_label.get_rect()
        score_rect.center = (window_width-score_rect.width/2-20,25)
        window.blit(score_label, score_rect)

        if pause:
            finish = True
            game = True
            pause_label= pygame.font.Font(None, 100).render('Pause', True, (255,0,0))
            window.blit(pause_label, (250, 150))

            pygame.mixer_music.pause()

            restart_btn.rect.y = 400
            menu_btn.rect.y = 550

            continue_btn.draw()
            continue_btn.update()
            restart_btn.draw()
            restart_btn.update()
            menu_btn.draw()
            menu_btn.update()

        if not finish:
            player.update()
            for enemy in enemies:
                dx = enemy.rect.centerx - player.rect.centerx
                dy = enemy.rect.centery - player.rect.centery
                ang = -math.atan2(-dy, dx) - math.pi
                enemy.update(ang)
                if player.hitbox.colliderect(enemy.hitbox):
                    damage_sound.play()
                    player.hp -= enemy.hp
                    red_tone -= enemy.hp * 1.2
                    if enemy in boss_list:
                        enemy.kill()
                        boss_round = False
                        boss_list.clear()
                    else:
                        enemy.spawn()
            if player.hp <= 30:
                heal.draw()
                if player.hitbox.colliderect(heal.rect):
                    heal_sound.play()
                    player.hp += 20
                    red_tone += 40
                    if player.hp > 100:
                        player.hp = 100
                    heal.spawn()
            for bullet in bullets:
                bullet.update()
                if math.sqrt((bullet.rect.x - player.rect.x)**2 + (bullet.rect.y - player.rect.y)**2) > 1000:
                    bullet.kill()
                    break
                bullet.draw()
            collide = pygame.sprite.groupcollide(bullets, enemies, True, False)
            if collide:
                levelup = False
                enemy = list(collide.values())[0][0]
                for a in arms:
                    if db.is_active(arms.index(a)):
                        enemy.hp -= damagex[arms.index(a)]
                if enemy.hp <= 0:
                    if enemy in boss_list:
                        coins_sound.play()
                        boss_list.clear()
                        boss_round = False
                        enemy.kill()
                        for a in arms:
                            if db.is_active(arms.index(a)):
                                score += enemy.max_hp * damagex[arms.index(a)]
                    else:
                        coin_sound.play()
                        enemy.spawn()
                        for a in arms:
                            if db.is_active(arms.index(a)):
                                score += enemy.max_hp * damagex[arms.index(a)]
            if score % 15 == 0 and score != 0 and not boss_round:
                boss = Enemy(enemy_images[1], 0, 0, 70, 70, 2)
                boss.max_hp = 15
                boss_list.append(boss)
                boss.spawn()
                enemies.add(boss)
                boss_round = True
            if score % 30 == 0 and score != 0 and levelup == False:
                levelup_sound.play()
                level += 1
                levelup = True
                if level >= 4:
                    enemy = Enemy(enemy_images[0], 0, 0, 70, 70, 2)
                    enemy.max_hp = level
                    enemy.spawn()
                    enemies.add(enemy)
                for enemy in enemies:
                    if enemy not in boss_list:
                        enemy.max_hp = level
                    if level in [6,9]:
                        enemy.speed += 1

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE] and player.hp > 0:
                pause = True

            if player.hp <= 0:
                pygame.mixer_music.stop()
                gameover_sound.play()

                db.add_result(score)
                finish = True

    pygame.display.update()
    clock.tick(FPS)
