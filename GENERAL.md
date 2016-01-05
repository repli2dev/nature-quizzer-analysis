- Number of users having at least one answer:
    SELECT COUNT(DISTINCT id_user) FROM answer JOIN round USING (id_round) WHERE main = TRUE

- Number of registered users.
    SELECT COUNT(id_user) FROM user WHERE anonymous = FALSE

- Number of registered users via external logins.
    SELECT COUNT(id_user) FROM user WHERE anonymous = FALSE AND password IS NULL

- Number of questions in total:
    SELECT COUNT(*) FROM answer WHERE main = TRUE

- Number of question by type:
    SELECT COUNT(*) FROM answer WHERE main = TRUE GROUP BY question_type;
    
- Success rate per day
    SELECT
        inserted::DATE,
        COUNT(*) AS all,
        COUNT(NULLIF(NOT (SELECT bool_and(correct) FROM answer AS distractor WHERE distractor.id_round = answer.id_round AND answer.question_seq_num = distractor.question_seq_num AND distractor.main = FALSE), TRUE)) AS correct
    FROM answer
    WHERE main = TRUE
    GROUP BY inserted::DATE
    ORDER BY inserted::DATE
    
-- Success by type of question
    SELECT
        question_type,
        COUNT(*) AS all,
        COUNT(NULLIF(NOT (SELECT bool_and(correct) FROM answer AS distractor WHERE distractor.id_round = answer.id_round AND answer.question_seq_num = distractor.question_seq_num AND distractor.main = FALSE), TRUE)) AS correct,
        COUNT(NULLIF(NOT (SELECT bool_and(correct) FROM answer AS distractor WHERE distractor.id_round = answer.id_round AND answer.question_seq_num = distractor.question_seq_num AND distractor.main = FALSE), TRUE))::FLOAT/COUNT(*)::FLOAT AS ratio
    FROM answer
    WHERE main = TRUE
    GROUP BY answer.question_type
    
-- Time informations (interesting to group by time)
    SELECT MAX((extra->>'time')::FLOAT), AVG((extra->>'time')::FLOAT), MIN((extra->>'time')::FLOAT)  FROM answer WHERE (extra->>'time') != ''
    SELECT *  FROM answer WHERE (extra->>'time') != '' AND (extra->>'time')::FLOAT >= 60000;
    
-- Number of answers grouped by topics since the moment of having two (to be comparable)
    SELECT
    id_concept,
    COUNT(*)
    FROM "answer"
    JOIN organism_concept USING(id_organism)
    WHERE main = TRUE AND inserted > TIMESTAMP '2015-11-30'
    GROUP BY (id_concept)