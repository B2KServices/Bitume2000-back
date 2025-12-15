import { Request, Response, NextFunction } from "express";

export const runAsyncWrapper = (callback) => {
  return (req: Request, res: Response, next: NextFunction) => {
    callback(req, res, next).catch(next);
  };
};
