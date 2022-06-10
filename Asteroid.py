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

class Bullet(FlyingObject):
    def __init__(self, ship_ang, ship_x, ship_y):
        super().__init__("images/laserBlue01.png")
        self.angle = ship_ang
        self.center.x = ship_x
        self.center.y = ship_y
        self.radius = BULLET_RADIUS
        self.alive = BULLET_LIFE
        self.speed =  BULLET_SPEED
       
        
    def fire(self, ship_dx, ship_dy):
        self.velocity.dx -= ship_dx + math.sin(math.radians(self.angle)) * BULLET_SPEED
        self.velocity.dy += ship_dy + math.cos(math.radians(self.angle)) * BULLET_SPEED
         
    def advance(self):
        super().advance()
        self.alive -= 1
        if (self.alive <= 0):
            self.alive = False
            
class Ship(FlyingObject):
    def __init__(self):
        super().__init__("images/playerShip1_orange.png")
        self.angle = 1
        self.center.x =(SCREEN_WIDTH/2)
        self.center.y = (SCREEN_HEIGHT/2)
        self.radius = SHIP_RADIUS
        
    def draw(self):
        if (self.alive):
              
            arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture, self.angle, 255)
        if not self.alive:
            

            
            # Draw the damaged ship
            img = "images/damaged_ship2.png"
            self.texture = arcade.load_texture(img)
            arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture, self.angle, 255)
            self.center.x =(SCREEN_WIDTH/2)
            self.center.y = (SCREEN_HEIGHT/2)
            self.velocity.dx = 0
            self.velocity.dy = 0
#             self.img = "images/ship_explode.jpeg"
#             self.texture = arcade.load_texture(self.img)
#             self.width = self.texture.width
#             self.height = self.texture.height
#             arcade.draw_texture_rectangle(self.center.x, self.center.y, self.width, self.height, self.texture, self.angle, 60)
            
            # Draw Game over at the top of the screen
            img = "images/gameover.jpeg"
            texture = arcade.load_texture(img)
            arcade.draw_texture_rectangle(SCREEN_WIDTH - 400, SCREEN_HEIGHT - 70, 400, 200, texture, 0, 255)
            
            #draw a message on the screen
            img2 = "images/broken_ship_message.png"
            texture2 = arcade.load_texture(img2)
            arcade.draw_texture_rectangle(SCREEN_WIDTH - 400, SCREEN_HEIGHT - 200, 400, 100, texture2, 0, 255)
            
            # Draw Play Again at the botton of the screen
            img3 = "images/play_again.png"
            texture3 = arcade.load_texture(img3)
            arcade.draw_texture_rectangle(SCREEN_WIDTH - 400, SCREEN_HEIGHT - 500, 400, 200, texture3, 0, 255)
            arcade.finish_render()        
    
            
    def rotate_right(self):
        # Make the Ship rotate to the right direction 
        self.angle -= SHIP_TURN_AMOUNT
        
    def rotate_left(self):
        # Make the Ship rotate to the left direction 
        self.angle += SHIP_TURN_AMOUNT    
           
    def thrust_forward(self):
        # Thrust the ship forward
        self.velocity.dx -= math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.velocity.dy += math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT

    def thrust_backward(self):
        # Thrust the ship backward
        self.velocity.dx += math.sin(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
        self.velocity.dy -= math.cos(math.radians(self.angle)) * SHIP_THRUST_AMOUNT
class Game(arcade.Window):
    """
    This class handles all the game callbacks and interaction
    This class will then call the appropriate functions of
    each of the above classes.
    You are welcome to modify anything in this class.
    """

    def __init__(self, width, height):
        """
        Sets up the initial conditions of the game
        :param width: Screen width
        :param height: Screen height
        """
        super().__init__(width, height)
        arcade.set_background_color(arcade.color.SMOKY_BLACK)
        self.score = 0

        self.held_keys = set()

        # TODO: declare anything here you need the game class to track
        self.bullets = []
         
        
        self.ship = Ship()
        self.asteroids = []
        
        # Begin the Game with a number of Asteroids
        #INITIAL_ROCK_COUNT: for easy mode
        #INTERMEDIATE_LEVEL_ROCK_COUNT: for Intermediate mode
        #HARD_LEVEL_ROCK_COUNT: for HARD mode
        for i in range(INITIAL_ROCK_COUNT):
            big = LargeAsteroid()
            self.asteroids.append(big)
   
        # Game sound effect
        self.bullet_sound = arcade.load_sound("sound/bullet.wav")
        self.asteroid_sound = arcade.load_sound("sound/asteroid.wav")
        self.ship_sound = arcade.load_sound("sound/ship.wav")
        self.game_over_sound = arcade.load_sound("sound/game_over.wav")
        self.congrats_sound = arcade.load_sound("sound/congratulations.wav")
        self.ship_rotation_sound = arcade.load_sound("sound/rotation.wav")
       
        
        
        

            
        
    def on_draw(self):
        """
        Called automatically by the arcade framework.
        Handles the responsibility of drawing all elements.
        """

        # clear the screen to begin drawing
        arcade.start_render()
        

        # TODO: draw each object
        self.ship.draw()
        for asteroid in self.asteroids:
            asteroid.draw()
            

        if self.asteroids == []:
            # Draw Congratulations at the top of the screen
            img = "images/congratulations.png"
            texture = arcade.load_texture(img)
            arcade.draw_texture_rectangle(SCREEN_WIDTH /2, SCREEN_HEIGHT /2, SCREEN_WIDTH - 150, SCREEN_WIDTH - 150, texture, 0, 255)
            arcade.finish_render()
            
            
        for bullet in self.bullets:
            bullet.draw()
            
        self.check_collisions()
        self.draw_score()
        
    def draw_score(self):
        """
        Puts the current score on the screen
        """
        score_text = "Score: {}".format(self.score)
        start_x = 10
        start_y = SCREEN_HEIGHT - 20
        arcade.draw_text(score_text, start_x=start_x, start_y=start_y, font_size=15, color=arcade.color.WHITE)
       
                   
    def remove_dead_bullets(self):
        
        """ Revemove all bullet that is dead"""
        for bullet in self.bullets:
            if (not bullet.alive):
                self.bullets.remove(bullet)
    
    def remove_dead_asteroids(self):
        """ Remove all asteroids that are dead"""
        
        for asteroid in self.asteroids:
            if (not asteroid.alive):
                
                self.asteroids.remove(asteroid)
                if self.asteroids == []:
                    arcade.play_sound(self.congrats_sound)
                    arcade.play_sound(self.congrats_sound)
                
    def check_collisions(self):
        """
        Checks to see if there is an asteroid and bullet colision,
        and asteroid and ship colison
        :return:
        """
        
        for asteroid in self.asteroids:
            for bullet in self.bullets:
                if ((bullet.alive) and (asteroid.alive)):
                    distance_x = abs(asteroid.center.x - bullet.center.x)
                    distance_y = abs(asteroid.center.y - bullet.center.y)
                    max_distance = asteroid.radius + bullet.radius
                    if ((distance_x < max_distance) and (distance_y < max_distance)):
                        
                        """We have an asteroid and a bullet collision!!"""
                        
                        bullet.alive = False
                        asteroid.break_apart(self.asteroids)
                        self.score += SCORE_HIT
                        #Play an asteroid explosion sound
                        arcade.play_sound(self.asteroid_sound)
                        asteroid.draw()
                            
                       
                        
            if ((asteroid.alive) and (self.ship.alive)):
                distance_x = abs(asteroid.center.x - self.ship.center.x)
                distance_y = abs(asteroid.center.y - self.ship.center.y)
                max_distance = asteroid.radius + self.ship.radius
                if ((distance_x < max_distance) and (distance_y < max_distance)):
                    
                    """We have an asteroid and the ship collision!!"""
                    

                    self.ship.alive = False
                    self.score = 0
                    # Play the Ship explosion sound
                    arcade.play_sound(self.ship_sound)
                    # Play a game-over sound
                    arcade.play_sound(self.game_over_sound)
                    
        
                    
    
        
    def update(self, delta_time):
        """
        Update each object in the game.
        :param delta_time: tells us how much time has actually elapsed
        """
        self.check_keys()

        # TODO: Tell everything to advance or move forward one step in time
        for asteroid in self.asteroids:
            asteroid.advance()
            asteroid.Spin(asteroid.spin)
            
        for bullet in self.bullets:
            bullet.advance()
            
            
        self.remove_dead_bullets()
        self.remove_dead_asteroids()
        self.ship.advance()
        
        
        # TODO: Check for collisions
        self.check_collisions()
        
                    
                    
    def check_keys(self):
        """
        This function checks for keys that are being held down.
        You will need to put your own method calls in here.
        """
        if arcade.key.LEFT in self.held_keys:
            self.ship.rotate_left()

        if arcade.key.RIGHT in self.held_keys:
            self.ship.rotate_right()

        if arcade.key.UP in self.held_keys:
            self.ship.thrust_forward()

        if arcade.key.DOWN in self.held_keys:
            self.ship.thrust_backward()

        # Machine gun mode...
        #if arcade.key.SPACE in self.held_keys:
        #    pass


    def on_key_press(self, key: int, modifiers: int):
        """
        Puts the current key in the set of keys that are being held.
        You will need to add things here to handle firing the bullet.
        """
        if self.ship.alive:
            self.held_keys.add(key)

            if key == arcade.key.SPACE:
                # TODO: Fire the bullet here!
                bullet = Bullet(self.ship.angle, self.ship.center.x, self.ship.center.y)
                self.bullets.append(bullet)
                bullet.fire(self.ship.velocity.dx, self.ship.velocity.dy)
                #Make a bullet sound
                arcade.play_sound(self.bullet_sound)
              
                    
                

    def on_key_release(self, key: int, modifiers: int):
        """
        Removes the current key from the set of held keys.
        """
        if key in self.held_keys:
            self.held_keys.remove(key)


# Creates the game and starts it going
window = Game(SCREEN_WIDTH, SCREEN_HEIGHT)
arcade.run()   