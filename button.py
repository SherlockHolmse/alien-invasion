# 导入了模块pygame.font，它让Pygame能够将文本渲染到屏幕上
import pygame.font
class Button():
    # 方法__init__()接受参数self，对象ai_settings和screen，以及msg，其中msg是要在按钮中显示的文本
    # msg是要在按钮中显示的文本
    def __init__(self, ai_settings, screen, msg):
        """初始化按钮的属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 设置按钮的尺寸和其他属性
        self.width, self.height = 200, 50
        self.button_color = (255,192,203)
        self.text_color = (30, 144, 255)
        # 指定使用什么字体来渲染文本。实参None让Pygame使用默认字体，而48指定了文本的字号
        self.font = pygame.font.SysFont(None, 48)

        # 创建一个表示按钮的rect对象，并将其center属性设置为屏幕的center属性,使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # 按钮的标签只需创建一次
        # Pygame通过将你要显示的字符串渲染为图像来处理文本,调用prep_msg()来处理这样的渲染。
        self.prep_msg(msg)


    # 方法prep_msg()接受实参self以及要渲染为图像的文本（msg）
    def prep_msg(self, msg):
        """将msg渲染为图像，并使其在按钮上居中"""
        # 调用font.render()将存储在msg中的文本转换为图像，然后将该图像存储在msg_image中
        '''方法font.render()还接受一个布尔实参，该实参指定开启还是关闭反锯齿功能（反锯齿让文本的边缘更平滑）。
        余下的两个实参分别是文本颜色和背景色。我们启用了反锯齿功能，并将文本的背景色设置为按钮的颜色
（如果没有指定背景色，Pygame将以透明背景的方式渲染文本）'''
        self.msg_image = self.font.render(msg, True, self.text_color,
                                        self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        # 绘制一个用颜色填充的按钮，再绘制文本
        # 调用screen.fill()来绘制表示按钮的矩形，再调用screen.blit()
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)