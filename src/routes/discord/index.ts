import { Router } from "express";
import { runAsyncWrapper } from "~/middlewares";
import { getUsers } from "~/controllers/users.controller";
import sendMessage from "./send-message";

const router: Router = Router({ mergeParams: true });

router.use("/send-message", sendMessage);
router.get("/", runAsyncWrapper(getUsers));

export default router;
