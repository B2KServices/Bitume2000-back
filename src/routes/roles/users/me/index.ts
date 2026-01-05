import { Router } from "express";
import { runAsyncWrapper } from "@/src/middlewares";
import getJwtRequired from "@/src/middlewares/GetJwtRequired";
import { getMyRoles, updateMyRoles } from "@/src/controllers/roles.controller";

const router: Router = Router({ mergeParams: true });

router.get("/", getJwtRequired, runAsyncWrapper(getMyRoles));
router.post("/", getJwtRequired, runAsyncWrapper(updateMyRoles));

export default router;
