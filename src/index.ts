import dotenv from "dotenv";
import { createServer } from "http";
import initApp from "./app";
import { logError, logInfo } from "@/src/middlewares";
import config from "@/src/configs/config";
import { startBot } from "@/src/bot";
import { initSocket } from "@/src/loaders/socket";

dotenv.config();

const startServer = async () => {
  try {
    const port = process.env.PORT || 5001;
    const app = await initApp();
    const httpServer = createServer(app);
    initSocket(httpServer);

    httpServer.listen(port, () => {
      logInfo("Server started on port " + config.APP_PORT, {
        context: "Started App",
      });
    });
    await startBot();
  } catch (err) {
    logError(JSON.stringify(err), { context: "Started App" });
    process.exit(1);
  }
};

startServer();
