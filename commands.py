import math

import random


import sessions

class Command:
  def __init__(self, message):
    self.message = message
    # Split up command
    parts = message.content[1:].split(' ')
    if len(parts) == 0:
      return;
    self.parts = parts

async def evaluate_command(message):
  command = Command(message=message)
  if not command:
    print('Command not complete')
    return

  # Get correct method for command
  commands = {
    "test": "test_command",
    "split": "split_command"
  }

  command_name = commands.get(command.parts[0])

  if command_name == None:
    print('Command not found')
    return;

  commands_instance = Commands()
  command_method = getattr(commands_instance, command_name, None)

  # Call method or complain
  if command_method:
    await command_method(command)
  else:
    print('Command method not found')

async def is_long_enough(command, arg_count, expected=None):
  if len(command.parts) >= arg_count:
    return True
  if expected:
    await command.message.channel.send(f'Command not valid! Expected: "{expected}"')
  return False

class Commands:
  async def test_command(self, command):
    print('test')
  
  async def split_command(self, command):
    if not await is_long_enough(command, 4, '$split [me/#channel] [how many] teams/ppl'):
      return;

    # Determine target
    raw_target=command.parts[1]
    #print(f'raw_target: "{raw_target}"')
    #print(f'author.id: "{command.message.author.id}"')

    user_target = None
    channel_target = None

    # Set user_target or channel_targer
    if raw_target.startswith('<@') and raw_target.endswith('>'):
      user_target = int(raw_target[2:-1])
    elif raw_target.startswith('<#') and raw_target.endswith('>'):
      channel_target = int(raw_target[2:-1])
    elif raw_target == 'me':
      user_target = command.message.author.id
    else:
      await command.message.channel.send(f'Target "{raw_target}" it not recognized.\nUse @ for users or # for channels or "me" to target yourself.')
      return
    
    # Set channel_target based on user_target
    if not channel_target:
      user = command.message.guild.get_member(user_target)
      if user:
        channel = user.voice.channel
        if channel:
          channel_target = channel.id

    # Print out target information and retun if channel_target has not been determined
    if user_target:
      await command.message.channel.send(f'Target is User {user_target}')
      if not channel_target:
        await command.message.channel.send(f'**ERROR: User {user_target} is not currently in a channel**')
        return
    await command.message.channel.send(f'Target is Channel {channel_target}')

    # Determine channel
    channel = command.message.guild.get_channel(channel_target)
    if not channel:
      command.message.channel.send(f'**INTERNAL ERROR: {channel_target} is not associated with any channel**')
    
    # Calculate number of required groups/number of people per group
    team_count = None
    user_per_team = None

    count = int(command.parts[2])
    specifier = command.parts[3].lower()

    # Read the count in regard to the given specifier
    if specifier == 'teams':
      team_count = count
    elif specifier == 'ppl':
      user_per_team = count
    else:
      await command.message.channel.send(f'The count specifier has to either be "teams" or "ppl"(people per team) but is "{specifier}"')
      return
    
    # Get Channel members and their count
    channel_population = channel.members
    channel_population_count = len(channel_population)

    # Create the missing value
    if not team_count:
      team_count = math.ceil(channel_population_count/user_per_team)
    if not user_per_team:
      user_per_team = math.ceil(channel_population_count/team_count)
    
    await command.message.channel.send(f'Creating {team_count} groups of {user_per_team} people each')

    # Create the session
    session = await sessions.register_session()

    # Create the channels
    channel_name = channel.name
    for i in range(team_count):
      team = await command.message.guild.create_voice_channel(f'{channel_name}-group-{i}')
      await session.register_team(team)
      for j in range(user_per_team):
        if len(channel_population) == 0:
          break
        user = random.choice(channel_population)
        channel_population.remove(user)
        await user.move_to(team)


    