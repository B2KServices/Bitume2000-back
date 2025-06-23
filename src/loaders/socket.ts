// socket.ts
import { Server as HTTPServer } from "http";
import { Server as SocketIOServer } from "socket.io";
import { logInfo } from "~/middlewares";

let io: SocketIOServer;

export const initSocket = (server: HTTPServer) => {
  io = new SocketIOServer(server, {
    cors: {
      origin: "*",
    },
  });

  io.on("connection", (socket) => {
    logInfo(`🧠 WebSocket connecté: ${socket.id}`);

    socket.on("message", (data) => {
      logInfo(`📨 Message reçu: ${data}`);
      socket.emit("message", "Réponse du serveur");
    });

    socket.on("disconnect", () => {
      logInfo(`❌ WebSocket déconnecté: ${socket.id}`);
    });
  });
};

// Pour réutiliser le `io` dans d'autres modules
export const getSocketIO = (): SocketIOServer => io;
