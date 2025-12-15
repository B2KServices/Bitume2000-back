import { Meme, User } from "@/src/models";
import { logInfo } from "@/src/middlewares";
import {
  ActionRowBuilder,
  ButtonBuilder,
  ButtonInteraction,
  ButtonStyle,
  MessageFlags,
  TextChannel,
} from "discord.js";
import { userInAuth } from "@/src/services/auth.service";
import { MemeType, MemeVoteType } from "@/src/types";
import config from "@/src/configs/config";
import dayjs from "dayjs";
import { generateMemeButton } from "@/src/bot/services/chatEvent.service";
import {
  getVoteForMeme,
  updateVoteQuery,
  voteQuery,
} from "@/src/models/querys";

export const authButton = async (
  interaction: ButtonInteraction,
  userId: string,
) => {
  const user = await User.findOne({
    where: { discordId: interaction.user.id },
  });

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
    logInfo(`${user?.username} approved his authentication`, {
      userId: user?.userId,
      userName: user?.username,
      context: "Authentication",
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
  await interaction.deferReply({ ephemeral: true });

  const voteValue = Number(interaction.customId.split(";")[2]);
  const voteType =
    voteValue === 1 ? MemeVoteType.UPVOTE : MemeVoteType.DOWNVOTE;

  const [memeUser, voter, meme] = await Promise.all([
    User.findOne({ where: { userId } }),
    User.findOne({ where: { discordId: interaction.user.id } }),
    Meme.findOne({ where: { discordId: interaction.message.id } }),
  ]);

  if (!memeUser || !voter || !meme) {
    await interaction.editReply({
      content: `❌ ${!memeUser ? "Utilisateur (auteur)" : !voter ? "Utilisateur (voteur)" : "Mème"} non trouvé.`,
    });
    return;
  }

  if (voter.userId === userId) {
    await interaction.editReply({
      content: "❌ Vous n'êtes pas autorisé à voter pour ce mème.",
    });
    return;
  }

  const previousVote = await getVoteForMeme(voter.userId, meme.memeId);

  if (previousVote?.voteType === voteType) {
    await interaction.editReply({
      content: "❌ Vous avez déjà voté pour ce mème.",
    });
    return;
  }

  if (previousVote) {
    logInfo("${voter.username} change his vote", {
      userId: voter.userId,
      userName: voter.username,
      context: "Meme Vote",
      memeId: meme.memeId,
    });
    meme.votes -= previousVote.voteType === MemeVoteType.UPVOTE ? 1 : -1;
    await updateVoteQuery(voter.userId, meme.memeId, voteType);
  } else {
    logInfo("${voter.username} voted", {
      userId: voter.userId,
      userName: voter.username,
      context: "Meme Vote",
      memeId: meme.memeId,
    });
    await voteQuery(voter.userId, meme.memeId, voteType);
  }

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
    logInfo(`${meme.memeId} has been voted as dud meme`, {
      postedUserId: memeUser.userId,
      postedUserName: memeUser.username,
      context: "Meme Vote",
      memeId: meme.memeId,
      type: "DUD_MEME",
    });
    await repostMeme(
      MemeType.DUD_MEME,
      config.DISCORD_DUD_MEME_CHANNEL_ID,
      async () => {
        await interaction.message.delete();
        memeUser.dudMeme += 1;
      },
    );
  } else if (meme.votes >= config.MEME_VOTE_REQUIRED * 2) {
    logInfo(`${meme.memeId} has been voted as legendary meme`, {
      postedUserId: memeUser.userId,
      postedUserName: memeUser.username,
      context: "Meme Vote",
      memeId: meme.memeId,
      type: "BEST_MEME",
    });
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

  await interaction.editReply({
    content: "✅ Vote enregistré !",
  });
};
