import dotenv from "dotenv";
import * as process from "node:process";

dotenv.config();

interface Config {
  ENV: string;
  APP_PORT: number;
  PG_USER: string;
  PG_PASS: string;
  PG_NAME: string;
  PG_IP: string;
  PG_PORT: number;
  PG_HOST: string;
  PG_DIALECT: string;
  PG_DATABASE: string;
  JWT_SECRET: string;
  DISCORD_TOKEN: string;
  DISCORD_CLIENT_ID: string;
  BITUMEMC_URL: string;
  DISCORD_CHAT_MC_ID: string;
  DISCORD_GUILD_ID: string;
  DISCORD_MEME_CHANNEL_ID: string;
  DISCORD_DUD_MEME_CHANNEL_ID: string;
  DISCORD_BEST_MEME_CHANNEL_ID: string;
  DISCORD_ANNOUNCE_CHANNEL_ID: string;
  MEME_VOTE_REQUIRED: number;
  MEME_VOTE_COOLDOWN: number;
}

const config: Config = {
  ENV: process.env.ENV || "development",
  APP_PORT: Number(process.env.APP_PORT) || 5001,
  PG_USER: process.env.PG_USER || "",
  PG_PASS: process.env.PG_PASS || "",
  PG_NAME: process.env.PG_NAME || "",
  PG_IP: process.env.PG_IP || "",
  PG_PORT: Number(process.env.PG_PORT) || 5432,
  PG_HOST: process.env.PG_HOST || "",
  PG_DIALECT: process.env.PG_DIALECT || "postgres",
  PG_DATABASE: process.env.PG_DATABASE || "",
  JWT_SECRET: process.env.JWT_SECRET || "",
  DISCORD_TOKEN: process.env.DISCORD_TOKEN || "",
  DISCORD_CLIENT_ID: process.env.DISCORD_CLIENT_ID || "",
  BITUMEMC_URL: process.env.BITUMEMC_URL || "",
  DISCORD_CHAT_MC_ID: process.env.DISCORD_CHAT_MC_ID || "",
  DISCORD_GUILD_ID: process.env.DISCORD_GUILD_ID || "",
  DISCORD_MEME_CHANNEL_ID: process.env.DISCORD_MEME_CHANNEL_ID || "",
  DISCORD_DUD_MEME_CHANNEL_ID: process.env.DISCORD_DUD_MEME_CHANNEL_ID || "",
  DISCORD_BEST_MEME_CHANNEL_ID: process.env.DISCORD_BEST_MEME_CHANNEL_ID || "",
  DISCORD_ANNOUNCE_CHANNEL_ID: process.env.DISCORD_ANNOUNCE_CHANNEL_ID || "",
  MEME_VOTE_REQUIRED: Number(process.env.MEME_VOTE_REQUIRED) || 5,
  MEME_VOTE_COOLDOWN: Number(process.env.MEME_VOTE_COOLDOWN) || 60, // in seconds
};

export default config;
