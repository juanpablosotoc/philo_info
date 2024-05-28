DROP DATABASE IF EXISTS philo_info;
CREATE DATABASE philo_info;
USE philo_info;
CREATE TABLE Solo (
	id INT PRIMARY KEY AUTO_INCREMENT,
	email VARCHAR(50) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL
);
CREATE TABLE Threads (
	thread_id INT PRIMARY KEY AUTO_INCREMENT,
    openai_thread_id VARCHAR(50),
	user_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Solo(id)
);
CREATE TABLE Thread_messages (
	thread_message_id INT PRIMARY KEY AUTO_INCREMENT,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	content MEDIUMTEXT NOT NULL,
	type VARCHAR(25) NOT NULL,
	thread_id INT NOT NULL,
    FOREIGN KEY (thread_id) REFERENCES Threads(thread_id)
);