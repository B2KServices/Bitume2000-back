import { Router } from "express";
import { runAsyncWrapper } from "~/middlewares";
import { getMe } from "~/controllers/users.controller";
import getJwtRequired from "~/middlewares/GetJwtRequired";

const router: Router = Router({ mergeParams: true });

router.get("/", getJwtRequired, runAsyncWrapper(getMe));

export default router;
