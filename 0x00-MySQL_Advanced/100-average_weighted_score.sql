-- A stored procedure ComputeAverageWeightedScoreForUser that
-- computes and store the average weighted score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser (user_id INT)
BEGIN
    DECLARE tw_score INT DEFAULT 0;
    DECLARE tw INT DEFAULT 0;

    SELECT SUM(corrections.score * projects.weight)
        INTO tw_score
        FROM corrections
            INNER JOIN projects
                ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

    SELECT SUM(projects.weight)
        INTO tw
        FROM corrections
            INNER JOIN projects
                ON corrections.project_id = projects.id
        WHERE corrections.user_id = user_id;

    IF tw = 0 THEN
        UPDATE users
            SET users.average_score = 0
            WHERE users.id = user_id;
    ELSE
        UPDATE users
            SET users.average_score = tw_score / tw
            WHERE users.id = user_id;
    END IF;
END $$
DELIMITER ;