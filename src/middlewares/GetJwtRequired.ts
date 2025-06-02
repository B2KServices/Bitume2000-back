import jwt from "jsonwebtoken";
import config from "~/configs/config";
import { NextFunction, Request, Response } from "express";
import { UnauthorizedError } from "~/errors";

function getJwtRequired(req: Request, res: Response, next: NextFunction): void {
  const token = req.cookies.authcookie;

  if (!token) {
    throw new UnauthorizedError();
  }
  try {
    req.userId = jwt.verify(token, config.JWT_SECRET) as string;
    next();
  } catch (err) {
    res.sendStatus(403);
    return;
  }
}

export default getJwtRequired;
