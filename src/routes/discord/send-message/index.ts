import { Router } from "express";
import { runAsyncWrapper } from "@/src/middlewares";
import { sendChat } from "@/src/controllers/discord.controller";

const router: Router = Router({ mergeParams: true });

router.post("/", runAsyncWrapper(sendChat));

export default router;
