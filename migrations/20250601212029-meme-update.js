"use strict";
const { Sequelize } = require("sequelize");

/** @type {import('sequelize-cli').Migration} */
module.exports = {
  async up(queryInterface) {
    await queryInterface.context.addColumn("user", "meme_last_vote", {
      type: Sequelize.DATE,
      allowNull: true,
      defaultValue: null,
    });
    await queryInterface.context.createTable("meme", {
      meme_id: {
        type: Sequelize.UUID,
        allowNull: false,
        unique: true,
        primaryKey: true,
        defaultValue: Sequelize.literal("gen_random_uuid()"),
      },
      votes: {
        type: Sequelize.INTEGER,
        allowNull: false,
      },
      author_id: {
        type: Sequelize.UUID,
        allowNull: false,
        references: {
          model: "user",
          key: "user_id",
        },
      },
      discord_id: {
        type: Sequelize.STRING,
        allowNull: false,
      },
      meme_type: {
        type: Sequelize.INTEGER,
        allowNull: false,
        defaultValue: 0,
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
