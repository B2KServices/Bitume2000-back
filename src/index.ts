import dotenv from "dotenv";
import { createServer } from "http";
import initApp from "./app";
import { logInfo } from "~/middlewares";
import config from "~/configs/config";
import { startBot } from "~/bot";
import { initSocket } from "~/loaders/socket";

dotenv.config();

const startServer = async () => {
  try {
    const port = process.env.PORT || 5001;
    const app = await initApp();
    const httpServer = createServer(app);
    initSocket(httpServer);

    httpServer.listen(port, () => {
      logInfo("Server started on port " + config.APP_PORT);
    });
    await startBot();
  } catch (err) {
    console.error(err);
    process.exit(1);
  }
};

startServer();
