import { logError, logInfo } from "~/middlewares";
import { Role, RoleCategory, User, UsersHasRoles } from "~/models";
import config from "~/configs/config";
import { client } from "~/bot/client";
import { ActionRowBuilder, ActivityType, TextChannel } from "discord.js";
import { NotFoundError } from "~/errors";
import { version } from "~~/package.json";

export const sendMessageToChannel = async (
  content: string,
  channelId: string,
) => {
  const guild = await client.guilds.fetch(config.DISCORD_GUILD_ID);
  if (!guild) {
    logError("Guild not found");
    return;
  }

  const channel = (await client.channels.fetch(channelId)) as TextChannel;
  if (!channel) throw new NotFoundError("Channel not found on Discord");

  await guild.members.fetch();

  const splitedContent = content.split(" ");

  const editedContent = await Promise.all(
    splitedContent.map(async (word) => {
      if (!word.startsWith("@")) return word;

      const possiblyUsername = word.slice(1);

      const userDb = await User.findOne({
        where: { username: possiblyUsername },
      });
      if (userDb) {
        return `<@${userDb.discordId}>`;
      }
      const memberByUsername = guild.members.cache.find(
        (m) => m.user.username === possiblyUsername,
      );
      if (memberByUsername) {
        return `<@${memberByUsername.user.id}>`;
      }

      const memberByDisplayName = guild.members.cache.find(
        (m) => m.displayName === possiblyUsername,
      );
      if (memberByDisplayName) {
        return `<@${memberByDisplayName.user.id}>`;
      }
      return word;
    }),
  );

  const finalMessage = editedContent.join(" ");
  await channel.send(finalMessage);
};

export const removeRoleOnUser = async (
  userDiscordId: string,
  roleDiscordId: string,
) => {
  const guild = await client.guilds.fetch(config.DISCORD_GUILD_ID);
  if (!guild) {
    logError("Guild not found");
    return;
  }
  const role = await guild.roles.fetch(roleDiscordId);
  const user = await guild.members.fetch(userDiscordId);
  if (!role) {
    throw new NotFoundError("role not found on Discord");
  }
  if (!user) {
    throw new NotFoundError("user not found on Discord");
  }
  await user.roles.remove(role);
  return;
};

export const addRoleToUser = async (
  userDiscordId: string,
  roleDiscordId: string,
) => {
  const guild = await client.guilds.fetch(config.DISCORD_GUILD_ID);
  if (!guild) {
    logError("Guild not found");
    return;
  }
  const role = await guild.roles.fetch(roleDiscordId);
  const user = await guild.members.fetch(userDiscordId);
  if (!role) {
    throw new NotFoundError("role not found on Discord");
  }
  if (!user) {
    throw new NotFoundError("user not found on Discord");
  }
  await user.roles.add(role);
  return;
};

export const sendPrivateMessage = async (
  userId: string,
  content: string,
  actions?: ActionRowBuilder<any>,
) => {
  const user = await User.findOne({
    where: {
      userId: userId,
    },
  });
  if (!user) {
    logError(`User with ID ${userId} not found`);
    return false;
  }
  const discordUser = await client.users.fetch(user.discordId);
  if (!discordUser) {
    logError(`Discord user with ID ${user.discordId} not found`);
    return false;
  }

  try {
    await discordUser.send({
      content: content,
      components: [actions ? actions : new ActionRowBuilder()],
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
    {
      name: "Position",
      color: "#4a8b29",
    },
    {
      name: "IRL",
      color: "#00ff00",
    },
    {
      name: "Autres",
      color: "#f1c232",
    },
    {
      name: "Stratégie",
      color: "#9900ff",
    },
    {
      name: "Réflexion",
      color: "#00ffff",
    },
    {
      name: "Combat",
      color: "#e91e1e",
    },
    {
      name: "Party Games",
      color: "#ff9900",
    },
    {
      name: "Survie/ Aventure",
      color: "#cccccc",
    },
    {
      name: "Course",
      color: "#0161ff",
    },
    {
      name: "FPS",
      color: "#00de8c",
    },
  ]);
  return;
};

export const generateRoles = async () => {
  logInfo("Creating roles...");
  const categories = await RoleCategory.findAll();
  const guild = await client.guilds.fetch(config.DISCORD_GUILD_ID);
  if (!guild) {
    logError("Guild not found");
    return;
  }
  const roles = await guild.roles.fetch();
  if (!roles) {
    logError("Roles not found");
    return;
  }
  roles.forEach((value) => {
    const category = categories.find(
      (category) => category.color === value.hexColor.toLowerCase(),
    );
    if (category) {
      Role.create({
        name: value.name,
        color: value.hexColor,
        roleCategoryId: category.roleCategoryId,
        discordId: value.id,
      });
    }
  });
};

export const generateUsers = async () => {
  logInfo("Creating users...");
  const guild = await client.guilds.fetch(config.DISCORD_GUILD_ID);
  if (!guild) {
    logError("Guild not found");
    return;
  }

  const members = await guild.members.fetch();

  if (!members) {
    logError("Members not found");
    return;
  }

  for (const [_, member] of members) {
    const discordUser = member.user;

    if (!discordUser) continue;

    const dbUser = await User.create({
      discordId: discordUser.id,
      username: discordUser.username,
      avatarUrl: discordUser.avatar || undefined,
    });
    for (const [_, discordRole] of member.roles.cache) {
      const role = await Role.findOne({
        where: {
          discordId: discordRole.id,
        },
      });
      if (role) {
        await UsersHasRoles.create({
          userId: dbUser.userId,
          roleId: role.roleId,
        });
      }
    }
  }

  logInfo("Users and roles created successfully.");
};

export const setBotDefaultActivity = () => {
  client.user?.setActivity(`v${version}`, {
    type: ActivityType.Custom,
  });
};
