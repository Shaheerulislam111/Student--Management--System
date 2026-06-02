import json
import os

class Student:
    def _init_(self, student_id, name, grade):
        self.student_id = student_id
        self.name = name
        self.grade = grade

    def to_dict(self):
        return {"id": self.student_id, "name": self.name, "grade": self.grade}

class StudentManager:
    def _init_(self, filename="students.json"):
        self.filename = filename
        self.students = {}
        self.load_records()

    def load_records(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    data = json.load(file)
                    for s_id, s_info in data.items():
                        self.students[s_id] = Student(s_id, s_info['name'], s_info['grade'])
            except json.JSONDecodeError:
                self.students = {}

    def save_records(self):
        with open(self.filename, 'w') as file:
            json_data = {s_id: s_obj.to_dict() for s_id, s_obj in self.students.items()}
            json.dump(json_data, file, indent=4)

    def add_student(self, student_id, name, grade):
        if student_id in self.students:
            print(f"\n[Error] Student with ID '{student_id}' already exists!")
            return False
        self.students[student_id] = Student(student_id, name, grade)
        self.save_records()
        print(f"\n[Success] Student '{name}' added successfully!")
        return True

    def view_students(self):
        if not self.students:
            print("\n[Info] No student records found.")
            return
        print("\n" + "="*45)
        print(f"{'ID':<10} | {'Name':<20} | {'Grade':<10}")
        print("="*45)
        for s_id, s_obj in self.students.items():
            print(f"{s_id:<10} | {s_obj.name:<20} | {s_obj.grade:<10}")
        print("="*45)

    def update_student(self, student_id, new_name, new_grade):
        if student_id not in self.students:
            print(f"\n[Error] Student ID '{student_id}' not found.")
            return False
        if new_name: self.students[student_id].name = new_name
        if new_grade: self.students[student_id].grade = new_grade
        self.save_records()
        print(f"\n[Success] Student ID '{student_id}' updated successfully!")
        return True

    def delete_student(self, student_id):
        if student_id not in self.students:
            print(f"\n[Error] Student ID '{student_id}' not found.")
            return False
        name = self.students[student_id].name
        del self.students[student_id]
        self.save_records()
        print(f"\n[Success] Student '{name}' deleted successfully!")
        return True

def main():
    manager = StudentManager()
    while True:
        print("\n** Student Management System **")
        print("1. Add New Student")
        print("2. View All Students")
        print("3. Update Student Record")
        print("4. Delete Student Record")
        print("5. Exit Application")
        choice = input("\nEnter your choice (1-5): ").strip()
        if choice == '1':
            s_id = input("Enter Student ID: ").strip()
            if not s_id: continue
            name = input("Enter Student Name: ").strip()
            grade = input("Enter Student Grade: ").strip()
            manager.add_student(s_id, name, grade)
        elif choice == '2':
            manager.view_students()
        elif choice == '3':
            s_id = input("Enter Student ID to update: ").strip()
            new_name = input("Enter New Name (or leave blank): ").strip()
            new_grade = input("Enter New Grade (or leave blank): ").strip()
            manager.update_student(s_id, new_name, new_grade)
        elif choice == '4':
            s_id = input("Enter Student ID to delete: ").strip()
            manager.delete_student(s_id)
        elif choice == '5':
            print("\nGoodbye!")
            break
        else:
            print("\n[Invalid Choice] Please try again.")

if _name_ == "_main_":
    main()