"use strict";
const { Sequelize } = require("sequelize");

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface) {
    await queryInterface.context.createTable("voted_meme", {
      voted_meme_id: {
        type: Sequelize.UUID,
        allowNull: false,
        unique: true,
        primaryKey: true,
        defaultValue: Sequelize.literal("gen_random_uuid()"),
      },
      meme_id: {
        type: Sequelize.UUID,
        allowNull: false,
        references: {
          model: "meme",
          key: "meme_id",
        },
      },
      user_id: {
        type: Sequelize.UUID,
        allowNull: false,
        references: {
          model: "user",
          key: "user_id",
        },
      },
      vote_type: {
        type: Sequelize.INTEGER,
        allowNull: false,
        defaultValue: 0, // 0 = upvote, 1 = downvote
      },
      created_at: {
        type: Sequelize.DATE,
        defaultValue: Sequelize.literal("NOW()"),
        allowNull: false,
      },
      updated_at: {
        type: Sequelize.DATE,
        defaultValue: Sequelize.literal("NOW()"),
        allowNull: false,
      },
    });
  },

  async down(queryInterface) {
    /**
     * Add reverting commands here.
     *
     * Example:
     * await queryInterface.dropTable('users');
     */
  },
};
