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

def trainer_login():
    email = input("Please enter your trainer login email: ")
    password = input("Password: ")
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT TrainerID, Name FROM Trainers WHERE Email = %s AND Password = %s", (email, password))
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

def trainer_dashboard(trainer_id):
    while True:
        print("\nTrainer Dashboard")
        print("1. Set Available Time")
        print("2. View Member Profile")
        print("3. Logout")
        choice = input("Please select an option: ")

        if choice == "1":
            set_available_time(trainer_id)
        elif choice == "2":
            view_member_profile()
        elif choice == "3":
            print("Logging out...")
            break
        else:
            print("Invalid choice, please try again.")

def set_available_time(trainer_id):
    print("1. Add new available time")
    print("2. Update existing available time")
    print("3. Delete available time")
    choice = input("Select an option: ")

    if choice == "1":
        print_current_times(trainer_id)
        available_time = input("Enter the new available time (YYYY-MM-DD HH:MM:SS): ")
        try:
            with establish_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("INSERT INTO TrainerAvailability (TrainerId, AvailableTime) VALUES (%s, %s)", (trainer_id, available_time))
                    conn.commit()
                    print("Available time added successfully!")
        except psycopg.DatabaseError as e:
            print(f"Error while accessing the database: {e}")

    elif choice == "2":
        print_current_times(trainer_id)
        old_time = input("Enter the existing available time to update (YYYY-MM-DD HH:MM:SS): ")
        new_time = input("Enter the new available time (YYYY-MM-DD HH:MM:SS): ")
        try:
            with establish_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("UPDATE TrainerAvailability SET AvailableTime = %s WHERE TrainerId = %s AND AvailableTime = %s", (new_time, trainer_id, old_time))
                    conn.commit()
                    print("Available time updated successfully!")
        except psycopg.DatabaseError as e:
            print(f"Error while accessing the database: {e}")

    elif choice == "3":
        print_current_times(trainer_id)
        available_time = input("Enter the available time to delete (YYYY-MM-DD HH:MM:SS): ")
        try:
            with establish_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM TrainerAvailability WHERE TrainerId = %s AND AvailableTime = %s", (trainer_id, available_time))
                    conn.commit()
                    print("Available time deleted successfully!")
        except psycopg.DatabaseError as e:
            print(f"Error while accessing the database: {e}")

    else:
        print("Invalid choice, please try again.")

def print_current_times(trainer_id):
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT AvailableTime FROM TrainerAvailability WHERE TrainerId = %s", (trainer_id,))
                current_times = cur.fetchall()
                print("Current available times:")
                for time in current_times:
                    print(time[0])
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def view_member_profile():
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT Name FROM Members")
                member_names = cur.fetchall()
                print("Member Names:")
                for name in member_names:
                    print(name[0])
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

    member_name = input("Enter the member's name: ")
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT * FROM Members WHERE Name = %s", (member_name,))
                member_info = cur.fetchone()
                if member_info:
                    print("Member Information:")
                    print(member_info)
                else:
                    print("Member not found.")
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
   while True:
       print("\nUpdate Profile")
       print("1. Update Name")
       print("2. Update Email")
       print("3. Update Password")
       print("4. Update Address")
       print("5. Update Phone Number")
       print("6. Update Fitness Goals")
       print("7. Update Health Metrics")
       print("8. Return to previous menu")
       choice = input("Please select an option: ")


       if choice == "1":
           new_name = input("Please enter your updated name: ")
           update_member_attribute(member_id, "Name", new_name)
       elif choice == "2":
           new_email = input("Updated Email: ")
           update_member_attribute(member_id, "Email", new_email)
       elif choice == "3":
           new_password = input("Updated Password: ")
           update_member_attribute(member_id, "Password", new_password)
       elif choice == "4":
           new_address = input("Updated Address: ")
           update_member_attribute(member_id, "Address", new_address)
       elif choice == "5":
           new_phone_number = input("Updated Phone Number: ")
           update_member_attribute(member_id, "PhoneNumber", new_phone_number)
       elif choice == "6":
           new_fitness_goals = input("Updated Fitness Goals: ")
           update_member_attribute(member_id, "FitnessGoals", new_fitness_goals)
       elif choice == "7":
           new_health_metrics = input("Updated Health Metrics: ")
           update_member_attribute(member_id, "HealthMetrics", new_health_metrics)
       elif choice == "8":
           break
       else:
           print("Invalid choice, please try again.")

def update_member_attribute(member_id, attribute, new_value):
   try:
       with establish_connection() as conn:
           with conn.cursor() as cur:
               cur.execute(f"UPDATE Members SET {attribute} = %s WHERE MemberID = %s", (new_value, member_id))
               conn.commit()
               print(f"{attribute} updated successfully!")
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

def add_exercise_routine(member_id):
    routine_name = input("Enter the name of the new exercise routine: ")
    routine_details = input("Enter the details of the new exercise routine: ")
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO ExerciseRoutines (MemberID, RoutineName, RoutineDetails) VALUES (%s, %s, %s)", (member_id, routine_name, routine_details))
                conn.commit()
                print("Exercise routine added successfully!")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def add_fitness_achievement(member_id):
    achievement_name = input("Enter the name of the new fitness achievement: ")
    achievement_details = input("Enter the details of the new fitness achievement: ")
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO FitnessAchievements (MemberID, AchievementName, AchievementDetails) VALUES (%s, %s, %s)", (member_id, achievement_name, achievement_details))
                conn.commit()
                print("Fitness achievement added successfully!")
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
                
                cur.execute("SELECT fc.ClassName, fc.Schedule FROM FitnessClasses fc JOIN PersonalTrainingSession pts ON fc.Schedule = pts.Schedule WHERE pts.MemberID = %s", (member_id,))
                classes = cur.fetchall()
                print("\nCurrent Group Fitness Classes:")
                for class_ in classes:
                    print(f"Class Name: {class_[0]}, Schedule: {class_[1]}")

                cur.execute("""
                    SELECT pts.Schedule, t.Name AS TrainerName, t.Specialization
                    FROM PersonalTrainingSession pts 
                    JOIN Trainers t ON pts.TrainerID = t.TrainerID 
                    WHERE pts.MemberID = %s
                """, (member_id,))
                sessions = cur.fetchall()
                print("\nCurrent Personal Training Sessions:")
                for session in sessions:
                    print(f"Schedule: {session[0]}, Trainer Name: {session[1]}, Specialization: {session[2]}")
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
        print("9. Add Exercise Routine")
        print("10. Display Fitness Achievements")
        print("11. Add Fitness Achievement")
        print("12. Logout")
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
            add_exercise_routine(member_id)
        elif choice == "10":
            display_fitness_achievements(member_id)
        elif choice == "11":
            add_fitness_achievement(member_id)
        elif choice == "12":
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
                    print("The room is booked at the following times:")
                    for booking in existing_bookings:
                        print(booking[0])

                    print("Do you want to delete or update a booking? (delete/update/no)")
                    choice = input()
                    if choice.lower() == 'delete':
                        booking_time = input("Enter the booking time to delete (YYYY-MM-DD HH:MM:SS): ")
                        if (booking_time,) in existing_bookings:
                            cur.execute("DELETE FROM RoomBookings WHERE RoomID = %s AND BookingTime = %s", (room_id, booking_time))
                            conn.commit()
                            print("Booking deleted successfully!")
                        else:
                            print("That booking time does not exist.")
                    elif choice.lower() == 'update':
                        old_booking_time = input("Enter the old booking time (YYYY-MM-DD HH:MM:SS): ")
                        if (old_booking_time,) in existing_bookings:
                            new_booking_time = input("Enter the new booking time (YYYY-MM-DD HH:MM:SS): ")
                            cur.execute("UPDATE RoomBookings SET BookingTime = %s WHERE RoomID = %s AND BookingTime = %s", (new_booking_time, room_id, old_booking_time))
                            conn.commit()
                            print("Booking updated successfully!")
                        else:
                            print("That booking time does not exist.")
                else:
                    print("The room is not booked at any time.")
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
    show_available_class_times()
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
                cur.execute("""
                    SELECT b.BillID, b.MemberID, m.Name, b.StaffID, b.Amount, b.BillDate, b.Status 
                    FROM Billing b
                    JOIN Members m ON b.MemberID = m.MemberID
                    ORDER BY b.BillID
                """)
                billing_records = cur.fetchall()
                print("\nBilling Information:")
                for record in billing_records:
                    print(f"Bill ID: {record[0]}, Member ID: {record[1]}, Member Name: {record[2]}, Staff ID: {record[3]}, Amount: {record[4]}, Bill Date: {record[5]}, Status: {record[6]}")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def billing_and_payment_processing():
    list_billing_information()
    print("1. Process payment")
    print("2. Declare as unpaid")
    print("3. Add a bill")
    print("4. Delete a bill")
    choice = input("Select an option: ")

    if choice == "1":
        process_payment()
    elif choice == "2":
        declare_bill_as_unpaid()
    elif choice == "3":
        add_bill_for_member()
    elif choice == "4":
        delete_bill()
    else:
        print("Invalid choice, please try again.")

def process_payment():
    bill_id = input("Enter Bill ID for processing: ")
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT Amount, Status FROM Billing WHERE BillID = %s", (bill_id,))
                amount, status = cur.fetchone()

                if status == 'Paid':
                    print("This bill has already been paid.")
                    return

                print(f"Processing payment for bill ID {bill_id}, amount: {amount}")
                payment_status = simulate_payment_process(amount)  # Simulate the payment process

                if payment_status:
                    cur.execute("UPDATE Billing SET Status = 'Paid' WHERE BillID = %s", (bill_id,))
                    conn.commit()
                    print("Payment successful! Billing status updated.")
                else:
                    print("Payment failed. Please try again.")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def declare_bill_as_unpaid():
    bill_id = input("Enter Bill ID to declare as unpaid: ")
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE Billing SET Status = 'Unpaid' WHERE BillID = %s", (bill_id,))
                conn.commit()
                print("Bill declared as unpaid successfully!")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def add_bill_for_member():
    print_member_names()
    member_name = input("Enter the member's name to add a bill for: ")
    amount = input("Enter the amount of the bill: ")
    bill_date = input("Enter the bill date (YYYY-MM-DD): ")
    status = input("Enter the status of the bill (Paid/Unpaid): ")
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT MemberID FROM Members WHERE Name = %s", (member_name,))
                member_id = cur.fetchone()[0]
                cur.execute("INSERT INTO Billing (MemberID, Amount, BillDate, Status) VALUES (%s, %s, %s, %s)", (member_id, amount, bill_date, status))
                conn.commit()
                print("Bill added successfully!")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def delete_bill():
    print_member_names()
    member_name = input("Enter the member's name to delete a bill for: ")
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT MemberID FROM Members WHERE Name = %s", (member_name,))
                member_id = cur.fetchone()[0]
                cur.execute("SELECT BillID FROM Billing WHERE MemberID = %s", (member_id,))
                bill_ids = cur.fetchall()
                print("Bill IDs:")
                for bill_id in bill_ids:
                    print(bill_id[0])
                bill_id = input("Enter Bill ID to delete: ")
                cur.execute("DELETE FROM Billing WHERE BillID = %s", (bill_id,))
                conn.commit()
                print("Bill deleted successfully!")
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def print_member_names():
    try:
        with establish_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT Name FROM Members")
                member_names = cur.fetchall()
                print("Member Names:")
                for name in member_names:
                    print(name[0])
    except psycopg.DatabaseError as e:
        print(f"Error while accessing the database: {e}")

def simulate_payment_process(amount):
   print(f"Simulating payment process for amount: {amount}")
   print("...")
   return True

def main_menu():
    while True:
        print("\nWelcome to the Health and Fitness Club Management System!")
        print("1. Member Registration")
        print("2. Member Login")
        print("3. Trainer Login")
        print("4. Admin Login")
        print("5. Exit")
        choice = input("Please select an option: ")

        if choice == "1":
            member_registration()
        elif choice == "2":
            member_id = member_login()
            if member_id:
                member_dashboard(member_id)
        elif choice == "3":
            trainer_id = trainer_login()
            if trainer_id:
                trainer_dashboard(trainer_id)
        elif choice == "4":
            staff_id = admin_login()
            if staff_id:
                admin_dashboard(staff_id)
        elif choice == "5":
            print("Thank you for using the Health and Fitness Club Management System!")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
   main_menu()
