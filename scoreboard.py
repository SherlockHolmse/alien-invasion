import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():
    """显示得分信息的类"""
    # 我们在__init__()中包含形参ai_settings、screen和stats，让它能够报告我们跟踪的值


    def __init__(self, ai_settings, screen, stats):
        """初始化显示得分涉及的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ai_settings = ai_settings
        self.stats = stats

        # 显示得分信息时使用的字体设置
        self.text_color = (135, 206, 235)
        self.font = pygame.font.SysFont(None, 48)
        # 准备包含最高得分和当前得分的图像
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()


    def prep_score(self):
        """将得分转换为一幅渲染的图像"""
        # 函数round()通常让小数精确到小数点后多少位，其中小数位数是由第二个实参指定的
        rounded_score = int(round(self.stats.score, -1))
        # 字符串格式设置指令，它让Python将数值转换为字符串时在其中插入逗号
        score_str = "{:,}".format(rounded_score)
        # 再将这个字符串传递给创建图像的render()
        self.score_image = self.font.render("score:"+ score_str, True, self.text_color,
                                        self.ai_settings.bg_color)


        # 将得分放在屏幕右上角，并在得分增大导致这个数字更宽时让它向左延伸
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高得分转换为渲染的图像"""

        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render("best score:" + high_score_str, True,
                                               self.text_color, self.ai_settings.bg_color)

        # 将最高得分放在屏幕顶部中央
        self.high_score_rect = self.high_score_image.get_rect()

        self.high_score_rect.centerx = self.screen_rect.centerx
        # 将其top属性设置为当前得分图像的top属性
        self.high_score_rect.top = self.score_rect.top




    # 这个方法将得分图像显示到屏幕上，并将其放在score_rect指定的位置
    def show_score(self):
        """在屏幕上显示当前得分和最高得分及飞船"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        # 绘制飞船
        # 为在屏幕上显示飞船，我们对编组调用了draw()。Pygame将绘制每艘飞船
        self.ships.draw(self.screen)


    def prep_level(self):
        """将等级转换为渲染的图像"""
        self.level_image = self.font.render("level:" + str(self.stats.level), True,
                                          self.text_color, self.ai_settings.bg_color)

        # 将等级放在得分下方
        self.level_rect = self.level_image.get_rect()

        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

    def prep_ships(self):
        """显示还余下多少艘飞船"""
        # 方法prep_ships()创建一个空编组self.ships，用于存储飞船实例
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
             ship = Ship(self.ai_settings, self.screen)
             ship.rect.x = 10 + ship_number * ship.rect.width
             ship.rect.y = 10
             self.ships.add(ship)