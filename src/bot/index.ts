import { client } from "./client";
import { registerCommands } from "./commands";
import { registerEvents } from "./events";
import config from "~/configs/config";
import { logInfo } from "~/middlewares";

export const startBot = async () => {
  registerEvents();
  await registerCommands();
  await client.login(config.DISCORD_TOKEN);
  logInfo("Discord bot started", {
    context: "Started App",
  });
};
