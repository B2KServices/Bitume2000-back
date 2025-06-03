import { Router } from "express";
import { runAsyncWrapper } from "~/middlewares";
import { getUsers } from "~/controllers/users.controller";
import me from "./me";

const router: Router = Router({ mergeParams: true });

router.use("/me", me);
router.get("/", runAsyncWrapper(getUsers));

export default router;
