import { NotFoundError } from "@/src/errors";
import { User } from "@/src/models";

export const getMe = async (userId: string) => {
  const user = await User.findOne({ where: { userId: userId } });
  if (!user) throw new NotFoundError("user not found");
  return user;
};

export const getUsers = async () => {
  return await User.findAll();
};
