import User from "./User";
import Role from "./Role";
import RoleCategory from "./RoleCategory";
import RoleRequest from "./RoleRequest";
import UsersHasRoles from "./UsersHasRoles";
import Meme from "./Meme";

// ----------- OTM Relationships -----------

// RoleCategory → Role
RoleCategory.hasMany(Role, {
  foreignKey: "roleCategoryId",
  as: "roles",
});
Role.belongsTo(RoleCategory, {
  foreignKey: "roleCategoryId",
  as: "roleCategory",
});

// RoleCategory → RoleRequest
RoleCategory.hasMany(RoleRequest, {
  foreignKey: "roleCategoryId",
  as: "roleRequests",
});
RoleRequest.belongsTo(RoleCategory, {
  foreignKey: "roleCategoryId",
  as: "roleCategory",
});

// User → RoleRequest
User.hasMany(RoleRequest, {
  foreignKey: "userId",
  as: "roleRequests",
});
RoleRequest.belongsTo(User, {
  foreignKey: "userId",
  as: "user",
});

// ----------- MTM Relationship -----------

// User ⇄ Role via UsersHasRoles
User.belongsToMany(Role, {
  through: UsersHasRoles,
  foreignKey: "userId",
  otherKey: "roleId",
  as: "roles",
});

Role.belongsToMany(User, {
  through: UsersHasRoles,
  foreignKey: "roleId",
  otherKey: "userId",
  as: "users",
});

// Meme → User
User.hasMany(Meme, {
  foreignKey: "authorId",
  as: "memes",
});

Meme.belongsTo(User, {
  foreignKey: "authorId",
  as: "user",
});

export { User, Role, RoleCategory, RoleRequest, UsersHasRoles, Meme };
