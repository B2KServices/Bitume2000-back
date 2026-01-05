import { REST, Routes } from "discord.js";
import config from "@/src/configs/config";
import { logError, logInfo } from "@/src/middlewares";

const commands = [
  {
    name: "players",
    description: "Récupérer la liste des joueurs sur bitumemc",
  },
  {
    name: "tps",
    description: "Récupérer le TPS du serveur",
  },
  {
    name: "play",
    description: "Jouer de la musique",
    options: [
      {
        name: "recherche",
        type: 3,
        description: "URL de la musique à jouer ou recherche",
        required: false,
      },
    ],
  },
  {
    name: "clear",
    description: "Supprimer les messages en masse",
    options: [
      {
        name: "nombre",
        type: 4,
        description: "Nombre de messages à supprimer",
        required: true,
      },
      {
        name: "utilisateur",
        type: 6,
        description: "ID de l'utilisateur dont les messages seront supprimés",
        required: false,
      },
    ],
  },
];

export const registerCommands = async () => {
  const rest = new REST({ version: "10" }).setToken(config.DISCORD_TOKEN);

  try {
    logInfo("Started refreshing application (/) commands.", {
      context: "Commands",
    });

    await rest.put(Routes.applicationCommands(config.DISCORD_CLIENT_ID), {
      body: commands,
    });

    logInfo("Successfully reloaded application (/) commands.", {
      context: "Commands",
    });
  } catch (error) {
    logError(`Error registering commands: ${error}`, { context: "Commands" });
  }
};
