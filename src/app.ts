import "module-alias/register";
import cors from "cors";
import express, { Application } from "express";
import allRoutes from "./routes";
import { logDebug } from "~/middlewares/Logger";
import { SequelizeStorage, Umzug } from "umzug";
import { sequelize } from "~/loaders";
import * as console from "node:console";
import errorHandler from "~/middlewares/ErrorHandler";
import morgan from "morgan";
import bodyParser from "body-parser";
import cookieParser from "cookie-parser";

declare module "express" {
  interface Request {
    userId?: string;
  }
}
const app = express();

const corsOption = {
  origin: true,
  methods: "GET,HEAD,PUT,PATCH,POST,DELETE,OPTIONS",
  credentials: true,
  exposedHeaders: ["x-auth-token"],
};

app.use(morgan("dev"));
app.use(express.json());
app.use((req, res, next) => {
  req.app.locals.config = {};
  next();
});
app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "X-Requested-With");
  res.header("Access-Control-Allow-Headers", "Content-Type");
  res.header("Access-Control-Allow-Methods", "PUT, GET, POST, DELETE, OPTIONS");
  next();
});
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(cookieParser());
app.use(express.json({ limit: "10mb" })); // for parsing application/json
app.use(cors(corsOption));

app.use("/api", allRoutes);

app.use(errorHandler);
export default async (): Promise<Application> => {
  const umzugMigration = new Umzug({
    migrations: { glob: "migrations/*.js" },
    context: sequelize.getQueryInterface(),
    storage: new SequelizeStorage({
      sequelize: sequelize,
      tableName: "sequelize_migration",
      columnName: "name",
    }),
    logger: console,
  });
  const umzugSeeder = new Umzug({
    migrations: { glob: "seeders/*.js" },
    context: sequelize.getQueryInterface(),
    storage: new SequelizeStorage({
      sequelize: sequelize,
      modelName: "sequelize_migration",
      tableName: "sequelize_migration",
      columnName: "name",
    }),
    logger: console,
  });

  try {
    logDebug("[Migration] Starting...");
    await umzugMigration.up();
    await umzugSeeder.up();
    logDebug("[Migration] Up to date.");
  } catch {
    logDebug("[Migration] error");
  }

  return app;
};
