from random import choice, randint

import discord

import db

FAIL_FLAVOR = [
    "`{username}` slipped on ice while trying to throw a snowball at `{target}` and missed!",
    "`{username}` went too X-TREME this time and the jetpack snapped on the bucket of snowballs flew in the wrong direction, completely missing `{target}`!",
    "`{username}` didn't see the puffle passing by and tripped on top of it while trying to throw a snowball at `{target}`, missing their shot as a result!",
    "`{username}` threw a snowball at `{target}` but `{target}` somehow teleported away, so the snowball missed!",
]

CRIT_FLAVOR = [
    "`{username}` figured out the shortcut button to spam snowballs and threw {num} snowballs at `{target}` in one go!",
    "`{username}` successfully snapped a jetpack on a bucket full of snowballs and sent {num} snowballs directly to `{target}`'s face!",
    "`{username}` came in with a tractor and dumped a load of {num} snowballs on top of `{target}`!",
    "`{username}` activated their ninja skills and performed a wombo combo at `{target}` with {num} snowballs!",
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

