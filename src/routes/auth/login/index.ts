import { Router } from "express";
import discord from "./discord";

const router: Router = Router({ mergeParams: true });

router.use("/discord", discord);

export default router;
