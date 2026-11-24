




CREATE TABLE IF NOT EXISTS votes (
    vote_id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    poll_id INT NOT NULL,
    option_id INT NOT NULL,

    PRIMARY KEY (vote_id),

    UNIQUE KEY unique_user_poll (user_id, poll_id),


CONSTRAINT fk_votes_poll
    FOREIGN KEY (poll_id)
    REFERENCES polls(poll_id)
    ON DELETE CASCADE,

CONSTRAINT fk_votes_option
    FOREIGN KEY (poll_id, option_id)
    REFERENCES poll_options(poll_id, option_id)
    );