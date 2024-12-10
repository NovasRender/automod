import discord
import discord.ext
import discord.ui
import os
from discord.ext import commands
import time
import requests

logurl = "https://discord.com/api/webhooks/1315884945738170402/DjUMBrRO2XwF_xX_xjcR6xZiGbD9P5O_5ta5TBVRaq7_nOj-RC3d4FZbQSQQwFTF_csy"


def dclog(text):
    requests.post(logurl, text)

dclog("Script Runtime Started")

baddef = "$$nigger, $$nigga, $$faggot, $$chink, $$spic, $$kike, $$gook, $$retard, $$tranny, $$cunt, $$whore, $$dyke, $$coon, $$wetback, $$beaner, $&jap, $$paki, $$raghead, $$sandnigger, $$wop, $$gyp, $$mick, $$kraut, $$hebe, $$sambo, $$chug, $$cholo, $$redskin, $$chinaman, $$guido, $$golliwog, $$ni66er, $$n1gger, $$n!gger, $$nigg3r, $$nigg@r, $$f@ggot, $$ch1nk, $$sp1c, $$k1ke, $$g00k, $$g0ok, $$r3tard, $$tr@ nny, $$wh0re, $$b1tch, $$d!ke, $$c00n, $$wetb@ck, $$j@p, $$p@ki, $$w0p, $$m1ck, $$kr@ut, $$h3be, $$chinam@n, $$guid0, $$g0lliwog"

from keep_alive import keep_alive
keep_alive()

filecontent = NotImplemented

with open('saves.txt', 'r') as file:
    filecontent = file.read()



def add_flagged_word(server_id, word):

    server_id = format(server_id)
    
    line = NotImplemented
    
    with open('saves.txt', 'r') as file:
        line = [line.strip() for line in file if server_id in line]

    if not line:
       
        with open('saves.txt', 'w') as wfile:
           with open('saves.txt', 'r') as rfile:
              wfile.write(f"{rfile}\n{server_id}|{word}")
    else:
       
        with open('saves.txt', 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if server_id in line:
                lines[i] = f"{line.strip()},{word}"
                break

        with open('savese.txt', 'w') as file:
            file.writelines(lines)



def get_flagged_words(server_id):

    server_id = format(server_id)
    after = NotImplemented
    with open('saves.txt', 'r') as file:
        logg("Opened Saves")
        logg(file.read())
        for line in file:
            if server_id in line:
                logg("Found Line With Data")
                after_pipe = line.split('|', 1)[1].strip()
                logg(f"Data Found: {after_pipe}")
                print(after_pipe)
                after = after_pipe
                break

    return after
  


def remove_flagged_word(server_id, word):

    server_id = format(server_id)
    
    nl = NotImplemented
    
    with open('saves.txt', 'r') as file:
        line = [line.strip() for line in file if server_id in line]

    parts = line.split('|')
    if len(parts) > 1:
        items = [item for item in parts[1].split(',') if item != word]
        nl = parts[0] + "|" + ",".join(items)
        
        with open('saves.txt', 'r') as file:
            lines = file.readlines()

        for i, line in enumerate(lines):
            if server_id in line:
                lines[i] = nl
                break

        with open('savese.txt', 'w') as file:
            file.writelines(lines)

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
    name = "┊automod-logging"

    if discord.utils.get(message.guild.channels, name=name):
      channel = discord.utils.get(message.guild.channels, name=name)

    if not discord.utils.get(message.guild.channels, name=name):

      channel = await message.guild.create_text_channel(name)

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
  
  if message and "$default" in message:
    flagtype = "default"

  word = message.split("$")[1]
  
  
  embed = discord.Embed(title="Add Flag", description=f"Successfully added a {flagtype} flag! (flagged {word} : db {message})!", color=0x00ff00)
  e = baddef.split(", ")
  print(format(e))
  if flagtype == "default":
    for x in range(0, len(e)):
      z = e[int(x)]
      add_flagged_word(ctx.guild.id,z)
    print(f"added {z}!")
  
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
