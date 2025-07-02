"""
Main Program Module
This module contains the main program logic and user interface
for the Student CRUD Management System.
"""

import os
import sys
from typing import Dict, Any
from student_controller import StudentController
from student_model import Student


class StudentManagementSystem:
    """
    Main class that handles the user interface and program flow.
    This class provides a command-line interface for the CRUD operations.
    """
    
    def __init__(self):
        """Initialize the Student Management System."""
        self.controller = StudentController()
        self.running = True
    
    def clear_screen(self):
        """Clear the terminal screen for better user experience."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self):
        """Display the application header."""
        print("=" * 60)
        print("           STUDENT MANAGEMENT SYSTEM")
        print("         Object-Oriented CRUD Application")
        print("=" * 60)
        print()
    
    def display_menu(self):
        """Display the main menu options."""
        print("MAIN MENU:")
        print("1. Create New Student")
        print("2. View All Students")
        print("3. Search Student by ID")
        print("4. Update Student Information")
        print("5. Delete Student")
        print("6. Search Students")
        print("7. View Statistics")
        print("8. Sample Data (for testing)")
        print("9. Exit")
        print("-" * 40)
    
    def get_user_input(self, prompt: str, input_type: type = str, required: bool = True):
        """
        Get validated user input.
        
        Args:
            prompt (str): Input prompt message
            input_type (type): Expected input type (str, int, float)
            required (bool): Whether input is required
            
        Returns:
            User input converted to specified type
        """
        while True:
            try:
                user_input = input(prompt).strip()
                
                if not user_input and required:
                    print("This field is required. Please enter a value.")
                    continue
                
                if not user_input and not required:
                    return None
                
                if input_type == str:
                    return user_input
                elif input_type == int:
                    return int(user_input)
                elif input_type == float:
                    return float(user_input)
                
            except ValueError:
                print(f"Invalid input. Please enter a valid {input_type.__name__}.")
            except KeyboardInterrupt:
                print("\nOperation cancelled.")
                return None
    
    def create_student_interface(self):
        """Interface for creating a new student."""
        print("\n" + "=" * 40)
        print("CREATE NEW STUDENT")
        print("=" * 40)
        
        try:
            # Collect student information
            student_data = {}
            
            student_data['student_id'] = self.get_user_input("Enter Student ID: ")
            if student_data['student_id'] is None:
                return
            
            student_data['name'] = self.get_user_input("Enter Full Name: ")
            if student_data['name'] is None:
                return
            
            student_data['email'] = self.get_user_input("Enter Email Address: ")
            if student_data['email'] is None:
                return
            
            student_data['age'] = self.get_user_input("Enter Age: ", int)
            if student_data['age'] is None:
                return
            
            student_data['major'] = self.get_user_input("Enter Major/Field of Study: ")
            if student_data['major'] is None:
                return
            
            student_data['gpa'] = self.get_user_input("Enter GPA (0.0-4.0): ", float)
            if student_data['gpa'] is None:
                return
            
            # Create student using controller
            success, message, student = self.controller.create_student(student_data)
            
            print("\n" + "-" * 40)
            if success:
                print("✓ SUCCESS:")
                print(message)
                print(f"\nStudent Details:")
                print(f"ID: {student.student_id}")
                print(f"Name: {student.name}")
                print(f"Email: {student.email}")
                print(f"Age: {student.age}")
                print(f"Major: {student.major}")
                print(f"GPA: {student.gpa:.2f}")
                print(f"Created: {student.created_at}")
            else:
                print("✗ ERROR:")
                print(message)
            
        except Exception as e:
            print(f"✗ Unexpected error: {str(e)}")
        
        input("\nPress Enter to continue...")
    
    def view_all_students_interface(self):
        """Interface for viewing all students."""
        print("\n" + "=" * 40)
        print("ALL STUDENTS")
        print("=" * 40)
        
        success, message, students = self.controller.read_all_students()
        
        print(message)
        
        if success and students:
            print("\n" + "-" * 100)
            print(f"{'ID':<10} {'Name':<20} {'Email':<25} {'Age':<5} {'Major':<15} {'GPA':<5}")
            print("-" * 100)
            
            for student in students:
                print(f"{student.student_id:<10} {student.name:<20} {student.email:<25} "
                      f"{student.age:<5} {student.major:<15} {student.gpa:<5.2f}")
            
            print("-" * 100)
            print(f"Total Students: {len(students)}")
        
        input("\nPress Enter to continue...")
    
    def search_student_by_id_interface(self):
        """Interface for searching a student by ID."""
        print("\n" + "=" * 40)
        print("SEARCH STUDENT BY ID")
        print("=" * 40)
        
        student_id = self.get_user_input("Enter Student ID to search: ")
        if student_id is None:
            return
        
        success, message, student = self.controller.read_student_by_id(student_id)
        
        print("\n" + "-" * 40)
        if success and student:
            print("✓ STUDENT FOUND:")
            print(f"ID: {student.student_id}")
            print(f"Name: {student.name}")
            print(f"Email: {student.email}")
            print(f"Age: {student.age}")
            print(f"Major: {student.major}")
            print(f"GPA: {student.gpa:.2f}")
            print(f"Created: {student.created_at}")
            print(f"Last Updated: {student.updated_at}")
        else:
            print("✗ " + message)
        
        input("\nPress Enter to continue...")
    
    def update_student_interface(self):
        """Interface for updating student information."""
        print("\n" + "=" * 40)
        print("UPDATE STUDENT INFORMATION")
        print("=" * 40)
        
        student_id = self.get_user_input("Enter Student ID to update: ")
        if student_id is None:
            return
        
        # First, check if student exists
        success, message, student = self.controller.read_student_by_id(student_id)
        
        if not success or not student:
            print(f"✗ {message}")
            input("\nPress Enter to continue...")
            return
        
        # Display current information
        print(f"\nCurrent Information for {student.name}:")
        print(f"1. Name: {student.name}")
        print(f"2. Email: {student.email}")
        print(f"3. Age: {student.age}")
        print(f"4. Major: {student.major}")
        print(f"5. GPA: {student.gpa:.2f}")
        
        print("\nEnter new values (press Enter to keep current value):")
        
        updated_data = {}
        
        new_name = self.get_user_input(f"New Name [{student.name}]: ", required=False)
        if new_name:
            updated_data['name'] = new_name
        
        new_email = self.get_user_input(f"New Email [{student.email}]: ", required=False)
        if new_email:
            updated_data['email'] = new_email
        
        new_age = self.get_user_input(f"New Age [{student.age}]: ", int, required=False)
        if new_age is not None:
            updated_data['age'] = new_age
        
        new_major = self.get_user_input(f"New Major [{student.major}]: ", required=False)
        if new_major:
            updated_data['major'] = new_major
        
        new_gpa = self.get_user_input(f"New GPA [{student.gpa:.2f}]: ", float, required=False)
        if new_gpa is not None:
            updated_data['gpa'] = new_gpa
        
        if not updated_data:
            print("No changes made.")
            input("\nPress Enter to continue...")
            return
        
        # Update student
        success, message, updated_student = self.controller.update_student(student_id, updated_data)
        
        print("\n" + "-" * 40)
        if success:
            print("✓ SUCCESS:")
            print(message)
            print(f"\nUpdated Information:")
            print(f"ID: {updated_student.student_id}")
            print(f"Name: {updated_student.name}")
            print(f"Email: {updated_student.email}")
            print(f"Age: {updated_student.age}")
            print(f"Major: {updated_student.major}")
            print(f"GPA: {updated_student.gpa:.2f}")
            print(f"Last Updated: {updated_student.updated_at}")
        else:
            print("✗ ERROR:")
            print(message)
        
        input("\nPress Enter to continue...")
    
    def delete_student_interface(self):
        """Interface for deleting a student."""
        print("\n" + "=" * 40)
        print("DELETE STUDENT")
        print("=" * 40)
        
        student_id = self.get_user_input("Enter Student ID to delete: ")
        if student_id is None:
            return
        
        # First, show student information
        success, message, student = self.controller.read_student_by_id(student_id)
        
        if not success or not student:
            print(f"✗ {message}")
            input("\nPress Enter to continue...")
            return
        
        # Display student information
        print(f"\nStudent to be deleted:")
        print(f"ID: {student.student_id}")
        print(f"Name: {student.name}")
        print(f"Email: {student.email}")
        print(f"Major: {student.major}")
        
        # Confirm deletion
        confirm = self.get_user_input("\nAre you sure you want to delete this student? (yes/no): ")
        
        if confirm and confirm.lower() in ['yes', 'y']:
            success, message = self.controller.delete_student(student_id)
            
            print("\n" + "-" * 40)
            if success:
                print("✓ SUCCESS:")
                print(message)
            else:
                print("✗ ERROR:")
                print(message)
        else:
            print("Deletion cancelled.")
        
        input("\nPress Enter to continue...")
    
    def search_students_interface(self):
        """Interface for searching students by different criteria."""
        print("\n" + "=" * 40)
        print("SEARCH STUDENTS")
        print("=" * 40)
        
        print("Search by:")
        print("1. Name")
        print("2. Major")
        print("3. Email")
        print("4. Student ID")
        
        choice = self.get_user_input("Enter your choice (1-4): ")
        if choice is None:
            return
        
        field_map = {
            '1': 'name',
            '2': 'major',
            '3': 'email',
            '4': 'student_id'
        }
        
        if choice not in field_map:
            print("Invalid choice.")
            input("\nPress Enter to continue...")
            return
        
        search_field = field_map[choice]
        search_term = self.get_user_input(f"Enter search term for {search_field}: ")
        if search_term is None:
            return
        
        success, message, students = self.controller.search_students(search_term, search_field)
        
        print("\n" + "-" * 40)
        print(message)
        
        if success and students:
            print("\n" + "-" * 100)
            print(f"{'ID':<10} {'Name':<20} {'Email':<25} {'Age':<5} {'Major':<15} {'GPA':<5}")
            print("-" * 100)
            
            for student in students:
                print(f"{student.student_id:<10} {student.name:<20} {student.email:<25} "
                      f"{student.age:<5} {student.major:<15} {student.gpa:<5.2f}")
            
            print("-" * 100)
        
        input("\nPress Enter to continue...")
    
    def view_statistics_interface(self):
        """Interface for viewing system statistics."""
        print("\n" + "=" * 40)
        print("SYSTEM STATISTICS")
        print("=" * 40)
        
        success, message, stats = self.controller.get_statistics()
        
        if success and stats:
            print(f"Total Students: {stats['total_students']}")
            print(f"Average GPA: {stats['average_gpa']}")
            print(f"Highest GPA: {stats['highest_gpa']}")
            print(f"Lowest GPA: {stats['lowest_gpa']}")
            print(f"Average Age: {stats['average_age']} years")
            
            print("\nMajor Distribution:")
            print("-" * 30)
            for major, count in stats['major_distribution'].items():
                percentage = (count / stats['total_students']) * 100
                print(f"{major}: {count} students ({percentage:.1f}%)")
        else:
            print(message)
        
        input("\nPress Enter to continue...")
    
    def load_sample_data(self):
        """Load sample data for testing purposes."""
        print("\n" + "=" * 40)
        print("LOAD SAMPLE DATA")
        print("=" * 40)
        
        sample_students = [
            {
                'student_id': 'STU001',
                'name': 'John Doe',
                'email': 'john.doe@email.com',
                'age': 20,
                'major': 'Computer Science',
                'gpa': 3.8
            },
            {
                'student_id': 'STU002',
                'name': 'Jane Smith',
                'email': 'jane.smith@email.com',
                'age': 19,
                'major': 'Mathematics',
                'gpa': 3.9
            },
            {
                'student_id': 'STU003',
                'name': 'Mike Johnson',
                'email': 'mike.johnson@email.com',
                'age': 21,
                'major': 'Physics',
                'gpa': 3.5
            },
            {
                'student_id': 'STU004',
                'name': 'Sarah Wilson',
                'email': 'sarah.wilson@email.com',
                'age': 20,
                'major': 'Computer Science',
                'gpa': 3.7
            },
            {
                'student_id': 'STU005',
                'name': 'David Brown',
                'email': 'david.brown@email.com',
                'age': 22,
                'major': 'Engineering',
                'gpa': 3.6
            }
        ]
        
        success_count = 0
        for student_data in sample_students:
            success, message, student = self.controller.create_student(student_data)
            if success:
                success_count += 1
        
        print(f"✓ Successfully loaded {success_count} sample students.")
        print("You can now test all CRUD operations with this sample data.")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main program loop."""
        print("Welcome to the Student Management System!")
        print("Loading application...")
        
        while self.running:
            try:
                self.clear_screen()
                self.display_header()
                self.display_menu()
                
                choice = self.get_user_input("Enter your choice (1-9): ")
                
                if choice == '1':
                    self.create_student_interface()
                elif choice == '2':
                    self.view_all_students_interface()
                elif choice == '3':
                    self.search_student_by_id_interface()
                elif choice == '4':
                    self.update_student_interface()
                elif choice == '5':
                    self.delete_student_interface()
                elif choice == '6':
                    self.search_students_interface()
                elif choice == '7':
                    self.view_statistics_interface()
                elif choice == '8':
                    self.load_sample_data()
                elif choice == '9':
                    print("\nThank you for using the Student Management System!")
                    print("Goodbye!")
                    self.running = False
                else:
                    print("Invalid choice. Please select a number from 1-9.")
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\nProgram interrupted by user.")
                confirm = input("Do you want to exit? (yes/no): ")
                if confirm.lower() in ['yes', 'y']:
                    self.running = False
            except Exception as e:
                print(f"\nUnexpected error: {str(e)}")
                input("Press Enter to continue...")


def main():
    """
    Main function to start the Student Management System.
    This is the entry point of the application.
    """
    try:
        # Create and run the application
        app = StudentManagementSystem()
        app.run()
        
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        print("Please contact the system administrator.")
        sys.exit(1)


# Entry point of the program
if __name__ == "__main__":
    main()
