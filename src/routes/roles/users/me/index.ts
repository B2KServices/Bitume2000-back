import { Router } from "express";
import { runAsyncWrapper } from "~/middlewares";
import getJwtRequired from "~/middlewares/GetJwtRequired";
import { getMyRoles, updateMyRoles } from "~/controllers/roles.controller";

const router: Router = Router({ mergeParams: true });

router.get("/", getJwtRequired, runAsyncWrapper(getMyRoles));
router.post("/", getJwtRequired, runAsyncWrapper(updateMyRoles));

export default router;
