import psycopg
import sys
from datetime import date

DB_NAME = "final4"
USER = "postgres"
HOST = "localhost"
PASSWORD = "student"

def establish_connection():
    try:
        connection = psycopg.connect(
            dbname=DB_NAME, user=USER, host=HOST, password=PASSWORD
        )
    except psycopg.OperationalError as e:
        print(f"Failed to connect to the database: {e}")
        sys.exit(1)
    return connection

def show_available_trainers():
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT t.TrainerID, t.Name, t.Specialization, a.AvailabilityId, a.AvailableTime FROM Trainers t JOIN TrainerAvailability a ON t.TrainerID = a.TrainerId")
                trainers = cur.fetchall()
                print("\nAvailable Trainers:")
                for trainer in trainers:
                    print(f"ID: {trainer[0]}, Name: {trainer[1]}, Specialization: {trainer[2]}, Availability ID: {trainer[3]}, Available Time: {trainer[4]}")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def show_available_class_times():
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT ClassID, ClassName, Schedule, MaxParticipants, CurrentParticipants, TrainerID FROM FitnessClasses WHERE CurrentParticipants < MaxParticipants AND (TrainerID IS NULL OR BookedByTrainer = FALSE)")
                classes = cur.fetchall()
                print("\nAvailable Classes:")
                for class_ in classes:
                    print(f"ID: {class_[0]}, Name: {class_[1]}, Schedule: {class_[2]}, Max Participants: {class_[3]}, Current Participants: {class_[4]}")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def member_registration():
    """Handles member registration."""
    name = input("Please enter your name: ")
    email = input("Email: ")
    password = input("Password: ")
    address = input("Address: ")
    phone_number = input("Phone Number: ")
    fitness_goals = input("Fitness Goals: ")
    health_metrics = input("Health Metrics: ")

    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO Members (Name, Email, Password, Address, PhoneNumber, FitnessGoals, HealthMetrics) VALUES (%s, %s, %s, %s, %s, %s, %s)", (name, email, password, address, phone_number, fitness_goals, health_metrics))
                conn.commit()
                print("Registration successful!")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def update_member_profile(member_id):
    name = input("Please enter your updated name: ")
    email = input("Updated Email: ")
    password = input("Updated Password: ")
    address = input("Updated Address: ")
    phone_number = input("Updated Phone Number: ")
    fitness_goals = input("Updated Fitness Goals: ")
    health_metrics = input("Updated Health Metrics: ")

    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE Members SET Name = %s, Email = %s, Password = %s, Address = %s, PhoneNumber = %s, FitnessGoals = %s, HealthMetrics = %s WHERE MemberID = %s", (name, email, password, address, phone_number, fitness_goals, health_metrics, member_id))
                conn.commit()
                print("Profile updated successfully!")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def display_exercise_routines(member_id):
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM ExerciseRoutines WHERE MemberID = %s", (member_id,))
                routines = cur.fetchall()
                print("Exercise Routines:")
                for routine in routines:
                    print(routine)
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def display_fitness_achievements(member_id):
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM FitnessAchievements WHERE MemberID = %s", (member_id,))
                achievements = cur.fetchall()
                print("Fitness Achievements:")
                for achievement in achievements:
                    print(achievement)
    except psycopg.DatabaseError as e:
                print(f"Error while accessing the database: {e}")

def member_login():
    email = input("Please enter your login email: ")
    password = input("Password: ")
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT MemberID, Name FROM Members WHERE Email = %s AND Password = %s", (email, password))
                result = cur.fetchone()
                if result:
                    print(f"Login successful!\nWelcome, {result[1]}!")
                    return result[0]
                else:
                    print("Invalid login details!")
                    return None
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")
        return None


def admin_login():
    email = input("Please enter your admin login email: ")
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT StaffID, Name FROM AdminStaff WHERE Email = %s", (email,))
                result = cur.fetchone()
                if result:
                    print(f"Admin Login successful!\nWelcome, {result[1]}!")
                    return result[0]
                else:
                    print("Invalid admin login details!")
                    return None
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")
        return None

def add_available_room_admin():
    room_id = input("Enter Room ID: ")
    room_name = input("Enter Room Name: ")
    max_capacity = input("Enter Maximum Capacity: ")

    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO Rooms (RoomID, RoomName, RoomCapacity) VALUES (%s, %s, %s)", (room_id, room_name, max_capacity))
                conn.commit()
                print("Room added successfully!")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def show_available_rooms():
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT r.RoomID, r.RoomName, r.RoomCapacity, t.Name AS TrainerName, t.Specialization, rb.BookingTime
                    FROM Rooms r
                    LEFT JOIN RoomBookings rb ON r.RoomID = rb.RoomID
                    LEFT JOIN Trainers t ON rb.TrainerID = t.TrainerID
                    ORDER BY r.RoomID
                """)
                rooms = cur.fetchall()
                print("\nRooms and Bookings:")
                for room in rooms:
                    print(f"Room ID: {room[0]}, Room Name: {room[1]}, Capacity: {room[2]}, Trainer: {room[3]}, Specialization: {room[4]}, Booking Time: {room[5]}")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def schedule_personal_training_session(member_id):
    print("Please select a trainer:")
    show_available_trainers()
    trainer_id = input("Trainer ID: ")
    availability_id = input("Availability ID: ")

    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM TrainerAvailability WHERE AvailabilityId = %s RETURNING AvailableTime", (availability_id,))
                schedule = cur.fetchone()[0]
                cur.execute("INSERT INTO PersonalTrainingSession (Schedule, MemberID, TrainerID) VALUES (%s, %s, %s)", (schedule, member_id, trainer_id))

                cur.execute("UPDATE FitnessClasses SET TrainerID = %s, BookedByTrainer = TRUE WHERE Schedule = %s", (trainer_id, schedule))

                conn.commit()
                print("Session scheduled successfully!")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def register_for_group_fitness_class(member_id):
    print("Please select a class:")
    show_available_class_times()
    class_id = input("Class ID: ")

    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT MaxParticipants, CurrentParticipants FROM FitnessClasses WHERE ClassID = %s", (class_id,))
                max_participants, current_participants = cur.fetchone()
                if current_participants < max_participants:
                    cur.execute("UPDATE FitnessClasses SET CurrentParticipants = CurrentParticipants + 1 WHERE ClassID = %s", (class_id,))
                    conn.commit()
                    print("You have successfully registered for the class!")
                else:
                    print("The selected class is full.")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def sync_wearable_device(member_id):
    device_type = input("Please enter your wearable device type: ")
    workout_time = input("Workout Time (YYYY-MM-DD HH:MM:SS): ")
    heart_rate = input("Heart Rate: ")
    active_calories = input("Active Calories: ")
    steps = input("Steps: ")

    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO WearableDevice (MemberID, DeviceType, WorkoutTime, HeartRate, ActiveCalories, Steps) VALUES (%s, %s, %s, %s, %s, %s)", (member_id, device_type, workout_time, heart_rate, active_calories, steps))
                conn.commit()
                print("Wearable device data synced successfully!")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def view_dashboard(member_id):
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT Name, Email, Address, PhoneNumber, FitnessGoals, HealthMetrics FROM Members WHERE MemberID = %s", (member_id,))
                member_info = cur.fetchone()
                print("Dashboard Information:")
                if member_info:
                    print(f"Name: {member_info[0]}\nEmail: {member_info[1]}\nAddress: {member_info[2]}\nPhone Number: {member_info[3]}\nFitness Goals: {member_info[4]}\nHealth Metrics: {member_info[5]}")
                cur.execute("SELECT DeviceType, WorkoutTime, HeartRate, ActiveCalories, Steps FROM WearableDevice WHERE MemberID = %s", (member_id,))
                device_info = cur.fetchall()
                print("\nWearable Device Data:")
                for device in device_info:
                    print(f"Device Type: {device[0]}, Workout Time: {device[1]}, Heart Rate: {device[2]}, Active Calories: {device[3]}, Steps: {device[4]}")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def show_available_trainers():
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT t.TrainerID, t.Name, t.Specialization, a.AvailabilityId, a.AvailableTime FROM Trainers t JOIN TrainerAvailability a ON t.TrainerID = a.TrainerId")
                trainers = cur.fetchall()
                print("\nAvailable Trainers:")
                for trainer in trainers:
                    print(f"ID: {trainer[0]}, Name: {trainer[1]}, Specialization: {trainer[2]}, Availability ID: {trainer[3]}, Available Time: {trainer[4]}")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def show_available_class_times():
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT ClassID, ClassName, Schedule, MaxParticipants, CurrentParticipants, TrainerID FROM FitnessClasses WHERE CurrentParticipants < MaxParticipants AND (TrainerID IS NULL OR BookedByTrainer = FALSE)")
                classes = cur.fetchall()
                print("\nAvailable Classes:")
                for class_ in classes:
                    print(f"ID: {class_[0]}, Name: {class_[1]}, Schedule: {class_[2]}, Max Participants: {class_[3]}, Current Participants: {class_[4]}")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def admin_dashboard(staff_id):
    while True:
        print("\nAdmin Dashboard")
        print("1. Room Booking Management")
        print("2. Equipment Maintenance Monitoring")
        print("3. Class Schedule Updating")
        print("4. Billing and Payment Processing")
        print("5. Add Available Room")
        print("6. Logout")
        choice = input("Please select an option: ")

        if choice == "1":
            room_booking_management()
        elif choice == "2":
            equipment_maintenance_monitoring()
        elif choice == "3":
            class_schedule_updating()
        elif choice == "4":
            billing_and_payment_processing()
        elif choice == "5":
            add_available_room_admin()
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice, please try again.")

def member_dashboard(member_id):
    while True:
        print("\nMember Dashboard")
        print("1. Schedule Personal Training Session")
        print("2. Register for Group Fitness Class")
        print("3. Sync Wearable Device")
        print("4. View Dashboard")
        print("5. Show Available Trainers")
        print("6. Show Available Class Times")
        print("7. Update Profile")
        print("8. Display Exercise Routines")
        print("9. Display Fitness Achievements")
        print("10. Logout")
        choice = input("Please select an option: ")

        if choice == "1":
            schedule_personal_training_session(member_id)
        elif choice == "2":
            register_for_group_fitness_class(member_id)
        elif choice == "3":
            sync_wearable_device(member_id)
        elif choice == "4":
            view_dashboard(member_id)
        elif choice == "5":
            show_available_trainers()
        elif choice == "6":
            show_available_class_times()
        elif choice == "7":
            update_member_profile(member_id)
        elif choice == "8":
            display_exercise_routines(member_id)
        elif choice == "9":
            display_fitness_achievements(member_id)
        elif choice == "10":
            break
        else:
            print("Invalid choice, please try again.")

def room_booking_management():
    show_available_rooms()
    room_id = input("Enter Room ID: ")

    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                # Check if the room is available
                cur.execute("SELECT BookingTime FROM RoomBookings WHERE RoomID = %s", (room_id,))
                existing_bookings = cur.fetchall()
                if existing_bookings:
                    print("The room is already booked at the following times:")
                    for booking in existing_bookings:
                        print(booking[0])
                    return

                # If the room is available, proceed with booking
                trainer_id = input("Enter Trainer ID: ")
                booking_time = input("Enter Booking Time (YYYY-MM-DD HH:MM:SS): ")
                booking_reason = input("Enter Booking Reason: ")

                # Insert booking into RoomBookings table
                cur.execute("INSERT INTO RoomBookings (RoomID, BookingTime, TrainerID, BookingReason) VALUES (%s, %s, %s, %s)", (room_id, booking_time, trainer_id, booking_reason))
                conn.commit()
                print("Room booking successful!")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def list_equipment():
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT EquipmentID, EquipmentName, LastCheck, CurrentCheck, Status FROM EquipmentMaintenance")
                equipments = cur.fetchall()
                print("\nEquipment List:")
                for equipment in equipments:
                    print(f"ID: {equipment[0]}, Name: {equipment[1]}, Last Check: {equipment[2]}, Current Check: {equipment[3]}, Status: {equipment[4]}")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def update_equipment_status():
    list_equipment()
    equipment_id = input("Enter Equipment ID to update: ")
    new_status = input("Enter new status: ")
    today = date.today()

    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                # Update the current check to today's date and status as per the input
                cur.execute("UPDATE EquipmentMaintenance SET CurrentCheck = %s, Status = %s WHERE EquipmentID = %s", (today, new_status, equipment_id))
                conn.commit()
                print("Equipment status updated successfully!")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def equipment_maintenance_monitoring():
    print("Equipment Maintenance Monitoring")
    update_option = input("Do you want to update equipment status? (yes/no): ")

    if update_option.lower() == 'yes':
        update_equipment_status()
    else:
        print("No updates made.")

def class_schedule_updating():
    print("Class Schedule Updating")
    class_id = input("Enter Class ID: ")
    new_schedule = input("Enter New Schedule (YYYY-MM-DD HH:MM:SS): ")
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE FitnessClasses SET Schedule = %s WHERE ClassID = %s", (new_schedule, class_id))
                conn.commit()
                print("Class schedule updated successfully!")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def list_billing_information():
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT BillID, MemberID, StaffID, Amount, BillDate, Status FROM Billing ORDER BY BillID")
                billing_records = cur.fetchall()
                print("\nBilling Information:")
                for record in billing_records:
                    print(f"Bill ID: {record[0]}, Member ID: {record[1]}, Staff ID: {record[2]}, Amount: {record[3]}, Bill Date: {record[4]}, Status: {record[5]}")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def billing_and_payment_processing():
    list_billing_information()
    bill_id = input("Enter Bill ID to update: ")
    new_status = input("Enter new status (Paid/Unpaid): ")

    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE Billing SET Status = %s WHERE BillID = %s", (new_status, bill_id))
                conn.commit()
                print("Bill status updated successfully!")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def main_menu():
    while True:
        print("\nWelcome to the Health and Fitness Club Management System!")
        print("1. Member Registration")
        print("2. Member Login")
        print("3. Admin Login")
        print("4. Exit")
        choice = input("Please select an option: ")

        if choice == "1":
            member_registration()
        elif choice == "2":
            member_id = member_login()
            if member_id:
                member_dashboard(member_id)
        elif choice == "3":
            staff_id = admin_login()
            if staff_id:
                admin_dashboard(staff_id)
        elif choice == "4":
            print("Thank you for using the Health and Fitness Club Management System!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main_menu()
