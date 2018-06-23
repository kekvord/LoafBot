import discord
from discord.ext import commands
import asyncio
from utils import *
class Moderation:
	def __init__(self, bot):
	    self.bot = bot

	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, user : discord.Member, *, reason = None):
		"""kicks the user"""
		await ctx.guild.kick(user)

		title = ctx.message.author.display_name + ' kicked ' + user.display_name
		message = user.mention + '\n**' + user.id + '**'
		if reason != None:
			message += '\n' + reason

		em = discord.Embed(title=title, description=message, colour=0x0012d8)
		em.set_author(name=user.display_name, icon_url=user.avatar_url)
		await send_publiclogs(self.bot, ctx.guild, embed=em)

	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, user : discord.Member, *, reason = None):
		"""bans the user"""
		await ctx.guild.ban(user)

		title = ctx.message.author.display_name + ' banned ' + user.display_name
		message = user.mention + '\n**+ user.id' + '**'
		if reason != None:
			message += '\n' + reason

		em = discord.Embed(title=title, description=message, colour=0x00086b)
		em.set_author(name=user.display_name, icon_url=user.avatar_url)
		await send_publiclogs(self.bot, ctx.guild, embed=em)



	@commands.command(pass_context=True)
	@commands.has_permissions(manage_messages=True)
	async def mute(self, ctx, user : discord.Member, time : int, denomination : str, *, reason : str = None):
		"""mutes the user for the specified amount of time"""
		if denomination in ['s', 'm', 'h', 'd']:
			role = get_muterole(ctx.guild)
			if role in user.roles:
				umention = user.mention
				already = umention
				already += ' has already been muted'
				await ctx.send(already)
			else:
				await user.add_roles(role)
				umention = user.mention
				if reason is None:
					muted = umention
					muted += ' was muted for '
					muted += str(tint)
					muted += denomination
				else:
					muted = umention
					muted += ' was muted for '
					muted += str(tint)
					muted += denomination
					muted += ' (`'
					muted += reason
					muted += '`)'


				await ctx.send(muted)
				await send_publiclogs(self.bot, ctx.guild, muted)
				timedenoms = {'s':1, 'm':60, 'h':3600, 'd':86400}
				t = time * timedenoms[denomination]
				await asyncio.sleep(t)
				if role in user.roles:
					await user.remove_roles(role)
					await send_publiclogs(self.bot, ctx.guild, user.mention + ' is no longer muted.')


		else:
			await ctx.send('Correct usage is: >mute <user> <time integer> <s/m/h/d> [reason]')

	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def unmute(self, ctx, user: discord.Member):
		"""unmutes the specified muted user"""
		role = get_muterole(ctx.guild)
		umention = user.mention
		if role in user.roles:
			await user.remove_roles(role)
			await ctx.send(umention + ' is no longer muted.')
			await send_publiclogs(self.bot, ctx.guild, user.mention + ' is no longer muted.')
		else:
			await ctx.send(umention + ' is not muted.')

def setup(bot):
	bot.add_cog(Moderation(bot))