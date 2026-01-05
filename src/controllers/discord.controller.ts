import { Request, Response } from "express";
import { sendMessageToChannel } from "@/src/services/discord.service";
import { HttpStatusCode } from "axios";

export const sendChat = async (req: Request, res: Response) => {
  const { content, channelId, username } = req.body;
  await sendMessageToChannel(content, channelId, username);
  res.sendStatus(HttpStatusCode.NoContent);
};
