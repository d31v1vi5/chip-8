import click
import src.vm as vm

@click.command()
@click.argument("rom")
def emulator(rom):
  print("Emulator launched.")
  virtual_machine = vm.VM()
  virtual_machine.load_rom(rom)
  virtual_machine.run()