# coding: cp1252
import os
import sys
import cv2
from PIL import Image
import discord, asyncio
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(command_prefix="g-", intents=intents)
client2 = discord.Client(intents=intents)
framecnt = 0

TOKEN="TOKEN1"
TOKEN2 = "TOKEN2"

@client.command()
async def ping(ctx):
    await ctx.send(f"pong! {round(client.latency * 1000)}ms")
    print(f"sent! message : pong! {round(client.latency * 1000)}ms")

@client.command()
async def clear(ctx):
    await ctx.channel.purge()
    print(f"Message cleared!")

@client.command()
async def badapple(ctx):
    # get channel id from message
    channel_id = ctx.message.channel.id
    await handleLooping(ctx, channel_id)

CHARS = ["@", "#", "S", "%", "$", "?", "*", ";", ";", ",", "."]

def resizedGrayImage(image, newWidth=40):
    width,height = image.size
    aspectRatio = height/width
    newHeight = int(aspectRatio * newWidth)
    # newHeight = 40
    resizedGrayImage = image.resize((newWidth, newHeight)).convert('L')
    return resizedGrayImage

def pixToChars(image):
    pixels = image.getdata()
    characters = "".join([CHARS[pixel//25] for pixel in pixels])
    return characters

async def generateFrame(image, ctx, newWidth=40, framecnt=0, channel_id=0):
    newImageData = pixToChars(resizedGrayImage(image))
    totalPixels = len(newImageData)
    asciiImage = "```\n"
    asciiImage += "\n".join([newImageData[index:(index+newWidth)] for index in range(0, totalPixels, newWidth)])
    asciiImage += "```"
    if(framecnt % 2 == 0):
        channel = client.get_channel(channel_id)
        print(f"client: {client}", framecnt)
        await channel.send(asciiImage)
    else:
        channel = client2.get_channel(channel_id)
        print(f"client2: {client2}", framecnt)
        await channel.send(asciiImage)
    # os.system('clear') 

cap = cv2.VideoCapture("badApple1.mp4")

async def handleLooping(ctx, channel_id):
    i=0
    while True:
        ret,frame = cap.read()
        cv2.imshow("frame", frame)
        if i % 15 == 0:
            await generateFrame(Image.fromarray(frame), ctx, framecnt=i, channel_id=channel_id)
        cv2.waitKey(5)
        i+=1



print(TOKEN)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.create_task(client.start(TOKEN))
loop.create_task(client2.start(TOKEN2))
loop.run_forever()
