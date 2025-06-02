import { Router } from "express";
import { runAsyncWrapper } from "~/middlewares/AsyncWrapper";
import { getHealthCheck } from "~/controllers/healthCheck.controller";
import users from "./users";
import auth from "./auth";
import roles from "./roles";
import discord from "./discord";

const router: Router = Router({ mergeParams: true });

router.use("/users", users);
router.use("/auth", auth);
router.use("/roles", roles);
router.use("/discord", discord);
router.get("/", runAsyncWrapper(getHealthCheck));

export default router;
