"""
File: asteroids.py
Original Author: Br. Burton
Designed to be completed by others
This program implements the asteroids game.
"""
"""Completed by Nelson Georges"""
import arcade
import random
import math 
from abc import ABC, abstractmethod

# These are Global constants to use throughout the game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BULLET_RADIUS = 30
BULLET_SPEED = 10
BULLET_LIFE = 60

SHIP_TURN_AMOUNT = 5 
SHIP_THRUST_AMOUNT = 0.25
SHIP_RADIUS = 30

INITIAL_ROCK_COUNT = 5
INTERMEDIATE_LEVEL_ROCK_COUNT = 10
HARD_LEVEL_ROCK_COUNT = 15

BIG_ROCK_SPIN = 1
BIG_ROCK_SPEED = 1.5
BIG_ROCK_RADIUS = 15

MEDIUM_ROCK_SPIN = -2
MEDIUM_ROCK_RADIUS = 5
MEDIUM_ROCK_SPEED = 1.5

SMALL_ROCK_SPIN = 5
SMALL_ROCK_RADIUS = 2
SMALL_ROCK_SPEED = 1.5

SCORE_HIT = 2

class Point:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        
class Velocity:
    def __init__(self):
        self.dx = 0
        self.dy = 0

class FlyingObject(ABC):
    
    def __init__(self, img):
        self.center = Point()
        self.velocity = Velocity()
        self.alive = True
        self.img = img
        self.texture = arcade.load_texture(self.img)
        self.width = self.texture.width
        self.height = self.texture.height
        self.radius = 0
        self.angle = 0
        self.speed = 0
        self.direction = 0
        
        
    def advance(self):
        
        self.center.x += self.velocity.dx
        self.center.y += self.velocity.dy
       
        # This is for screen wrapping on edges
        if self.center.x > SCREEN_WIDTH:
            self.center.x -= SCREEN_WIDTH
        if self.center.x < 0:
            self.center.x += SCREEN_WIDTH
            
        # This is for screen wrapping on top and bottom
        if self.center.y > SCREEN_HEIGHT:
            self.center.y -= SCREEN_HEIGHT
        if self.center.y < 0:
            self.center.y  += SCREEN_HEIGHT    
            
    def is_alive(self):
        return self.alive
    
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture, self.angle, 255)

class Asteroid(FlyingObject):
    def __init__(self, img):
        super().__init__(img)
        self.radius = 0
 
    def Spin(self, spin):
        # Make the asteroid spin
        self.spin = spin
        self.angle += self.spin
        
    def draw(self):
        arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture, self.angle, 255)
        if not self.alive:
            self.img = "images/explode.jpg"
            self.texture = arcade.load_texture(self.img)
            self.width = self.texture.width
            self.height = self.texture.height
            arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture, self.angle, 255)
class SmallAsteroid(Asteroid):
    def __init__(self):
        super().__init__("images/meteorGrey_small1.png")
        self.radius = SMALL_ROCK_RADIUS
        self.spin = SMALL_ROCK_SPIN
        self.speed = SMALL_ROCK_SPEED
        self.center.x = random.randint(1, 50)
        self.center.y = random.randint(1, 150)
        self.direction = random.randint(1, 50)
        self.velocity.dx = math.cos(math.radians(self.direction)) * self.speed
        self.velocity.dy = math.cos(math.radians(self.direction)) * self.speed
        
    def break_apart(self, asteroids):
        self.alive = False
        
class MediumAsteroid(Asteroid):
    def __init__(self):
        super().__init__("images/meteorGrey_med1.png")
        self.radius = MEDIUM_ROCK_RADIUS
        self.speed = MEDIUM_ROCK_SPEED
        self.center.x = random.randint(1, 50)
        self.center.y = random.randint(1, 150)
        self.direction = random.randint(1, 50)
        self.velocity.dx = math.cos(math.radians(self.direction)) * self.speed
        self.velocity.dy = math.cos(math.radians(self.direction)) * self.speed
        self.spin = MEDIUM_ROCK_SPIN
    
    def break_apart(self, asteroids):           
         
        # Create a small asteroid
        sma_ast1 = SmallAsteroid()
        sma_ast1.center.x = self.center.x
        sma_ast1.center.y = self.center.y
        sma_ast1.velocity.dy =  self.velocity.dy + 1.5
        sma_ast1.velocity.dx =  self.velocity.dx + 1.5
        
        # Create a second small asteroid
        sma_ast2 = SmallAsteroid()
        sma_ast2.center.x = self.center.x
        sma_ast2.center.y = self.center.y
        sma_ast1.velocity.dy =  self.velocity.dy - 1.5
        sma_ast1.velocity.dx =  self.velocity.dx - 1.5
         
        # Add the small asteroids to the ist of Asteroids
        asteroids.append(sma_ast1)
        asteroids.append(sma_ast2)
        self.alive = False        
        
class LargeAsteroid(Asteroid):
    def __init__(self):
        super().__init__("images/meteorGrey_big1.png")
        
        self.radius = BIG_ROCK_RADIUS
        self.center.x = random.randint(1, 50)
        self.center.y = random.randint(1, 150)
        self.direction = random.randint(1, 50)
        self.speed = BIG_ROCK_SPEED
        self.velocity.dx = math.cos(math.radians(self.direction)) * self.speed
        self.velocity.dy = math.cos(math.radians(self.direction)) * self.speed
        self.spin = BIG_ROCK_SPIN
    
        
    def break_apart(self, asteroids):
        
        #create a medium asteroid
        med_ast1 = MediumAsteroid()
        med_ast1.center.x = self.center.x
        med_ast1.center.y = self.center.y
        med_ast1.velocity.dy = self.velocity.dy + 2
         
        # Create a second medium asteroid
        med_ast2 = MediumAsteroid()
        med_ast2.center.x = self.center.x
        med_ast2.center.y = self.center.y
        med_ast2.velocity.dy = self.velocity.dy - 2
         
        # Create a small asteroid
        sma_ast = SmallAsteroid()
        sma_ast.center.x = self.center.x
        sma_ast.center.y = self.center.y
        sma_ast.velocity.dx = self.velocity.dx + 5
         
        # Add the asteroids being created to the list of asteroids
        asteroids.append(med_ast1)
        asteroids.append(med_ast2)
        asteroids.append(sma_ast)
        self.alive = False                 