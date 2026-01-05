import cron from "node-cron";
import { synchronizeDiscordData } from "@/src/services/discord.service";
import { logError, logInfo } from "@/src/middlewares/Logger";

export const midnightCron = () => {
  cron.schedule("0 0 * * *", async () => {
    logInfo("Running task at midnight", {
      context: "cron",
    });
    try {
      await synchronizeDiscordData();
    } catch (error) {
      logError(`Erreur lors de la synchronisation Discord : ${error}`);
    }
  });
};

export const schedule = () => {
  logInfo("Scheduling cron job", {
    context: "cron",
  });
  midnightCron();
};
