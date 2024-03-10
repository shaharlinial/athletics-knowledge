CREATE TABLE athletes (
    athlete_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    sex ENUM('M', 'F', 'O')
);

CREATE TABLE `teams` (
    team_id INT PRIMARY KEY AUTO_INCREMENT,
    NOC CHAR(3) NOT NULL,
    team_name VARCHAR(255) NOT NULL
);

CREATE TABLE `olympics` (
    olympics_id INT PRIMARY KEY AUTO_INCREMENT,
    games VARCHAR(255) NOT NULL,
    year SMALLINT,
    season ENUM('Summer', 'Winter'),
    city VARCHAR(255) NOT NULL
);

CREATE TABLE `events` (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    olympics_id INT,
    sport VARCHAR(255) NOT NULL,
    event_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (olympics_id) REFERENCES olympics(olympics_id)
);

CREATE TABLE `athlete_events` (
    athlete_id INT,
    team_id INT,
    event_id INT,
    medal ENUM('Gold', 'Silver', 'Bronze', 'NA'),
    weight INT,
    height INT,
    age INT,
    PRIMARY KEY (athlete_id, event_id, team_id, medal),
    FOREIGN KEY (athlete_id) REFERENCES athletes(athlete_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (event_id) REFERENCES events(event_id)
);

CREATE TABLE `users` (
    user_id INT PRIMARY KEY,
    user_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    points INT DEFAULT 0
);

CREATE TABLE `preferences` (
    preference_id INT PRIMARY KEY,
    user_id INT,
    preference_param VARCHAR(255),
    preference_value VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE `question_templates` (
    template_id INT PRIMARY KEY,
    template_query VARCHAR(255) NOT NULL,
    template_text VARCHAR(255) NOT NULL
);

CREATE TABLE `question_template_params` (
    param_id INT PRIMARY KEY,
    template_id INT,
    param_value VARCHAR(255),
    FOREIGN KEY (template_id) REFERENCES question_templates(template_id)
);

CREATE TABLE `questions` (
    question_id INT PRIMARY KEY,
    question_template_id INT,
    user_id INT,
    generated_question_text VARCHAR(255) NOT NULL
);

CREATE TABLE `user_progress` (
    user_id INT,
    question_id INT,
    answer_id INT,
    is_correct BOOLEAN,
    points_earned INT,
    bonus_points_earned INT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, question_id, timestamp)
);

CREATE TABLE `answers` (
    answer_id INT PRIMARY KEY AUTO_INCREMENT,
    question_id INT,
    answer_text VARCHAR(255),
    is_correct BOOLEAN NOT NULL,
    points INT NOT NULL DEFAULT 0
);