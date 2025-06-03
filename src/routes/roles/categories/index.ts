import { Router } from "express";
import { runAsyncWrapper } from "~/middlewares";
import { getCategories } from "~/controllers/roles.controller";

const router: Router = Router({ mergeParams: true });

router.get("/", runAsyncWrapper(getCategories));

export default router;
