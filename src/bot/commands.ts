import { REST, Routes } from "discord.js";
import config from "~/configs/config";
import { logError, logInfo } from "~/middlewares";

const commands = [
  {
    name: "players",
    description: "Récupérer la liste des joueurs sur bitumemc",
  },
  {
    name: "tps",
    description: "Récupérer le TPS du serveur",
  },
];

export const registerCommands = async () => {
  const rest = new REST({ version: "10" }).setToken(config.DISCORD_TOKEN);

  try {
    logInfo("Started refreshing application (/) commands.");

    await rest.put(Routes.applicationCommands(config.DISCORD_CLIENT_ID), {
      body: commands,
    });

    logInfo("Successfully reloaded application (/) commands.");
  } catch (error) {
    logError(error);
  }
};
