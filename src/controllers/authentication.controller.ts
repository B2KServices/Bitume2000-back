import { Request, Response } from "express";
import * as authService from "@/src/services/auth.service";
import { HttpStatusCode } from "axios";

export const loginDiscord = async (req: Request, res: Response) => {
  const { username } = req.body;
  const ret = await authService.registerDiscord(username);
  res.cookie("authcookie", ret.token, { maxAge: 900000, httpOnly: true });
  res.status(HttpStatusCode.Ok).json({ user: ret.user });
};
