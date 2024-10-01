import discord
from discord.ext import commands
import random
import asyncio
import json
import os

intents = discord.Intents.default()
intents.messages = True  
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)


LEADERBOARD_FILE = 'leaderboard.json'


def load_scores():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_scores(scores):
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(scores, f)

scores = load_scores()

def generate_question(difficulty):

    operations = ['+', '-', '*', '/']
    
    operation = random.choice(operations)

    if difficulty == 'easy':
        a, b = random.randint(1, 10), random.randint(1, 10)
        points = 10  
    elif difficulty == 'medium':
        a, b = random.randint(10, 50), random.randint(1, 20)
        points = 20  
    elif difficulty == 'hard':
        a, b = random.randint(50, 100), random.randint(1, 30)
        points = 30  
    else:
        return None, None  

    if operation == '+':
        return f"{a} + {b}", a + b, points
    elif operation == '-':
        return f"{a} - {b}", a - b, points
    elif operation == '*':
        return f"{a} * {b}", a * b, points
    elif operation == '/':
        b = random.randint(1, 10) if difficulty == 'easy' else random.randint(1, 20) if difficulty == 'medium' else random.randint(1, 30)
        return f"{a} / {b}", round(a / b, 2), points  

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='math')
async def math_quiz(ctx, difficulty: str = 'easy'):
    valid_difficulties = ['easy', 'medium', 'hard']
    if difficulty.lower() not in valid_difficulties:
        await ctx.send(f'Invalid difficulty! Choose from: {", ".join(valid_difficulties)}.')
        return
    
    question, answer, points = generate_question(difficulty.lower())  
    await ctx.send(f'**Math Question:** What is {question}?')

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await bot.wait_for('message', check=check, timeout=30)
        if float(msg.content) == answer: 
            await ctx.send(f'Correct! You get {points} points!')
            scores[str(ctx.author)] = scores.get(str(ctx.author), 0) + points
            save_scores(scores) 
        else:
            await ctx.send(f'Incorrect! The correct answer was {answer}.')
    except asyncio.TimeoutError:
        await ctx.send(f'Time is up! The correct answer was {answer}.')

@bot.command(name='leaderboard')
async def leaderboard(ctx):
    leaderboard = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    leaderboard_message = '**Leaderboard:**\n'
    for user, score in leaderboard:
        leaderboard_message += f'{user}: {score} points\n'
    await ctx.send(leaderboard_message)

bot.run('BOT TOKEN')
