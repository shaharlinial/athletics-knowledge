CREATE TABLE Athletes (
    AthleteID INT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Sex CHAR(1) NOT NULL,
    Age INT,
    CONSTRAINT check_sex CHECK (Sex IN ('M', 'F'))
);

CREATE TABLE Teams (
    TeamID INT PRIMARY KEY,
    TeamName VARCHAR(255) NOT NULL,
    NOC CHAR(3) NOT NULL
);

CREATE TABLE Olympics (
    OlympicsID INT PRIMARY KEY,
    Games VARCHAR(255) NOT NULL,
    Year INT,
    Season VARCHAR(6) NOT NULL,
    City VARCHAR(255) NOT NULL,
    CONSTRAINT check_season CHECK (Season IN ('Summer', 'Winter'))
);

CREATE TABLE Events (
    EventID INT PRIMARY KEY,
    OlympicsID INT,
    Sport VARCHAR(255) NOT NULL,
    EventName VARCHAR(255) NOT NULL,
    PRIMARY KEY (EventID),
    FOREIGN KEY (OlympicsID) REFERENCES Olympics(OlympicsID)
);

CREATE TABLE AthleteEvents (
    AthleteID INT,
    TeamID INT,
    EventID INT,
    Medal VARCHAR(10) DEFAULT 'NA',
    Weight INT,  -- Weight for this specific event
    PRIMARY KEY (AthleteID, EventID),
    FOREIGN KEY (AthleteID) REFERENCES Athletes(AthleteID),
    FOREIGN KEY (TeamID) REFERENCES Teams(TeamID),
    FOREIGN KEY (EventID) REFERENCES Events(EventID),
    CONSTRAINT check_medal CHECK (Medal IN ('Gold', 'Silver', 'Bronze', 'NA'))
);
