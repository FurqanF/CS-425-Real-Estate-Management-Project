
-- Real Estate Management System
-- Authors: Furqan Farooqui, Abriel Simmons

DROP TABLE IF EXISTS Booking;
DROP TABLE IF EXISTS Property;
DROP TABLE IF EXISTS CreditCard;
DROP TABLE IF EXISTS Address;
DROP TABLE IF EXISTS Renter;
DROP TABLE IF EXISTS Agent;
DROP TABLE IF EXISTS UserTable;

-- ENUM TYPE for User Role
DROP TYPE IF EXISTS user_role;
CREATE TYPE user_role AS ENUM ('Agent','Renter');

CREATE TABLE UserTable (
    UserID SERIAL PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Number VARCHAR(20),
    Role user_role,
    Location VARCHAR(100),
    Ratings DOUBLE PRECISION
);

CREATE TABLE Agent (
    AgentID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    AgencyName VARCHAR(100),
    JobTitle VARCHAR(50),
    FOREIGN KEY (UserID) REFERENCES UserTable(UserID)
);

CREATE TABLE Renter (
    RenterID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    PreferredLocation VARCHAR(100),
    Budget DOUBLE PRECISION,
    MoveInDate DATE,
    FOREIGN KEY (UserID) REFERENCES UserTable(UserID)
);

CREATE TABLE Address (
    AddressID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    Street VARCHAR(100),
    City VARCHAR(50),
    State VARCHAR(50),
    ZipCode VARCHAR(10),
    FOREIGN KEY (UserID) REFERENCES UserTable(UserID)
);

CREATE TABLE CreditCard (
    CardNumber VARCHAR(20) PRIMARY KEY,
    UserID INT NOT NULL,
    BillingAddressID INT,
    ExpiryDate DATE,
    CVV VARCHAR(4),
    FOREIGN KEY (UserID) REFERENCES UserTable(UserID),
    FOREIGN KEY (BillingAddressID) REFERENCES Address(AddressID)
);

CREATE TABLE Property (
    PropertyID SERIAL PRIMARY KEY,
    AgentID INT NOT NULL,
    Type VARCHAR(50),
    Address VARCHAR(200),
    City VARCHAR(50),
    State VARCHAR(50),
    SquareFeet DOUBLE PRECISION,
    Bedrooms INT,
    Price DOUBLE PRECISION,
    Availability BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (AgentID) REFERENCES Agent(AgentID)
);

CREATE TABLE Booking (
    BookingID SERIAL PRIMARY KEY,
    PropertyID INT NOT NULL,
    RenterID INT NOT NULL,
    CardNumber VARCHAR(20),
    StartDate DATE,
    EndDate DATE,
    TotalCost DOUBLE PRECISION,
    FOREIGN KEY (PropertyID) REFERENCES Property(PropertyID),
    FOREIGN KEY (RenterID) REFERENCES Renter(RenterID),
    FOREIGN KEY (CardNumber) REFERENCES CreditCard(CardNumber)
);

CREATE OR REPLACE FUNCTION check_property_availability()
RETURNS trigger AS $$
BEGIN
    PERFORM 1 FROM Property WHERE PropertyID = NEW.PropertyID AND Availability = TRUE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Cannot create booking. Property % is not available.', NEW.PropertyID;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_property_availability
BEFORE INSERT ON Booking
FOR EACH ROW
EXECUTE FUNCTION check_property_availability();

-- sample data
INSERT INTO UserTable (Name, Email, Number, Role, Location, Ratings) VALUES
('Alice Smith', 'alice@example.com', '555-1111', 'Agent', 'New York', 4.8),
('Bob Johnson', 'bob@example.com', '555-2222', 'Renter', 'Chicago', 4.5),
('Carla Davis', 'carla@example.com', '555-3333', 'Agent', 'Los Angeles', 4.9);

INSERT INTO Agent (UserID, AgencyName, JobTitle) VALUES
(1, 'DreamHomes Realty', 'Senior Agent'),
(3, 'Prime Properties', 'Listing Agent');

INSERT INTO Renter (UserID, PreferredLocation, Budget, MoveInDate) VALUES
(2, 'Downtown Chicago', 2500.00, '2025-12-01');

INSERT INTO Address (UserID, Street, City, State, ZipCode) VALUES
(1, '123 Main St', 'New York', 'NY', '10001'),
(2, '456 Oak St', 'Chicago', 'IL', '60601');

INSERT INTO CreditCard (CardNumber, UserID, BillingAddressID, ExpiryDate, CVV) VALUES
('1111222233334444', 2, 2, '2027-05-01', '123');

INSERT INTO Property (AgentID, Type, Address, City, State, SquareFeet, Bedrooms, Price, Availability) VALUES
(1, 'Apartment', '789 Elm St', 'New York', 'NY', 950, 2, 3000.00, TRUE),
(2, 'House', '321 Pine St', 'Los Angeles', 'CA', 1800, 3, 4800.00, TRUE);

INSERT INTO Booking (PropertyID, RenterID, CardNumber, StartDate, EndDate, TotalCost) VALUES
(1, 1, '1111222233334444', '2025-12-10', '2026-01-10', 3000.00);

SELECT * FROM UserTable;
SELECT * FROM Agent;
SELECT * FROM Renter;
SELECT * FROM Address;
SELECT * FROM CreditCard;
SELECT * FROM Property;
SELECT * FROM Booking;