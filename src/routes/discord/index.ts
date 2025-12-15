import { Router } from "express";
import { runAsyncWrapper } from "@/src/middlewares";
import { getUsers } from "@/src/controllers/users.controller";
import sendMessage from "./send-message";

const router: Router = Router({ mergeParams: true });

router.use("/send-message", sendMessage);
router.get("/", runAsyncWrapper(getUsers));

export default router;
