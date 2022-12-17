import discord
from discord.ext import commands
import re
from aitextgen.TokenDataset import TokenDataset
from aitextgen.tokenizers import train_tokenizer
from aitextgen.utils import GPT2ConfigCPU
from aitextgen import aitextgen
import textwrap
ai2 = aitextgen(model_folder="path/to/file/trained_model",
tokenizer_file="path/to/file/aitextgen.tokenizer.json")
pattern = r"<@(.*?)>"
def has_letters(string):
  # Use a regular expression to check if the string contains any letters
  if re.search(r'[a-zA-Z]', string):
    return True
  else:
    return False
def Average(lst):
    return sum(lst) / len(lst)
def getspamness(instr):
    inputmessage = str(instr)+":"
    out = ai2.generate_one(prompt=inputmessage)
    return out.partition('\n')[0]
def checkspam(fullin):
    print("Starting...")
    fullin = fullin.replace("\n","")
    inputstr = fullin
    n = 8
    inputstr = inputstr.replace("0", "a")
    chunks = [inputstr[i:i+n] for i in range(0, len(inputstr), n)]
    #print(chunks)

    wrapstr=chunks
    #while len(wrapstr[len(wrapstr)-1]) <8:
    #    wrapstr[len(wrapstr)-1] = wrapstr[len(wrapstr)-1] + "0"
    if len(wrapstr[len(wrapstr)-1]) <8:
      del wrapstr[-1]
    if wrapstr == []:
      wrapstr = ["hello te"]
    base = []
    for i in range(len(wrapstr)):
        print(getspamness(wrapstr[i]))
        base.append(int(getspamness(wrapstr[i])[-2]))
    print("average spam amount is: "+str(Average(base)))
    return int(Average(base))
bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())

@bot.event
async def on_message(message):
  # Check if message is longer than 1000 characters\
  print("on_message! message.content is: "+str(message.content))
  if len(message.content) > 4:
    string = message.content
    match = re.search(pattern, string)

    if match:
        print("stripping pings...")
        print(string.replace(match.group(0), ""))
        print(has_letters(match.group(0)))
        print(len(match.group(0)))
        if not len(match.group(0)) > 22:
          
          if not has_letters(match.group(0)):
            string = string.replace(match.group(0), "")
        if string.replace(" ","") == "":
          string = "hello te"
    try:
      if checkspam(str(string.lower())) >=4:
        print(checkspam(str(string.lower())))
        if True:
          await message.delete()
          print("deleted message")
    except:
      await message.delete()
    # Count number of different character types in message
    #num_char_types = len(set(message.content))
    ## Check if there are less than 6 different character types
    #if num_char_types < 7:
    #  # Delete the message
    #  await message.delete()
    #  print("deleted message")

bot.run('TOKEN')