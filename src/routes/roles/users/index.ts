import { Router } from "express";
import { runAsyncWrapper } from "@/src/middlewares";
import { getUsers } from "@/src/controllers/users.controller";
import me from "./me";

const router: Router = Router({ mergeParams: true });

router.use("/me", me);
router.get("/", runAsyncWrapper(getUsers));

export default router;
