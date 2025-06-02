import { Request, Response } from "express";
import { sendMessageToChannel } from "~/services/discord.service";

export const sendChat = async (req: Request, res: Response) => {
  const { content, channelId } = req.body;
  await sendMessageToChannel(content, channelId);
  res.sendStatus(204);
};
