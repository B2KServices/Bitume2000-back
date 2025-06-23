import { ChatInputCommandInteraction, GuildMember } from "discord.js";
import axios from "axios";
import config from "~/configs/config";
import { joinVoiceChannel } from "@discordjs/voice";
import {
  addToQueue,
  getTracksFromUrl,
  sendMusicPanel,
  updateMessages,
} from "~/bot/services/musicPlayer.service";

export const playersCommand = async (
  interaction: ChatInputCommandInteraction,
) => {
  try {
    const response = await axios.get<{ players: number }>(
      `${config.BITUMEMC_URL}/players`,
    );
    const players = response.data.players;

    await interaction.reply(
      `🧑‍💻 Il y a actuellement ${players} joueur${players > 1 ? "s" : ""} connecté${players > 1 ? "s" : ""}.`,
    );
  } catch (error) {
    console.error("Error fetching players:", error);
    await interaction.reply(
      "⚠️ Impossible de récupérer le nombre de joueurs pour le moment.",
    );
  }
};

export const playMusicCommand = async (
  interaction: ChatInputCommandInteraction,
) => {
  await interaction.deferReply();
  if (!interaction.guild) {
    await interaction.editReply(
      "⚠️ Cette commande ne peut être utilisée que dans un serveur.",
    );
    return;
  }
  const url_arg = interaction.options.getString("recherche");
  if (!url_arg) {
    await sendMusicPanel(interaction);
    return;
  }
  const urls = await getTracksFromUrl(url_arg);
  if (!urls) {
    await interaction.editReply(
      "⚠️ Impossible de trouver une piste musicale pour l'URL fournie.",
    );
    return;
  }

  const member = interaction.member as GuildMember;
  const voiceChannel = member?.voice?.channel;

  if (!voiceChannel) {
    await interaction.editReply(
      "⚠️ Vous devez être dans un salon vocal pour utiliser cette commande.",
    );
    return;
  }

  const connection = joinVoiceChannel({
    channelId: voiceChannel.id,
    guildId: voiceChannel.guild.id,
    adapterCreator: voiceChannel.guild.voiceAdapterCreator as any,
  });

  for (const url of urls) {
    if (!url) {
      console.error("URL is null or undefined, skipping...");
    } else {
      await addToQueue(connection, url);
    }
  }
  await updateMessages();
  sendMusicPanel(interaction);
};
