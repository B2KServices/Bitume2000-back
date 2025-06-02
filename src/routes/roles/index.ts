import { Router } from "express";
import categories from "./categories";
import users from "./users";

const router: Router = Router({ mergeParams: true });

router.use("/categories", categories);
router.use("/users", users);

export default router;
