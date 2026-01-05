import { UnauthorizedError } from "@/src/errors";
import { Request, Response } from "express";
import { HttpStatusCode } from "axios";
import * as rolesService from "@/src/services/roles.service";

export const getCategories = async (req: Request, res: Response) => {
  const categories = await rolesService.getCategories();
  res.status(HttpStatusCode.Ok).json(categories);
};

export const getMyRoles = async (req: Request, res: Response) => {
  const userId = req.userId;
  if (!userId) {
    throw new UnauthorizedError();
  }
  const roles = await rolesService.getMyRoles(userId);
  res.status(HttpStatusCode.Ok).json(roles);
};

export const updateMyRoles = async (req: Request, res: Response) => {
  const userId = req.userId;
  const { roleId, isAdd } = req.body;
  if (!userId) {
    throw new UnauthorizedError();
  }
  await rolesService.updateMyRoles(roleId, isAdd, userId);
  res.sendStatus(HttpStatusCode.NoContent);
};
