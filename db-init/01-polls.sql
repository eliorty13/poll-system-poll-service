


CREATE TABLE IF NOT EXISTS polls (
    poll_id INT NOT NULL AUTO_INCREMENT,
    question_title VARCHAR(255) NOT NULL,
    first_option VARCHAR(255) NOT NULL,
    second_option VARCHAR(255) NOT NULL,
    third_option VARCHAR(255) NOT NULL,
    fourth_option VARCHAR(255) NOT NULL DEFAULT 'No option assigned',
    PRIMARY KEY (poll_id)
);