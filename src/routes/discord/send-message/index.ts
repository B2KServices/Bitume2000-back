import { Router } from "express";
import { runAsyncWrapper } from "~/middlewares";
import { sendChat } from "~/controllers/discord.controller";

const router: Router = Router({ mergeParams: true });

router.post("/", runAsyncWrapper(sendChat));

export default router;
