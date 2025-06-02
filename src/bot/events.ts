import { Events, MessageFlags } from "discord.js";
import { client } from "./client";
import config from "~/configs/config";
import { logError, logInfo } from "~/middlewares";
import { Role, RoleCategory, User } from "~/models";
import {
  generateRoleCategories,
  generateRoles,
  generateUsers,
} from "~/services/discord.service";
import { playersCommand } from "~/bot/services/commands.service";
import {
  chatMinecraftEvent,
  createNewMeme,
} from "~/bot/services/chatEvent.service";
import {
  authButton,
  memeVoteInteraction,
} from "~/bot/services/buttonEvent.service";

export const registerEvents = () => {
  client.on(Events.ClientReady, async (readyClient) => {
    console.log(`Logged in as ${readyClient.user.tag}!`);

    const roleCategories = await RoleCategory.findAll();
    if (!roleCategories || roleCategories.length === 0) {
      logError("No role categories found");
      await generateRoleCategories();
    }

    const roles = await Role.findAll();
    if (!roles || roles.length === 0) {
      logError("No roles found");
      await generateRoles();
    }

    const users = await User.findAll();
    if (!users || users.length === 0) {
      logError("No users found");
      await generateUsers();
    }
  });

  client.on(Events.MessageCreate, async (message) => {
    if (message.author.bot) return;
    if (!message.channel || message.channel.type !== 0) return; // Ignore non-text channels
    const content = message.content.trim();
    logInfo(`[${message.channel.name}] ${message.author.username}: ${content}`);
    if (message.channelId === config.DISCORD_CHAT_MC_ID) {
      await chatMinecraftEvent(message, content);
    }
    if (message.channelId === config.DISCORD_MEME_CHANNEL_ID) {
      await createNewMeme(message);
    }
  });

  client.on(Events.InteractionCreate, async (interaction) => {
    if (interaction.isChatInputCommand()) {
      if (interaction.commandName === "players") {
        await playersCommand(interaction);
      } else if (interaction.commandName === "tps") {
        await interaction.reply("Coming soon!");
      }
    } else if (interaction.isButton()) {
      const [action, userId] = interaction.customId.split(";");
      if (action === "approve_auth") {
        await authButton(interaction, userId);
      } else if (action === "meme_vote") {
        await memeVoteInteraction(interaction, userId);
      }
    }
  });
};
