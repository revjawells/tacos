import pygame
import random

WIDTH = 800
HEIGHT = 600

SPAWNTIME = 500

pygame.init()

pygame.display.set_caption("It's raining tacos!")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.image.load("bg.png")
song = pygame.mixer.Sound("rainingtacos.ogg")

class Thing:
	def __init__(self, sprite, x, y, dx=0, dy=0, hidden=False, paused=False):
		self.sprite = pygame.image.load(sprite)
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy
		self.hidden = hidden
		self.paused = paused

	def update(self):
		if not self.paused:
			self.x += self.dx
			self.y += self.dy
	
	def draw(self, surface):
		if not self.hidden:
			screen.blit(self.sprite, (self.x, self.y))

	def iscollision(self, thing):
		if self.hidden or thing.hidden:
			return False

		r = self.sprite.get_rect()
		r.x = self.x
		r.y = self.y

		s = thing.sprite.get_rect()
		s.x = thing.x
		s.y = thing.y

		return r.colliderect(s)

	def isinbounds(self):
		return self.x >= 0 and self.x < WIDTH and self.y >= 0 and self.y < HEIGHT

over = False

def draw_text(surface, text):
	font = pygame.font.SysFont("sans", 30, True)
	label = font.render(text, 1, pygame.Color("white"))
	surface.blit(label, (15, 15))

taco = Thing("taco.png", WIDTH / 2, (HEIGHT / 2) + 90)

sprites = [taco]
bank = ["lettuce.png", "cheese.png", "meat.png", "sourcream.png"]

tick = 0
score = 0
song.play(-1)

while not over:
	screen.blit(bg, (0, 0))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			over = True

	(x, y) = pygame.mouse.get_pos()
	taco.x = x

	newtick = pygame.time.get_ticks()
	if (newtick - tick) > SPAWNTIME:
		# Generate a new sprite
		sprite = Thing(random.choice(bank),
				random.randint(150, WIDTH - 150), 0,
				random.randint(-1, 1) * random.randint(0, 1),
				random.randint(1, 3))
		sprites.append(sprite)
		tick = newtick
	
	for sprite in sprites:
		sprite.update()
		sprite.draw(screen)

	for sprite in sprites[1:]:
		if sprite != taco and not sprite.isinbounds():
			sprites.remove(sprite)
			score = score - 1

		if taco.iscollision(sprite):
			sprites.remove(sprite)
			score = score + 1

	draw_text(screen, "Score: " + str(score))
	pygame.display.update()
