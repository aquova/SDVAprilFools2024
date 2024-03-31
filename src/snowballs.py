from random import choice, randint

import discord

import db

FAIL_FLAVOR = [
    "{username} figured out the cheatcode to spam snowballs, and threw {num} at {target}!",
    "{username} successfully rocketed a bucket of snowballs, and hit {target} with {num} in the face!",
]

CRIT_FLAVOR = [
    "{username} slipped on ice while trying to throw a snowball at {target}, and missed!",
    "{username} went too X-TREME and fired a rocket full of snowballs at {target}... but it flew in the wrong direction!",
]

def throw_snowball(src: discord.User | discord.Member, target: discord.User | discord.Member) -> str:
    success = db.use_snowball(src.id)
    if not success:
        return "You don't have any snowballs left!"
    odds = randint(1, 20)
    if odds == 1: # Fail
        flavor = choice(FAIL_FLAVOR)
        return flavor.format(username=str(src), target=str(target))
    elif odds == 20: # Crit
        num = randint(2, 10)
        db.snowball_hit(target.id, num)
        flavor = choice(CRIT_FLAVOR)
        return flavor.format(username=str(src), num=num, target=str(target))
    else:
        db.snowball_hit(target.id)
        return f"`{str(src)}` threw a snowball at `{str(target)}`"

