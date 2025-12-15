import {
  CreationOptional,
  DataTypes,
  InferAttributes,
  InferCreationAttributes,
  Model,
} from "sequelize";
import { sequelize } from "@/src/loaders";
import RoleCategory from "@/src/models/RoleCategory";
import User from "@/src/models/User";

export interface RoleRequestModel
  extends Model<
    InferAttributes<RoleRequestModel>,
    InferCreationAttributes<RoleRequestModel>
  > {
  roleRequestId: CreationOptional<string>;
  name: string;
  userId: string;
  roleCategoryId: string;
  createdAt: CreationOptional<Date>;
  updatedAt: CreationOptional<Date>;
}

const RoleRequest = sequelize.define<RoleRequestModel>(
  "role_request",
  {
    roleRequestId: {
      type: DataTypes.UUID,
      primaryKey: true,
      allowNull: false,
      defaultValue: DataTypes.UUIDV4,
    },
    roleCategoryId: {
      type: DataTypes.UUID,
      allowNull: false,
      references: {
        model: RoleCategory,
        key: "roleCategoryId",
      },
    },
    userId: {
      type: DataTypes.UUID,
      allowNull: false,
      references: {
        model: User,
        key: "userId",
      },
    },
    name: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    createdAt: {
      type: DataTypes.DATE,
      allowNull: false,
    },
    updatedAt: {
      type: DataTypes.DATE,
      allowNull: false,
    },
  },
  {
    tableName: "role_request",
    timestamps: true,
    underscored: true,
    createdAt: "created_at",
    updatedAt: "updated_at",
  },
);

export default RoleRequest;
