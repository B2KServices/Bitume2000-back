import { ChatInputCommandInteraction } from "discord.js";
import axios from "axios";
import config from "~/configs/config";

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
