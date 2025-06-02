import { Meme, User } from "~/models";
import { logDebug } from "~/middlewares";
import {
  ActionRowBuilder,
  ButtonBuilder,
  ButtonInteraction,
  ButtonStyle,
  MessageFlags,
  TextChannel,
} from "discord.js";
import { userInAuth } from "~/services/auth.service";
import { MemeType } from "~/types";
import config from "~/configs/config";
import dayjs from "dayjs";
import { generateMemeButton } from "~/bot/services/chatEvent.service";

export const authButton = async (
  interaction: ButtonInteraction,
  userId: string,
) => {
  const user = await User.findOne({
    where: { discordId: interaction.user.id },
  });
  logDebug(`clicked by ${user?.userId}, ${userId}`);

  if (user?.userId !== userId) {
    await interaction.reply({
      content: "❌ Vous n'êtes pas autorisé à approuver cette demande.",
      flags: MessageFlags.Ephemeral,
    });
    return;
  }

  const userAuth = userInAuth.find((u) => u.userId === userId);
  if (userAuth) {
    userAuth.approved = true;
    await interaction.message.edit({
      content: "✅ Connexion approuvée. Vous pouvez maintenant vous connecter.",
      components: [],
    });
  } else {
    await interaction.reply({
      content: "❌ Aucune demande de connexion trouvée.",
      flags: MessageFlags.Ephemeral,
    });
  }
};

export const memeVoteInteraction = async (
  interaction: ButtonInteraction,
  userId: string,
) => {
  const vote = Number(interaction.customId.split(";")[2]);

  const memeUser = await User.findOne({ where: { userId } });
  if (!memeUser) {
    await interaction.reply({
      content: "❌ Utilisateur non trouvé.",
      flags: MessageFlags.Ephemeral,
    });
    return;
  }

  const user = await User.findOne({
    where: { discordId: interaction.user.id },
  });
  if (!user) {
    await interaction.reply({
      content: "❌ Utilisateur non trouvé.",
      flags: MessageFlags.Ephemeral,
    });
    return;
  }

  console.log(`${user.userId} - ${userId}`);
  if (user.userId == userId) {
    await interaction.reply({
      content: "❌ Vous n'êtes pas autorisé à voter pour ce mème.",
      flags: MessageFlags.Ephemeral,
    });
    return;
  }

  const now = dayjs();
  const lastVote = user.memeLastVote ? dayjs(user.memeLastVote) : null;
  if (lastVote) {
    const cooldownEnd = lastVote.add(config.MEME_VOTE_COOLDOWN, "millisecond");

    if (now.isBefore(cooldownEnd)) {
      const secondsLeft = cooldownEnd.diff(now, "second");
      await interaction.reply({
        content: `⏳ Tu dois attendre encore ${secondsLeft} seconde(s) avant de pouvoir voter à nouveau.`,
        flags: MessageFlags.Ephemeral,
      });
      return;
    }
  }

  const meme = await Meme.findOne({
    where: { discordId: interaction.message.id },
  });
  if (!meme) {
    await interaction.reply({
      content: "❌ Mème non trouvé.",
      flags: MessageFlags.Ephemeral,
    });
    return;
  }

  meme.votes += vote;

  const repostPayload = {
    content: interaction.message.content,
    files: interaction.message.attachments.map((a) => a.url),
  };

  if (meme.votes <= 0) {
    meme.memeType = MemeType.DUD_MEME;
    const dudChannel = (await interaction.guild?.channels.fetch(
      config.DISCORD_DUD_MEME_CHANNEL_ID,
    )) as TextChannel;
    await dudChannel.send(repostPayload);
    await interaction.message.delete();
    memeUser.dudMeme += 1;
    await memeUser.save();
  } else if (meme.votes >= config.MEME_VOTE_REQUIRED * 2) {
    meme.memeType = MemeType.BEST_MEME;
    const bestChannel = (await interaction.guild?.channels.fetch(
      config.DISCORD_BEST_MEME_CHANNEL_ID,
    )) as TextChannel;
    await bestChannel.send(repostPayload);
    await interaction.message.delete();
    memeUser.legendaryMeme += 1;
    await memeUser.save();
  } else {
    const upvote = new ButtonBuilder({
      customId: `meme_vote;${userId};+1`,
      label: "Upvote ⬆️",
      style: ButtonStyle.Success,
    });
    const downvote = new ButtonBuilder({
      customId: `meme_vote;${userId};-1`,
      label: "Downvote ⬇️",
      style: ButtonStyle.Danger,
    });
    const progress = generateMemeButton(meme.votes, interaction.message.id);
    const actions = new ActionRowBuilder<ButtonBuilder>()
      .addComponents(upvote)
      .addComponents(progress)
      .addComponents(downvote);
    await interaction.message.edit({
      components: [actions],
    });
  }

  user.memeLastVote = now.toDate();
  await meme.save();
  await user.save();

  const nextVoteDate = now.add(config.MEME_VOTE_COOLDOWN, "millisecond");
  const secondsUntilNextVote = nextVoteDate.diff(dayjs(), "second");

  await interaction.reply({
    content: `✅ À voté !\nTu pourras voter à nouveau dans ${secondsUntilNextVote} seconde(s).`,
    flags: MessageFlags.Ephemeral,
  });
};
