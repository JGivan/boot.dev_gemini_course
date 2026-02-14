from functions import get_file_content

test_1 = get_file_content.get_file_content("calculator", "main.py")
test_2 = get_file_content.get_file_content("calculator", "pkg/calculator.py")
test_3 = get_file_content.get_file_content("calculator", "/bin/cat")
test_4 = get_file_content.get_file_content("calculator", "pkg/does_not_exist.py")

for test in [test_1, test_2, test_3, test_4]:
    print(test)