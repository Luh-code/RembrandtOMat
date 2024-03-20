def evaluate_command(command):
  # Split up command
  parts = command[1:].split(' ')
  if len(parts) == 0:
    return;

  # Get correct method for command
  commands = {
    "test": "test_command"
  }

  command_name = commands.get(parts[0])

  if command_name == None:
    print('Command not found')
    return;

  commands_instance = Commands()
  command_method = getattr(commands_instance, command_name, None)

  # Call method or complain
  if command_method:
    command_method()
  else:
    print('Command method not found')

class Commands:
  def test_command(command):
    print('test')
