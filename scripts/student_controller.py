"""
Student Controller Module
This module contains the StudentController class which handles
all CRUD operations and business logic for student management.
"""

from typing import List, Dict, Any, Optional, Tuple
from student_model import Student


class StudentController:
    """
    StudentController class handles all CRUD operations for student data.
    This class acts as the business logic layer between the model and the view.
    """
    
    def __init__(self):
        """
        Initialize the StudentController with an empty list of students.
        This list serves as our temporary data storage.
        """
        self.students_data: List[Dict[str, Any]] = []
    
    def create_student(self, student_data: Dict[str, Any]) -> Tuple[bool, str, Optional[Student]]:
        """
        Create a new student record.
        
        Args:
            student_data (Dict[str, Any]): Dictionary containing student information
            
        Returns:
            Tuple[bool, str, Optional[Student]]: (success, message, student_object)
        """
        try:
            # Create Student object from provided data
            student = Student(
                student_id=student_data.get('student_id', ''),
                name=student_data.get('name', ''),
                email=student_data.get('email', ''),
                age=student_data.get('age', 0),
                major=student_data.get('major', ''),
                gpa=student_data.get('gpa', 0.0)
            )
            
            # Get existing student IDs for validation
            existing_ids = [s['student_id'] for s in self.students_data]
            
            # Validate all fields
            is_valid, errors = student.validate_all_fields(existing_ids)
            
            if not is_valid:
                error_message = "Validation failed:\n" + "\n".join(f"- {error}" for error in errors)
                return False, error_message, None
            
            # Add student to data storage
            self.students_data.append(student.to_dict())
            
            return True, f"Student {student.name} (ID: {student.student_id}) created successfully!", student
            
        except Exception as e:
            return False, f"Error creating student: {str(e)}", None
    
    def read_all_students(self) -> Tuple[bool, str, List[Student]]:
        """
        Retrieve all student records.
        
        Returns:
            Tuple[bool, str, List[Student]]: (success, message, list_of_students)
        """
        try:
            if not self.students_data:
                return True, "No students found in the system.", []
            
            students = [Student.from_dict(data) for data in self.students_data]
            return True, f"Found {len(students)} student(s).", students
            
        except Exception as e:
            return False, f"Error retrieving students: {str(e)}", []
    
    def read_student_by_id(self, student_id: str) -> Tuple[bool, str, Optional[Student]]:
        """
        Retrieve a specific student by ID.
        
        Args:
            student_id (str): ID of the student to retrieve
            
        Returns:
            Tuple[bool, str, Optional[Student]]: (success, message, student_object)
        """
        try:
            if not student_id:
                return False, "Student ID cannot be empty.", None
            
            # Search for student with matching ID
            for data in self.students_data:
                if data['student_id'] == student_id:
                    student = Student.from_dict(data)
                    return True, "Student found successfully.", student
            
            return False, f"Student with ID '{student_id}' not found.", None
            
        except Exception as e:
            return False, f"Error retrieving student: {str(e)}", None
    
    def update_student(self, student_id: str, updated_data: Dict[str, Any]) -> Tuple[bool, str, Optional[Student]]:
        """
        Update an existing student record.
        
        Args:
            student_id (str): ID of the student to update
            updated_data (Dict[str, Any]): Dictionary containing updated information
            
        Returns:
            Tuple[bool, str, Optional[Student]]: (success, message, updated_student_object)
        """
        try:
            if not student_id:
                return False, "Student ID cannot be empty.", None
            
            # Find the student to update
            student_index = None
            for i, data in enumerate(self.students_data):
                if data['student_id'] == student_id:
                    student_index = i
                    break
            
            if student_index is None:
                return False, f"Student with ID '{student_id}' not found.", None
            
            # Get current student data
            current_data = self.students_data[student_index].copy()
            
            # Update only provided fields
            for key, value in updated_data.items():
                if key in current_data and key != 'student_id':  # Don't allow ID changes
                    current_data[key] = value
            
            # Create updated student object for validation
            updated_student = Student.from_dict(current_data)
            
            # Get existing IDs (excluding current student)
            existing_ids = [s['student_id'] for i, s in enumerate(self.students_data) if i != student_index]
            
            # Validate updated data
            is_valid, errors = updated_student.validate_all_fields(existing_ids)
            
            if not is_valid:
                error_message = "Validation failed:\n" + "\n".join(f"- {error}" for error in errors)
                return False, error_message, None
            
            # Update timestamp
            updated_student.update_timestamp()
            
            # Save updated data
            self.students_data[student_index] = updated_student.to_dict()
            
            return True, f"Student {updated_student.name} (ID: {student_id}) updated successfully!", updated_student
            
        except Exception as e:
            return False, f"Error updating student: {str(e)}", None
    
    def delete_student(self, student_id: str) -> Tuple[bool, str]:
        """
        Delete a student record.
        
        Args:
            student_id (str): ID of the student to delete
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            if not student_id:
                return False, "Student ID cannot be empty."
            
            # Find and remove the student
            for i, data in enumerate(self.students_data):
                if data['student_id'] == student_id:
                    deleted_student = self.students_data.pop(i)
                    return True, f"Student {deleted_student['name']} (ID: {student_id}) deleted successfully!"
            
            return False, f"Student with ID '{student_id}' not found."
            
        except Exception as e:
            return False, f"Error deleting student: {str(e)}"
    
    def search_students(self, search_term: str, search_field: str = 'name') -> Tuple[bool, str, List[Student]]:
        """
        Search for students based on a specific field.
        
        Args:
            search_term (str): Term to search for
            search_field (str): Field to search in ('name', 'major', 'email')
            
        Returns:
            Tuple[bool, str, List[Student]]: (success, message, list_of_matching_students)
        """
        try:
            if not search_term:
                return False, "Search term cannot be empty.", []
            
            valid_fields = ['name', 'major', 'email', 'student_id']
            if search_field not in valid_fields:
                return False, f"Invalid search field. Valid fields: {', '.join(valid_fields)}", []
            
            matching_students = []
            search_term_lower = search_term.lower()
            
            for data in self.students_data:
                field_value = str(data.get(search_field, '')).lower()
                if search_term_lower in field_value:
                    matching_students.append(Student.from_dict(data))
            
            if not matching_students:
                return True, f"No students found matching '{search_term}' in {search_field}.", []
            
            return True, f"Found {len(matching_students)} student(s) matching '{search_term}' in {search_field}.", matching_students
            
        except Exception as e:
            return False, f"Error searching students: {str(e)}", []
    
    def get_statistics(self) -> Tuple[bool, str, Dict[str, Any]]:
        """
        Get statistical information about students.
        
        Returns:
            Tuple[bool, str, Dict[str, Any]]: (success, message, statistics_dict)
        """
        try:
            if not self.students_data:
                return True, "No students in the system.", {}
            
            total_students = len(self.students_data)
            gpas = [data['gpa'] for data in self.students_data]
            ages = [data['age'] for data in self.students_data]
            majors = [data['major'] for data in self.students_data]
            
            # Calculate statistics
            avg_gpa = sum(gpas) / len(gpas)
            max_gpa = max(gpas)
            min_gpa = min(gpas)
            avg_age = sum(ages) / len(ages)
            
            # Count majors
            major_counts = {}
            for major in majors:
                major_counts[major] = major_counts.get(major, 0) + 1
            
            statistics = {
                'total_students': total_students,
                'average_gpa': round(avg_gpa, 2),
                'highest_gpa': max_gpa,
                'lowest_gpa': min_gpa,
                'average_age': round(avg_age, 1),
                'major_distribution': major_counts
            }
            
            return True, "Statistics calculated successfully.", statistics
            
        except Exception as e:
            return False, f"Error calculating statistics: {str(e)}", {}
    
    def export_data(self) -> Tuple[bool, str, List[Dict[str, Any]]]:
        """
        Export all student data.
        
        Returns:
            Tuple[bool, str, List[Dict[str, Any]]]: (success, message, student_data_list)
        """
        try:
            return True, f"Exported {len(self.students_data)} student records.", self.students_data.copy()
        except Exception as e:
            return False, f"Error exporting data: {str(e)}", []
    
    def import_data(self, data: List[Dict[str, Any]]) -> Tuple[bool, str]:
        """
        Import student data (replace existing data).
        
        Args:
            data (List[Dict[str, Any]]): List of student data dictionaries
            
        Returns:
            Tuple[bool, str]: (success, message)
        """
        try:
            # Validate imported data
            valid_students = []
            errors = []
            
            for i, student_data in enumerate(data):
                student = Student.from_dict(student_data)
                existing_ids = [s.student_id for s in valid_students]
                is_valid, validation_errors = student.validate_all_fields(existing_ids)
                
                if is_valid:
                    valid_students.append(student)
                else:
                    errors.append(f"Row {i+1}: " + ", ".join(validation_errors))
            
            if errors:
                return False, "Import failed due to validation errors:\n" + "\n".join(errors)
            
            # Replace existing data
            self.students_data = [student.to_dict() for student in valid_students]
            
            return True, f"Successfully imported {len(valid_students)} student records."
            
        except Exception as e:
            return False, f"Error importing data: {str(e)}"
