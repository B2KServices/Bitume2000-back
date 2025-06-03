import {
  CreationOptional,
  DataTypes,
  InferAttributes,
  InferCreationAttributes,
  Model,
} from "sequelize";
import { sequelize } from "~/loaders";
import { MemeType } from "~/types";

export interface MemeModel
  extends Model<
    InferAttributes<MemeModel>,
    InferCreationAttributes<MemeModel>
  > {
  memeId: CreationOptional<string>;
  authorId: CreationOptional<string>;
  discordId: string;
  memeType: CreationOptional<MemeType>;
  votes: number;
  createdAt: CreationOptional<Date>;
  updatedAt: CreationOptional<Date>;
}

const Meme = sequelize.define<MemeModel>(
  "meme",
  {
    memeId: {
      type: DataTypes.UUID,
      primaryKey: true,
      allowNull: false,
      defaultValue: DataTypes.UUIDV4,
    },
    votes: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: 0,
    },
    authorId: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    discordId: {
      type: DataTypes.STRING,
      allowNull: false,
    },
    memeType: {
      type: DataTypes.INTEGER,
      allowNull: false,
      defaultValue: MemeType.IN_PROGRESS,
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
    tableName: "meme",
    timestamps: true,
    underscored: true,
    createdAt: "created_at",
    updatedAt: "updated_at",
  },
);

export default Meme;
