DROP DATABASE IF EXISTS factic;
CREATE DATABASE factic;
USE factic;
CREATE TABLE Users (
	id INT PRIMARY KEY AUTO_INCREMENT,
	email VARCHAR(50) UNIQUE NOT NULL,
    hashed_password VARCHAR(255),
    alternative_token VARCHAR(255) UNIQUE
);
CREATE INDEX idx_alternative_token
ON Users (alternative_token);
CREATE TABLE LocalOpenaiDb(
    openai_db_id VARCHAR(50) PRIMARY KEY
);
CREATE TABLE Threads (
	id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
	user_id INT NOT NULL,
    openai_db_id VARCHAR(50) NOT NULL,
    FOREIGN KEY (openai_db_id) REFERENCES LocalOpenaiDb(openai_db_id),
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);
CREATE TABLE LocalOpenaiThreads (
	thread_id INT PRIMARY KEY,
	openai_thread_id VARCHAR(50) NOT NULL UNIQUE,
    FOREIGN KEY (thread_id) REFERENCES Threads(id)
);
CREATE TABLE Messages (
	id INT PRIMARY KEY AUTO_INCREMENT,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	thread_id INT NOT NULL,
    FOREIGN KEY (thread_id) REFERENCES Threads(id) ON DELETE CASCADE
);
CREATE TABLE ProcessedMessageInfo (
	message_id INT PRIMARY KEY,
    text TEXT NOT NULL,
    FOREIGN KEY (message_id) REFERENCES Messages(id) ON DELETE CASCADE
);
CREATE TABLE Topics (
	id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    topic VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE TopicQuestions (
	id SMALLINT AUTO_INCREMENT PRIMARY KEY,
    question VARCHAR(100) NOT NULL,
    topic_id SMALLINT NOT NULL,
    FOREIGN KEY(topic_id) REFERENCES Topics(id) ON DELETE CASCADE
);
CREATE TABLE RequestTypes (
    id TINYINT PRIMARY KEY AUTO_INCREMENT,
    description VARCHAR(50) NOT NULL UNIQUE
);
INSERT INTO RequestTypes (description) VALUES ('change_appearance'), 
('quiz'), ('contact'), ('create_playlist'), ('recap'), ('other');
CREATE TABLE Requests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    message_id INT NOT NULL,
    content VARCHAR(1000) NOT NULL,
    request_type_id TINYINT NOT NULL,
    FOREIGN KEY (message_id) REFERENCES Messages(id) ON DELETE CASCADE,
    FOREIGN KEY (request_type_id) REFERENCES RequestTypes(id) ON DELETE CASCADE
);
CREATE TABLE Texts(
	id INT PRIMARY KEY AUTO_INCREMENT,
    text TEXT NOT NULL,
    message_id INT NOT NULL,
	FOREIGN KEY (message_id) REFERENCES Messages(id) ON DELETE CASCADE
);
CREATE TABLE Links(
	id INT PRIMARY KEY AUTO_INCREMENT,
    link VARCHAR(255) NOT NULL,
    message_id INT NOT NULL,
	FOREIGN KEY (message_id) REFERENCES Messages(id) ON DELETE CASCADE
);
CREATE TABLE Files(
	id INT PRIMARY KEY AUTO_INCREMENT,
	path VARCHAR(100) NOT NULL UNIQUE,
    preview_path VARCHAR(100) UNIQUE,
	message_id INT,
	FOREIGN KEY (message_id) REFERENCES Messages(id) ON DELETE CASCADE
);	
CREATE TABLE LocalOpenaiDbFiles(
    file_id INT PRIMARY KEY,
    openai_db_id VARCHAR(50) NOT NULL,
    FOREIGN KEY (file_id) REFERENCES Files(id),
    FOREIGN KEY (openai_db_id) REFERENCES LocalOpenaiDb(openai_db_id) ON DELETE CASCADE
);
CREATE TABLE OutputChoices (
	id TINYINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE OutputCombinations (
	id INT,
    message_id INT,
    output_choice_id TINYINT,
    PRIMARY KEY (id, message_id, output_choice_id),
    FOREIGN KEY (output_choice_id) REFERENCES OutputChoices(id) ON DELETE CASCADE,
    FOREIGN KEY (message_id) REFERENCES Messages(id) ON DELETE CASCADE
);
