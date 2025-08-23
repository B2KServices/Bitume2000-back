import { User } from "~/models";
import { UnauthorizedError } from "~/errors";
import { sendPrivateMessage } from "~/services/discord.service";
import { ActionRowBuilder, ButtonBuilder, ButtonStyle } from "discord.js";
import { UserModel } from "~/models/User";
import jwt from "jsonwebtoken";
import config from "~/configs/config";
import { logInfo } from "~/middlewares";

export const userInAuth: { userId: string; approved: boolean }[] = [];
export const generateJWT = (userId: string): string => {
  return jwt.sign(userId, config.JWT_SECRET);
};

export const registerDiscord = async (
  username: string,
): Promise<{ user: UserModel; token: string }> => {
  const user = await User.findOne({
    where: {
      username,
    },
  });
  if (!user) throw new UnauthorizedError();
  const userId = user.userId;
  logInfo(`User ${username} is trying to authenticate`, {
    context: "Auth Service",
    userId,
  });
  const message = `Bonjour, ${user.username} !\nUne demande de connexion a été faites merci d'approuver la demande pour continuer.\nSi vous n'êtes pas à l'origine de cette demande, veuillez ignorer ce message.`;
  const approveButton = new ButtonBuilder({
    customId: `approve_auth;${userId}`,
    label: "Approuver",
    style: ButtonStyle.Success,
  });
  const actions = new ActionRowBuilder().addComponents(approveButton);
  const messageIsSent = await sendPrivateMessage(userId, message, actions);
  if (!messageIsSent) throw new UnauthorizedError("Failed to send message");
  userInAuth.push({ userId, approved: false });
  let i = 0;
  while (i < 30) {
    const userAuth = userInAuth.find((u) => u.userId === userId);
    if (userAuth && userAuth.approved) {
      userInAuth.filter((u) => u.userId !== userId);
      return { user, token: generateJWT(userId) };
    }
    await new Promise((resolve) => setTimeout(resolve, 1000));
    i++;
  }
  throw new UnauthorizedError();
};
