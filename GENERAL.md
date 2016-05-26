- Number of users having at least one answer:
    SELECT COUNT(DISTINCT id_user) FROM answer JOIN round USING (id_round) WHERE main = TRUE

- Number of registered users.
    SELECT COUNT(id_user) FROM "user" WHERE anonymous = FALSE

- Number of registered users via external logins.
    SELECT COUNT(id_user) FROM "user" WHERE anonymous = FALSE AND password IS NULL

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
    SELECT MAX((extra->>'time')::FLOAT), AVG((extra->>'time')::FLOAT), MIN((extra->>'time')::FLOAT)  FROM answer WHERE (extra->>'time') != '' AND main = TRUE
    SELECT MAX((extra->>'time')::FLOAT), AVG((extra->>'time')::FLOAT), MIN((extra->>'time')::FLOAT)  FROM answer WHERE (extra->>'time') != '' AND main = TRUE GROUP BY question_type
    SELECT *  FROM answer WHERE (extra->>'time') != '' AND (extra->>'time')::FLOAT >= 60000 AND main = TRUE
    
-- Number of answers grouped by topics since the moment of having two (to be comparable)
    SELECT
    id_concept,
    COUNT(*)
    FROM "answer"
    JOIN organism_concept USING(id_organism)
    WHERE main = TRUE AND inserted > TIMESTAMP '2015-11-30'
    GROUP BY (id_concept)
    
-- Number of finished quizzes
    SELECT COUNT(*), c FROM (SELECT id_round, COUNT(*) as C FROM round JOIN answer USING (id_round) WHERE main = TRUE GROUP BY id_round) t
    GROUP BY C

-- Answering time with question type
    SELECT question_type, ROUND(((extra->>'time')::FLOAT))  FROM answer WHERE (extra->>'time') != '' AND main = TRUE
    
-- Distribution of most asked questions
    SELECT
        answer.id_organism,
        organism.latin_name,
        organism_name.name AS name,
                        organism_commonness.value AS value,
        organism_difficulty.value AS difficulty,
        COUNT(*) AS count
    FROM answer
    JOIN organism ON organism.id_organism = answer.id_organism
    JOIN organism_name ON organism_name.id_organism = organism.id_organism AND organism_name.id_language = 1
                JOIN organism_commonness ON organism.id_organism = organism_commonness.id_organism
    LEFT JOIN organism_difficulty ON organism_difficulty.id_organism = organism.id_organism AND organism_difficulty.id_model = 1 -- For displayed organism we join estimated difficulty (not much so related to the query)
    WHERE main = TRUE
    GROUP BY answer.id_organism, latin_name, name, difficulty, organism_commonness.value
    ORDER BY count DESC
    
-- Most/least difficult organisms (+ from given topic)
    SELECT * FROM "organism_difficulty" JOIN organism_name ON organism_name.id_organism = organism_difficulty.id_organism AND id_language = 1 ORDER BY value DESC
    SELECT * FROM "organism_difficulty" JOIN organism_name ON organism_name.id_organism = organism_difficulty.id_organism AND id_language = 1 WHERE organism_difficulty.id_organism IN (SELECT id_organism FROM organism_concept WHERE id_concept = 2) ORDER BY value ASC

-- Organisms that were most distractiful
    SELECT
    a.id_organism,
    a1.name,
    b.id_organism,
    b1.name,
    COUNT(b.id_organism) AS "count_distracted",
    (SElECT COUNT(*) FROM answer AS x WHERE main = FALSE AND x.id_organism = b.id_organism) AS "count_total",
    COUNT(b.id_organism)::FLOAT / (SElECT COUNT(*) FROM answer AS x WHERE main = FALSE AND x.id_organism = b.id_organism) AS "ratio"
    FROM answer a
    JOIN answer b ON b.id_round = a.id_round AND a.question_seq_num = b.question_seq_num AND b.main = FALSE
    JOIN organism_name AS a1 ON a1.id_organism = a.id_organism AND a1.id_language = 1
    JOIN organism_name AS b1 ON b1.id_organism = b.id_organism AND b1.id_language = 1
    WHERE a.main = TRUE
    GROUP BY a.id_organism, b.id_organism, a1.name, b1.name
    ORDER BY COUNT(b.id_organism)::FLOAT / (SElECT COUNT(*) FROM answer AS x WHERE main = FALSE AND x.id_organism = b.id_organism) DESC
    
    
-- Statistics of organisms used as question / distractor
    SELECT
    answer.id_organism,
    name,
    COUNT (case when main = TRUE then 1 end) AS used_as_main,
    COUNT (case when main = FALSE then 1 end) AS used_as_distractor
    FROM answer
    JOIN organism_name ON organism_name.id_organism = answer.id_organism AND id_language = 1
    GROUP BY answer.id_organism, name
    ORDER BY used_as_distractor DESC

--- Organisms (with distance between them) in which given organism as distractor was used
    SELECT b.id_organism, name, distance, COUNT(*) AS count, (SELECT COUNT(*) FROM answer where id_organism = b.id_organism AND main = TRUE) as total_asked,
    (SELECT COUNT(*) FROM answer x where x.id_organism = 91 AND main = TRUE) as distractor_total_asked
    FROM "answer"
    JOIN answer as b ON b.id_round = answer.id_round and answer.question_seq_num = b.question_seq_num AND b.main = TRUE
    JOIN organism_name ON organism_name.id_organism = b.id_organism AND id_language = 1
    JOIN organism_distance ON id_organism_from = answer.id_organism AND id_organism_to = b.id_organism
    WHERE answer."id_organism" = '91' AND answer."main" = 'false'
    GROUP BY b.id_organism, distance, name
    ORDER BY count DESC
    
--- List organisms with are asked more then uniform distribution over organisms (commonness!)
    SELECT
     *
    FROM
    (SELECT
    name AS commonness_value,
    value,
    (SELECT COUNT(*) FROM answer WHERE id_organism = organism_name.id_organism AND main = TRUE) AS organism_asked,
    (SELECT COUNT(*) FROM answer WHERE main = TRUE) AS total_asked,
    (SELECT COUNT(*) FROM answer WHERE id_organism = organism_name.id_organism AND main = TRUE) / (SELECT COUNT(*) FROM answer WHERE main = TRUE)::FLOAT AS ratio
    FROM organism_name 
    JOIN organism_commonness USING (id_organism)
    WHERE id_language = 1
    ) t
    WHERE ratio > (SELECT COUNT(*) FROM organism)::FLOAT/(SELECT COUNT(*) FROM answer WHERE main = TRUE)
    ORDER BY ratio DESC