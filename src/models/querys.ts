import { sequelize } from "@/src/loaders";
import { QueryTypes } from "sequelize";
import { MemeVoteType } from "@/src/types";
import * as console from "node:console";

export const voteQuery = async (
  userId: string,
  memeId: string,
  voteType: MemeVoteType,
) => {
  await sequelize.query(
    `
    INSERT INTO voted_meme (user_id, meme_id, vote_type)
    VALUES (:userId, :memeId, :voteType)
    `,
    {
      replacements: { userId, memeId, voteType },
      type: QueryTypes.INSERT,
    },
  );
};

export const updateVoteQuery = async (
  userId: string,
  memeId: string,
  voteType: MemeVoteType,
) => {
  await sequelize.query(
    `
        UPDATE voted_meme
        SET vote_type = :voteType
        WHERE user_id = :userId AND meme_id = :memeId
        `,
    {
      replacements: { userId, memeId, voteType },
      type: QueryTypes.UPDATE,
    },
  );
};

export const getVotedMemes = async (
  userId: string,
  voteType?: MemeVoteType,
) => {
  console.log("fetching votes for user:", userId, "voteType:", voteType);
  console.log(`
      SELECT m.meme_id AS "memeId"
      FROM voted_meme votes
             JOIN meme m ON m.meme_id = votes.meme_id
      WHERE votes.user_id = :userId ${voteType !== undefined ? "AND votes.vote_type = :voteType" : ""};`);

  return (await sequelize.query(
    `
      SELECT m.meme_id AS "memeId"
      FROM voted_meme votes
             JOIN meme m ON m.meme_id = votes.meme_id
      WHERE votes.user_id = :userId ${voteType !== undefined ? "AND votes.vote_type = :voteType" : ""};`,
    {
      replacements: { userId, voteType },
      type: QueryTypes.SELECT,
    },
  )) as { memeId: string }[];
};

export const getVoteForMeme = async (
  userId: string,
  memeId: string,
): Promise<{ voteType: MemeVoteType } | null> => {
  const result = await sequelize.query(
    `
    SELECT vote_type AS "voteType"
    FROM voted_meme
    WHERE user_id = :userId AND meme_id = :memeId
    LIMIT 1
    `,
    {
      replacements: { userId, memeId },
      type: QueryTypes.SELECT,
    },
  );

  // result est un tableau de 0 ou 1 élément
  if (result.length > 0) {
    return result[0] as { voteType: MemeVoteType };
  }

  return null;
};
