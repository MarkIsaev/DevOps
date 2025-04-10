CREATE TABLE "user" (
    id integer NOT NULL,
    username varchar(150) NOT NULL,
    email varchar(150) NOT NULL,
    password varchar(200) NOT NULL,
    role varchar(50) NOT NULL,
    date_created timestamp,
    PRIMARY KEY (id),
    UNIQUE (username),
    UNIQUE (email)
);

CREATE TABLE "category" (
    id integer NOT NULL,
    name varchar(100) NOT NULL,
    user_id integer,
    PRIMARY KEY (id),
    UNIQUE (name),
    FOREIGN KEY (user_id) REFERENCES "user" (id)
);

CREATE TABLE "note" (
    id integer NOT NULL,
    title varchar(200) NOT NULL,
    content text NOT NULL,
    timestamp timestamp,
    user_id integer NOT NULL,
    category_id integer,
    PRIMARY KEY (id),
    FOREIGN KEY (user_id) REFERENCES "user" (id),
    FOREIGN KEY (category_id) REFERENCES "category" (id)
);

CREATE TABLE "shared_notes" (
    note_id integer NOT NULL,
    user_id integer NOT NULL,
    PRIMARY KEY (note_id, user_id),
    FOREIGN KEY (note_id) REFERENCES "note" (id),
    FOREIGN KEY (user_id) REFERENCES "user" (id)
);
