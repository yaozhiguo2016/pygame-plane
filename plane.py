# 初始化pygame环境，并创建一个窗口
import pygame
from sys import exit
import random

pygame.init()
# 创建一个窗口
screen = pygame.display.set_mode((400, 600), 0, 32)
# 设置窗口的名称
window_title = pygame.display.set_caption("hey plane")
# 导入背景图片
background = pygame.image.load('bg.jpg').convert()

game_over = False

score = 0
font = pygame.font.Font(None, 32)

# 飞机对象
class Plane(object):
    def __init__(self):
        self.x = 200
        self.y = 200
        self.image = pygame.image.load('plane.png').convert_alpha()

    def move(self, mouse_x, mouse_y):
        self.x = mouse_x - self.image.get_width() / 2
        self.y = mouse_y - self.image.get_height() / 2

    def restart(self, mouse_x, mouse_y):
        self.move(mouse_x, mouse_y)

# 子弹对象
class Bullet(object):
    def __init__(self):
        self.x = -1
        self.y = -1
        self.active = False
        self.image = pygame.image.load('bullet.png').convert_alpha()

    def move(self, mouse_x, mouse_y):
        # 飞出去的子弹不再回收
        if self.y < 0:
            self.active = False
        # 激活的子弹保持移动
        if self.active:
            self.y -= 0.5

    def restart(self):
        # 设置子弹的发射位置（因为move()方法不再回收，所以激活子弹时要设置子弹的发射位置）
        self.x = mouse_x - self.image.get_width() / 2
        self.y = mouse_y - self.image.get_height() / 2
        self.active = True

# 敌机对象
class Enemy(object):
    def __init__(self):
        self.restart()
        self.image = pygame.image.load('enemy.png').convert_alpha()

    def move(self, mouse_x, mouse_y):
        if self.y > 600:
            self.restart()
        else:
            self.y += self.speed

    def restart(self):
        self.x = random.randint(20, 320)
        self.y = random.randint(-500, -50)
        self.speed = random.uniform(0.1, 0.5)

# 子弹和敌机碰撞检测
def check_hit(b, e):
    if (e.x < b.x < e.x + e.image.get_width()) and (e.y < b.y < e.y + e.image.get_height()):
        b.active = False
        e.restart()
        return True
    return False        
        
# 飞机和敌机碰撞检测
def check_crash(p, e):
    if (p.x < e.x + 0.5  *  e.image.get_width()) and (p.x + 0.5 * p.image.get_width() > e.x) and (
                p.y < e.y + 0.3 * e.image.get_height()) and (p.y + 0.8 * p.image.get_height() > e.y):
        return True
    return False
    
# 创建飞机对象
plane = Plane()

# 创建弹夹对象
bullets = []
for i in range(5):
    bullets.append(Bullet())
count_b = len(bullets)
index_b = 0

# 创建敌机群对象
enemies = []
for i in range(3):
    enemies.append(Enemy())# 初始化发射之间间隔
interval = 0

# 设置循环运行
while True:
    # 获取鼠标的位置(放在循环中，因为要获取实时的鼠标位置)
    mouse_x, mouse_y = pygame.mouse.get_pos()# 获取光标的位置
    text = font.render("Score: %d" % score, 1, (0, 255, 0))

    # 使得程序能正常退出
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP and game_over:
            for b in bullets:
                b.restart()
            for e in enemies:
                e.restart()
            plane.restart(mouse_x, mouse_y)
            game_over = False
            score = 0

    if not game_over:
        # 在窗口中把背景放置进去
        screen.blit(background, (0, 0))
        # 绘制分数
        screen.blit(text, (5, 5))

        # 按照一定时间间隔发射子弹
        interval -= 1
        if interval < 0:  # 如果时间间隔到，就激活一个子弹对象
            interval = 250
            bullets[index_b].restart()
            index_b = (index_b + 1) % count_b
        for b in bullets:
            if b.active:  # 发射激活的子弹
                for e in enemies:
                    if check_hit(b, e):
                        score += 100
                b.move(mouse_x, mouse_y)
                screen.blit(b.image, (b.x, b.y))

        # 飞机跟随鼠标位置
        plane.move(mouse_x, mouse_y)
        # 放置飞机
        screen.blit(plane.image, (plane.x, plane.y))

        # 放置敌机
        for e in enemies:
            if check_crash(plane, e):
                game_over = True
            screen.blit(e.image, (e.x, e.y))
            e.move(mouse_x, mouse_y)
    else:
        text = font.render('kick and again ?', 1, (0, 255, 0))
        screen.blit(text, (120, 280))

    # 刷新界面，把所做的更改显示出来
    pygame.display.update()