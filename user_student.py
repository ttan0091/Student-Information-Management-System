from user import User
from unit import Unit
import random
# Group Number: 74
# Allocated Tutor Name: Jinx Haung
# Group Members:
# 1. Tan Tao
# 2. Shofi Taneem
# 3. Khanjan Pandya

class UserStudent(User):
    def __init__(self, user_id=0, user_name="", user_password="", user_role="ST", user_status="enabled",
                 enrolled_units=None):
        super().__init__(user_id, user_name, user_password, user_role, user_status)
        if enrolled_units is None:
            enrolled_units = []
        self.enrolled_units = enrolled_units

    def __str__(self):
        enrolled_units_str = ""
        for unit, score in self.enrolled_units:
            enrolled_units_str += f"{unit}:{score},"
        enrolled_units_str = enrolled_units_str.rstrip(',')
        return super().__str__() + ", " + enrolled_units_str

    def student_menu(self):
        print("-----------------------Student options:---------------------")
        print("                     1. List available units")
        print("                     2. List enrolled units")
        print("                     3. Enrol a unit")
        print("                     4. Drop a unit")
        print("                     5. Check score")
        print("                     6. Generate score")
        print("                     7. Logout")

    def list_available_units(self):
        available_units = []
        with open(self.file_path_unit, "r") as file:
            for line in file:
                unit_info = line.strip().split(", ")
                if int(unit_info[3]) > 0:  # the capacity of the unit > 0
                    available_units.append(unit_info)

        if len(available_units) == 0:
            print("Sorry, there are no available units")
        else:
            # Define the format string with headers and field width
            format_str = "{:<10} {:<20} {:<30}".format("Unit ID", "Unit name", "Unit Description")
            print(format_str)
            print("-" * len(format_str))

            for unit_info in available_units:
                # Use the defined format string to print each unit info
                unit_str = "{:<10} {:<20} {:<30}".format(unit_info[0], unit_info[1], unit_info[2])
                print(unit_str)

    def list_enrolled_units(self):
        if not self.enrolled_units:
            print("The student has no units.")
            return

        print("{:<10}{:<10}".format("Unit", "Score"))
        print("-" * 20)
        for unit, score in self.enrolled_units:
            print("{:<10}{:<10}".format(unit, score))

    def enrol_unit(self, unit_code):
        # check if the student has already enrolled in 3 units
        if len(self.enrolled_units) >= 3:
            print("Sorry, you cannot enrol in more than 3 units")
            return
        unit_code = unit_code.upper()
        # check if the student has already enrolled
        for code, score in self.enrolled_units:
            if code == unit_code:
                print("Sorry, you have already enrolled in this unit")
                return

        # get the details of unit
        unit = self.get_unit_by_code(unit_code)

        if unit is None:
            print("Sorry, the unit does not exist")
            return

        # check if the unit is full
        if unit.unit_capacity <= 0:
            print("Sorry, the unit is full")
            return

        # update the enrolled units of the student
        self.enrolled_units.append((unit_code, -1))
        # write the student back to the file
        self.update_user_student()

        # write the new capacity back to the unit file
        unit.unit_capacity -= 1
        unit.update_unit()
        print("You have successfully enrolled in the unit:" + unit_code)

    def drop_unit(self, unit_code):
        unit_code = unit_code.upper()
        # check if the unit is enrolled by the student
        enrolled = False
        for unit_c, score in self.enrolled_units:
            if unit_c == unit_code:
                enrolled = True
                # modify the enrolled units of the student object
                self.enrolled_units.remove((unit_c, score))
                break

        if not enrolled:
            print("Sorry, you are not enrolled in this unit")
            return

        # write the new capacity back to the file
        unit = self.get_unit_by_code(unit_code)
        unit.unit_capacity += 1
        unit.update_unit()
        print("You have successfully dropped the unit:" + unit_code)

        # write the student back to the file
        self.update_user_student()


    def check_score(self, unit_code=""):
        if unit_code:
            # check score for a specific unit
            unit_code = unit_code.upper()
            for unit, score in self.enrolled_units:
                if unit == unit_code:
                    print(f"{'Unit':<10}{'Score':<10}")
                    print("-" * 20)
                    print(f"{unit:<10}{score:<10}")
                    return
            print(f"Sorry, you are not enrolled in {unit_code}")
        else:
            # check score for all units
            print("All units you have enrolled in:")
            print(f"{'Unit':<10}{'Score':<10}")
            print("-" * 20)
            for unit, score in self.enrolled_units:
                print(f"{unit:<10}{score:<10}")

    def generate_score(self, unit_code):
        unit_code = unit_code.upper()
        # check if the unit is in the unit.txt file
        unit = self.get_unit_by_code(unit_code)
        if unit is None:
            print("Sorry, the unit does not exist")
            return

        # check if the unit is enrolled by the student
        enrolled = False
        for unit_c, score in self.enrolled_units:
            if unit_c == unit_code:
                enrolled = True
                break

        if not enrolled:
            print("Sorry, you are not enrolled in this unit")
            return

        # find the tuple of the unit
        score_str = -1
        for unit, score in self.enrolled_units:
            if unit == unit_code:
                score_str = score
                break
        # remove the item from the list
        self.enrolled_units.remove((unit_code, score_str))
        # generate a random score
        score_str = random.randint(0, 100)
        # add the tuple back to the list
        self.enrolled_units.append((unit_code, score_str))
        print("Score Generated!")
        print("Your score for " + unit_code + " is " + str(score_str))

        # write the student back to the file
        self.update_user_student()

    def get_unit_by_code(self, unit_code):
        unit_code = unit_code.upper()
        with open(self.file_path_unit, "r") as file:
            lines = file.readlines()
            for line in lines:
                values = line.strip().split(", ")
                if values[1].upper() == unit_code:
                    unit = Unit(int(values[0]), values[1], values[2], int(values[3]))
                    return unit
            return None

    def update_user_student(self):
        with open(self.file_path_user, "r") as file:
            lines = file.readlines()
        with open(self.file_path_user, "w") as file:
            for line in lines:
                user_info = line.strip().split(", ")
                if user_info[0] == self.user_id:
                    line = str(self) + "\n"
                file.write(line)
