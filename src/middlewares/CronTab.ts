import cron from "node-cron";
import {
  sendMessageToChannel,
  synchronizeDiscordData,
} from "~/services/discord.service";
import { logError, logInfo } from "~/middlewares/Logger";
import config from "~/configs/config";

export const midnightCron = () => {
  cron.schedule("0 0 * * *", async () => {
    logInfo("Running midnight task");
    try {
      await synchronizeDiscordData();
    } catch (error) {
      logError(`Error synchronizing Discord: ${error}`);
    }
  });
};

let wplaceIsUpStatus = true;

export const scheduleWplaceHealthCheck = () => {
  cron.schedule("*/1 * * * *", async () => {
    try {
      const response = await fetch("https://backend.wplace.live/health");
      const isUp = response.ok;

      if (isUp && !wplaceIsUpStatus) {
        logInfo("Wplace is up");
        await sendMessageToChannel(
          "Wplace is up",
          config.DISCORD_ANNOUNCE_CHANNEL_ID,
        );
      } else if (!isUp && wplaceIsUpStatus) {
        logError("Wplace is down");
        await sendMessageToChannel(
          "Wplace is down",
          config.DISCORD_ANNOUNCE_CHANNEL_ID,
        );
      }

      wplaceIsUpStatus = isUp;
    } catch (error) {
      if (wplaceIsUpStatus) {
        logError(`Wplace is down (network error): ${error}`);
        await sendMessageToChannel(
          "Wplace is down",
          config.DISCORD_ANNOUNCE_CHANNEL_ID,
        );
      }
      wplaceIsUpStatus = false;
    }
  });
};

export const schedule = () => {
  logInfo("Scheduling cron jobs");
  midnightCron();
  scheduleWplaceHealthCheck();
};
