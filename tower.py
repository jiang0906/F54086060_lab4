import time

import pygame
import os
import math

TOWER_IMAGE = pygame.image.load(os.path.join("images", "rapid_test.png"))


class Circle:
    def __init__(self, center, radius):
        self.center = center
        self.radius = radius

    def collide(self, enemy):
        """
        Q2.2)check whether the enemy is in the circle (attack range), if the enemy is in range return True
        :param enemy: Enemy() object
        :return: Bool
        """

        """
        Hint:
        x1, y1 = enemy.get_pos()
        ...
        """
        # 要知道敵人是否有在攻擊範圍內，需要攻擊範圍的半徑以及敵人與塔中心的直線距離
        # 當敵人與塔中心的距離小於攻擊範圍半徑時(true)，觸發下一個動作
        x, y = self.center
        x1, y1 = enemy.get_pos()
        distance = math.sqrt((x - x1) ** 2 + (y - y1) ** 2)
        if distance <= self.radius:
            return True
        else:
            return False

    def draw_transparent(self, win):
        """
        Q1) draw the tower effect range, which is a transparent circle.
        :param win: window surface
        :return: None
        """
        # 我的備註:畫一個幾何圖形前，要先建立一個畫布(surface)
        # 畫布設定和視窗一樣大，這樣座標也好確定
        transparent_surface = pygame.Surface(win.get_size(), pygame.SRCALPHA)
        transparency = 128  # define transparency: 0~255, 0 is fully transparent

        # draw the rectangle on the transparent surface
        pygame.draw.circle(transparent_surface, (128, 128, 128, transparency), self.center, self.radius)
        win.blit(transparent_surface, (0, 0))
        pass


class Tower:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(TOWER_IMAGE, (70, 70))  # image of the tower
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # center of the tower
        self.range = 150  # tower attack range
        self.damage = 2   # tower damage
        self.range_circle = Circle(self.rect.center, self.range)  # attack range circle (class Circle())
        self.cd_count = 0  # used in self.is_cool_down()
        self.cd_max_count = 60  # used in self.is_cool_down()
        self.is_selected = True  # the state of whether the tower is selected
        self.type = "tower"

    def is_cool_down(self):
        """
        Q2.1) Return whether the tower is cooling down
        (1) Use a counter to computer whether the tower is cooling down (( self.cd_count
        :return: Bool
        """

        """
        Hint:
        let counter be 0
        if the counter < max counter then
            set counter to counter + 1
        else 
            counter return to zero
        end if
        """
        # cd時間為0(true)才可以攻擊，否則會持續順著時間直到cd = cd_max
        if self.cd_count < self.cd_max_count:
            self.cd_count += 1
            return False
        else:
            self.cd_count = 0
            return True

    def attack(self, enemy_group):
        """
        Q2.3) Attack the enemy.
        (1) check the the tower is cool down ((self.is_cool_down()
        (2) if the enemy is in attack range, then enemy get hurt. ((Circle.collide(), enemy.get_hurt()
        :param enemy_group: EnemyGroup()
        :return: None
        """
        # 當tower冷卻且enemy在攻擊範圍內時，tower發動攻擊(=enemy受傷害)
        for enemy in enemy_group.get():
            if self.is_cool_down() and self.range_circle.collide(enemy):
                enemy.get_hurt(self.damage)
                return


    def is_clicked(self, x, y):
        """
        Bonus) Return whether the tower is clicked
        (1) If the mouse position is on the tower image, return True
        :param x: mouse pos x
        :param y: mouse pos y
        :return: Bool
        """
        # 我的備註:因為大於等於小於這類的運算符號無法在不同狀態(int,tuple...)之間運作，所以要先設成座標才能都是int
        # 因為原點在視窗的左上角，所以由小到大分別是左到右、上到下
        # (x, y)為滑鼠點擊的座標，如果點擊位置在tower的圖檔位置內(true)，即可觸發下一個動作

        x_left, y_top = self.rect.topleft
        x_right, y_bottom = self.rect.bottomright

        if x_left <= x <= x_right and y_top <= y <= y_bottom:
            return True
        else:
            return False


    def get_selected(self, is_selected):
        """
        Bonus) Change the attribute self.is_selected
        :param is_selected: Bool
        :return: None
        """
        self.is_selected = is_selected

    def draw(self, win):
        """
        Draw the tower and the range circle
        :param win:
        :return:
        """
        # draw range circle
        if self.is_selected:
            self.range_circle.draw_transparent(win)
        # draw tower
        win.blit(self.image, self.rect)


class TowerGroup:
    def __init__(self):
        self.constructed_tower = [Tower(250, 380), Tower(420, 400), Tower(600, 400)]

    def get(self):
        return self.constructed_tower

