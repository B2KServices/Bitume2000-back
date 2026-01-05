import { Router } from "express";
import { runAsyncWrapper } from "@/src/middlewares";
import { getMe } from "@/src/controllers/users.controller";
import getJwtRequired from "@/src/middlewares/GetJwtRequired";

const router: Router = Router({ mergeParams: true });

router.get("/", getJwtRequired, runAsyncWrapper(getMe));

export default router;
