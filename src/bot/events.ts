import { ActivityType, Events, Interaction } from "discord.js";
import { client } from "./client";
import config from "~/configs/config";
import { logError, logInfo } from "~/middlewares";
import { Role, RoleCategory, User } from "~/models";
import {
  generateRoleCategories,
  generateRoles,
  generateUsers,
} from "~/services/discord.service";
import {
  playersCommand,
  playMusicCommand,
  clearCommand,
} from "~/bot/services/commands.service";
import {
  chatMinecraftEvent,
  createNewMeme,
} from "~/bot/services/chatEvent.service";
import {
  authButton,
  memeVoteInteraction,
} from "~/bot/services/buttonEvent.service";
import { version } from "~~/package.json";
import { handleMusicButton } from "~/bot/services/musicPlayer.service";
import * as console from "node:console";

export const registerEvents = () => {
  client.on(Events.ClientReady, async (readyClient) => {
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

    readyClient.user.setActivity(`v${version}`, {
      type: ActivityType.Custom,
    });
  });

  client.on(Events.MessageCreate, async (message) => {
    if (message.author.bot) return;
    if (!message.channel || message.channel.type !== 0) return;
    if (message.thread) return;
    const content = message.content.trim();
    logInfo(
      `[${message.channel.name}] ${message.author.username}: ${content}`,
      {
        userId: message.author.id,
        userName: message.author.username,
        context: "MessageCreate",
        channelId: message.channelId,
        channelName: message.channel?.name || "unknown",
      },
    );
    if (message.channelId === config.DISCORD_CHAT_MC_ID) {
      await chatMinecraftEvent(message, content);
    }
    if (message.channelId === config.DISCORD_MEME_CHANNEL_ID) {
      await createNewMeme(message);
    }
  });

  client.on(Events.InteractionCreate, async (interaction: Interaction) => {
    try {
      // 🧩 Slash Commands

      if (interaction.isChatInputCommand()) {
        logInfo("slash command used: " + interaction.type, {
          userId: interaction.user.id,
          userName: interaction.user.username,
          context: "Interaction slash command",
          commandName: interaction.commandName,
        });
        switch (interaction.commandName) {
          case "players":
            return playersCommand(interaction);
          case "tps":
            return interaction.reply("Coming soon!");
          case "play":
            return playMusicCommand(interaction);
          case "clear":
            return clearCommand(interaction);
          default:
            return interaction.reply({
              content: "❓ Commande inconnue.",
              ephemeral: true,
            });
        }
      }

      // 🔘 Button Interactions
      if (interaction.isButton()) {
        const [action, userId] = interaction.customId.split(";");
        logInfo(`button interaction used: ${interaction.customId}`, {
          userId: interaction.user.id,
          userName: interaction.user.username,
          context: "Interaction button",
          action,
          targetUserId: userId,
        });

        // 🔐 Auth & vote
        if (action === "approve_auth") {
          return authButton(interaction, userId);
        }

        if (action === "meme_vote") {
          return memeVoteInteraction(interaction, userId);
        }

        // 🎵 Music controls
        return handleMusicButton(interaction);
      }
    } catch (err) {
      console.error("❌ Erreur lors de l'interaction :", err);
      logError("❌ Error during interaction: " + err, {
        userId: interaction.user.id,
        userName: interaction.user.username,
        context: "Interaction error",
      });
      if (interaction.isRepliable()) {
        await interaction
          .reply({
            content: "❌ Une erreur est survenue lors du traitement.",
            ephemeral: true,
          })
          .catch(() => {});
      }
    }
  });
};
