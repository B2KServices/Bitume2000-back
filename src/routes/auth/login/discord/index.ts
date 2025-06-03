import { Router } from "express";
import { runAsyncWrapper } from "~/middlewares";
import { loginDiscord } from "~/controllers/authentication.controller";

const router: Router = Router({ mergeParams: true });

router.post("/", runAsyncWrapper(loginDiscord));

export default router;
