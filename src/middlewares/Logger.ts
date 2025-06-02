import { addColors, createLogger, format, transports } from "winston";
import dayjs from "dayjs";

const { combine, printf, colorize } = format;

// Définir les couleurs personnalisées pour chaque niveau
const customColors = {
  info: "green",
  warn: "yellow",
  error: "red",
  debug: "magenta",
  prod: "white", // couleur personnalisée pour le niveau 'prod' si utilisé
};

// Appliquer les couleurs personnalisées
addColors(customColors);

// Formatter personnalisé avec couleur
const customLog = printf(({ level, message }) => {
  const logTime = dayjs().format("HH:mm:ss");
  return `[${level} ${logTime}]: ${message}`;
});

const customLevels = {
  prod: 0,
  warn: 1,
  error: 2,
  info: 3,
  debug: 4,
};

export const logger = createLogger({
  levels: customLevels,
  format: combine(
    colorize({ all: true }), // Active la coloration sur tout le message
    customLog,
  ),
  transports: [new transports.Console()],
  exitOnError: false,
});

export const logError = (message: any) => {
  logger.log("error", message);
};

export const logInfo = (message: any) => {
  logger.log("info", message);
};

export const logWarn = (message: any) => {
  logger.log("warn", message);
};

export const logDebug = (message: any) => {
  logger.log("debug", message);
};
