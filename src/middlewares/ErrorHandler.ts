import { ErrorRequestHandler } from "express";
import { CustomError } from "@/src/errors";
import { logError } from "@/src/middlewares/Logger";

const ErrorHandler: ErrorRequestHandler = (err, req, res, _next) => {
  if (res) {
    if (err instanceof CustomError) {
      return res.status(err.statusCode).json({
        status: err.status,
        message: err.message,
      });
    }

    logError(err);

    return res.status(500).json({
      status: "error",
      message: "Internal Server Error",
    });
  } else {
    logError(err);
  }
};

export default ErrorHandler;
