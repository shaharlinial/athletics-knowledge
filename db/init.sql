CREATE TABLE athletes (
    athlete_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    sex ENUM('M', 'F', 'O')
);
CREATE TABLE `countries` (
    NOC CHAR(3) NOT NULl PRIMARY KEY,
    name CHAR(50)
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

CREATE TABLE `sports` (
    sport_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE `events` (
    event_id INT PRIMARY KEY AUTO_INCREMENT,
    olympics_id INT,
    sport_id INT,
    event_name VARCHAR(255) NOT NULL,
    FOREIGN KEY (olympics_id) REFERENCES olympics(olympics_id),
    FOREIGN KEY (sport_id) REFERENCES sports(sport_id)
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
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(50) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    points INT DEFAULT 0,
    UNIQUE(user_name)
);

CREATE TABLE `country_preferences` (
    preference_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    preference_value CHAR(3),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (preference_value) REFERENCES countries(NOC)
);

CREATE TABLE `year_preferences` (
    preference_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    preference_param VARCHAR(10),
    preference_value SMALLINT,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE `sports_preferences` (
    preference_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    preference_value INT,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (preference_value) REFERENCES sports(sport_id)
);

CREATE TABLE `question_templates` (
    template_id INT PRIMARY KEY AUTO_INCREMENT,
    template_query TEXT NOT NULL,
    template_text TEXT NOT NULL
);


CREATE TABLE `answers` (
    answer_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    question_id INT,
    answer_text TEXT,
    is_correct BOOLEAN NOT NULL,
    points INT NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    FOREIGN KEY (question_id) REFERENCES question_templates(template_id)
);

INSERT INTO countries (NOC, name) VALUES
('AFG', 'Afghanistan'),
('AHO', 'Curacao'),
('ALB', 'Albania'),
('ALG', 'Algeria'),
('AND', 'Andorra'),
('ANG', 'Angola'),
('ANT', 'Antigua and Barbuda'),
('ANZ', 'Australasia'),
('ARG', 'Argentina'),
('ARM', 'Armenia'),
('ARU', 'Aruba'),
('ASA', 'American Samoa'),
('AUS', 'Australia'),
('AUT', 'Austria'),
('AZE', 'Azerbaijan'),
('BAH', 'Bahamas'),
('BAN', 'Bangladesh'),
('BAR', 'Barbados'),
('BDI', 'Burundi'),
('BEL', 'Belgium'),
('BEN', 'Benin'),
('BER', 'Bermuda'),
('BHU', 'Bhutan'),
('BIH', 'Bosnia and Herzegovina'),
('BIZ', 'Belize'),
('BLR', 'Belarus'),
('BOH', 'Bohemia'),
('BOL', 'Boliva'),
('BOT', 'Botswana'),
('BRA', 'Brazil'),
('BRN', 'Bahrain'),
('BRU', 'Brunei'),
('BUL', 'Bulgaria'),
('BUR', 'Burkina Faso'),
('CAF', 'Central African Republic'),
('CAM', 'Cambodia'),
('CAN', 'Canada'),
('CAY', 'Cayman Islands'),
('CGO', 'Republic of Congo'),
('CHA', 'Chad'),
('CHI', 'Chile'),
('CHN', 'China'),
('CIV', 'Ivory Coast'),
('CMR', 'Cameroon'),
('COD', 'Democratic Republic of the Congo'),
('COK', 'Cook Islands'),
('COL', 'Colombia'),
('COM', 'Comoros'),
('CPV', 'Cape Verde'),
('CRC', 'Costa Rica'),
('CRO', 'Croatia'),
('CRT', 'Crete'),
('CUB', 'Cuba'),
('CYP', 'Cyprus'),
('CZE', 'Czech Republic'),
('DEN', 'Denmark'),
('DJI', 'Djibouti'),
('DMA', 'Dominica'),
('DOM', 'Dominican Republic'),
('ECU', 'Ecuador'),
('EGY', 'Egypt'),
('ERI', 'Eritrea'),
('ESA', 'El Salvador'),
('ESP', 'Spain'),
('EST', 'Estonia'),
('ETH', 'Ethiopia'),
('EUN', 'Russia'),
('FIJ', 'Fiji'),
('FIN', 'Finland'),
('FRA', 'France'),
('FRG', 'Germany'),
('FSM', 'Micronesia'),
('GAB', 'Gabon'),
('GAM', 'Gambia'),
('GBR', 'UK'),
('GBS', 'Guinea-Bissau'),
('GDR', 'Germany'),
('GEO', 'Georgia'),
('GEQ', 'Equatorial Guinea'),
('GER', 'Germany'),
('GHA', 'Ghana'),
('GRE', 'Greece'),
('GRN', 'Grenada'),
('GUA', 'Guatemala'),
('GUI', 'Guinea'),
('GUM', 'Guam'),
('GUY', 'Guyana'),
('HAI', 'Haiti'),
('HKG', 'Hong Kong'),
('HON', 'Honduras'),
('HUN', 'Hungary'),
('INA', 'Indonesia'),
('IND', 'India'),
('IOA', 'Individual Olympic Athletes'),
('IRI', 'Iran'),
('IRL', 'Ireland'),
('IRQ', 'Iraq'),
('ISL', 'Iceland'),
('ISR', 'Israel'),
('ISV', 'Virgin Islands'),
('ITA', 'Italy'),
('IVB', 'Virgin Islands, British'),
('JAM', 'Jamaica'),
('JOR', 'Jordan'),
('JPN', 'Japan'),
('KAZ', 'Kazakhstan'),
('KEN', 'Kenya'),
('KGZ', 'Kyrgyzstan'),
('KIR', 'Kiribati'),
('KOR', 'South Korea'),
('KOS', 'Kosovo'),
('KSA', 'Saudi Arabia'),
('KUW', 'Kuwait'),
('LAO', 'Laos'),
('LAT', 'Latvia'),
('LBA', 'Libya'),
('LBR', 'Liberia'),
('LCA', 'Saint Lucia'),
('LES', 'Lesotho'),
('LIB', 'Lebanon'),
('LIE', 'Liechtenstein'),
('LTU', 'Lithuania'),
('LUX', 'Luxembourg'),
('MAD', 'Madagascar'),
('MAL', 'Malaysia'),
('MAR', 'Morocco'),
('MAS', 'Malaysia'),
('MAW', 'Malawi'),
('MDA', 'Moldova'),
('MDV', 'Maldives'),
('MEX', 'Mexico'),
('MGL', 'Mongolia'),
('MHL', 'Marshall Islands'),
('MKD', 'Macedonia'),
('MLI', 'Mali'),
('MLT', 'Malta'),
('MNE', 'Montenegro'),
('MON', 'Monaco'),
('MOZ', 'Mozambique'),
('MRI', 'Mauritius'),
('MTN', 'Mauritania'),
('MYA', 'Myanmar'),
('NAM', 'Namibia'),
('NBO', 'North Borneo'),
('NCA', 'Nicaragua'),
('NED', 'Netherlands'),
('NEP', 'Nepal'),
('NFL', 'Newfoundland'),
('NGR', 'Nigeria'),
('NIG', 'Niger'),
('NOR', 'Norway'),
('NRU', 'Nauru'),
('NZL', 'New Zealand'),
('OMA', 'Oman'),
('PAK', 'Pakistan'),
('PAN', 'Panama'),
('PAR', 'Paraguay'),
('PER', 'Peru'),
('PHI', 'Philippines'),
('PLE', 'Palestine'),
('PLW', 'Palau'),
('PNG', 'Papua New Guinea'),
('POL', 'Poland'),
('POR', 'Portugal'),
('PRK', 'North Korea'),
('PUR', 'Puerto Rico'),
('QAT', 'Qatar'),
('RHO', 'Zimbabwe'),
('ROT', 'Refugee Olympic Team'),
('ROU', 'Romania'),
('RSA', 'South Africa'),
('RUS', 'Russia'),
('RWA', 'Rwanda'),
('SAA', 'Germany'),
('SAM', 'Samoa'),
('SCG', 'Serbia and Montenegro'),
('SEN', 'Senegal'),
('SEY', 'Seychelles'),
('SIN', 'Singapore'),
('SKN', 'Turks and Caicos Islands'),
('SLE', 'Sierra Leone'),
('SLO', 'Slovenia'),
('SMR', 'San Marino'),
('SOL', 'Solomon Islands'),
('SOM', 'Somalia'),
('SRB', 'Serbia'),
('SRI', 'Sri Lanka'),
('SSD', 'South Sudan'),
('STP', 'Sao Tome and Principe'),
('SUD', 'Sudan'),
('SUI', 'Switzerland'),
('SUR', 'Suriname'),
('SVK', 'Slovakia'),
('SWE', 'Sweden'),
('SWZ', 'Swaziland'),
('SYR', 'Syria'),
('TAN', 'Tanzania'),
('TCH', 'Czech Republic'),
('TGA', 'Tonga'),
('THA', 'Thailand'),
('TJK', 'Tajikistan'),
('TKM', 'Turkmenistan'),
('TLS', 'Timor-Leste'),
('TOG', 'Togo'),
('TPE', 'Taiwan'),
('TTO', 'Trinidad and Tobago'),
('TUN', 'Tunisia'),
('TUR', 'Turkey'),
('TUV', 'Tuvalu'),
('UAE', 'United Arab Emirates'),
('UAR', 'United Arab Republic'),
('UGA', 'Uganda'),
('UKR', 'Ukraine'),
('UNK', 'Unknown'),
('URS', 'Russia'),
('URU', 'Uruguay'),
('USA', 'USA'),
('UZB', 'Uzbekistan'),
('VAN', 'Vanuatu'),
('VEN', 'Venezuela'),
('VIE', 'Vietnam'),
('VIN', 'Saint Vincent'),
('VNM', 'Vietnam'),
('WIF', 'West Indies Federation'),
('YAR', 'North Yemen'),
('YEM', 'Yemen'),
('YMD', 'South Yemen'),
('YUG', 'Yugoslavia'),
('ZAM', 'Zambia'),
('ZIM', 'Zimbabwe');



INSERT INTO `question_templates` (`template_id`, `template_query`, `template_text`)
VALUES
    (1, 'SELECT
    t.NOC AS country,
    COUNT(*) AS c
FROM
    athlete_events AS ae
INNER JOIN
    teams AS t ON t.team_id = ae.team_id
INNER JOIN
    events AS e ON e.event_id = ae.event_id
INNER JOIN
    olympics AS o ON o.olympics_id = e.olympics_id
WHERE
    o.season = \'Summer\' AND
    ae.medal = \'Gold\' AND
    (
        t.NOC IN (
            SELECT preference_value FROM country_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM country_preferences WHERE user_id = <user_id>)
    )
    AND o.year >= COALESCE(
        (SELECT preference_value FROM year_preferences WHERE preference_param = \'start_year\' AND user_id = <user_id>), 1000
    )
    AND o.year <= COALESCE(
        (SELECT preference_value FROM year_preferences WHERE preference_param = \'end_year\' AND user_id = <user_id>), 3000
    )
    AND (
        e.sport_id IN (
            SELECT preference_value FROM sports_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM sports_preferences WHERE user_id = <user_id>)
    )
GROUP BY
    t.NOC
ORDER BY
    c DESC
LIMIT 4;', 'Among the [countries], which country secured the most gold medals in the [years] Summer Olympics?'),

(2, 'SELECT
    t.NOC AS country,
    COUNT(*) AS c
FROM
    athlete_events AS ae
INNER JOIN
    teams AS t ON t.team_id = ae.team_id
INNER JOIN
    events AS e ON e.event_id = ae.event_id
INNER JOIN
    olympics AS o ON o.olympics_id = e.olympics_id
WHERE
    o.season = \'Summer\' AND
    ae.medal = \'Gold\' AND
    (
        t.NOC IN (
            SELECT preference_value FROM country_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM country_preferences WHERE user_id = <user_id>)
    )
    AND o.year >= COALESCE(
        (SELECT preference_value FROM year_preferences WHERE preference_param = \'start_year\' AND user_id = <user_id>), 1000
    )
    AND o.year <= COALESCE(
        (SELECT preference_value FROM year_preferences WHERE preference_param = \'end_year\' AND user_id = <user_id>), 3000
    )
    AND (
        e.sport_id IN (
            SELECT preference_value FROM sports_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM sports_preferences WHERE user_id = <user_id>)
    )
GROUP BY
    t.NOC
ORDER BY
    c DESC
LIMIT 4;', 'In the [years] Winter Olympics, which athlete among [countries] won the most medals across all sports?'),

(3, 'SELECT
    t.NOC AS country,
    COUNT(*) AS total_medals
FROM
    athlete_events AS ae
INNER JOIN
    teams AS t ON t.team_id = ae.team_id
INNER JOIN
    events AS e ON e.event_id = ae.event_id
INNER JOIN
    olympics AS o ON o.olympics_id = e.olympics_id
WHERE
    o.year = \'2000\' AND
    o.season = \'Summer\' AND
    ae.medal != \'NA\' AND (
        t.NOC IN (
            SELECT preference_value FROM country_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM country_preferences WHERE user_id = <user_id>)
    )
    AND o.year >= COALESCE(
        (SELECT preference_value FROM year_preferences WHERE preference_param = \'start_year\' AND user_id = <user_id>), 1000
    )
    AND o.year <= COALESCE(
        (SELECT preference_value FROM year_preferences WHERE preference_param = \'end_year\' AND user_id = <user_id>), 3000
    )
GROUP BY
    t.NOC
ORDER BY
    total_medals DESC
LIMIT 4;', 'Among the [countries] in the [years] Summer Olympics, which nation topped the medal tally in [sports]?'),

(4, 'SELECT
    t.NOC AS country,
    COUNT(*) AS gold_medals
FROM
    athlete_events AS ae
INNER JOIN
    teams AS t ON t.team_id = ae.team_id
INNER JOIN
    events AS e ON e.event_id = ae.event_id
INNER JOIN
    olympics AS o ON o.olympics_id = e.olympics_id
INNER JOIN
    athletes AS a ON a.athlete_id = ae.athlete_id
INNER JOIN
    sports AS s ON s.sport_id = e.sport_id
WHERE
    ae.medal = \'Gold\' AND
    s.name = \'Swimming\' AND
    (
        t.NOC IN (
            SELECT preference_value FROM country_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM country_preferences WHERE user_id = <user_id>)
    )
    AND o.year >= COALESCE(
        (SELECT preference_value FROM year_preferences WHERE preference_param = \'start_year\' AND user_id = <user_id>), 1000
    )
    AND o.year <= COALESCE(
        (SELECT preference_value FROM year_preferences WHERE preference_param = \'end_year\' AND user_id = <user_id>), 3000
    )
GROUP BY
    t.NOC
ORDER BY
    gold_medals DESC
LIMIT 4;', 'Among the [countries] which swimmer won the most gold medals in the [years] Olympics?'),

(5, 'SELECT
    t.NOC AS country,
    SUM(CASE WHEN o.season = \'Winter\' THEN 1 ELSE 0 END) AS winter_medals,
    SUM(CASE WHEN o.season = \'Summer\' THEN 1 ELSE 0 END) AS summer_medals,
    ROUND(
        SUM(CASE WHEN o.season = \'Winter\' THEN 1 ELSE 0 END) /
        SUM(CASE WHEN o.season = \'Summer\' THEN 1 ELSE 0 END),
        2
    ) AS winter_to_summer_ratio
FROM
    athlete_events AS ae
INNER JOIN
    teams AS t ON t.team_id = ae.team_id
INNER JOIN
    events AS e ON e.event_id = ae.event_id
INNER JOIN
    olympics AS o ON o.olympics_id = e.olympics_id
INNER JOIN
    athletes AS a ON a.athlete_id = ae.athlete_id
WHERE
    ae.medal != \'NA\' AND
    (
        t.NOC IN (
            SELECT preference_value FROM country_preferences WHERE user_id = 2
        )
        OR NOT EXISTS (SELECT 1 FROM country_preferences WHERE user_id = 2)
    )
    AND o.year >= COALESCE(
        (SELECT preference_value FROM year_preferences WHERE preference_param = \'start_year\' AND user_id = 2), 1000
    )
    AND o.year <= COALESCE(
        (SELECT preference_value FROM year_preferences WHERE preference_param = \'end_year\' AND user_id = 2), 3000
    )
    AND (
        e.sport_id IN (
            SELECT preference_value FROM sports_preferences WHERE user_id = 2
        )
        OR NOT EXISTS (SELECT 1 FROM sports_preferences WHERE user_id = 2)
    )
GROUP BY
    t.NOC LIMIT 4;', 'For the [countries], what is the ratio of Winter to Summer Olympics medals?'),
    (6, 'SELECT
    t.NOC AS country,
    SUM(CASE WHEN o.season = \'Winter\' THEN 1 ELSE 0 END) AS winter_medals,
    SUM(CASE WHEN o.season = \'Summer\' THEN 1 ELSE 0 END) AS summer_medals,
    ROUND(
        SUM(CASE WHEN o.season = \'Winter\' THEN 1 ELSE 0 END) /
        SUM(CASE WHEN o.season = \'Summer\' THEN 1 ELSE 0 END),
        2
    ) AS winter_to_summer_ratio
FROM
    athlete_events AS ae
INNER JOIN
    teams AS t ON t.team_id = ae.team_id
INNER JOIN
    events AS e ON e.event_id = ae.event_id
INNER JOIN
    olympics AS o ON o.olympics_id = e.olympics_id
INNER JOIN
    athletes AS a ON a.athlete_id = ae.athlete_id
WHERE
    ae.medal != \'NA\' AND
    (
        t.NOC IN (
            SELECT preference_value FROM country_preferences WHERE user_id = 2
        )
        OR NOT EXISTS (SELECT 1 FROM country_preferences WHERE user_id = 2)
    )
    AND o.year >= COALESCE(
        (SELECT preference_value FROM year_preferences WHERE preference_param = \'start_year\' AND user_id = 2), 1000
    )
    AND o.year <= COALESCE(
        (SELECT preference_value FROM year_preferences WHERE preference_param = \'end_year\' AND user_id = 2), 3000
    )
    AND (
        e.sport_id IN (
            SELECT preference_value FROM sports_preferences WHERE user_id = 2
        )
        OR NOT EXISTS (SELECT 1 FROM sports_preferences WHERE user_id = 2)
    )
GROUP BY
    t.NOC
HAVING
    SUM(CASE WHEN o.season = \'Summer\' THEN 1 ELSE 0 END) > 0
    AND SUM(CASE WHEN o.season = \'Winter\' THEN 1 ELSE 0 END) > 0 -- Remove countries with no summer or winter medals
ORDER BY
    winter_to_summer_ratio DESC
LIMIT 4;', 'Which of the [countries] have the highest ratio of Winter to Summer Olympics medals?'),

(7, 'SELECT
    t.NOC AS country,
    COUNT(*) AS female_gold_medallists
FROM
    athlete_events AS ae
INNER JOIN
    teams AS t ON t.team_id = ae.team_id
INNER JOIN
    events AS e ON e.event_id = ae.event_id
INNER JOIN
    olympics AS o ON o.olympics_id = e.olympics_id
INNER JOIN
    athletes AS a ON a.athlete_id = ae.athlete_id
WHERE
    a.sex = \'F\' AND
    ae.medal = \'Gold\' AND (
        t.NOC IN (
            SELECT preference_value FROM country_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM country_preferences WHERE user_id = <user_id>)
    )
    AND o.year >= COALESCE(
        (SELECT preference_value FROM year_preferences WHERE preference_param = \'t.start_year\' AND user_id = <user_id>), 1000
    )
    AND o.year <= COALESCE(
        (SELECT preference_value FROM year_preferences WHERE preference_param = \'t.end_year\' AND user_id = <user_id>), 3000
    )
    AND (
        e.sport_id IN (
            SELECT preference_value FROM sports_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM sports_preferences WHERE user_id = <user_id>)
    )
GROUP BY
    t.NOC
ORDER BY
    female_gold_medallists DESC
LIMIT 4;', 'Among the [countries] participating in the [years] Olympics, which nation had the highest number of female gold medallists?'),

(8, 'SELECT
    t.NOC AS country,
    COUNT(*) AS c
FROM
    athlete_events AS ae
INNER JOIN
    teams AS t ON t.team_id = ae.team_id
INNER JOIN
    events AS e ON e.event_id = ae.event_id
INNER JOIN
    olympics AS o ON o.olympics_id = e.olympics_id
WHERE
    o.season = \'Winter\' AND
    ae.medal = \'Gold\' AND
    (
        t.NOC IN (
            SELECT preference_value FROM country_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM country_preferences WHERE user_id = <user_id>)
    )
    AND o.year >= COALESCE(
        (SELECT preference_value FROM year_preferences WHERE preference_param = \'start_year\' and user_id = <user_id>), 1000
    )
    AND o.year <= COALESCE(
        (SELECT preference_value FROM year_preferences WHERE preference_param = \'end_year\' and user_id = <user_id>), 3000
    )
    AND (
        e.sport_id IN (
            SELECT preference_value FROM sports_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM sports_preferences WHERE user_id = <user_id>)
    )
GROUP BY
    t.NOC
ORDER BY
    c DESC
LIMIT 4;', 'Among the [countries], which country secured the most gold medals in the [years] Winter Olympics?'),

(9, 'SELECT
    t.NOC AS country,
    COUNT(*) AS female_participations
FROM
    athlete_events AS ae
INNER JOIN
    teams AS t ON t.team_id = ae.team_id
INNER JOIN
    events AS e ON e.event_id = ae.event_id
INNER JOIN
    olympics AS o ON o.olympics_id = e.olympics_id
INNER JOIN
    athletes AS a ON a.athlete_id = ae.athlete_id
WHERE
    a.sex = \'F\' AND
    (
        t.NOC IN (
            SELECT preference_value FROM country_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM country_preferences WHERE user_id = <user_id>)
    )
    AND (
        e.sport_id IN (
            SELECT preference_value FROM sports_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM sports_preferences WHERE user_id = <user_id>)
    )
GROUP BY
    t.NOC
ORDER BY
    female_participations DESC
LIMIT 4;', 'Among the [countries] participating in the [years] Olympics, which nation had the highest number of female participations?'),

(10, 'SELECT
    t.NOC AS country,
    MAX(ae.height) AS athlete_height
FROM
    athlete_events AS ae
INNER JOIN
    teams AS t ON t.team_id = ae.team_id
INNER JOIN
    events AS e ON e.event_id = ae.event_id
INNER JOIN
    olympics AS o ON o.olympics_id = e.olympics_id
INNER JOIN
    athletes AS a ON a.athlete_id = ae.athlete_id
WHERE
    ae.height IS NOT NULL
    AND (
        t.NOC IN (
            SELECT preference_value FROM country_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM country_preferences WHERE user_id = <user_id>)
    )
    AND (
        e.sport_id IN (
            SELECT preference_value FROM sports_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM sports_preferences WHERE user_id = <user_id>)
    )
GROUP BY
    t.NOC
ORDER BY
    MAX(ae.height) ASC
LIMIT 4;', 'Among the [countries] participating in [sports], which country had the shortest athlete (in cm) of all time?'),

(11, 'SELECT
    t.NOC AS country,
    MAX(ae.height) AS athlete_height
FROM
    athlete_events AS ae
INNER JOIN
    teams AS t ON t.team_id = ae.team_id
INNER JOIN
    events AS e ON e.event_id = ae.event_id
INNER JOIN
    olympics AS o ON o.olympics_id = e.olympics_id
INNER JOIN
    athletes AS a ON a.athlete_id = ae.athlete_id
WHERE
    ae.height IS NOT NULL
    AND (
        t.NOC IN (
            SELECT preference_value FROM country_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM country_preferences WHERE user_id = <user_id>)
    )
    AND (
        e.sport_id IN (
            SELECT preference_value FROM sports_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM sports_preferences WHERE user_id = <user_id>)
    )
GROUP BY
    t.NOC
ORDER BY
    MAX(ae.height) DESC
LIMIT 4;', 'Among the [countries] participating in [sports], which country had the tallest athlete (in cm) of all time?'),

(12, 'SELECT
    t.NOC AS country,
    MAX(ae.weight) AS athlete_weight
FROM
    athlete_events AS ae
INNER JOIN
    teams AS t ON t.team_id = ae.team_id
INNER JOIN
    events AS e ON e.event_id = ae.event_id
INNER JOIN
    olympics AS o ON o.olympics_id = e.olympics_id
INNER JOIN
    athletes AS a ON a.athlete_id = ae.athlete_id
WHERE
    ae.weight IS NOT NULL
    AND (
        t.NOC IN (
            SELECT preference_value FROM country_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM country_preferences WHERE user_id = <user_id>)
    )
    AND (
        e.sport_id IN (
            SELECT preference_value FROM sports_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM sports_preferences WHERE user_id = <user_id>)
    )
GROUP BY
    t.NOC
ORDER BY
    MAX(ae.weight) DESC
LIMIT 4;', 'Among the [countries] participating in [sports] Olympics, which athlete had the highest weight of all time?'),

(13, 'SELECT
    t.NOC AS country,
    MAX(ae.weight) AS athlete_weight
FROM
    athlete_events AS ae
INNER JOIN
    teams AS t ON t.team_id = ae.team_id
INNER JOIN
    events AS e ON e.event_id = ae.event_id
INNER JOIN
    olympics AS o ON o.olympics_id = e.olympics_id
INNER JOIN
    athletes AS a ON a.athlete_id = ae.athlete_id
WHERE
    ae.weight IS NOT NULL
    AND (
        t.NOC IN (
            SELECT preference_value FROM country_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM country_preferences WHERE user_id = <user_id>)
    )
    AND (
        e.sport_id IN (
            SELECT preference_value FROM sports_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM sports_preferences WHERE user_id = <user_id>)
    )
GROUP BY
    t.NOC
ORDER BY
    MAX(ae.weight) ASC
LIMIT 4;', 'Among the [countries] participating in [sports] Olympics, which athlete had the lowest weight of all time?'),

(14, 'SELECT
    t.NOC AS country,
    MIN(ae.age) AS athlete_age
FROM
    athlete_events AS ae
INNER JOIN
    teams AS t ON t.team_id = ae.team_id
INNER JOIN
    events AS e ON e.event_id = ae.event_id
INNER JOIN
    olympics AS o ON o.olympics_id = e.olympics_id
INNER JOIN
    athletes AS a ON a.athlete_id = ae.athlete_id
WHERE
    ae.age IS NOT NULL
    AND (
        t.NOC IN (
            SELECT preference_value FROM country_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM country_preferences WHERE user_id = <user_id>)
    )
    AND (
        e.sport_id IN (
            SELECT preference_value FROM sports_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM sports_preferences WHERE user_id = <user_id>)
    )
GROUP BY
    t.NOC
ORDER BY
    MIN(ae.age) ASC
LIMIT 4;', 'Among the [countries] participating in [sports] Olympics, which nation had the youngest athlete of all time?'),

(15, 'SELECT
    t.NOC AS country,
    MIN(ae.age) AS athlete_age
FROM
    athlete_events AS ae
INNER JOIN
    teams AS t ON t.team_id = ae.team_id
INNER JOIN
    events AS e ON e.event_id = ae.event_id
INNER JOIN
    olympics AS o ON o.olympics_id = e.olympics_id
INNER JOIN
    athletes AS a ON a.athlete_id = ae.athlete_id
WHERE
    ae.age IS NOT NULL
    AND (
        t.NOC IN (
            SELECT preference_value FROM country_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM country_preferences WHERE user_id = <user_id>)
    )
    AND (
        e.sport_id IN (
            SELECT preference_value FROM sports_preferences WHERE user_id = <user_id>
        )
        OR NOT EXISTS (SELECT 1 FROM sports_preferences WHERE user_id = <user_id>)
    )
GROUP BY
    t.NOC
ORDER BY
    MIN(ae.age) DESC
LIMIT 4;', 'Among the [countries] participating in [sports] Olympics, which nation had the oldest athlete of all time?');
