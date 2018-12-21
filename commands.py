import discord
from utils.config import ROLES
from utils.embeds import Embed
from utils.roles import is_valid_role
from discord.utils import get
from discord.ext.commands import HelpFormatter
from utils.perms import is_mod_or_admin

formatter = HelpFormatter()

msg_cache = dict()


async def help_cmd(bot, ctx, *args):
    if len(args) == 0:
        pages = bot.formatter.format_help_for(ctx, bot)
    else:
        cmd_str = args[0][0]
        command = bot.commands.get(cmd_str)

        if command is None:
            emb = discord.Embed(title='Command: {}'.format(cmd_str), type='rich',
                                description='Invalid command entered', color=0xff0000)
            await bot.send_message(ctx.message.channel, embed=emb)
            return
        else:
            pages = bot.formatter.format_help_for(ctx, command)
    for page in pages:
        await bot.send_message(ctx.message.channel, page)


async def init(bot, channel, user):
    if not is_mod_or_admin(user):
        await bot.send_message(channel, "Must be mod or admin to initiate")
    else:
        await bot.send_message(channel, "Initiating...")

        all_paired_embeds = Embed.create_embeds()
        for i in range(0, len(all_paired_embeds)):
            init_embed = discord.Embed(title=all_paired_embeds[i].title, type='rich',
                                       description=all_paired_embeds[i].message, color=0xffffff)
            init_message = await bot.send_message(channel, embed=init_embed)

            role_group = list(sorted(ROLES.keys()))[i]
            curr_roles = ROLES[role_group]
            msg_cache[role_group] = init_message
            for r, emoji in curr_roles.items():
                reaction = get(bot.get_all_emojis(), name=emoji)
                # if reaction is not a default Discord reaction
                if reaction is None:
                    reaction = emoji
                await bot.add_reaction(init_message, reaction)


async def add_emoji(bot, channel, user, args):
    if not is_mod_or_admin(user):
        await bot.send_message(channel, "Must be mod or admin to initiate")
        return False
    else:
        if len(args) < 3:
            await __error_msg("Insufficient arguments", "Must supply <role> <emoji> <category> in respective order",
                              bot, channel)
            return False
        # hail to the all-mighty if (yif the if)
        emote = get(bot.get_all_emojis(), name=args[1])
        if emote is None:
            emote = args[1]
        if not is_valid_role(user, args[0]):
            await __error_msg("Invalid role", "Role **{}** is invalid. Try again".format(args[0]), bot, channel)
            return False
        if args[2] not in ROLES.keys():
            await __error_msg("Invalid category", "Category **{}** is invalid. Try again".format(args[2]),
                              bot, channel)
            return False
        if args[0] in ROLES[args[2]]:
            await __error_msg("Double Entry", "Role **{}** is already in the list of {}".format(args[0], args[2]),
                              bot, channel)
            return False
        if args[2] not in msg_cache.keys():
            await __error_msg("Welp IDK", "Restart me. Too much went wrong to fix", bot, channel)
            return False

        ROLES[args[2]][args[0]] = args[1]
        # TODO: this code can raise an error if provided an emote that is neither a custom nor normal one
        await bot.add_reaction(msg_cache[args[2]], emote)
        return True


#TODO: doesn't work the way I want it to - does not actually remove the emote. Just the bot's liking of the emote.
async def remove_emoji(bot, channel, user, args):
    if not is_mod_or_admin(user):
        await bot.send_message(channel, "Must be mod or admin to initiate")
        return False

    if len(args) < 2:
        await __error_msg("Insufficient arguments", "Must supply <role> <category> in respective order",
                          bot, channel)
        return False
    if args[1] not in ROLES.keys():
        await __error_msg("Invalid category", "Category **{}** is invalid. Try again".format(args[1]),
                          bot, channel)
        return False
    if args[0] not in ROLES[args[1]]:
        await __error_msg("Invalid Role", "Role **{}** was not found. Try again".format(args[0]),
                          bot, channel)
        return False
    if args[1] not in msg_cache.keys():
        await __error_msg("Welp IDK", "Restart me. Too much went wrong to fix", bot, channel)
        return False

    await bot.remove_reaction(msg_cache[args[1]], ROLES[args[1]][args[0]], bot.user)
    del ROLES[args[1]][args[0]]
    return True


async def __error_msg(title, message, bot, channel):
    await bot.send_message(channel, embed=discord.Embed(title=title, type='rich',
                                                        description=message, color=0xff0000))
