import { Router } from "express";
import { runAsyncWrapper } from "~/middlewares";
import { getNextBus } from "~/controllers/transit.controller";

const router: Router = Router({ mergeParams: true });

router.get("/:stopId", runAsyncWrapper(getNextBus));

export default router;
