import discord
from discord.ext import commands
import requests
import riot_auth
import asyncio
import sys
import aioconsole
import json
from discord import app_commands



discord_api_key = "**************************************************"


BASE_URL = 'https://na1.api.riotgames.com'

intents = discord.Intents.all()


auth = riot_auth.RiotAuth()


bot = commands.Bot(command_prefix='!', intents=intents)

logged_in = False


#DISCORD API HANDLING
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
       synced = await bot.tree.sync()
       print(f"Synced {len(synced)} commands(s)")
    except Exception as e:
       print(e)

@bot.tree.command(name="login")
@app_commands.describe(username = "Riot Username")
@app_commands.describe(password = "Riot Password")
async def login(interaction: discord.Interaction, username : str, password : str):
  asyncio.run(auth.authorize(username=username,password=password))
  print(f"Access Token Type: {auth.token_type}\n")
  print(f"Access Token: {auth.access_token}\n")
  print(f"Entitlements Token: {auth.entitlements_token}\n")
  print(f"User ID: {auth.user_id}")
  global logged_in
  logged_in = True
  await interaction.response.send_message(f"Logged in!")
  

@bot.tree.command(name="shop")
async def check_shop(message: discord.Interaction):
  if(logged_in):
      vresponse = requests.get('https://valorant-api.com/v1/version')
      vresponse_data = vresponse.json()
      if 'data' in vresponse_data:
         version_data = vresponse_data['data']
         if 'riotClientVersion' in version_data:
            version = version_data['riotClientVersion']
            print(version)
      store_headers = {
         "Authorization": f'Bearer {auth.access_token}',
         "X-Riot-ClientPlatform": "ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9",
         "X-Riot-ClientVersion": version,
         "X-Riot-Entitlements-JWT": auth.entitlements_token,
         }
      try:
         ushop_response = requests.get(f'https://pd.na.a.pvp.net/store/v2/storefront/{auth.user_id}',headers=store_headers)
         ushop_response.raise_for_status()
         ushop_data = ushop_response.json()
         print(ushop_data)
         print('\n\n')
         item_id1 = ushop_data['SkinsPanelLayout']['SingleItemOffers'][0]
         item_id2 = ushop_data['SkinsPanelLayout']['SingleItemOffers'][1]
         item_id3 = ushop_data['SkinsPanelLayout']['SingleItemOffers'][2]
         item_id4 = ushop_data['SkinsPanelLayout']['SingleItemOffers'][3]
         
         skin1_response = requests.get(f'https://valorant-api.com/v1/weapons/skinlevels/{item_id1}')
         skin2_response = requests.get(f'https://valorant-api.com/v1/weapons/skinlevels/{item_id2}')
         skin3_response = requests.get(f'https://valorant-api.com/v1/weapons/skinlevels/{item_id3}')
         skin4_response = requests.get(f'https://valorant-api.com/v1/weapons/skinlevels/{item_id4}')


         skin1_response_data = skin1_response.json()
         skin2_response_data = skin2_response.json()
         skin3_response_data = skin3_response.json()
         skin4_response_data = skin4_response.json()


         skin1_item_name = skin1_response_data['data']['displayName']
         skin2_item_name = skin2_response_data['data']['displayName']
         skin3_item_name = skin3_response_data['data']['displayName']
         skin4_item_name = skin4_response_data['data']['displayName']

         skin1_item_cost = ushop_data['SkinsPanelLayout']['SingleItemStoreOffers'][0]['Cost']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']
         skin2_item_cost = ushop_data['SkinsPanelLayout']['SingleItemStoreOffers'][1]['Cost']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']
         skin3_item_cost = ushop_data['SkinsPanelLayout']['SingleItemStoreOffers'][2]['Cost']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']
         skin4_item_cost = ushop_data['SkinsPanelLayout']['SingleItemStoreOffers'][3]['Cost']['85ad13f7-3d1b-5128-9eb2-7cd8ee0b5741']

         skin1_image = skin1_response_data['data']['displayIcon']
         skin2_image = skin2_response_data['data']['displayIcon']
         skin3_image = skin3_response_data['data']['displayIcon']
         skin4_image = skin4_response_data['data']['displayIcon']

         print(skin1_item_name)
         print(f' {skin1_item_cost}\n')
         print(skin2_item_name)
         print(f' {skin2_item_cost}\n')
         print(skin3_item_name)
         print(f' {skin3_item_cost}\n')
         print(skin4_item_name)
         print(f' {skin4_item_cost}\n')
         embed1 = discord.Embed(
            colour=discord.Colour.dark_red(),
            title=skin1_item_name,
            description=skin1_item_cost
         )
         embed1.set_image(url=skin1_image)

         embed2 = discord.Embed(
            colour=discord.Colour.dark_red(),
            title=skin2_item_name,
            description=skin2_item_cost
         )
         embed2.set_image(url=skin2_image)
         embed3 = discord.Embed(
            colour=discord.Colour.dark_red(),
            title=skin3_item_name,
            description=skin3_item_cost
         )
         embed3.set_image(url=skin3_image)
         embed4 = discord.Embed(
            colour=discord.Colour.dark_red(),
            title=skin4_item_name,
            description=skin4_item_cost
         )
         embed4.set_image(url=skin4_image)
         await message.channel.send(embed=embed1)
         await message.channel.send(embed=embed2)
         await message.channel.send(embed=embed3)
         await message.channel.send(embed=embed4)

      except requests.exceptions.RequestException as e:
         print(f"Request error: {e}")
      except KeyError as e:
         print(f"Key error: {e}")
  else:
     await message.channel.send("Not logged in!")
     
  

@bot.tree.command(name="logout")
async def logout(interaction : discord.Interaction):
   global logged_in
   auth.token_type = None
   auth.access_token = None
   auth.entitlements_token = None
   auth.user_id = None
   logged_in = False
   await interaction.response.send_message("Successfully logged out")





bot.run(discord_api_key)



