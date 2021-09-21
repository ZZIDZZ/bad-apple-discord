import os
import sys
import cv2
from PIL import Image
import discord, asyncio
from discord.ext import commands

client = commands.Bot(command_prefix="g-")


TOKEN="TOKEN HERE"

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
    await handleLooping(ctx)

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

async def generateFrame(image, ctx, newWidth=40):
    newImageData = pixToChars(resizedGrayImage(image))
    totalPixels = len(newImageData)
    asciiImage = "```\n"
    asciiImage += "\n".join([newImageData[index:(index+newWidth)] for index in range(0, totalPixels, newWidth)])
    asciiImage += "```"
    await ctx.send(asciiImage)
    # os.system('clear') 

cap = cv2.VideoCapture("badApple.mp4")

async def handleLooping(ctx):
    i=0
    while True:
        ret,frame = cap.read()
        cv2.imshow("frame", frame)
        if i % 30 == 0:
            await generateFrame(Image.fromarray(frame), ctx)
        cv2.waitKey(5)
        i+=1



print(TOKEN)
client.run(TOKEN)