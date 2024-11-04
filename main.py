import discord
import discord.ext
import discord.ui
import os
from discord.ext import commands
import time
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import sqlalchemy

engine = create_engine('sqlite:///serverflags.db')
Base = sqlalchemy.orm.declarative_base()
session = sessionmaker(bind=engine)
session = session()


class FlaggedWord(Base):
  
  __tablename__ = 'flagged_words'
  id = Column(Integer, primary_key=True, autoincrement=True)
  server_id = Column(String, nullable=False)
  word = Column(String, nullable=False)

Base.metadata.create_all(engine)


def add_flagged_word(server_id, word):
    flagged_word = FlaggedWord(server_id=server_id, word=word)
    session.add(flagged_word)
    session.commit()

def get_flagged_words(server_id):
    return session.query(FlaggedWord).filter_by(server_id=server_id).all()
  
def remove_flagged_word(server_id, word):
    flagged_word = session.query(FlaggedWord).filter_by(server_id=server_id, word=word).first()
    if flagged_word:
        session.delete(flagged_word)
        session.commit()



from deep_translator import GoogleTranslator



word_list = None


client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

flags = []

async def prc():
  await client.process_commands(message)

@client.event
async def on_message(message):
  print("Entered On Message")
  if message.author.bot or message.author.guild_permissions.administrator:
    print("Returning")
    await client.process_commands(message)
    return



  import re
  def check_message_for_flags(server_id, message):
      words = get_flagged_words(server_id)
      mild_flags = []
      strict_flags = []

      for word_entry in words:
          if word_entry.word.startswith("$$"):
              strict_flags.append(word_entry.word[2:])
          elif word_entry.word.startswith("$"):
              mild_flags.append(word_entry.word[1:])



      translated_text = GoogleTranslator(source='auto', target='en').translate(message)
      print("theu")
      print(f"{translated_text}{message}")



    
      for word in mild_flags:
          if re.search(rf"\b{re.escape(word)}\b", message, re.IGNORECASE) or re.search(rf"\b{re.escape(word)}\b", translated_text, re.IGNORECASE):
            wor = word
            print("tian")
            return True, word, "mild"

      for word in strict_flags:
          if re.search(rf"{re.escape(word)}", message, re.IGNORECASE) or re.search(rf"\b{re.escape(word)}\b", translated_text, re.IGNORECASE):
              wor = word
              print("bad")
              return True, word, "strict"
      
      return False, None, None
  print(format(check_message_for_flags(message.guild.id, message.content)))
  if False or None in check_message_for_flags(message.guild.id, message.content):
    return
  #cxt = client.message.context(message)
  await message.delete()
  




  async def checkforautomodlogchannel():
    channel = None

    if discord.utils.get(message.guild.channels, name="automod-logs"):
      channel = discord.utils.get(message.guild.channels, name="automod-logs")

    if not discord.utils.get(message.guild.channels, name="automod-logs"):

      channel = await message.guild.create_text_channel("automod-logs")

    await channel.send(f"**{message.author}** has been timed out for using a flagged word: {message.content}")

    return

  await checkforautomodlogchannel()
  await client.process_commands(message)



@client.event
async def on_ready():

  print(f"Bot Is Ready With User {client.user}")
  
@client.command()
async def addflag(ctx, *, message):
  await ctx.message.delete()
  if ctx.author.guild_permissions.administrator == False:
    await ctx.send("You are not permitted to use this command")
    return

  flag = discord.Embed(title="Error While Executing Command", description=f"Please provide valid syntax!\n\n${message} - **Mild Moderation**\n-# Will only flag if it is alone, eg: flagged word is HI, it wont flag HIYA\n\n$${message} - **Strict Moderation**\n-# Will flag in every way, eg: flagged word is HI, it will flag HIYA or HIE!", color=0xff0000)
  flagtype = ""
  if message and not "$" in message:
    await ctx.reply(embed=flag)

    
    return

  if message and "$" in message:
    flagtype = "Mild"
    
  if message and "$$" in message:
    flagtype = "Strict"

  word = message.split("$")[1]
  
  embed = discord.Embed(title="Add Flag", description=f"Successfully added a {flagtype} flag! (flagged {word} : db {message})!", color=0x00ff00)


  
  add_flagged_word(ctx.guild.id, message)
  
  await ctx.send(embed=embed)
  
@client.command()
async def checkflags(ctx):
  
  await ctx.message.delete()

  flags = get_flagged_words(ctx.guild.id)

  word_list = "\n".join([f"Flag {i+1}: {word.word}" for i, word in enumerate(flags)])

  embed = discord.Embed(title="Flagged Words", description=f"List of all flagged words in **{ctx.guild.id}**\n\n{word_list}", color=0x00ff00)
  
  if flags:
    await ctx.send(embed=embed)
  else:

    embed = discord.Embed(title="Flagged Words", description="\nNo flagged words found...\n\n !addflag <flag> to flag a new word!")
    
    await ctx.send(embed=embed)


@client.command()
async def removeflag(ctx, *, message):

  await ctx.message.delete()

  if ctx.author.guild_permissions.administrator == False:
    return

  if not message:
    await ctx.send("Please provide a flag to remove.")
    return
  num = "$"
  flag = "Mild"
  if "$$" in message:
    num = "$$"
    flag = "Strict"
  visual = message.split(num)[1]

  fleg = get_flagged_words(ctx.guild.id)

  word_list = "\n".join([f"Flag {i+1}: {word.word}" for i, word in enumerate(fleg)])
  
  print(format(message))
  print(f"message : {message}\n\ngetflags {word_list}")


  
  if message in word_list:
    print("In flagged : attempting removal")
    remove_flagged_word(ctx.guild.id, message)

    embed = discord.Embed(title="Remove Flag", description=f"Removed A {flag}!\n\n{visual} is now not flagged.", color=0x00ff00)
    
    await ctx.send(embed=embed)


    


# run
client.run(os.getenv("Token"))