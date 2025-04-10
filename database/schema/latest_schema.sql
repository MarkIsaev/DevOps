CREATE TABLE user (
	id INTEGER NOT NULL, 
	username VARCHAR(150) NOT NULL, 
	email VARCHAR(150) NOT NULL, 
	password VARCHAR(200) NOT NULL, 
	role VARCHAR(50) NOT NULL, 
	date_created TIMESTAMP, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	UNIQUE (email)
);
CREATE TABLE category (
	id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (name), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE TABLE note (
	id INTEGER NOT NULL, 
	title VARCHAR(200) NOT NULL, 
	content TEXT NOT NULL, 
	timestamp DATETIME, 
	user_id INTEGER NOT NULL, 
	category_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	FOREIGN KEY(category_id) REFERENCES category (id)
);
CREATE TABLE shared_notes (
	note_id INTEGER NOT NULL, 
	user_id INTEGER NOT NULL, 
	PRIMARY KEY (note_id, user_id), 
	FOREIGN KEY(note_id) REFERENCES note (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
