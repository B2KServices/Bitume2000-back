import { client } from "@/src/bot/client";
import { logError, logInfo } from "@/src/middlewares";
import {
  ActionRowBuilder,
  ActivityType,
  Collection,
  Guild,
  GuildMember,
  Role as DiscordRole,
  TextChannel,
} from "discord.js";
import { NotFoundError } from "@/src/errors";
import config from "@/src/configs/config";
import { Role, RoleCategory, User, UsersHasRoles } from "@/src/models";
import { version } from "@/package.json";

/**
 * Récupère la guild depuis le cache ou fetch si nécessaire
 */
export const getGuild = async (): Promise<Guild> => {
  const guild = client.guilds.cache.get(config.DISCORD_GUILD_ID);
  if (guild) return guild;

  return await client.guilds.fetch(config.DISCORD_GUILD_ID);
};

/**
 * Récupère un membre depuis le cache ou fetch si nécessaire
 */
export const getMember = async (
  guild: Guild,
  memberId: string,
): Promise<GuildMember | null> => {
  try {
    const cached = guild.members.cache.get(memberId);
    if (cached) return cached;

    return await guild.members.fetch(memberId);
  } catch (error) {
    logError(`Member ${memberId} not found`, { error });
    return null;
  }
};

/**
 * Récupère tous les membres depuis le cache ou fetch si nécessaire
 */
export const getAllMembers = async (
  guild: Guild,
): Promise<Collection<string, GuildMember>> => {
  if (guild.members.cache.size >= guild.memberCount) {
    return guild.members.cache;
  }
  return await guild.members.fetch();
};
/**
 * Récupère un rôle depuis le cache ou fetch si nécessaire
 */
export const getRole = async (
  guild: Guild,
  roleId: string,
): Promise<DiscordRole | null> => {
  try {
    const cached = guild.roles.cache.get(roleId);
    if (cached) return cached;

    return await guild.roles.fetch(roleId);
  } catch (error) {
    logError(`Role ${roleId} not found`, { error });
    return null;
  }
};

/**
 * Récupère tous les rôles depuis le cache ou fetch si nécessaire
 */
export const getAllRoles = async (guild: Guild) => {
  if (guild.roles.cache.size > 0) {
    return guild.roles.cache;
  }
  return await guild.roles.fetch();
};

/**
 * Récupère un user Discord depuis le cache ou fetch si nécessaire
 */
export const getUser = async (userId: string) => {
  try {
    const cached = client.users.cache.get(userId);
    if (cached) return cached;

    return await client.users.fetch(userId);
  } catch (error) {
    logError(`User ${userId} not found`, { error });
    return null;
  }
};

/**
 * Récupère un channel depuis le cache ou fetch si nécessaire
 */
export const getChannel = async (channelId: string) => {
  try {
    const cached = client.channels.cache.get(channelId);
    if (cached) return cached;

    return await client.channels.fetch(channelId);
  } catch (error) {
    logError(`Channel ${channelId} not found`, { error });
    return null;
  }
};

export const getTextChannel = async (channelId: string) => {
  const channel = await getChannel(channelId);
  if (!channel || !channel.isTextBased()) {
    throw new NotFoundError("Channel not found on Discord");
  }
  return channel as TextChannel;
};

export const sendMessageToChannel = async (
  content: string,
  channelId: string,
  username?: string,
) => {
  const guild = await getGuild();
  if (!guild) {
    logError("Guild not found");
    return;
  }

  const channel = await getTextChannel(channelId);

  const members = await getAllMembers(guild);
  const splitedContent = content.split(" ");

  const editedContent = await Promise.all(
    splitedContent.map(async (word) => {
      if (!word.startsWith("@")) return word;
      if (word.startsWith("@everyone") || word.startsWith("@here")) {
        return `${word.slice(1)}`;
      }

      const possiblyUsername = word.slice(1);

      const userDb = await User.findOne({
        where: { username: possiblyUsername },
      });
      if (userDb) {
        return `<@${userDb.discordId}>`;
      }
      const memberByUsername = members.find(
        (m) => m.user.username === possiblyUsername,
      );
      if (memberByUsername) {
        return `<@${memberByUsername.user.id}>`;
      }

      const memberByDisplayName = members.find(
        (m) => m.displayName === possiblyUsername,
      );
      if (memberByDisplayName) {
        return `<@${memberByDisplayName.user.id}>`;
      }
      return word;
    }),
  );

  const finalMessage = `${username ? `\`\`${username}\`\` ` : ""}${editedContent.join(" ")}`;
  logInfo(`Sending message to channel ${channel.name}: ${finalMessage}`, {
    context: "Discord Service",
    channelId,
  });
  await channel.send(finalMessage);
};

export const removeRoleOnUser = async (
  userDiscordId: string,
  roleDiscordId: string,
) => {
  const guild = await getGuild();
  if (!guild) {
    logError("Guild not found");
    return;
  }

  const role = await getRole(guild, roleDiscordId);
  const user = await getMember(guild, userDiscordId);

  if (!role) {
    throw new NotFoundError("role not found on Discord");
  }
  if (!user) {
    throw new NotFoundError("user not found on Discord");
  }

  const userDb = await User.findOne({
    where: { discordId: userDiscordId },
  });

  logInfo(`Removing role ${role.name} from user ${user.user.username}`, {
    context: "Discord Service",
    userDiscordId,
    roleId: roleDiscordId,
    userId: userDb?.userId,
  });

  await user.roles.remove(role);
};

export const addRoleToUser = async (
  userDiscordId: string,
  roleDiscordId: string,
) => {
  const guild = await getGuild();
  if (!guild) {
    logError("Guild not found");
    return;
  }

  const role = await getRole(guild, roleDiscordId);
  const user = await getMember(guild, userDiscordId);

  if (!role) {
    throw new NotFoundError("role not found on Discord");
  }
  if (!user) {
    throw new NotFoundError("user not found on Discord");
  }

  const userDb = await User.findOne({
    where: { discordId: userDiscordId },
  });

  logInfo(`Adding role ${role.name} to user ${user.user.username}`, {
    context: "Discord Service",
    userDiscordId,
    roleId: roleDiscordId,
    userId: userDb?.userId,
  });

  await user.roles.add(role);
};

export const sendPrivateMessage = async (
  userId: string,
  content: string,
  actions?: ActionRowBuilder<any>,
) => {
  const user = await User.findOne({
    where: { userId: userId },
  });

  if (!user) {
    logError(`User with ID ${userId} not found`);
    return false;
  }

  const discordUser = await getUser(user.discordId);
  if (!discordUser) {
    logError(`Discord user with ID ${user.discordId} not found`);
    return false;
  }

  try {
    await discordUser.send({
      content: content,
      components: actions ? [actions] : [],
    });
    logInfo(`Message sent to ${discordUser.username}: ${content}`);
    return true;
  } catch (error) {
    logError(`Failed to send message to ${discordUser.username}: ${error}`);
    return false;
  }
};

export const generateRoleCategories = async () => {
  logInfo("Creating role categories...");
  await RoleCategory.bulkCreate([
    { name: "Position", color: "#4a8b29" },
    { name: "IRL", color: "#00ff00" },
    { name: "Autres", color: "#f1c232" },
    { name: "Stratégie", color: "#9900ff" },
    { name: "Réflexion", color: "#00ffff" },
    { name: "Combat", color: "#e91e1e" },
    { name: "Party Games", color: "#ff9900" },
    { name: "Survie/ Aventure", color: "#cccccc" },
    { name: "Course", color: "#0161ff" },
    { name: "FPS", color: "#00de8c" },
  ]);
};

export const generateRoles = async () => {
  logInfo("Creating roles...");
  const guild = await getGuild();
  if (!guild) {
    logError("Guild not found");
    return;
  }

  const [categories, dbRoles] = await Promise.all([
    RoleCategory.findAll(),
    Role.findAll({}),
  ]);

  const roles = await getAllRoles(guild);
  if (!roles || roles.size === 0) {
    logError("No roles found");
    return;
  }
  roles.forEach((value) => {
    if (dbRoles.some((role) => role.discordId === value.id)) {
      logInfo(`Role ${value.name} already exists in the database.`, {
        context: "Discord Sync",
      });
    } else {
      const category = categories.find(
        (cat) => cat.color === value.hexColor.toLowerCase(),
      );
      if (category) {
        logInfo(`Preparing role ${value.name} for creation.`, {
          context: "Discord Sync",
        });
        Role.create({
          name: value.name,
          color: value.hexColor,
          roleCategoryId: category.roleCategoryId,
          discordId: value.id,
        });
      }
    }
  });
};

export const generateUsers = async () => {
  logInfo("Creating users...", { context: "Discord Sync" });

  const guild = await getGuild();
  if (!guild) {
    logError("Guild not found");
    return;
  }

  const members = await getAllMembers(guild);
  if (!members || members.size === 0) {
    logError("No members found");
    return;
  }

  for (const [_, member] of members) {
    const discordUser = member.user;
    if (!discordUser || discordUser.bot) continue;

    if (!discordUser) continue;
    const existingUser = await User.findOne({
      where: {
        discordId: discordUser.id,
      },
    });

    const dbUser =
      existingUser ??
      (await User.create({
        discordId: discordUser.id,
        username: discordUser.username,
        avatarUrl: discordUser.avatar || undefined,
      }));
    for (const [_, discordRole] of member.roles.cache) {
      const role = await Role.findOne({
        where: {
          discordId: discordRole.id,
        },
      });
      if (role) {
        const userHasRole = await UsersHasRoles.findOne({
          where: {
            userId: dbUser.userId,
            roleId: role.roleId,
          },
        });
        if (!userHasRole) {
          await UsersHasRoles.create({
            userId: dbUser.userId,
            roleId: role.roleId,
          });
        }
      }
    }
  }

  logInfo("Users and roles updated successfully.", { context: "Discord Sync" });
};

export const setBotDefaultActivity = () => {
  client.user?.setActivity(`v${version}`, {
    type: ActivityType.Custom,
  });
};

export const synchronizeDiscordData = async () => {
  logInfo("Synchronizing Discord data...", {
    context: "Discord Sync",
  });
  await generateRoles();
  await generateUsers();
  logInfo("Discord data synchronized successfully.", {
    context: "Discord Sync",
  });
};
