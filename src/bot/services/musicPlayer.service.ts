import {
  AudioPlayer,
  AudioPlayerStatus,
  createAudioPlayer,
  createAudioResource,
  NoSubscriberBehavior,
  StreamType,
  VoiceConnection,
} from "@discordjs/voice";
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-expect-error
import ytdl from "ytdl-core";
import ytSearch from "yt-search";
import { client } from "~/bot/client";
import {
  ActionRowBuilder,
  ActivityType,
  ButtonBuilder,
  ButtonInteraction,
  ButtonStyle,
  ChatInputCommandInteraction,
  EmbedBuilder,
  Message,
  MessageFlags,
} from "discord.js";
import ytpl from "@distube/ytpl";
import { setBotDefaultActivity } from "~/services/discord.service";

export let activeMessages: Message[] = [];
interface Track {
  url: string;
  title: string;
  author: string;
}

interface MusicSession {
  connection: VoiceConnection;
  player: AudioPlayer;
  queue: Track[];
  playing: boolean;
  actualTrack?: Track;
}

let idleTimeout: NodeJS.Timeout | null = null;
let session: MusicSession | null = null;
let isLoopMusic = false;

export const addToQueue = async (connection: VoiceConnection, url: string) => {
  try {
    const info = await ytdl.getInfo(url);
    const track: Track = {
      url,
      title: info.videoDetails.title,
      author: info.videoDetails.author.name,
    };

    if (!session) {
      const player = createAudioPlayer({
        behaviors: {
          noSubscriber: NoSubscriberBehavior.Pause,
        },
      });

      session = {
        connection,
        player,
        queue: [track],
        playing: false,
      };

      connection.subscribe(player);
      setupListeners();
      playNext();
    } else {
      session.queue.push(track);
      if (idleTimeout) {
        clearTimeout(idleTimeout);
        idleTimeout = null;
      }
    }

    return track;
  } catch (err) {
    console.error("❌ Failed to fetch track info", err);
    throw new Error("Invalid or unreachable URL");
  }
};

const setupListeners = () => {
  if (!session) return;

  session.player.removeAllListeners(); // 🔄 Sécurité contre les doublons

  session.player.on(AudioPlayerStatus.Idle, () => {
    if (!session) return;
    session.playing = false;
    setBotDefaultActivity();

    if (session.queue.length === 0 && !isLoopMusic) {
      idleTimeout = setTimeout(() => {
        console.log("🕒 No track added after 1 minute. Disconnecting...");
        session?.connection.destroy();
        session = null;
        idleTimeout = null;
      }, 60_000); // 1 minute
    }

    playNext();
  });

  session.player.on("error", (err) => {
    console.error("🎧 Player error:", err);
    if (session) {
      session.playing = false;
      playNext();
    }
  });
};

const playNext = async () => {
  if (
    !session ||
    session.playing ||
    (session.queue.length === 0 && !isLoopMusic)
  )
    return;

  const track = isLoopMusic ? session.actualTrack : session.queue.shift();
  if (!track) return;

  session.actualTrack = track;
  session.playing = true;

  const stream = ytdl(track.url, {
    filter: "audioonly",
    quality: "highestaudio",
    highWaterMark: 1 << 25,
    dlChunkSize: 1 << 20,
  });

  const resource = createAudioResource(stream, {
    inputType: StreamType.WebmOpus,
    inlineVolume: true,
  });
  if (!client.user) return false;
  client.user.setActivity(`🎶 ${track.title} by ${track.author}`, {
    type: ActivityType.Listening,
  });
  await updateMessages();
  session.player.play(resource);
};

export const stopMusic = () => {
  if (session) {
    session.player.stop();
    session.queue = [];
    session.playing = false;
    session.actualTrack = undefined;

    session.connection.destroy();
    setBotDefaultActivity();
    session = null;
    activeMessages.forEach((msg) => msg.delete().catch(() => {}));
    activeMessages = [];
  }
};

export const pauseMusic = (): boolean => {
  if (session && session.playing) {
    session.player.pause();
    session.playing = false;
    setBotDefaultActivity();
    return true;
  }
  return false;
};

export const resumeMusic = (): boolean => {
  if (session && !session.playing) {
    session.player.unpause();
    session.playing = true;

    const actualTrack = session.actualTrack;
    if (!actualTrack) return false;
    if (!client.user) return false;

    client.user.setActivity(
      `🎶 ${actualTrack.title} by ${actualTrack.author}`,
      {
        type: ActivityType.Listening,
      },
    );
    return true;
  }
  return false;
};

export const loopMusic = () => {
  isLoopMusic = !isLoopMusic;
};

export const skipMusic = () => {
  if (session) {
    session.player.stop();
    session.playing = false;
    session.actualTrack = undefined;
    playNext();
  }
};

export const getTrackUrl = async (url: string) => {
  if (!ytdl.validateURL(url)) {
    const searchResult = await ytSearch(url);
    const video = searchResult.videos[0];
    if (!video) {
      return null;
    }
    return video.url;
  }
  return url;
};

export const getQueue = (): Track[] => {
  return session?.queue ?? [];
};

export const sendMusicPanel = async (
  interaction: ChatInputCommandInteraction | ButtonInteraction,
) => {
  if (!session || !session.actualTrack) {
    return interaction.editReply({
      content: "❌ Aucune musique en cours.",
    });
  }

  const track = session.actualTrack;

  const embed = new EmbedBuilder()
    .setTitle("🎵 Musique en cours")
    .addFields(
      { name: "Titre", value: track.title },
      { name: "Auteur", value: track.author },
    )
    .setColor("#1DB954")
    .setFooter({
      text: isLoopMusic
        ? "🔁 En boucle"
        : `⏭ prochaine musique ${session.queue.length > 0 ? session.queue[0].title : "aucune"}`,
    });

  const buttons = new ActionRowBuilder<ButtonBuilder>().addComponents(
    new ButtonBuilder()
      .setCustomId("music_stop")
      .setLabel("stop")
      .setStyle(ButtonStyle.Danger),
    new ButtonBuilder()
      .setCustomId("music_toggle")
      .setLabel(session.playing ? "⏸ Pause" : "▶️ Lecture")
      .setStyle(ButtonStyle.Primary),
    new ButtonBuilder()
      .setCustomId("music_next")
      .setLabel("⏭ Suivant")
      .setStyle(ButtonStyle.Secondary),
    new ButtonBuilder()
      .setCustomId("music_queue")
      .setLabel("📃 Liste")
      .setStyle(ButtonStyle.Secondary),
    new ButtonBuilder()
      .setCustomId("music_loop")
      .setLabel(isLoopMusic ? "🔁 Boucle: ON" : "🔁 Boucle: OFF")
      .setStyle(ButtonStyle.Success),
  );

  if (interaction instanceof ChatInputCommandInteraction) {
    const message = await interaction.editReply({
      embeds: [embed],
      components: [buttons],
    });
    activeMessages.push(message);
  } else {
    for (const msg of activeMessages) {
      msg.edit({ embeds: [embed], components: [buttons] }).catch(console.error);
    }
    await interaction.deferUpdate(); // évite les erreurs "Unknown interaction"
  }
};

export const isPaused = (): boolean => {
  return session ? !session.player.state.status : false;
};
export function isYouTubePlaylist(url: string): boolean {
  return ytpl.validateID(url);
}

export async function getTracksFromUrl(query: string): Promise<string[]> {
  if (isYouTubePlaylist(query)) {
    return await fetchYouTubePlaylistTracks(query); // à implémenter
  } else {
    const singleUrl = await getTrackUrl(query);
    return singleUrl ? [singleUrl] : [];
  }
}

export async function fetchYouTubePlaylistTracks(
  playlistUrl: string,
): Promise<string[]> {
  if (!ytpl.validateID(playlistUrl)) return [];

  const playlist = await ytpl(playlistUrl, { limit: 100 }); // limite à 100 vidéos max
  return playlist.items.map((item) => item.url);
}

export const handleMusicButton = async (interaction: ButtonInteraction) => {
  if (!session) {
    return interaction.editReply({
      content: "❌ Aucune session musicale en cours.",
    });
  }

  switch (interaction.customId) {
    case "music_toggle":
      if (session.player.state.status === AudioPlayerStatus.Playing) {
        pauseMusic();
      } else {
        resumeMusic();
      }
      await sendMusicPanel(interaction);
      break;
    case "music_next":
      skipMusic();
      break;
    case "music_loop":
      loopMusic();
      await sendMusicPanel(interaction);
      break;
    case "music_queue":
      await sendQueuePanel(interaction);
      break;
    case "music_back_to_now_playing":
      await sendMusicPanel(interaction);
      break;
    case "music_stop":
      stopMusic();
      await interaction.reply({
        content: "🛑 Musique arrêtée et messages supprimés.",
        flags: MessageFlags.Ephemeral,
      });
      break;
    default:
      await interaction.reply({
        content: "❓ Bouton inconnu.",
        flags: MessageFlags.Ephemeral,
      });
  }
};

export const sendQueuePanel = async (interaction: ButtonInteraction) => {
  const row = new ActionRowBuilder<ButtonBuilder>().addComponents(
    new ButtonBuilder()
      .setCustomId("music_back_to_now_playing")
      .setLabel("🎵 En cours")
      .setStyle(ButtonStyle.Secondary),
  );

  if (!session || session.queue.length === 0) {
    interaction.message
      .edit({
        content: "📭 La file d'attente est vide.",
        embeds: [],
        components: [row],
      })
      .catch(() => {});
    return;
  }

  // Génère la description avec une limite de 3000 caractères
  const lines: string[] = [];
  let totalLength = 0;

  for (let i = 0; i < session.queue.length; i++) {
    const line = `${i + 1}. ${session.queue[i].title} — ${session.queue[i].author}`;
    if (totalLength + line.length + 1 > 3000) {
      lines.push("...");
      break;
    }
    lines.push(line);
    totalLength += line.length + 1;
  }

  const embed = new EmbedBuilder()
    .setTitle("📃 File d’attente")
    .setColor("#1DB954")
    .setDescription(lines.join("\n"));

  interaction.message
    .edit({
      content: "",
      embeds: [embed],
      components: [row],
    })
    .catch(() => {});

  await interaction.deferUpdate(); // évite l’erreur d’interaction expirée
};

export const updateMessages = async () => {
  if (!session || !session.actualTrack) return;

  const track = session.actualTrack;
  const embed = new EmbedBuilder()
    .setTitle("🎵 Musique en cours")
    .addFields(
      { name: "Titre", value: track.title },
      { name: "Auteur", value: track.author },
    )
    .setColor("#1DB954")
    .setFooter({
      text: isLoopMusic
        ? "🔁 En boucle"
        : `⏭ prochaine musique ${session.queue.length > 0 ? session.queue[0].title : "aucune"}`,
    });

  const buttons = new ActionRowBuilder<ButtonBuilder>().addComponents(
    new ButtonBuilder()
      .setCustomId("music_stop")
      .setLabel("stop")
      .setStyle(ButtonStyle.Danger),
    new ButtonBuilder()
      .setCustomId("music_toggle")
      .setLabel(session.playing ? "⏸ Pause" : "▶️ Lecture")
      .setStyle(ButtonStyle.Primary),
    new ButtonBuilder()
      .setCustomId("music_next")
      .setLabel("⏭ Suivant")
      .setStyle(ButtonStyle.Secondary),
    new ButtonBuilder()
      .setCustomId("music_queue")
      .setLabel("📃 Liste")
      .setStyle(ButtonStyle.Secondary),
    new ButtonBuilder()
      .setCustomId("music_loop")
      .setLabel(isLoopMusic ? "🔁 Boucle: ON" : "🔁 Boucle: OFF")
      .setStyle(ButtonStyle.Success),
  );

  for (const msg of activeMessages) {
    msg.edit({ embeds: [embed], components: [buttons] }).catch(console.error);
  }
};
