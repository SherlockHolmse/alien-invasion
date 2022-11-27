# 重构 重构旨在简化既有代码的结构，使其更容易扩展
import sys # 模块sys来退出游戏
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien
#简化run_game()并隔离事件管理循环
# 通过隔离事件循环，可将事件管理与游戏的其他方面（如更新屏幕）分离。
def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按键"""
    # 读取属性event.key，以检查按下的是否是右箭头键（pygame.K_RIGHT）
    # 这里之所以可以使用elif代码块，是因为每个事件都只与一个键相关联；
    # 如果玩家同时按下了左右箭头键，将检测到两个不同的事件
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    # 玩家按Q时结束游戏
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
    """如果还没有到达限制，就能发射一颗子弹"""
    # 创建一颗子弹，并将其加入到编组bullets中
    # 玩家按空格键时，创建一颗新子弹（一
    # 个名为new_bullet的Bullet实例）
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """响应松开"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


#check_events()的定义需要形参aliens，以便将它传递给check_play_button()。接下来，我
#们修改了调用check_play_button()的代码，以将合适的实参传递给它
def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
 bullets):
    """响应按键和鼠标事件"""
    '''每当用户按键时，都将在Pygame中注册一个事件。事件都是通过方法
    pygame.event.get()获取的'''
    # 监视键盘和鼠标事件
    # pygame.event.get()访问Pygame检测到的事件
    for event in pygame.event.get():
        # 玩家单击游戏窗口的关闭按钮时，将检测到pygame.QUIT事件。
        # 并用sys.exit()来退出游戏
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)



        #添加了一个新的elif代码块，用于响应KEYUP事件：
        #玩家松开右箭头键（K_RIGHT）时，我们将moving_right设置为False
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 使用了pygame.mouse. get_pos()，它返回一个元组，其中包含玩家单击时鼠标的x和y坐标
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
 bullets, mouse_x, mouse_y):
    """在玩家单击Play按钮时开始新游戏"""
    # 仅当玩家单击了Play按钮且游戏当前处于非活动状态时，游戏才重新开始
    # 标志button_clicked的值为True或False
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        # 隐藏光标  通过向set_visible()传递False，让Pygame在光标位于游戏窗口内时将其隐藏起来
        pygame.mouse.set_visible(False)
        if play_button.rect.collidepoint(mouse_x, mouse_y):
            # 重置游戏统计信息
            stats.reset_stats()
            stats.game_active = True

            # 重置记分牌图像
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            sb.prep_ships()

            # 清空外星人列表和子弹列表
            aliens.empty()
            bullets.empty()

            # 创建一群新的外星人，并让飞船居中
            create_fleet(ai_settings, screen, ship, aliens)
            ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
 play_button):
    """更新屏幕上的图像，并切换到新屏幕"""
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    # 在飞船和外星人后面重绘所有子弹
    # 方法bullets.sprites()返回一个列表，其中包含编组bullets中的所有精灵
    for bullet in bullets.sprites():
        # 遍历编组bullets中的精灵，并对每个精灵都调用draw_bullet()
        bullet.draw_bullet()
    # 调用其方法blitme()，让飞船出现在屏幕上
    ship.blitme()
    # 对编组调用draw()时，Pygame自动绘制编组的每个元素，绘制位置由元素的属性rect决定。
    # 在这里，aliens.draw(screen)在屏幕上绘制编组中的每个外星人
    aliens.draw(screen)

    # 显示得分
    sb.show_score()

    # 如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # 让最近绘制的屏幕可见
    # 每次执行while循环时都绘制一个空屏幕
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # 当你对编组调用update()时，编组将自动对其中的每个精灵调用update()，
    # 因此代码行bullets.update()将为编组bullets中的每颗子弹调用bullet.update()。
    bullets.update()

    # 删除已消失的子弹
    # 在for循环中，不应从列表或编组中删除条目，因此必须遍历编组的副本
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
        # 将输出写入到终端而花费的时间比将图形绘制到游戏窗口花费的时间要多

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
         aliens, bullets):
    """响应子弹和外星人的碰撞"""
    # 检查是否有子弹击中了外星人
    # 如果是这样，就删除相应的子弹和外星人
    '''方法sprite.groupcollide()将每颗子弹的rect同每个外星人的rect进行比较，并返回一个字
    典，其中包含发生了碰撞的子弹和外星人
    在这个字典中，每个键都是一颗子弹，而相应的值都是被击中的外星人'''

    '''新增的这行代码遍历编组bullets中的每颗子弹，再遍历编组aliens中的每个外星人。每当
    有子弹和外星人的rect重叠时，groupcollide()就在它返回的字典中添加一个键值对。两个实参
    True告诉Pygame删除发生碰撞的子弹和外星人。（要模拟能够穿行到屏幕顶端的高能子弹——消
    灭它击中的每个外星人，可将第一个布尔实参设置为False，并让第二个布尔实参为True。这样
    被击中的外星人将消失，但所有的子弹都始终有效，直到抵达屏幕顶端后消失'''
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    # 有子弹撞到外星人时，Pygame返回一个字典（collisions）我们检查这个字典是否存在,如果存在，就将得分加上一个外星人值的点数
    if collisions:
        # 与外星人碰撞的子弹都是字典collisions中的一个键；而与每颗子弹相关的值都是一个列表，其中包含该子弹撞到的外星人
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        # 调用prep_score()来创建一幅显示最新得分的新图像
        sb.prep_score()
    check_high_score(stats, sb)

    # 检查编组aliens是否为空。如果是，就使用方法empty()
    # 删除编组中余下的所有精灵，从而删除现有的所有子弹,加快游戏节奏
    # 还调用了create_fleet()，再次在屏幕上显示一群外星人
    if len(aliens) == 0:
        # 如果整群外星人都被消灭，就提高一个等级
        # 删除现有的子弹并新建一群外星人
        bullets.empty()
        ai_settings.increase_speed()
        # 提高等级
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)

def get_number_aliens_x(ai_settings, alien_width):
    """计算每行可容纳多少个外星人"""
    #计算可用于放置外星人的水平空间，以及其中可容纳多少个外星人
    available_space_x = ai_settings.screen_width - 2 * alien_width
    #int()将小数部分丢弃，相当于向下圆整
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕可容纳多少行外星人"""
    # 计算公式用括号括起来了，这样可将代码分成两行
    available_space_y = (ai_settings.screen_height -
                 (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    #创建一个外星人并将其加入当前行
    alien = Alien(ai_settings, screen)
    # 从外星人的rect属性中获取外星人宽度，并将这个值存储到alien_width中，以免反复访问属性rect
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """创建外星人群"""
    # 创建一个外星人，并计算一行,一列可容纳多少个外星人
    # 我们需要知道外星人的宽度和高度，因此在执行计算前，先创建一个外星人。这个外星人不是外星人群的成员，
    # 因此没有将它加入到编组aliens中
    # 外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # 创建外星人群
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """响应被外星人撞到的飞船"""
    if stats.ships_left > 0:
        # 将ships_left减1
        stats.ships_left -= 1
        # 更新记分牌
        # 在飞船被外星人撞到时调用prep_ships()，从而在玩家损失一艘飞船时更新飞船图像
        sb.prep_ships()
        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()
        # 创建一群新的外星人，并将飞船放到屏幕底端中央
        create_fleet(ai_settings, screen, ship, aliens)
        # 在Ship类中添加方法center_ship()
        ship.center_ship()
        # 从模块time中导入了函数sleep()，以便使用它来让游戏暂停
        sleep(0.5)
    else:
        stats.game_active = False
        # 游戏结束后，我们将重新显示光标，让玩家能够单击Play按钮来开始新游戏
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """检查是否有外星人到达了屏幕底端"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 像飞船被撞到一样进行处理
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break


# 更新了update_aliens()的定义，使其包含形参stats、screen和bullets，让它能够在调用ship_hit()时传递这些值
def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    """
    检查是否有外星人位于屏幕边缘，并更新整群外星人的位置
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # 检测外星人和飞船之间的碰撞
    #方法spritecollideany()接受两个实参：一个精灵和一个编组。它检查编组是否有成员与精
    #灵发生了碰撞，并在找到与精灵发生了碰撞的成员后就停止遍历编组。在这里，它遍历编组aliens，
    #并返回它找到的第一个与飞船发生了碰撞的外星人。
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)

    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)


def check_high_score(stats, sb):
    """检查是否诞生了新的最高得分"""
    # 使用stats来比较当前得分和最高得分，并在必要时使用sb来修改最高得分图像
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


