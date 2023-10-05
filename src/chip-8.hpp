#include <cstdint>


class Chip8 {
private:
  std::uint8_t registers[16] = {};
  std::uint8_t memory[4096] = {};
  std::uint16_t index = 0;
  std::uint16_t pc = 0;
  std::uint16_t stack[16] = {};
  std::uint8_t sp = 0;
  // Perhaps change display height and width for constants.
  std::uint32_t display[64 * 32] = {};

public:

  const unsigned int START_ADDRESS = 0x200;

  Chip8() {
    // Should move to initializer list.
    pc = START_ADDRESS;
    // Should initialize fonts.
    // Needs a random number generator.
  }

  // Perhaps change the filename type to string
  void load_rom(char const* filename);

  // Jump to a machine code routine at nnn.
  // Note: Ignored by modern interpreters.
  void op_0nnn();

  // Clear the display.
  void op_00E0();

  // Return from a subroutine.
  void op_00EE();

  // Jump to location nnn.
  void op_1nnn();

  // Call subroutine at nnn.
  void op_2nnn();

  // Skip next instruction if Vx == kk.
  void op_3xkk();

  // Skip next instruction if Vx != kk.
  void op_4xkk();

  // Skip next instruction if Vc == Vy.
  void op_5xy0();

  // Set Vx = kk.
  void op_6xkk();

  // Set Vx = Vx + kk.
  void op_7xkk();

  // Set Vx = Vy.
  void op_8xy0();

  // Set Vx = Vx OR Vy.
  void op_8xy1();

  // Set Vx = Vx AND Vy.
  void op_8xy2();

  // Set Vx = Vx XOR Vy.
  void op_8xy3();

  // Set Vx = Vx + Vy, set VF = carry.
  void op_8xy4();

  // Set Vx = Vx - Vy, set VF = NOT borrow.
  void op_8xy5();

  // Set Vx = Vx SHR 1.
  void op_8xy6();

  // Set Vx = Vy - Vx, set VF = NOT borrow.
  void op_8xy7();

  // Set Vx = Vx SHL 1.
  void op_8xyE();

  // Skep next instruction if Vx != Vy.
  void op_9xy0();

  // Set I = nnn;
  void op_Annn();

  // Jump to location nnn + V0.
  void op_Bnnn();

  // Set Vx = random byte AND kk.
  void op_Cxkk();

  // Display n-byte sprite starting at memory location I at (Vx, Vy), set VF = collision.
  void op_Dxyn();

  // Skip next instruction if key with the value of Vx is pressed.
  void op_Ex9E();

  // Set Vx = delay timer value.
  void op_Fx07();

  // Wait for a key press, store the value of the key in Vx.
  void op_Fx0A();

  // Set delay timer = Vx.
  void op_Fx15();

  // Set sound timer = Vx.
  void op_Fx18();

  // Set I = I + Vx.
  void op_Fx1E();

  // Set I = location of sprite for digit Vx.
  void op_Fx29();

  // Store BCD representation of Vx in memory locations I, I+1 and I+2.
  void op_Fx33();

  // Store registers V0 through Vx in memory starting at location I.
  void op_Fx55();

  // Read registers V0 through Vx from memory starting at location I.
  void op_Fx65();

};