import random
import re
import string

from user import User
from user_admin import UserAdmin
from user_student import UserStudent
from user_teacher import UserTeacher
from unit import Unit
# Group Number: 74
# Allocated Tutor Name: Jinx Haung
# Group Members:
# 1. Tan Tao
# 2. Shofi Taneem
# 3. Khanjan Pandya

def generate_test_data():
    # create admin user
    admin = UserAdmin(user_name="admin", user_password="password")
    with open(admin.file_path_user, "w") as file:
        file.write(str(admin) + "\n")

    # create units
    units = [Unit(unit_code="FIT9131", unit_name="Java", unit_capacity=15),
             Unit(unit_code="FIT9132", unit_name="Database", unit_capacity=15),
             Unit(unit_code="FIT9136", unit_name="Python", unit_capacity=15)]
    with open(admin.file_path_unit, "w") as file:
        for unit in units:
            file.write(str(unit) + "\n")

    # create teachers and assign to units
    teachers = [UserTeacher(user_name="John Jones", user_password="password", teach_units=[units[0].unit_code]),
                UserTeacher(user_name="Ethan Lee", user_password="password", teach_units=[units[1].unit_code]),
                UserTeacher(user_name="Grace Chen", user_password="password", teach_units=[units[2].unit_code])]

    with open(admin.file_path_user, "a") as file:
        for teacher in teachers:
            file.write(str(teacher) + "\n")

    # create 10 students and assign to units
    student_names = ["Jack Sparrow", "Michael Davis", "Sarah Thompson", "Brandon Lee", "Rachel Hernandez",
                     "David Wilson", "Megan Rodriguez", "Christopher Brown", "Jasmine Garcia", "Tyler Mitchell"]
    students = [UserStudent(user_name=name, user_password="password",
                            enrolled_units=[(unit.unit_code, random.randint(0, 100)) for unit in units])
                for name in student_names]

    with open(admin.file_path_user, "a") as file:
        for student in students:
            file.write(str(student) + "\n")


def main_menu():
    print("-------Welcome to Student Information Management System-------")
    print("                     1. Admin")
    print("                     2. Teacher")
    print("                     3. Student")
    print("                     4. Exit")


def main():
    # generate test data
    generate_test_data()
    while True:
        main_menu()
        # validate input , input must be a number between 1 and 4
        role = validate_number_between(1, 4, "Please choose your role : ")
        #  admin
        if role == 1:
            main_admin()
        # teacher
        elif role == 2:
            main_teacher()
        # student
        elif role == 3:
            main_student()
        # exit
        elif role == 4:
            print("-------Thank you for using our system-------")
            return


def main_admin():
    print("Login as admin")

    # validate username and password
    user = validate_role()
    if user.user_role != "AD":
        print("You are not admin, please select role again")
        return

    print("Welcome, " + user.user_name + "!")
    # convert user to UserAdmin
    user_password = user.user_password
    user = UserAdmin(user_id=user.user_id, user_name=user.user_name)
    # Can not use the constructor to set the password, will cause double encryption
    user.user_password = user_password

    # display admin menu, do the action
    while True:
        user.admin_menu()
        # validate input , input must be a number between 1 and 7

        option = validate_number_between(1, 7, "Select an option(1-7):")

        if option == 1:
            str_name = input("Please enter the user name : ")
            user.search_user(str_name)
        elif option == 2:
            user.list_all_users()
        elif option == 3:
            user.list_all_units()
        elif option == 4:
            str_name = input("Please enter the user name : ")
            user.enable_disable_user(str_name)
        elif option == 5:
            str_name = validate_username_input()
            str_password = validate_password_input()
            str_role = validate_ad_ta_st_input()
            str_status = validate_enable_disable_input()

            new_user = User(user_name=str_name, user_password=str_password,
                            user_role=str_role, user_status=str_status)
            user.add_user(new_user)
        elif option == 6:
            str_name = validate_username_input()
            user.delete_user(str_name)
        else:
            break


def main_teacher():
    print("Login as teacher")

    # validate username and password
    user = validate_role()
    if user.user_role != "TA":
        print("You are not a teacher, please select role again.")
        return
    print("Welcome, " + user.user_name + "!")

    # convert user to UserTeacher
    user_password = user.user_password
    user = UserTeacher(user_id=user.user_id, user_name=user.user_name)
    user.user_password = user_password
    # get teach units from file
    with open(user.file_path_user, "r") as f:
        for line in f:
            if line.split(", ")[0] == user.user_id:
                pattern = r"\'(.*?)\'"  # get the string between ''
                match = re.findall(pattern, line)
                user.teach_units.extend(match)
                break
    # display teacher menu, do the action
    while True:
        user.teacher_menu()
        # validate input , input must be a number between 1 and 6
        option = validate_number_between(1, 6, "Select an option(1-6):")

        if option == 1:
            user.list_teach_units()
        elif option == 2:
            # create a new unit
            unit_code = validate_unitcode_input()
            unit_name = validate_unitname_input()
            unit_capacity = validate_number_between(1, 300, "Please enter the unit capacity(1-300) : ")
            unit = Unit(unit_code=unit_code, unit_name=unit_name, unit_capacity=unit_capacity)

            user.add_teach_unit(unit)
        elif option == 3:
            str_unit_code = validate_unitcode_input()
            if str_unit_code not in user.teach_units:
                print("You are not teaching this unit")
            else:
                user.delete_teach_unit(str_unit_code)
        elif option == 4:
            str_unit_code = validate_unitcode_input()
            if str_unit_code not in user.teach_units:
                print("You are not teaching this unit")
            else:
                print("Students enrolled in Unit " + str_unit_code + " :")
                user.list_enrol_students(str_unit_code)
        elif option == 5:
            str_unit_code = validate_unitcode_input()
            if str_unit_code not in user.teach_units:
                print("You are not teaching this unit")
            else:
                user.show_unit_avg_max_min_score(str_unit_code)
        else:
            break


def main_student():
    print("Login as student")

    # validate username and password
    user = validate_role()
    if user.user_role != "ST":
        print("You are not a student, please select role again.")
        return
    print("Welcome, " + user.user_name + "!")

    # convert user to UserStudent
    user_password = user.user_password
    user = UserStudent(user_id=user.user_id, user_name=user.user_name)
    # Can not use the constructor to set the password, will cause double encryption
    user.user_password = user_password
    # set enrolled_units
    enrolled_units = []
    with open("data/user.txt", "r") as f:
        for line in f:
            if line.split(", ")[0] == user.user_id:
                tuple_list = line.split(", ")[5].split(",")
                for tuple in tuple_list:
                    unit_code = tuple.split(":")[0]
                    unit_score = int(tuple.split(":")[1])
                    enrolled_units.append((unit_code, unit_score))
    user.enrolled_units = enrolled_units

    # display student menu, do the action
    while True:
        user.student_menu()
        # validate input , input must be a number between 1 and 7
        option = validate_number_between(1, 7, "Select an option(1-7):")

        if option == 1:
            user.list_available_units()
        elif option == 2:
            user.list_enrolled_units()
        elif option == 3:  # Enrol a unit
            unit_code = validate_unitcode_input()
            user.enrol_unit(unit_code)
        elif option == 4:  # Drop a unit
            unit_code = validate_unitcode_input()
            user.drop_unit(unit_code)
        elif option == 5:  # Check score
            unit_code = input("Please enter the unit code, or press enter to list all units you enrol: ")
            user.check_score(unit_code)
        elif option == 6:  # Generate score
            unit_code = validate_unitcode_input()
            user.generate_score(unit_code)
        else:
            break


def validate_unitcode_input():
    # validate unit code format
    while True:
        unit_code = input("Please enter the unit code(5-7 characters): ")
        if len(unit_code) < 5 or len(unit_code) > 7:
            print("Invalid input. ")
        else:
            return unit_code.upper()


def validate_ad_ta_st_input():
    # validate user status format
    while True:
        status = input("Please enter the user role (AD/TA/ST): ").upper()
        if status not in ["AD", "TA", "ST"]:
            print("Invalid input. Please enter a valid status.")
        else:
            break
    return status


def validate_username_input():
    # validate username format
    while True:
        name = input("Please enter username(1-30 letters): ")
        if len(name) > 30 or len(name) < 1:
            print("Invalid input. ")
            continue
        is_alpha = True
        for c in name:
            if not c.isalpha() and not c.isspace():
                print("Invalid input.")
                is_alpha = False
                break
        if is_alpha:
            break

    return name


def validate_unitname_input():
    # validate username format
    while True:
        name = input("Please enter unit name(1-30 letters): ")
        if len(name) > 30 or len(name) < 1:
            print("Invalid input. ")
            continue
        is_alpha = True
        for c in name:
            if not c.isalpha() and not c.isspace():
                print("Invalid input.")
                is_alpha = False
                break
        if is_alpha:
            break
    return name


def validate_enable_disable_input():
    # validate user status format
    status = ""
    while True:
        status_input = input("Please enter the user status (E/D): ")
        if status_input.upper() != "E" and status_input.upper() != "D":
            print("Invalid input. Please enter a valid status.")
        else:
            if status_input.upper() == "E":
                status = "enabled"
            else:
                status = "disabled"
            break
    return status


def validate_password_input():
    # validate password format
    while True:
        password = input("Please enter your password(1-30 characters): ")
        if len(password) > 30 or len(password) < 1:
            print("Invalid input. Please enter a valid password.")
        else:
            break
    return password


def validate_number_between(min: int, max: int, message: str):
    while True:
        try:
            number = int(input(message))
            if number < min or number > max:
                print("Invalid input. Please enter a number between {} and {}.".format(min, max))
            else:
                break
        except ValueError:
            print("Invalid input. Input must be a number between {} and {}.".format(min, max))
    return number


def validate_role():
    # validate username and password
    user = User()
    while True:
        # validate username format
        name = validate_username_input()

        # validate password format
        password = validate_password_input()
        print(name)
        print(password)

        # validate username and password
        user_info = user.login(name, password)

        if not user_info:
            print("Invalid username or password. Please try again.")
        else:
            # user_id, user_name, user_password, user_role, user_status
            user.user_id = user_info.split(", ")[0]
            user.user_name = user_info.split(", ")[1]
            user.user_password = user_info.split(", ")[2]
            user.user_role = user_info.split(", ")[3]
            user.user_status = user_info.split(", ")[4]
            break
    return user


if __name__ == "__main__":
    main()
