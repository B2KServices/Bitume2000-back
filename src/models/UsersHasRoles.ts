import {
  CreationOptional,
  DataTypes,
  InferAttributes,
  InferCreationAttributes,
  Model,
} from "sequelize";
import { sequelize } from "@/src/loaders";

export interface UsersHasRolesModel
  extends Model<
    InferAttributes<UsersHasRolesModel>,
    InferCreationAttributes<UsersHasRolesModel>
  > {
  usersHasRolesId: CreationOptional<string>;
  userId: string;
  roleId: string;
  createdAt: CreationOptional<Date>;
  updatedAt: CreationOptional<Date>;
}

const UsersHasRoles = sequelize.define<UsersHasRolesModel>(
  "users_has_roles",
  {
    usersHasRolesId: {
      type: DataTypes.UUID,
      defaultValue: DataTypes.UUIDV4,
      allowNull: false,
      primaryKey: true,
    },
    userId: {
      type: DataTypes.UUID,
      allowNull: false,
      field: "user_id",
    },
    roleId: {
      type: DataTypes.UUID,
      allowNull: false,
      field: "role_id",
    },
    createdAt: {
      type: DataTypes.DATE,
      allowNull: false,
      defaultValue: DataTypes.NOW,
      field: "created_at",
    },
    updatedAt: {
      type: DataTypes.DATE,
      allowNull: false,
      defaultValue: DataTypes.NOW,
      field: "updated_at",
    },
  },
  {
    tableName: "users_has_roles",
    timestamps: true,
    underscored: true,
  },
);

export default UsersHasRoles;
