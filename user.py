import random


# Group Number: 74
# Allocated Tutor Name: Jinx Haung
# Group Members:
# 1. Tan Tao
# 2. Shofi Taneem
# 3. Khanjan Pandya

class User:
    # Required variables
    file_path_user: str = "data/user.txt"
    file_path_unit = "data/unit.txt"
    str_1 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    str_2 = "!#$%&()*+-./:;<=>?@\\^_`{|}~"

    def __init__(self, user_id: int = 0, user_name: str = "", user_password: str = "", user_role: str = "",
                 user_status: str = ""):
        self.user_id = user_id if user_id != 0 else self.generate_user_id()
        self.user_name = user_name
        self.user_password = self.encrypt(user_password) if user_password else ""
        self.user_role = user_role
        self.user_status = user_status

    def __str__(self):
        return f"{self.user_id}, {self.user_name}, {self.user_password}, {self.user_role}, {self.user_status}"

    def generate_user_id(self):
        while True:
            user_id = random.randint(10000, 99999)
            if not self.check_user_id_exist(user_id):
                return user_id

    def check_user_id_exist(self, user_id: int):
        with open(self.file_path_user, "r") as file:
            for line in file:
                user_info = line.strip().split(", ")
                if int(user_info[0]) == user_id:
                    return True
        return False

    def check_username_exist(self, username: str):
        with open(self.file_path_user, "r") as file:
            for line in file:
                user_info = line.strip().split(", ")
                if user_info[1].lower() == username.lower():
                    return True
        return False

    def encrypt(self, password: str):
        encrypted = "^^^"
        for i in range(len(password)):
            c = password[i]
            ascii_code = ord(c)
            index1 = ascii_code % len(self.str_1)
            char1 = self.str_1[index1]
            index2 = i % len(self.str_2)
            char2 = self.str_2[index2]
            encrypted += char1 + char2
            # str_1 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
            # str_2 = "!#$%&()*+-./:;<=>?@\\^_`{|}~"
        encrypted += "$$$"
        return encrypted

    #  {self.user_id}, {self.user_name}, {self.user_password}, {self.user_role}, {self.user_status}
    def login(self, username: str, password: str):
        with open(self.file_path_user, "r") as file:
            for line in file:
                user_info = line.strip().split(", ")
                if user_info[1].lower() == username.lower():
                    if user_info[2] == self.encrypt(password):
                        if user_info[4] == "enabled":
                            return line.strip()
                        else:
                            print("Your account is disabled, please contact the administrator.")
                            return None
                    else:
                        print("Wrong password.")
                        return None
            else:
                print("Username not found.")
                return None
