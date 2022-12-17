import discord
from discord.ext import commands
from aitextgen.TokenDataset import TokenDataset
from aitextgen.tokenizers import train_tokenizer
from aitextgen.utils import GPT2ConfigCPU
from aitextgen import aitextgen
import textwrap
ai2 = aitextgen(model_folder="absolute_path_to_file/trained_model",
tokenizer_file="absolute_path_to_file/aitextgen.tokenizer.json")
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
    while len(wrapstr[len(wrapstr)-1]) <8:
        wrapstr[len(wrapstr)-1] = wrapstr[len(wrapstr)-1] + "0"
    base = []
    for i in range(len(wrapstr)):
        base.append(int(getspamness(wrapstr[i])[-2]))
    print("average spam amount is: "+str(Average(base)))
    return int(Average(base))
bot = commands.Bot(command_prefix='!',intents=discord.Intents.all())

@bot.event
async def on_message(message):
  # Check if message is longer than 1000 characters\
  print("on_message! message.content len is: "+str(len(message.content)))
  if len(message.content) > 4:
    if checkspam(str(message.content)) >=4:
      await message.delete()
      print("deleted message")
    # Count number of different character types in message
    #num_char_types = len(set(message.content))
    ## Check if there are less than 6 different character types
    #if num_char_types < 7:
    #  # Delete the message
    #  await message.delete()
    #  print("deleted message")

bot.run('token')