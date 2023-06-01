from user import User

# Group Number: 74
# Allocated Tutor Name: Jinx Haung
# Group Members:
# 1. Tan Tao
# 2. Shofi Taneem
# 3. Khanjan Pandya
class UserAdmin(User):
    def __init__(self, user_id: int = 0, user_name: str = "", user_password: str = "",
                 user_role: str = "AD", user_status: str = "enabled"):
        super().__init__(user_id, user_name, user_password, user_role, user_status)

    def __str__(self):
        return super().__str__()

    def admin_menu(self):
        print("---------------------Admin menu:---------------------")
        print("                     1. Search user")
        print("                     2. List all users")
        print("                     3. List all units")
        print("                     4. Enable/disable user")
        print("                     5. Add user")
        print("                     6. Delete user")
        print("                     7. Logout")

    def search_user(self, user_name: str):
        with open(self.file_path_user, "r") as file:
            for line in file:
                user_info = line.strip().split(", ")
                if user_info[1].lower() == user_name.lower():
                    print(line.strip())
                    return
        print(f"User {user_name} not found.")

    def list_all_users(self):
        # Define the format string with headers and field width
        format_str = "{:<10} {:<20} {:<30} {:<10} {:<10}".format("User ID", "User name", "User Password", "User Role",
                                                                 "User Status")
        print(format_str)
        print("-" * len(format_str))

        with open(self.file_path_user, "r") as file:
            for line in file:
                user_info = line.strip().split(", ")
                # Use the defined format string to print each user info
                user_str = "{:<10} {:<20} {:<30} {:<10} {:<10}".format(user_info[0], user_info[1], user_info[2],
                                                                       user_info[3], user_info[4])
                print(user_str)

    def list_all_units(self):
        # Define the format string with headers and field width
        format_str = "{:<10} {:<20} {:<30}".format("Unit ID", "Unit name", "Unit Description")
        print(format_str)
        print("-" * len(format_str))

        with open(self.file_path_unit, "r") as file:
            for line in file:
                unit_info = line.strip().split(", ")
                # Use the defined format string to print each unit info
                unit_str = "{:<10} {:<20} {:<30}".format(unit_info[0], unit_info[1], unit_info[2])
                print(unit_str)

    def enable_disable_user(self, user_name: str):
        # Check if the user exists
        is_exist = self.check_username_exist(user_name)
        if not is_exist:
            print(f"User {user_name} not found.")
            return

        # if exists
        with open(self.file_path_user, "r") as file:
            lines = file.readlines()
        with open(self.file_path_user, "w") as file:
            for line in lines:
                user_info = line.strip().split(", ")
                if user_info[1].lower() == user_name.lower():
                    if user_info[4] == "enabled":
                        user_info[4] = "disabled"
                        print(f"User {user_name} has been disabled.")
                    else:
                        user_info[4] = "enabled"
                        print(f"User {user_name} has been enabled.")
                    line = ", ".join(user_info) + "\n"
                file.write(line)

    def add_user(self, user_obj):
        try:  # if the user object is not a valid User object, it will raise an exception
            is_exist = self.check_username_exist(user_obj.user_name)
            if not is_exist:
                with open(self.file_path_user, "a") as file:
                    file.write(str(user_obj) + "\n")
                print(f"User {user_obj.user_name} has been added.")
            else:
                print(f"Add failed. User {user_obj.user_name} already exists.")
        except Exception as e:
            print(e)

    def delete_user(self, user_name: str):
        with open(self.file_path_user, "r") as file:
            lines = file.readlines()
        with open(self.file_path_user, "w") as file:
            found = False
            for line in lines:
                user_info = line.strip().split(", ")
                if user_info[1] != user_name:
                    file.write(line)
                else:
                    found = True
            if found:
                print(f"User {user_name} has been deleted.")
            else:
                print(f"User {user_name} not found.")
