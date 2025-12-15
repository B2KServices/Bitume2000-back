import jwt from "jsonwebtoken";
import config from "@/src/configs/config";
import { NextFunction, Request, Response } from "express";
import { UnauthorizedError } from "@/src/errors";

function getJwtRequired(req: Request, res: Response, next: NextFunction): void {
  const token = req.cookies.authcookie;

  if (!token) {
    throw new UnauthorizedError();
  }
  try {
    req.userId = jwt.verify(token, config.JWT_SECRET) as string;
    next();
  } catch {
    res.sendStatus(403);
    return;
  }
}

export default getJwtRequired;
