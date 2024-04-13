CREATE TABLE Members (
    MemberID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    Email VARCHAR(255) UNIQUE,
    Password VARCHAR(255),
    Address TEXT,
    PhoneNumber VARCHAR(20),
    FitnessGoals TEXT,
    HealthMetrics TEXT
);

CREATE TABLE Trainers (
    TrainerId SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    Email VARCHAR(255) UNIQUE,
    Password VARCHAR(255),
    Specialization VARCHAR(255),
    Selected BOOLEAN
);

CREATE TABLE TrainerAvailability (
    AvailabilityId SERIAL PRIMARY KEY,
    TrainerId INT,
    AvailableTime TIMESTAMP,
    FOREIGN KEY (TrainerId) REFERENCES Trainers(TrainerId)
);

CREATE TABLE Rooms (
    RoomID SERIAL PRIMARY KEY,
    RoomName VARCHAR(255),
    RoomCapacity INT
);

CREATE TABLE AdminStaff (
    StaffID SERIAL PRIMARY KEY,
    Name VARCHAR(255),
    Email VARCHAR(255) UNIQUE,
    Password VARCHAR(255),
    Role VARCHAR(255)
);

CREATE TABLE FitnessClasses (
    ClassID SERIAL PRIMARY KEY,
    ClassName VARCHAR(255),
	BookedByTrainer BOOLEAN DEFAULT FALSE,
    Schedule TIMESTAMP,
    RoomID INT,
    TrainerID INT,
    MaxParticipants INT,
    CurrentParticipants INT,
	FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID),
    FOREIGN KEY (TrainerID) REFERENCES Trainers(TrainerId)
);

CREATE TABLE PersonalTrainingSession (
    SessionID SERIAL PRIMARY KEY,
    Schedule TIMESTAMP,
    MemberID INT,
    TrainerID INT,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    FOREIGN KEY (TrainerID) REFERENCES Trainers(TrainerId)
);

CREATE TABLE RoomBookings (
    BookingID SERIAL PRIMARY KEY,
    RoomID INT,
    BookingTime TIMESTAMP,
    TrainerID INT,
    BookingReason VARCHAR(255),
	FOREIGN KEY (RoomID) REFERENCES Rooms(RoomID),
    FOREIGN KEY (TrainerID) REFERENCES Trainers(TrainerId)
);


CREATE TABLE EquipmentMaintenance (
    EquipmentID SERIAL PRIMARY KEY,
    EquipmentName VARCHAR(255),
    LastCheck DATE,
    CurrentCheck DATE,
    Status VARCHAR(100),
    StaffID INT,
    FOREIGN KEY (StaffID) REFERENCES AdminStaff(StaffID)
);

CREATE TABLE Billing (
    BillID SERIAL PRIMARY KEY,
    MemberID INT,
    StaffID INT,
    Amount DECIMAL(10,2),
    BillDate DATE,
    Status VARCHAR(100),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    FOREIGN KEY (StaffID) REFERENCES AdminStaff(StaffID)
);


CREATE TABLE WearableDevice (
    DeviceID SERIAL PRIMARY KEY,
    MemberID INT,
    SessionID INT,
    DeviceType VARCHAR(100),
    WorkoutTime TIMESTAMP,
    HeartRate INT,
    ActiveCalories INT,
    Steps INT,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    FOREIGN KEY (SessionID) REFERENCES PersonalTrainingSession(SessionID)
);

CREATE TABLE ExerciseRoutines (
    RoutineID SERIAL PRIMARY KEY,
    MemberID INT,
    RoutineName VARCHAR(255),
    RoutineDetails TEXT,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

CREATE TABLE FitnessAchievements (
    AchievementID SERIAL PRIMARY KEY,
    MemberID INT,
    AchievementName VARCHAR(255),
    AchievementDetails TEXT,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID)
);

CREATE OR REPLACE FUNCTION check_room_booking() RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM RoomBookings WHERE RoomID = NEW.RoomID AND BookingTime = NEW.BookingTime) THEN
        RAISE EXCEPTION 'Room is already booked at the specified time.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER room_booking_trigger
BEFORE INSERT ON RoomBookings
FOR EACH ROW EXECUTE FUNCTION check_room_booking();

CREATE OR REPLACE FUNCTION update_trainer_id()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.BookedByTrainer THEN
        NEW.TrainerID = (SELECT TrainerID FROM TrainerAvailability WHERE StartTime <= NEW.Schedule AND EndTime > NEW.Schedule LIMIT 1);
    ELSE
        NEW.TrainerID = NULL;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_trainer_id_trigger
BEFORE INSERT OR UPDATE ON FitnessClasses
FOR EACH ROW EXECUTE FUNCTION update_trainer_id();

CREATE INDEX idx_email ON Members(Email);
CREATE INDEX idx_trainer_specialization ON Trainers(Specialization);
CREATE INDEX idx_scheduling ON FitnessClasses(Schedule);
