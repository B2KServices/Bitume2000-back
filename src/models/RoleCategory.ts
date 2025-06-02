import {
  CreationOptional,
  DataTypes,
  InferAttributes,
  InferCreationAttributes,
  Model,
} from "sequelize";
import { RoleModel } from "~/models/Role";
import { sequelize } from "~/loaders";

export interface RoleCategoryModel
  extends Model<
    InferAttributes<RoleCategoryModel>,
    InferCreationAttributes<RoleCategoryModel>
  > {
  roleCategoryId: CreationOptional<string>;
  name: string;
  createdAt: CreationOptional<Date>;
  updatedAt: CreationOptional<Date>;
  color: string;
  roles?: RoleModel[];
}

const RoleCategory = sequelize.define<RoleCategoryModel>(
  "roleCategory",
  {
    roleCategoryId: {
      type: DataTypes.UUID,
      primaryKey: true,
      allowNull: false,
      defaultValue: DataTypes.UUIDV4,
    },
    name: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    color: {
      type: DataTypes.STRING,
      allowNull: true,
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
    tableName: "role_category",
    timestamps: true,
    underscored: true,
    createdAt: "created_at",
    updatedAt: "updated_at",
  },
);

export default RoleCategory;
