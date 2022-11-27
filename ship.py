import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
     # rect的centerx等属性只能存储整数值，因此我们需要对Ship类做些修改
     # 我们在__init__()的形参列表中添加了ai_settings，让飞船能够获取其速度设置
     def __init__(self, ai_settings, screen):
         """初始化飞船并设置其初始位置
         screen指定了要将飞船绘制到什么地方"""
         super(Ship, self).__init__()
         self.screen = screen
         self.ai_settings = ai_settings

         # 加载飞船图像并获取其外接矩形
         self.image = pygame.image.load('images\ship.bmp')
         '''这个函数返回一个表示飞船的surface，
         而我们将这个surface存储到了self.image中'''
         self.rect = self.image.get_rect()
         # 使用get_rect()获取相应surface的属性rect
         self.screen_rect = screen.get_rect()

         # 将每艘新飞船放在屏幕底部中央
         '''要将游戏元素居中，可设置相应rect对象的属性center、centerx或centery。
         要让游戏元素与屏幕边缘对齐，可使用属性top、bottom、left或right；
         要调整游戏元素的水平或垂直位置，可使用属性x和y,
         它们分别是相应矩形左上角的x和y坐标。
         在Pygame中，原点(0, 0)位于屏幕左上角'''
         # 将self.rect.centerx（飞船中心的x坐标）设置为表示屏幕的矩形的属性centerx
         self.rect.centerx = self.screen_rect.centerx
         # 将self.rect.bottom（飞船下边缘的y坐标）设置为表示屏幕的矩形的属性bottom
         self.rect.bottom = self.screen_rect.bottom

         # 在飞船的属性center中存储小数值
         # 定义了一个可存储小数值的新属性self.center
         # 将self.rect.centerx的值转换为小数，并将结果存储到self.center中
         self.center = float(self.rect.centerx)

         # 移动标志
         self.moving_right = False
         self.moving_left = False
         #方法update()检查标志moving_right的状态
     def update(self):
             """根据移动标志调整飞船的位置"""
             # 添加了一个if代码块而不是elif代码块，
             # 这样如果玩家同时按下了左右箭头键，将先增大飞船的
             # rect.centerx值，再降低这个值，即飞船的位置保持不变
             if self.moving_right and self.rect.right < self.screen_rect.right:
                 # 更新飞船的center值，而不是rect
                 self.center += self.ai_settings.ship_speed_factor
             if self.moving_left and self.rect.left > 0:
                 self.center -= self.ai_settings.ship_speed_factor

             # 根据self.center更新rect对象
             # self.rect.centerx将只存储self.center的整数部分，但对显示飞船
             # 而言，这问题不大
             self.rect.centerx = self.center

     def blitme(self):
         """在指定位置绘制飞船"""
         self.screen.blit(self.image, self.rect)
         # 定义了方法blitme()，它根据self.rect指定的位置将图像绘制到屏幕上

     def center_ship(self):
         """让飞船在屏幕上居中"""
         self.center = self.screen_rect.centerx