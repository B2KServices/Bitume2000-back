import { sequelize } from "~/loaders";
import {
  CreationOptional,
  DataTypes,
  InferAttributes,
  InferCreationAttributes,
  Model,
} from "sequelize";
import { RoleModel } from "~/models/Role";

export interface UserModel
  extends Model<
    InferAttributes<UserModel>,
    InferCreationAttributes<UserModel>
  > {
  userId: CreationOptional<string>;
  username: string;
  password: CreationOptional<string>;
  discordId: string;
  avatarUrl: CreationOptional<string>;
  legendaryMeme: CreationOptional<number>;
  dudMeme: CreationOptional<number>;
  createdAt: CreationOptional<Date>;
  updatedAt: CreationOptional<Date>;
  roles?: RoleModel[];
  memeLastVote: CreationOptional<Date>;
}

const User = sequelize.define<UserModel>(
  "user",
  {
    userId: {
      type: DataTypes.UUID,
      primaryKey: true,
      allowNull: false,
      defaultValue: DataTypes.UUIDV4,
    },
    username: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    password: {
      type: DataTypes.STRING,
      allowNull: true,
    },
    discordId: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    avatarUrl: {
      type: DataTypes.STRING,
      allowNull: true,
    },
    legendaryMeme: {
      type: DataTypes.INTEGER,
      allowNull: true,
      defaultValue: 0,
    },
    dudMeme: {
      type: DataTypes.INTEGER,
      allowNull: true,
      defaultValue: 0,
    },
    memeLastVote: {
      type: DataTypes.DATE,
      allowNull: true,
      defaultValue: null,
    },
    createdAt: {
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW,
      allowNull: false,
    },
    updatedAt: {
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW,
      allowNull: false,
    },
  },
  {
    tableName: "user",
    timestamps: true,
    underscored: true,
    createdAt: "created_at",
    updatedAt: "updated_at",
  },
);

export default User;
