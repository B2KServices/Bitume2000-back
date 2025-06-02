import {
  CreationOptional,
  DataTypes,
  InferAttributes,
  InferCreationAttributes,
  Model,
} from "sequelize";
import { sequelize } from "~/loaders";
import { RoleCategoryModel } from "~/models/RoleCategory";

export interface RoleModel
  extends Model<
    InferAttributes<RoleModel>,
    InferCreationAttributes<RoleModel>
  > {
  roleId: CreationOptional<string>;
  discordId: string;
  name: string;
  roleCategoryId: string;
  color: string;
  roleCategory?: RoleCategoryModel;
}

const Role = sequelize.define<RoleModel>(
  "role",
  {
    roleId: {
      type: DataTypes.UUID,
      primaryKey: true,
      allowNull: false,
      defaultValue: DataTypes.UUIDV4,
    },
    discordId: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    name: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    roleCategoryId: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    color: {
      type: DataTypes.STRING,
      allowNull: true,
    },
  },
  {
    tableName: "role",
    timestamps: true,
    underscored: true,
    createdAt: "created_at",
    updatedAt: "updated_at",
  },
);

export default Role;
