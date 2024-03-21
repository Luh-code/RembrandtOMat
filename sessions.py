class Session:
  def __init__(self):
    self.teams = 0
  
  async def register_team(self, channel):
    team = channel
    self.teams+=1
    teams.update({team: self})
  
  async def remove_team(self):
    self.teams-=1
  
  async def is_empty(self):
    return self.teams == 0

sessions:Session = []
teams = {}

async def register_session():
  session = Session()
  sessions.append(session)
  return session

async def check_team(channel):
  return channel in teams

async def remove_team(channel):
  #print('remove team')
  if not await check_team(channel):
    return
  #print('removing team')
  session = teams.pop(channel)
  await session.remove_team()
  if await session.is_empty():
    sessions.remove(session)
  await channel.delete()
  #print('deleted team')

