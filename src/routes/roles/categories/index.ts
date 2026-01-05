import { Router } from "express";
import { runAsyncWrapper } from "@/src/middlewares";
import { getCategories } from "@/src/controllers/roles.controller";

const router: Router = Router({ mergeParams: true });

router.get("/", runAsyncWrapper(getCategories));

export default router;
