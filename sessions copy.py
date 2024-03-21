sessions = []
teams = {}

class Session:
  def __init__(self):
    self.teams = 0
  
  async def register_team(self, channel):
    self.teams+=1
    teams.update({channel.id: Team(channel=channel, session=self)})
  
  async def remove_team(self):
    self.teams-=1
  
  async def is_empty(self):
    return self.teams == 0

class Team:
  def __init__(self, channel, session):
    self.channel = channel
    self.session = session

async def register_session():
  session = Session()
  sessions.append(session)
  return session

async def check_team(channel):
  return channel.id in teams

async def remove_team(channel):
  if not await check_team(channel):
    print('removing team')
    session = teams.pop(channel.id)
    await session.remove_team()
    if await session.is_empty():
      sessions.pop(session)
    print('deleting channel')
    channel.delete()
    print('deleted channel')

