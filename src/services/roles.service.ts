import { Role, RoleCategory, User, UsersHasRoles } from "@/src/models";
import { BadRequestError, NotFoundError } from "@/src/errors";
import {
  addRoleToUser,
  removeRoleOnUser,
} from "@/src/services/discord.service";
import { logInfo } from "@/src/middlewares";

export const updateMyRoles = async (
  roleId: string,
  isAdd: boolean,
  userId: string,
) => {
  const role = await Role.findOne({
    where: {
      roleId,
    },
  });
  const user = await User.findOne({
    where: {
      userId,
    },
  });

  if (!user) throw new NotFoundError("user not found");
  if (!role) throw new NotFoundError("role not found");
  const userHasRole = await UsersHasRoles.findOne({
    where: { userId, roleId },
  });

  if (isAdd) {
    if (userHasRole != null) throw new BadRequestError("role already gained");
    await addRoleToUser(user.discordId, role.discordId);
    logInfo(`Added role ${role?.name} to user ${user?.username}`, {
      context: "Update My Roles",
      userId: user.userId,
      roleId: role.roleId,
      userDiscordId: user.discordId,
      roleDiscordId: role.discordId,
    });
    return await UsersHasRoles.create({
      userId,
      roleId,
    });
  } else {
    if (!userHasRole) throw new BadRequestError("role already remove");
    logInfo(`Remove role ${role?.name} to user ${user?.username}`, {
      context: "Update My Roles",
      userId: user.userId,
      roleId: role.roleId,
      userDiscordId: user.discordId,
      roleDiscordId: role.discordId,
    });
    await removeRoleOnUser(user.discordId, role.discordId);
    await userHasRole.destroy();
  }
};

export const getCategories = async () => {
  const categories = await RoleCategory.findAll({
    include: ["roles"],
  });
  if (!categories || categories.length === 0) {
    throw new NotFoundError("Categories not found");
  }
  return categories;
};

export const getMyRoles = async (userId: string) => {
  const user = await User.findOne({
    where: { userId },
    include: ["roles"],
  });
  if (!user) {
    throw new NotFoundError("User not found");
  }
  return user.roles;
};
