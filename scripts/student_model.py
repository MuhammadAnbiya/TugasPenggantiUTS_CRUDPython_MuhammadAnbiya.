"""
Student Model Module
This module contains the Student class which represents the data model
for student information with validation methods.
"""

import re
from datetime import datetime
from typing import Dict, Any, Optional


class Student:
    """
    Student class represents a student entity with validation methods.
    This class handles the data structure and validation logic for student information.
    """
    
    def __init__(self, student_id: str = "", name: str = "", email: str = "", 
                 age: int = 0, major: str = "", gpa: float = 0.0):
        """
        Initialize a Student object with provided information.
        
        Args:
            student_id (str): Unique identifier for the student
            name (str): Full name of the student
            email (str): Email address of the student
            age (int): Age of the student
            major (str): Academic major/field of study
            gpa (float): Grade Point Average (0.0 - 4.0)
        """
        self.student_id = student_id
        self.name = name
        self.email = email
        self.age = age
        self.major = major
        self.gpa = gpa
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.updated_at = self.created_at
    
    def validate_student_id(self, student_id: str) -> tuple[bool, str]:
        """
        Validate student ID format and uniqueness.
        
        Args:
            student_id (str): Student ID to validate
            
        Returns:
            tuple[bool, str]: (is_valid, error_message)
        """
        if not student_id:
            return False, "Student ID cannot be empty"
        
        if len(student_id) < 3:
            return False, "Student ID must be at least 3 characters long"
        
        # Check if student ID contains only alphanumeric characters
        if not student_id.isalnum():
            return False, "Student ID must contain only letters and numbers"
        
        return True, ""
    
    def validate_name(self, name: str) -> tuple[bool, str]:
        """
        Validate student name.
        
        Args:
            name (str): Student name to validate
            
        Returns:
            tuple[bool, str]: (is_valid, error_message)
        """
        if not name or not name.strip():
            return False, "Name cannot be empty"
        
        if len(name.strip()) < 2:
            return False, "Name must be at least 2 characters long"
        
        # Check if name contains only letters and spaces
        if not re.match(r"^[a-zA-Z\s]+$", name.strip()):
            return False, "Name must contain only letters and spaces"
        
        return True, ""
    
    def validate_email(self, email: str) -> tuple[bool, str]:
        """
        Validate email format using regex.
        
        Args:
            email (str): Email address to validate
            
        Returns:
            tuple[bool, str]: (is_valid, error_message)
        """
        if not email:
            return False, "Email cannot be empty"
        
        # Basic email regex pattern
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            return False, "Invalid email format"
        
        return True, ""
    
    def validate_age(self, age: int) -> tuple[bool, str]:
        """
        Validate student age.
        
        Args:
            age (int): Age to validate
            
        Returns:
            tuple[bool, str]: (is_valid, error_message)
        """
        if not isinstance(age, int):
            return False, "Age must be a number"
        
        if age < 16 or age > 100:
            return False, "Age must be between 16 and 100"
        
        return True, ""
    
    def validate_major(self, major: str) -> tuple[bool, str]:
        """
        Validate student major/field of study.
        
        Args:
            major (str): Major to validate
            
        Returns:
            tuple[bool, str]: (is_valid, error_message)
        """
        if not major or not major.strip():
            return False, "Major cannot be empty"
        
        if len(major.strip()) < 2:
            return False, "Major must be at least 2 characters long"
        
        return True, ""
    
    def validate_gpa(self, gpa: float) -> tuple[bool, str]:
        """
        Validate GPA value.
        
        Args:
            gpa (float): GPA to validate
            
        Returns:
            tuple[bool, str]: (is_valid, error_message)
        """
        if not isinstance(gpa, (int, float)):
            return False, "GPA must be a number"
        
        if gpa < 0.0 or gpa > 4.0:
            return False, "GPA must be between 0.0 and 4.0"
        
        return True, ""
    
    def validate_all_fields(self, existing_ids: list = None) -> tuple[bool, list]:
        """
        Validate all student fields at once.
        
        Args:
            existing_ids (list): List of existing student IDs to check for duplicates
            
        Returns:
            tuple[bool, list]: (is_valid, list_of_error_messages)
        """
        errors = []
        existing_ids = existing_ids or []
        
        # Validate each field
        is_valid, error = self.validate_student_id(self.student_id)
        if not is_valid:
            errors.append(error)
        elif self.student_id in existing_ids:
            errors.append("Student ID already exists")
        
        is_valid, error = self.validate_name(self.name)
        if not is_valid:
            errors.append(error)
        
        is_valid, error = self.validate_email(self.email)
        if not is_valid:
            errors.append(error)
        
        is_valid, error = self.validate_age(self.age)
        if not is_valid:
            errors.append(error)
        
        is_valid, error = self.validate_major(self.major)
        if not is_valid:
            errors.append(error)
        
        is_valid, error = self.validate_gpa(self.gpa)
        if not is_valid:
            errors.append(error)
        
        return len(errors) == 0, errors
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert Student object to dictionary format.
        
        Returns:
            Dict[str, Any]: Dictionary representation of the student
        """
        return {
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'age': self.age,
            'major': self.major,
            'gpa': self.gpa,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Student':
        """
        Create Student object from dictionary data.
        
        Args:
            data (Dict[str, Any]): Dictionary containing student data
            
        Returns:
            Student: Student object created from dictionary
        """
        student = cls(
            student_id=data.get('student_id', ''),
            name=data.get('name', ''),
            email=data.get('email', ''),
            age=data.get('age', 0),
            major=data.get('major', ''),
            gpa=data.get('gpa', 0.0)
        )
        
        # Preserve timestamps if they exist
        if 'created_at' in data:
            student.created_at = data['created_at']
        if 'updated_at' in data:
            student.updated_at = data['updated_at']
        
        return student
    
    def update_timestamp(self):
        """Update the last modified timestamp."""
        self.updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def __str__(self) -> str:
        """
        String representation of the Student object.
        
        Returns:
            str: Formatted string representation
        """
        return (f"Student(ID: {self.student_id}, Name: {self.name}, "
                f"Email: {self.email}, Age: {self.age}, Major: {self.major}, "
                f"GPA: {self.gpa:.2f})")
    
    def __repr__(self) -> str:
        """
        Official string representation of the Student object.
        
        Returns:
            str: Official string representation
        """
        return self.__str__()
