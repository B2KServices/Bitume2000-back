import {
  ChatInputCommandInteraction,
  GuildMember,
  TextChannel,
} from "discord.js";
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
  /* Temporary disable music feature TODO: fix that */
  await interaction.editReply(
    "⚠️ La fonctionnalité musicale est temporairement désactivée.",
  );
  return;
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

export const clearCommand = async (
  interaction: ChatInputCommandInteraction,
) => {
  const number = interaction.options.getInteger("nombre");
  const userId = interaction.options.getUser("utilisateur")?.id;
  const channel = interaction.channel as TextChannel;

  if (!channel || !number || number <= 0) {
    interaction.reply(
      "⚠️ Veuillez spécifier un nombre valide de messages à supprimer.",
    );
    return;
  }

  try {
    const messages = await channel.messages.fetch({ limit: 100 }); // fetch 100 messages max (Discord API limit)
    const now = Date.now();

    const filtered = messages
      .filter((msg) => !userId || msg.author.id === userId)
      .filter((msg) => now - msg.createdTimestamp < 14 * 24 * 60 * 60 * 1000) // only messages < 14 days old
      .first(number); // get only the desired number

    if (!filtered.length) {
      interaction.reply(
        "⚠️ Aucun message supprimable trouvé (âge > 14 jours ou aucun message correspondant).",
      );
      return;
    }

    await channel.bulkDelete(filtered);
    interaction.reply(`🗑️ ${filtered.length} message(s) supprimé(s).`);
  } catch (err) {
    console.error("Error during message deletion:", err);
    interaction.reply(
      "⚠️ Une erreur est survenue lors de la suppression des messages.",
    );
  }
};
