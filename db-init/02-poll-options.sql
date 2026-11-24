



CREATE TABLE IF NOT EXISTS poll_options (
    option_id INT NOT NULL AUTO_INCREMENT,
    poll_id INT NOT NULL,
    option_text VARCHAR(255) NOT NULL,

    PRIMARY KEY (option_id),

    UNIQUE KEY unique_poll_option (poll_id, option_id),

    CONSTRAINT fk_options_poll
        FOREIGN KEY (poll_id)
        REFERENCES polls(poll_id)
        ON DELETE CASCADE
);