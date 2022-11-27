import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf
def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init() # pygame.init()初始化背景设置，让Pygame能够正确地工作
    ai_settings = Settings()
    # 指定了游戏窗口的尺寸
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # 创建Play按钮
    play_button = Button(ai_settings, screen, "Play")

    # 创建存储游戏统计信息的实例，并创建记分牌
    stats = GameStats(ai_settings)
    # 导入新创建的类Scoreboard，并在创建实例stats后创建了一个名为sb的Scoreboard实例
    sb = Scoreboard(ai_settings, screen, stats)
    # 创建一艘飞船
    ship = Ship(ai_settings, screen)
    # 创建一个编组（group），用于存储所有有效的子弹，以便能够
    # 管理发射出去的所有子弹
    # 创建了一个Group实例，并将其命名为bullets
    bullets = Group()
    aliens = Group()

    # 创建外星人群
    gf.create_fleet(ai_settings, screen, ship, aliens)
    # 设置背景色
    bg_color = (128,0,128)

    # 开始游戏的主循环
    while True:
        #调用check_events()代码，将ship作为实参传递给它
        #在check_events()中，需要在玩家按空格键时处理bullets
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
                        aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                              bullets)
            # 更新子弹后再更新外星人的位置，因为稍后要检查是否有子弹撞到了外星人
            gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
            # 在update_screen()中，需要更新要绘制到屏幕上的bullets
            # 将sb传递给update_screen()，让它能够在屏幕上显示得分
            gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,bullets, play_button)

run_game()# 最后一行调用run_game()，这将初始化游戏并开始主循环