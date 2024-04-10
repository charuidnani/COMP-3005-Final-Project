import psycopg
import sys

DB_NAME = "final1"
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
        exit(1)
    return connection

def show_available_trainers():
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT TrainerID, Name, Specialization, Availability FROM Trainers")
                trainers = cur.fetchall()
                print("\nAvailable Trainers:")
                for trainer in trainers:
                    print(f"ID: {trainer[0]}, Name: {trainer[1]}, Specialization: {trainer[2]}, Availability: {trainer[3]}")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def show_available_class_times():
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT ClassID, ClassName, Schedule FROM FitnessClasses WHERE CurrentParticipants < MaxParticipants")
                classes = cur.fetchall()
                print("\nAvailable Classes:")
                for class_ in classes:
                    print(f"ID: {class_[0]}, Name: {class_[1]}, Schedule: {class_[2]}")
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
    password = input("Password: ")
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT StaffID, Name FROM AdminStaff WHERE Email = %s AND Password = %s", (email, password))
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


def schedule_personal_training_session(member_id):
    print("Please select a trainer:")
    show_available_trainers()
    trainer_id = input("Trainer ID: ")
    availability_id = input("Availability ID: ")

    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM TrainerAvailability WHERE AvailabilityId = %s RETURNING StartTime", (availability_id,))
                schedule = cur.fetchone()[0]
                cur.execute("INSERT INTO PersonalTrainingSession (Schedule, MemberID, TrainerID) VALUES (%s, %s, %s)", (schedule, member_id, trainer_id))
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
                cur.execute("SELECT t.TrainerID, t.Name, t.Specialization, a.AvailabilityId, a.StartTime, a.EndTime FROM Trainers t JOIN TrainerAvailability a ON t.TrainerID = a.TrainerId")
                trainers = cur.fetchall()
                print("\nAvailable Trainers:")
                for trainer in trainers:
                    print(f"ID: {trainer[0]}, Name: {trainer[1]}, Specialization: {trainer[2]}, Availability ID: {trainer[3]}, Start Time: {trainer[4]}, End Time: {trainer[5]}")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def show_available_class_times():
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT ClassID, ClassName, Schedule, MaxParticipants, CurrentParticipants FROM FitnessClasses WHERE CurrentParticipants < MaxParticipants")
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
        print("5. Logout")
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
        print("7. Logout")
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
            break
        else:
            print("Invalid choice, please try again.")

def room_booking_management():
    print("Room Booking Management")
    member_id = input("Enter Member ID: ")
    room_id = input("Enter Room ID: ")
    booking_time = input("Enter Booking Time (YYYY-MM-DD HH:MM:SS): ")
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO RoomBookings (RoomID, BookingTime, MemberID) VALUES (%s, %s, %s)", (room_id, booking_time, member_id))
                conn.commit()
                print("Room booking successful!")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def equipment_maintenance_monitoring():
    print("Equipment Maintenance Monitoring")
    equipment_name = input("Enter Equipment Name: ")
    last_check = input("Enter Last Check Date (YYYY-MM-DD): ")
    current_check = input("Enter Current Check Date (YYYY-MM-DD): ")
    status = input("Enter Status: ")
    staff_id = input("Enter Staff ID: ")
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO EquipmentMaintenance (EquipmentName, LastCheck, CurrentCheck, Status, StaffID) VALUES (%s, %s, %s, %s, %s)", (equipment_name, last_check, current_check, status, staff_id))
                conn.commit()
                print("Equipment maintenance record updated successfully!")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

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

def billing_and_payment_processing():
    print("Billing and Payment Processing")
    member_id = input("Enter Member ID: ")
    amount = input("Enter Amount: ")
    bill_date = input("Enter Bill Date (YYYY-MM-DD): ")
    status = input("Enter Status (Paid/Unpaid): ")
    staff_id = input("Enter Staff ID handling the billing: ")
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO Billing (MemberID, StaffID, Amount, BillDate, Status) VALUES (%s, %s, %s, %s, %s)", (member_id, staff_id, amount, bill_date, status))
                conn.commit()
                print("Billing information updated successfully!")
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
