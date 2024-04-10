INSERT INTO Members (Name, Email, Password, Address, PhoneNumber, FitnessGoals, HealthMetrics) VALUES
('John Doe', 'john.doe@example.com', 'password123', '123 Main St, Anytown, USA', '1234567890', 'Lose weight', 'Normal'),
('Jane Smith', 'jane.smith@example.com', 'password456', '456 Elm St, Anytown, USA', '0987654321', 'Gain muscle', 'Normal'),
('Robert Brown', 'robert.brown@example.com', 'password789', '789 Pine St, Anytown, USA', '1122334455', 'Improve stamina', 'Normal'),
('Emily Davis', 'emily.davis@example.com', 'password012', '012 Oak St, Anytown, USA', '5566778899', 'Increase flexibility', 'Normal');

INSERT INTO Trainers (Name, Email, Specialization, Selected) VALUES
('Tom Johnson', 'tom.johnson@example.com', 'Weightlifting', FALSE),
('Sally Peterson', 'sally.peterson@example.com', 'Cardio', FALSE),
('Bill Thompson', 'bill.thompson@example.com', 'Yoga', FALSE),
('Linda Anderson', 'linda.anderson@example.com', 'Pilates', FALSE);

INSERT INTO TrainerAvailability (TrainerId, AvailableTime) VALUES
(1, '2024-04-11 08:00:00'),
(1, '2024-04-12 14:00:00'),
(2, '2024-04-11 09:00:00'),
(3, '2024-04-12 10:00:00'),
(4, '2024-04-11 15:00:00');


INSERT INTO AdminStaff (Name, Email, Role) VALUES
('George Wilson', 'george.wilson@example.com', 'Manager'),
('Susan Miller', 'susan.miller@example.com', 'Receptionist'),
('Fred Taylor', 'fred.taylor@example.com', 'Maintenance'),
('Karen Davis', 'karen.davis@example.com', 'Billing');

INSERT INTO FitnessClasses (ClassName, Schedule, RoomID, TrainerID, MaxParticipants, CurrentParticipants) VALUES
('Yoga', '2024-04-11 10:00:00', 1, 3, 20, 10),
('Zumba', '2024-04-11 15:00:00', 2, 2, 20, 15),
('Weightlifting', '2024-04-10 09:00:00', 3, 1, 20, 12),
('Pilates', '2024-04-11 16:00:00', 4, 4, 20, 14);

INSERT INTO PersonalTrainingSession (Schedule, MemberID, TrainerID) VALUES
('2024-04-12 11:00:00', 1, 1),
('2024-04-12 16:00:00', 2, 2),
('2024-04-12 10:00:00', 3, 3),
('2024-04-12 15:00:00', 4, 4);

INSERT INTO RoomBookings (RoomID, BookingTime, MemberID) VALUES
(1, '2022-12-04 12:00:00', 1),
(2, '2022-12-04 17:00:00', 2),
(3, '2022-12-04 11:00:00', 3),
(4, '2022-12-04 16:00:00', 4);

INSERT INTO EquipmentMaintenance (EquipmentName, LastCheck, CurrentCheck, Status, StaffID) VALUES
('Treadmill', '2022-11-01', '2022-12-01', 'Good', 3),
('Dumbbells', '2022-11-01', '2022-12-01', 'Good', 3),
('Yoga Mats', '2022-11-01', '2022-12-01', 'Good', 3),
('Exercise Balls', '2022-11-01', '2022-12-01', 'Good', 3);

INSERT INTO Billing (MemberID, StaffID, Amount, BillDate, Status) VALUES
(1, 4, 100.00, '2022-12-01', 'Paid'),
(2, 4, 150.00, '2022-12-01', 'Unpaid'),
(3, 4, 120.00, '2022-12-01', 'Paid'),
(4, 4, 130.00, '2022-12-01', 'Unpaid');

INSERT INTO WearableDevice (MemberID, SessionID, DeviceType, WorkoutTime, HeartRate, ActiveCalories, Steps) VALUES
(1, 1, 'Smart Watch', '2022-12-05 13:00:00', 80, 200, 5000),
(2, 2, 'Fitness Tracker', '2022-12-05 18:00:00', 90, 300, 7000),
(3, 3, 'Smart Watch', '2022-12-05 12:00:00', 85, 250, 5500),
(4, 4, 'Fitness Tracker', '2022-12-05 17:00:00', 95, 350, 7500);

