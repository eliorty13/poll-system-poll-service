



CREATE TABLE IF NOT EXISTS votes (
    vote_id INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    poll_id INT NOT NULL,
    selected_option INT NOT NULL,
    PRIMARY KEY (vote_id),
    UNIQUE KEY unique_user_poll (user_id, poll_id),
    KEY fk_votes_poll (poll_id),
    CONSTRAINT fk_votes_poll
        FOREIGN KEY (poll_id)
        REFERENCES polls (poll_id)
        ON DELETE CASCADE,
    CONSTRAINT check_selected_option
        CHECK (selected_option BETWEEN 1 AND 4)
);