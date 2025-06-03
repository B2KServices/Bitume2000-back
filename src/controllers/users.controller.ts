import * as usersService from "../services/users.service";
import { Request, Response } from "express";
import { UnauthorizedError } from "~/errors";

export const getUsers = async (req: Request, res: Response) => {
  const users = await usersService.getUsers();
  res.status(200).json(users);
};

export const getMe = async (req: Request, res: Response) => {
  const userId = req.userId;
  if (!userId) {
    throw new UnauthorizedError("unauthorized");
  }
  const user = await usersService.getMe(userId);
  res.status(200).json(user);
};
