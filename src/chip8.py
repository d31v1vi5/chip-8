import random

def get_bytes(opcode):
  """Parses opcode into bytes."""
  
  byte_1 = (opcode & 0xF000) >> 12
  byte_2 = (opcode & 0x0F00) >> 8
  byte_3 = (opcode & 0x00F0) >> 4
  byte_4 = opcode & 0x000F
  return [byte_1, byte_2, byte_3, byte_4]


def get_nnn(bytes):
  """Returns NNN from bytes."""

  nnn = (bytes[1] << 8) | (bytes[2] << 4) | bytes[3]
  return nnn


def get_kk(bytes):
  """Returns KK from bytes."""

  kk = (bytes[2] << 4) | bytes[3]
  return kk


class Chip8:
  """CHIP8 interpreter."""
  
  REGISTERS_SIZE = 16 
  MEMORY_SIZE = 4096
  STACK_SIZE = 16
  DISPLAY_WIDTH = 64
  DISPLAY_HEIGHT = 32
  START_ADDRESS = 0x200
  FONT_START_ADDRESS = 0x50

  def __init__(self):
    self.registers = [0] * self.REGISTERS_SIZE
    self.memory = [0] * self.MEMORY_SIZE
    self.stack = [0] * self.STACK_SIZE
    self.display = [False] * self.DISPLAY_WIDTH * self.DISPLAY_HEIGHT

    self.index = 0
    self.program_counter = self.START_ADDRESS
    self.stack_pointer = 0

    self.delay_timer = 0
    self.sound_timer = 0
    self.key = 0
    self.init_font()

  def init_font(self):
    """Initializes fonts."""

    font = [
      0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
      0x20, 0x60, 0x20, 0x20, 0x70, # 1
      0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
      0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
      0x90, 0x90, 0xF0, 0x10, 0x10, # 4
      0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
      0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
      0xF0, 0x10, 0x20, 0x40, 0x40, # 7
      0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
      0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
      0xF0, 0x90, 0xF0, 0x90, 0x90, # A
      0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
      0xF0, 0x80, 0x80, 0x80, 0xF0, # C
      0xE0, 0x90, 0x90, 0x90, 0xE0, # D
      0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
      0xF0, 0x80, 0xF0, 0x80, 0x80  # F
    ]
    for index, value in enumerate(font):
      self.memory[self.FONT_START_ADDRESS + index] = value


  def load_rom(self, rom_path):
    """Loads ROM into memory."""

    START_ADDRESS = 0x200
    with open(rom_path, "rb") as rom:
      rom_data = rom.read()
      for index, value in enumerate(rom_data):
        self.memory[START_ADDRESS + index] = value


  def exec(self):
    """Execute a single instruction."""

    opcode = self.get_opcode()
    bytes = get_bytes(opcode)
    if self.delay_timer > 0:
      self.delay_timer -= 1
    match bytes:
      case [0x0, 0x0, 0xE, 0x0]:
        self.op_00E0()
      case [0x0, 0x0, 0xE, 0xE]:
        self.op_00EE()
      case [0x0, _, _, _]:
        nnn = get_nnn(bytes)
        self.op_0nnn(nnn)
      case [0x1, _, _, _]:
        nnn = get_nnn(bytes)
        self.op_1nnn(nnn)
      case [0x2, _, _, _]:
        nnn = get_nnn(bytes)
        self.op_2nnn(nnn) 
      case [0x3, x, _, _]:
        kk = get_kk(bytes)
        self.op_3xkk(x, kk)
      case [0x4, x, _, _]:
        kk = get_kk(bytes)
        self.op_4xkk(x, kk)
      case [0x5, x, y, 0x0]:
        self.op_5xy0(x, y)
      case [0x6, x, _, _]:
        kk = get_kk(bytes)
        self.op_6xkk(x, kk)
      case [0x7, x, _, _]:
        kk = get_kk(bytes)
        self.op_7xkk(x, kk)
      case [0x8, x, y, 0x0]:
        self.op_8xy0(x, y)
      case [0x8, x, y, 0x1]:
        self.op_8xy1(x, y)
      case [0x8, x, y, 0x2]:
        self.op_8xy2(x, y)
      case [0x8, x, y, 0x3]:
        self.op_8xy3(x, y)
      case [0x8, x, y, 0x4]:
        self.op_8xy4(x, y)
      case [0x8, x, y, 0x5]:
        self.op_8xy5(x, y)
      case [0x8, x, y, 0x6]:
        self.op_8xy6(x, y)
      case [0x8, x, y, 0x7]:
        self.op_8xy7(x, y)
      case [0x8, x, y, 0xE]:
        self.op_8xyE(x, y)
      case [0x9, x, y, 0x0]:
        self.op_9xy0(x, y)
      case [0xA, _, _, _]:
        nnn = get_nnn(bytes)
        self.op_Annn(nnn)
      case [0xB, _, _, _]:
        nnn = get_nnn(bytes)
        self.op_Bnnn(nnn)
      case [0xC, x, _, _]:
        kk = get_kk(bytes)
        self.op_Cxkk(x, kk)
      case [0xD, x, y, n]:
        self.op_Dxyn(x, y, n)
      case [0xE, x, 0x9, 0xE]:
        self.op_Ex9E(x)
      case [0xE, x, 0xA, 0x1]:
        self.op_ExA1(x)
      case [0xF, x, 0x0, 0x7]:
        self.op_Fx07(x)  
      case [0xF, x, 0x0, 0xA]:
        self.op_Fx0A(x)
      case [0xF, x, 0x1, 0x5]:
        self.op_Fx15(x)
      case [0xF, x, 0x1, 0x8]:
        self.op_Fx18(x)
      case [0xF, x, 0x1, 0xE]:
        self.op_Fx1E(x)
      case [0xF, x, 0x2, 0x9]:
        self.op_Fx29(x)
      case [0xF, x, 0x3, 0x3]:
        self.op_Fx33(x)
      case [0xF, x, 0x5, 0x5]:
        self.op_Fx55(x)
      case [0xF, x, 0x6, 0x5]:
        self.op_Fx65(x)  

  def get_opcode(self):
    opcode = self.memory[self.program_counter] << 8 | self.memory[self.program_counter + 1]
    self.program_counter += 2
    return opcode


  def op_0nnn(self, nnn):
    """Jump to a machine code routine at nnn."""
    pass


  def op_00E0(self):
    """Clear the display."""
    
    self.display = [False] * self.DISPLAY_WIDTH * self.DISPLAY_HEIGHT


  def op_00EE(self):
    """Return from a subroutine."""

    self.stack_pointer -= 1
    self.program_counter = self.stack[self.stack_pointer]


  def op_1nnn(self, nnn):
    """Jump to a location nnn."""
    
    self.program_counter = nnn


  def op_2nnn(self, nnn):
    """Call subroutine at nnn."""
    
    self.stack[self.stack_pointer] = self.program_counter
    self.stack_pointer += 1
    self.program_counter = nnn


  def op_3xkk(self, x, kk):
    """Skip next instruction if Vx = kk."""
    
    if self.registers[x] == kk:
      self.program_counter += 2


  def op_4xkk(self, x, kk):
    """Skip next instruction if Vx != kk."""
    
    if self.registers[x] != kk:
      self.program_counter += 2


  def op_5xy0(self, x, y):
    """Skip next instruction if Vx = Vy."""
    
    if self.registers[x] == self.registers[y]:
      self.program_counter += 2


  def op_6xkk(self, x, kk):
    """Set Vx = kk."""
    
    self.registers[x] = kk


  def op_7xkk(self, x, kk):
    """Set Vx = Vx + kk."""
    
    self.registers[x] = (self.registers[x] + kk) & 0xFF


  def op_8xy0(self, x, y):
    """Set Vx = Vy."""
    
    self.registers[x] = self.registers[y]


  def op_8xy1(self, x, y):
    """Set Vx = Vx OR Vy."""
    
    self.registers[x] |= self.registers[y]


  def op_8xy2(self, x, y):
    """Set Vx = Vx AND Vy."""
    
    self.registers[x] &= self.registers[y]


  def op_8xy3(self, x, y):
    """Set Vx = Vx XOR Vy."""
    
    self.registers[x] ^= self.registers[y]


  def op_8xy4(self, x, y):
    """Set Vx = Vx + Vy, set VF = carry."""
    
    sum = self.registers[x] + self.registers[y]
    self.registers[x] = sum & 0xFF
    self.registers[0xF] = (sum & 0x100) >> 8


  def op_8xy5(self, x, y):
    """Set Vx = Vx - Vy, set VF = NOT borrow."""
    
    if (self.registers[x] > self.registers[y]):
      self.registers[x] -= self.registers[y]
      self.registers[0xF] = 1
    else:
      self.registers[x] = 0x100 + self.registers[x] - self.registers[y]
    


  def op_8xy6(self, x, y):
    """Set Vx = Vx SHR 1."""
    
    self.registers[0xF] = self.registers[x] & 0x1
    self.registers[x] >>= 1


  def op_8xy7(self, x, y):
    """Set Vx = Vy - Vx, set VF = NOT borrow."""
    
    if (self.registers[x] < self.registers[y]):
      self.registers[x] = self.registers[y] - self.registers[x]
      self.registers[0xF] = 1
    else:
      self.registers[x] = 0x100 + self.registers[y] - self.registers[x]


  def op_8xyE(self, x, y):
    """Set Vx = Vx SHL 1."""
    
    self.registers[0xF] = (self.registers[x] & 0x80) >> 7
    self.registers[x] = (self.registers[x] << 1) % 0x100


  def op_9xy0(self, x, y):
    """Skip next instruction if VX != Vy."""
    
    if(self.registers[x] != self.registers[x]):
      self.program_counter += 2


  def op_Annn(self, nnn):
    """Set I = nnn."""
    
    self.index = nnn


  def op_Bnnn(self, nnn):
    """Jump to location nnn + V0."""
    
    self.program_counter = self.registers[0] + nnn


  def op_Cxkk(self, x, kk):
    """Set Vx = random byte AND kk."""
    
    random_byte = random.randint(0x0, 0xFF)
    self.registers[x] = random_byte & kk


  def op_Dxyn(self, x, y, n):
    """Display n-byte sprite starting at memory location I at (Vx, Vy) set VF = collision."""

    x_pos = self.registers[x] % self.DISPLAY_WIDTH
    y_pos = self.registers[y] % self.DISPLAY_HEIGHT

    self.registers[0xF] = 0x0
    for row in range(0x0, n):
      sprite_byte = self.memory[self.index + row]
      for col in range(0x0, 0x8):
        sprite_pixel = sprite_byte & (0x80 >> col)
        display_pixel_pos = (y_pos + row) % self.DISPLAY_HEIGHT * self.DISPLAY_WIDTH + (x_pos + col) % self.DISPLAY_WIDTH
        if sprite_pixel:
          if self.display[display_pixel_pos]:
            self.registers[0xF] = 0x1
          self.display[display_pixel_pos] ^= True


  def op_Ex9E(self, x):
    """Skip next instruction if the key with the value of Vx is pressed."""

    if self.key == self.registers[x]:
      self.program_counter += 2


  def op_ExA1(self, x):
    """Skip next instruction if the key with the value of Vx is not pressed."""

    if self.key != self.registers[x]:
      self.program_counter += 2


  def op_Fx07(self, x):
    """Set Vx = delay timer value."""
    
    self.registers[x] = self.delay_timer


  def op_Fx0A(self, x):
    """Wait for a key press, store the value of the kye in Vx"""
    if self.key is None:
      self.program_counter -= 2
    else:
      self.registers[x] = self.key


  def op_Fx15(self, x):
    """Set delay timer = Vx."""
    
    self.delay_timer = self.registers[x]


  def op_Fx18(self, x):
    """Set sound timer = Vx."""
    
    self.sound_timer = self.registers[x]


  def op_Fx1E(self, x):
    """Set I = I + Vx."""
    
    self.index = (self.index + self.registers[x]) & 0xFFFF


  def op_Fx29(self, x):
    """Set I = location of sprite for digit Vx""" 
    
    self.index = self.FONT_START_ADDRESS + 5 * self.registers[x]


  def op_Fx33(self, x):
    """Store BCD representation of Vx in memory location I, I+1 and I+2."""
    
    value = self.registers[x]
    self.memory[self.index + 2] = value % 10
    value //= 10
    self.memory[self.index + 1] = value % 10
    value //= 10
    self.memory[self.index] = value


  def op_Fx55(self, x):
    """Store registers V0 through Vx in memory starting at location I."""
    
    for i in range(0, x + 1):
      self.memory[self.index + i] = self.registers[i]


  def op_Fx65(self, x):
    """Read registers V0 through Vx in memory starting at location I."""
    
    for i in range(0, x + 1):
      self.registers[i] = self.memory[self.index + i]