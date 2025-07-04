import { ErrorRequestHandler } from "express";
import { CustomError } from "~/errors";
import { logError } from "~/middlewares/Logger";

const ErrorHandler: ErrorRequestHandler = (err, req, res) => {
  if (res) {
    if (err instanceof CustomError) {
      res.status(err.statusCode).json({
        status: err.status,
        message: err.message,
      });
      return;
    }

    logError(err);

    res.status(500).json({
      status: "error",
      message: "Internal Server Error",
    });
  } else {
    logError(err);
  }
  return;
};

export default ErrorHandler;
