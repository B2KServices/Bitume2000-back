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
import { MemeType, MemeVoteType } from "~/types";
import config from "~/configs/config";
import dayjs from "dayjs";
import { generateMemeButton } from "~/bot/services/chatEvent.service";
import { getVoteForMeme, updateVoteQuery, voteQuery } from "~/models/querys";

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
  const voteValue = Number(interaction.customId.split(";")[2]);
  const voteType =
    voteValue === 1 ? MemeVoteType.UPVOTE : MemeVoteType.DOWNVOTE;

  const [memeUser, voter, meme] = await Promise.all([
    User.findOne({ where: { userId } }),
    User.findOne({ where: { discordId: interaction.user.id } }),
    Meme.findOne({ where: { discordId: interaction.message.id } }),
  ]);

  if (!memeUser || !voter || !meme) {
    await interaction.reply({
      content: `❌ ${!memeUser ? "Utilisateur (auteur)" : !voter ? "Utilisateur (voteur)" : "Mème"} non trouvé.`,
      flags: MessageFlags.Ephemeral,
    });
    return;
  }

  if (voter.userId === userId) {
    await interaction.reply({
      content: "❌ Vous n'êtes pas autorisé à voter pour ce mème.",
      flags: MessageFlags.Ephemeral,
    });
    return;
  }

  const previousVote = await getVoteForMeme(voter.userId, meme.memeId); // tu dois créer cette fonction (voir plus bas)

  if (previousVote?.voteType === voteType) {
    await interaction.reply({
      content: "❌ Vous avez déjà voté pour ce mème.",
      flags: MessageFlags.Ephemeral,
    });
    return;
  }

  // Annule l'effet de l'ancien vote si nécessaire
  if (previousVote) {
    meme.votes -= previousVote.voteType === MemeVoteType.UPVOTE ? 1 : -1;
    await updateVoteQuery(voter.userId, meme.memeId, voteType);
  } else {
    await voteQuery(voter.userId, meme.memeId, voteType);
  }

  // Applique le nouveau vote
  meme.votes += voteValue;

  const repostPayload = {
    content: interaction.message.content,
    files: interaction.message.attachments.map((a) => a.url),
  };

  const repostMeme = async (
    type: MemeType,
    channelId: string,
    updateCallback: () => Promise<void>,
  ) => {
    meme.memeType = type;
    const targetChannel = (await interaction.guild?.channels.fetch(
      channelId,
    )) as TextChannel;
    await targetChannel.send(repostPayload);
    await updateCallback();
    await memeUser.save();
  };

  if (meme.votes <= 0) {
    await repostMeme(
      MemeType.DUD_MEME,
      config.DISCORD_DUD_MEME_CHANNEL_ID,
      async () => {
        await interaction.message.delete();
        memeUser.dudMeme += 1;
      },
    );
  } else if (meme.votes >= config.MEME_VOTE_REQUIRED * 2) {
    await repostMeme(
      MemeType.BEST_MEME,
      config.DISCORD_BEST_MEME_CHANNEL_ID,
      async () => {
        memeUser.legendaryMeme += 1;
        const validated = new ButtonBuilder({
          customId: `meme;${userId}`,
          label: "Validé ✅",
          style: ButtonStyle.Success,
          disabled: true,
        });
        const actions = new ActionRowBuilder<ButtonBuilder>().addComponents(
          validated,
        );
        await interaction.message.edit({ components: [actions] });
      },
    );
  } else {
    const actions = new ActionRowBuilder<ButtonBuilder>().addComponents(
      new ButtonBuilder({
        customId: `meme_vote;${userId};+1`,
        label: "Upvote ⬆️",
        style: ButtonStyle.Success,
      }),
      generateMemeButton(meme.votes, interaction.message.id),
      new ButtonBuilder({
        customId: `meme_vote;${userId};-1`,
        label: "Downvote ⬇️",
        style: ButtonStyle.Danger,
      }),
    );
    await interaction.message.edit({ components: [actions] });
  }

  voter.memeLastVote = dayjs().toDate();
  await Promise.all([voter.save(), meme.save()]);

  await interaction.reply({
    content: "✅ Vote enregistré !",
    flags: MessageFlags.Ephemeral,
  });
};
