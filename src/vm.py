import pygame
import src.chip8 as chip8

class VM:
  """Virtual machine."""

  SCREEN_WIDTH = 1280
  SCREEN_HEIGHT = 640

  def __init__(self):
    pygame.init()
    pygame.display.set_caption("CHIP-8")
    self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
    self.platform = chip8.Chip8()
    self.clock = pygame.time.Clock()
    self.running = True


  def load_rom(self, rom_path):
    """Loads ROM."""
    self.platform.load_rom(rom_path)


  def load_display(self):
    """Loads display from platform."""

    pixel_height_count = self.platform.DISPLAY_HEIGHT
    pixel_width_count = self.platform.DISPLAY_WIDTH
    pixel_height = self.SCREEN_HEIGHT / pixel_height_count
    pixel_width = self.SCREEN_WIDTH / pixel_width_count
    self.screen.fill("black")
    test = True
    for y in range(pixel_height_count):
      for x in range(pixel_width_count):
        is_visible_pixel = self.platform.display[y * pixel_width_count + x]
        if (is_visible_pixel):
          rect = pygame.Rect(x * pixel_width, y * pixel_height, pixel_width, pixel_height)
          pygame.draw.rect(self.screen, "white", rect) # Change the color to variable.
    pygame.display.flip()


  def get_key(self):
    """Get pressed key and pass it to platform."""

    key = pygame.key.get_pressed()
    if key[pygame.K_1]:
      self.platform.key = 0x1
    elif key[pygame.K_2]:
      self.platform.key = 0x2
    elif key[pygame.K_3]:
      self.platform.key = 0x3
    elif key[pygame.K_4]:
      self.platform.key = 0xC
    elif key[pygame.K_q]:
      self.platform.key = 0x4
    elif key[pygame.K_w]:
      self.platform.key = 0x5
    elif key[pygame.K_e]:
      self.platform.key = 0x6
    elif key[pygame.K_r]:
      self.platform.key = 0xD
    elif key[pygame.K_a]:
      self.platform.key = 0x7
    elif key[pygame.K_s]:
      self.platform.key = 0x8
    elif key[pygame.K_d]:
      self.platform.key = 0x9
    elif key[pygame.K_f]:
      self.platform.key = 0xE
    elif key[pygame.K_z]:
      self.platform.key = 0xA
    elif key[pygame.K_x]:
      self.platform.key = 0x0
    elif key[pygame.K_c]:
      self.platform.key = 0xB
    elif key[pygame.K_v]:
      self.platform.key = 0xF
    else:
      self.platform.key = None


  def run(self):
    """Run virtual machine."""
    
    while (self.running):
      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              self.running = False
      self.get_key()
      self.platform.exec()
      self.load_display()
    pygame.quit()