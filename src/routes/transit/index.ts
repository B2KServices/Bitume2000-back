import { Router } from "express";
import { runAsyncWrapper } from "@/src/middlewares";
import { getNextBus } from "@/src/controllers/transit.controller";

const router: Router = Router({ mergeParams: true });

router.get("/next-bus", runAsyncWrapper(getNextBus));

export default router;
