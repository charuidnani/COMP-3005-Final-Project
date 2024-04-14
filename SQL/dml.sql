INSERT INTO Rooms (RoomID, RoomName, RoomCapacity) VALUES
(1, 'Room A', 10),
(2, 'Room B', 15),
(3, 'Room C', 20),
(4, 'Room D', 12);

INSERT INTO Members (Name, Email, Password, Address, PhoneNumber, FitnessGoals, HealthMetrics) VALUES
('John Doe', 'john.doe@example.com', 'password123', '123 Main St, Anytown, USA', '1234567890', 'Lose weight', 'Normal'),
('Jane Smith', 'jane.smith@example.com', 'password456', '456 Elm St, Anytown, USA', '0987654321', 'Gain muscle', 'Normal'),
('Robert Brown', 'robert.brown@example.com', 'password789', '789 Pine St, Anytown, USA', '1122334455', 'Improve stamina', 'Normal'),
('Emily Davis', 'emily.davis@example.com', 'password012', '012 Oak St, Anytown, USA', '5566778899', 'Increase flexibility', 'Normal');

INSERT INTO Trainers (Name, Email, Password, Specialization, Selected) VALUES
('Tom Johnson', 'tom.johnson@example.com', 'password123', 'Weightlifting', FALSE),
('Sally Peterson', 'sally.peterson@example.com', 'password456', 'Cardio', FALSE),
('Bill Thompson', 'bill.thompson@example.com', 'password789', 'Yoga', FALSE),
('Linda Anderson', 'linda.anderson@example.com', 'password012', 'Pilates', FALSE);

INSERT INTO TrainerAvailability (TrainerId, AvailableTime) VALUES
(1, '2024-04-11 08:00:00'),
(1, '2024-04-12 14:00:00'),
(2, '2024-04-11 09:00:00'),
(3, '2024-04-12 10:00:00'),
(4, '2024-04-11 15:00:00');

INSERT INTO AdminStaff (Name, Email, Password, Role) VALUES
('George Wilson', 'george.wilson@example.com', 'password123', 'Manager'),
('Susan Miller', 'susan.miller@example.com', 'password456', 'Receptionist'),
('Fred Taylor', 'fred.taylor@example.com', 'password789', 'Maintenance'),
('Karen Davis', 'karen.davis@example.com', 'password012', 'Billing');

INSERT INTO FitnessClasses (ClassName, Schedule, RoomID, TrainerID, MaxParticipants, CurrentParticipants) VALUES
('Yoga', '2024-04-11 10:00:00', 1, NULL, 20, 10),
('Zumba', '2024-04-11 15:00:00', 2, NULL, 20, 15),
('Weightlifting', '2024-04-10 09:00:00', 3, 1, 20, 12),
('Pilates', '2024-04-11 16:00:00', 4, 4, 20, 14);

INSERT INTO PersonalTrainingSession (Schedule, MemberID, TrainerID) VALUES
('2024-04-12 11:00:00', 1, 1),
('2024-04-12 16:00:00', 2, 2),
('2024-04-12 10:00:00', 3, 3),
('2024-04-12 15:00:00', 4, 4);

INSERT INTO RoomBookings (RoomID, BookingTime, TrainerID, BookingReason) VALUES
(1, '2024-04-11 12:00:00', 1, 'Weightlifting Session'),
(2, '2024-04-11 17:00:00', 2, 'Cardio Training'),
(3, '2024-04-12 11:00:00', 3, 'Yoga Class'),
(4, '2024-04-12 16:00:00', 4, 'Pilates Class');


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

INSERT INTO ExerciseRoutines (MemberID, RoutineName, RoutineDetails) VALUES
(1, 'Morning Cardio', '30 minutes of running'),
(2, 'Evening Yoga', '20 minutes of yoga'),
(3, 'Afternoon Weights', '45 minutes of weightlifting'),
(4, 'Night Pilates', '30 minutes of pilates');

INSERT INTO FitnessAchievements (MemberID, AchievementName, AchievementDetails) VALUES
(1, '5k Run', 'Completed a 5k run'),
(2, '10k Steps', 'Walked 10k steps in a day'),
(3, '1 Hour Yoga', 'Did 1 hour of yoga'),
(4, 'Lifted 50kg', 'Lifted 50kg weights');
