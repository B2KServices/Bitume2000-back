import { Options, Sequelize } from "sequelize";
import config from "~/configs/config";
import pg from "pg";

const createDatabase = () => {
  let instance: null | Sequelize = null;

  const options: Options = {
    host: config.PG_HOST,
    port: config.PG_PORT || 5432,
    password: config.PG_PASS,
    dialect: "postgres",
    logging: false,
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000,
    },
  };

  const getInstance = () => {
    if (!instance) {
      pg.types.setTypeParser(20, (value: any) => parseInt(value, 10));
      pg.types.setTypeParser(
        1114,
        (str: string) => new Date(str.split(" ").join("T") + "Z"),
      );
      instance = new Sequelize(
        config.PG_DATABASE,
        config.PG_USER,
        config.PG_PASS,
        options,
      );
    }
    return instance;
  };

  return { getInstance };
};

const database = createDatabase();
export const sequelize = database.getInstance();
