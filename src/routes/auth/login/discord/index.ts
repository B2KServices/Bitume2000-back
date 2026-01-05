import { Router } from "express";
import { runAsyncWrapper } from "@/src/middlewares";
import { loginDiscord } from "@/src/controllers/authentication.controller";

const router: Router = Router({ mergeParams: true });

router.post("/", runAsyncWrapper(loginDiscord));

export default router;
