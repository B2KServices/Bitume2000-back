import winston, { createLogger, error, format, transports } from "winston";
import dayjs from "dayjs";
import LokiTransport from "winston-loki";
import config from "@/src/configs/config";
import { version } from "@/package.json";

const { combine, printf, colorize } = format;

// --- Transport Loki ---
const lokiTransport = new LokiTransport({
  host: config.LOKI_URL,
  labels: { app: "Bitume-Connect", env: config.ENV, version: version },
  headers: {
    "X-API-Key": config.LOKI_AUTH_KEY,
  },
  replaceTimestamp: true,
});

// --- Logger dédié Loki ---
const lokiLogger = createLogger({
  transports: [lokiTransport],
});

// --- Niveaux et couleurs console ---
const customLevels = lokiLogger.levels;

winston.addColors({
  info: "green",
  warn: "yellow",
  error: "red",
  debug: "magenta",
  prod: "white",
});

// --- Format console ---
const consoleFormat = printf(({ level, message }) => {
  const logTime = dayjs().format("HH:mm:ss");
  return `[${level} ${logTime}]: ${message}`;
});

// --- Logger console ---
export const logger = createLogger({
  levels: customLevels,
  format: combine(colorize({ all: true }), consoleFormat),
  transports: [new transports.Console()],
  exitOnError: false,
});

export const logError = (message: string, labels = {}) => {
  lokiLogger.error(message, { labels });
  logger.error(JSON.stringify(error));
};

export const logWarn = (message: string, labels = {}) => {
  lokiLogger.warn(message, { labels });
  logger.warn(message);
};

export const logInfo = (message: string, labels = {}) => {
  lokiLogger.info(message, { labels });
  logger.info(message);
};

export const logDebug = (message: string, labels = {}) => {
  lokiLogger.debug(message, { labels });
  logger.debug(message);
};
