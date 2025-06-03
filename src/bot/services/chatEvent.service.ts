import { logError } from "~/middlewares";
import axios from "axios";
import config from "~/configs/config";
import {
  ActionRowBuilder,
  ButtonBuilder,
  ButtonStyle,
  Message,
  MessageCreateOptions,
  TextChannel,
} from "discord.js";
import { Meme, User } from "~/models";

export const chatMinecraftEvent = async (
  message: Message,
  content: string,
): Promise<void> => {
  let finalMessage = `§7${content}`;
  let messageDisplayName =
    message.member?.displayName || message.author.username;

  if (message.reference?.messageId) {
    try {
      const repliedMessage = await message.channel.messages.fetch(
        message.reference.messageId,
      );
      const repliedContent = repliedMessage.content.trim().slice(0, 200);
      finalMessage = `§7"${repliedContent}"§r ↩\n → §n${messageDisplayName}§r:  ${content}`;
      messageDisplayName = repliedMessage.member
        ? repliedMessage.member.displayName
        : repliedMessage.author.username;
    } catch (err) {
      logError(`Impossible de récupérer le message répondu : ${err}`);
    }
  }

  try {
    await axios.post(
      `${config.BITUMEMC_URL}/chat`,
      {
        author: `${messageDisplayName}§r`,
        message: finalMessage,
      },
      {
        headers: {
          "Content-Type": "application/json; charset=utf-8",
        },
      },
    );
  } catch (err) {
    logError(`Erreur lors de l’envoi à l’API : ${err}`);
  }
};
export const generateMemeButton = (
  value: number,
  messageId: string,
): ButtonBuilder => {
  const total = config.MEME_VOTE_REQUIRED * 2;
  const filled = Math.floor((value / total) * 20);
  const text = `[${" |".repeat(filled)}${" -".repeat(20 - filled)} ] ${(filled / 20) * 100}%`;
  return new ButtonBuilder({
    customId: `progress_meme;${messageId};${value}`,
    label: text,
    style: ButtonStyle.Secondary,
    disabled: true,
  });
};
export const createNewMeme = async (message: Message) => {
  const channel = message.channel as TextChannel;
  const newContent = `> ${message.author}\n\n${message.content}`;
  const attachments = message.attachments.map((attachment) => attachment.url);
  const user = await User.findOne({
    where: { discordId: message.author.id },
  });
  if (!user) {
    logError(`User not found for author: ${message.author.id}`);
    return;
  }

  const upvote = new ButtonBuilder({
    customId: `meme_vote;${user.userId};+1`,
    label: "Upvote ⬆️",
    style: ButtonStyle.Success,
  });
  const downvote = new ButtonBuilder({
    customId: `meme_vote;${user.userId};-1`,
    label: "Downvote ⬇️",
    style: ButtonStyle.Danger,
  });
  const progress = generateMemeButton(config.MEME_VOTE_REQUIRED, message.id);
  const actions = new ActionRowBuilder<ButtonBuilder>()
    .addComponents(upvote)
    .addComponents(progress)
    .addComponents(downvote);
  const newMessage: MessageCreateOptions = {
    content: newContent,
    files: attachments,
    components: [actions],
  };

  const memeMessage = await channel.send(newMessage);
  Meme.create({
    discordId: memeMessage.id,
    authorId: user.userId,
    votes: config.MEME_VOTE_REQUIRED,
  }).catch((err) => {
    logError(`Failed to create meme in database: ${err}`);
  });
  await message.delete();
};
