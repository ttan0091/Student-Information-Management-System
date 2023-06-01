from unit import Unit
from user import User
# Group Number: 74
# Allocated Tutor Name: Jinx Haung
# Group Members:
# 1. Tan Tao
# 2. Shofi Taneem
# 3. Khanjan Pandya

class UserTeacher(User):
    def __init__(self, user_id: int = 0, user_name: str = "", user_password: str = "", user_role: str = "TA",
                 user_status: str = "enabled", teach_units=None):
        super().__init__(user_id, user_name, user_password, user_role, user_status)
        if teach_units is None:
            teach_units = []
        self.teach_units = teach_units

    def __str__(self):
        return f"{self.user_id}, {self.user_name}, {self.user_password}, {self.user_role}, {self.user_status}, {self.teach_units} "

    def teacher_menu(self):
        print("----------------------Teacher Options:-------------------------")
        print("                     1. List teach units")
        print("                     2. Add teach unit")
        print("                     3. Delete teach unit")
        print("                     4. List enrol students")
        print("                     5. Show avg, max, and min score of a unit")
        print("                     6. Logout")

    def list_teach_units(self):
        if not self.teach_units:
            print("The teacher has no units.")
            return
        header_str = "{:<10} {:<20} {:<40} {:<10}".format("Unit ID", "Unit Code", "Unit Name", "Capacity")
        print(header_str)
        print("-" * len(header_str))
        try:
            with open("data/unit.txt", "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("Error: Could not find the file 'unit.txt'. Please ensure that the file exists and try again.")
            lines = []
        for line in lines:
            unit_details = line.strip().split(", ")
            if unit_details[1] in self.teach_units:
                # Use the defined format string to print each unit info
                unit_str = "{:<10} {:<20} {:<40} {:<10}".format(unit_details[0], unit_details[1], unit_details[2],
                                                                unit_details[3])
                print(unit_str)

    def delete_teach_unit(self, unit_code: str):
        unit_code = unit_code.upper()
        # Remove the unit from the teacher's list
        self.teach_units.remove(unit_code)

        # Rewrite teach_units in data/user.txt file
        self.update_user_teacher()
        print(unit_code, "is removed from the teacher's list.")

        # Remove the unit from the unit.txt file
        try:
            with open(self.file_path_unit, "r") as file:
                lines = file.readlines()
            with open(self.file_path_unit, "w") as file:
                for line in lines:
                    unit_info = line.strip().split(", ")
                    if unit_info[1] != unit_code:
                        file.write(line)
            print(unit_code, "is removed from the Units list.")
        except FileNotFoundError:
            print("The file 'data/unit.txt' could not be found.")
        except Exception as e:
            print("An error occurred -11-:", e)

        # modify the student enrolled_units list in data/user.txt file
        try:
            with open(self.file_path_user, "r") as file:
                lines = file.readlines()
            with open(self.file_path_user, "w") as file:
                for line in lines:
                    user_info = line.strip().split(", ")
                    # Check if the user is a student,and if the unit_code is in the student's list,remove it
                    if user_info[3] == "ST":
                        unit_enrolled = [(k, v) for k, v in (kv.split(":") for kv in user_info[5].split(","))]
                        if any(k == unit_code for k, v in unit_enrolled):
                            unit_enrolled = [(k, v) for k, v in unit_enrolled if k != unit_code]
                            unit_str = ",".join([f"{k}:{v}" for k, v in unit_enrolled])
                            user_info[5] = unit_str
                            line = ", ".join(user_info) + "\n"
                    file.write(line)
                print(f"Unit {unit_code} has been removed from students' lists.")
        except FileNotFoundError:
            print("The file 'data/user.txt' could not be found.")

        print(unit_code, "is removed from the student's enrolled_units list.")

    def list_enrol_students(self, unit_code: str):
        unit_code = unit_code.upper()
        no_student_enrolled = True
        format_str = "{:<10} {:<20}  {:<10} {:<10} {:<10} ".format("user_id", "user_name",
                                                                   "user_role",
                                                                   "user_status", "enrolled_units ")
        print(format_str)
        print("-" * len(format_str))
        try:
            with open(self.file_path_user, "r") as file:
                for line in file:
                    user_info = line.strip().split(", ")
                    # Check if the user is a student, and if the unit_code is in the student's list
                    if user_info[3] == "ST" and any(unit_code in unit_str for unit_str in user_info[5].split(",")):
                        # Use the defined format string to print each student's info
                        student_str = "{:<10} {:<20} {:<10} {:<10} {:<10} ".format(user_info[0], user_info[1],
                                                                                   user_info[3], user_info[4],
                                                                                   user_info[5])
                        print(student_str)
                        no_student_enrolled = False
        except FileNotFoundError:
            print(f"Error: file {self.file_path_user} not found.")
        except Exception as e:
            print("Error occurred: ", e)

        if no_student_enrolled:
            print("No students enrolled in unit", unit_code)

    def add_teach_unit(self, teach_unit: Unit):

        # Check if the unit is already in the list
        if teach_unit.unit_code in self.teach_units:
            print("This unit already exists in teacher's list.")
            return

        # Check if the unit is already in the unit.txt file
        in_unit_file = False
        try:
            with open(self.file_path_unit, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("File not Found!")

        for line in lines:
            unit_info = line.strip().split(", ")
            if unit_info[1] == teach_unit.unit_code:
                in_unit_file = True
                break

        # add unit to the unit.txt file
        if not in_unit_file:
            teach_unit.save_unit()

        # add unit to the teacher's list
        self.teach_units.append(teach_unit.unit_code)
        # Rewrite the data/user.txt file
        self.update_user_teacher()
        print(teach_unit.unit_code, "is added to the teacher's list.")

    def show_unit_avg_max_min_score(self, unit_code: str):
        unit_code = unit_code.upper()
        unit_score = []
        try:
            with open(self.file_path_user, "r") as file:
                for line in file:
                    user_info = line.strip().split(", ")
                    # Check if the user is a student and the unit_code is in the student's enrolled_units list
                    if user_info[3] == "ST" and any(unit_code in unit_str for unit_str in user_info[5].split(",")):
                        for unit_tuple in user_info[5].split(","):
                            # Check if the unit_code matches,if so,append the score to the unit_score list
                            unit_tuple = unit_tuple.split(":")
                            if unit_tuple[0] == unit_code:
                                unit_score.append(int(unit_tuple[1]))
                                break
        except FileNotFoundError:
            print("Error: file not found.")  # or handle the exception in an appropriate way
        if not unit_score:
            print("No students enrolled in unit", unit_code)
            return
        print("Unit code:", unit_code)
        print("Average score:", sum(unit_score) / len(unit_score))
        print("Max score:", max(unit_score))
        print("Min score:", min(unit_score))

    def update_user_teacher(self):
        with open(self.file_path_user, "r") as file:
            lines = file.readlines()
        with open(self.file_path_user, "w") as file:
            for line in lines:
                user_info = line.strip().split(", ")
                if user_info[1] == self.user_name:
                    line = str(self) + "\n"
                file.write(line)
