import os
import json
import shutil
import filecmp
import difflib
from pathlib import Path
from ex5 import processDirectory
from ex5 import getVigenereFromStr


# to keep the output files comment the last block of code in the file.
# Change it for the number of test you want. (up to 1001).
NUM_OF_TESTS = 1001


def fix_str_key(dir_path):
    is_key_string = False
    with open(Path(dir_path) / "config.json", 'r') as config_file:
        config_dict = json.load(config_file)
        # If key is string use getVigenereFromStr method to convert to valid key
        if isinstance(config_dict["key"], str):
            is_key_string = True
            obj = getVigenereFromStr(config_dict["key"])
            good_key = obj.key_list
            config_dict["key"] = good_key

    if is_key_string:
        with open(Path(dir_path) / "config.json", 'w') as config_file:
            json.dump(config_dict, config_file, indent=4)


def compare_files(output_path, expected_path):
    try:
        result = filecmp.cmp(output_path, expected_path)
    except FileNotFoundError:
        print("FAILED :( -> File Not Found!")
        print(f"In comparing: {output_path} - {expected_path}")
        return False

    else:
        if not result:
            print("FAILED :(")
            with open(output_path, "r") as output_file:
                output = output_file.readlines()
            with open(expected_path, "r") as expected_file:
                expected = expected_file.readlines()
            diff = difflib.unified_diff(output, expected)
            print("\n".join(diff))
            return False
    return True


def test_examples():
    test_counter = 0
    for i in range(4):
        encryption_path, decryption_path = set_up(i)
        out_file = Path(encryption_path) / f"test{i}.enc"
        exp_file = out_file.parent / f"{i}.out"
        result1 = compare_files(str(out_file), str(exp_file))
        dst_file = Path(decryption_path) / out_file.name
        shutil.copy(out_file, dst_file)
        processDirectory(decryption_path)
        result2 = compare_files(dst_file.with_suffix('.txt'), out_file.with_suffix('.txt'))
        if result1 and result2:
            test_counter += 1
            print("PASSED :)")

    return test_counter


def set_up(num):
    encrypt_path = str(Path('tests') / f"test{num}e")
    decrypt_path = str(Path('tests') / f"test{num}d")
    fix_str_key(encrypt_path)
    fix_str_key(decrypt_path)
    print("____________________________________")
    print(f"test no.{num}:", end=" ")

    processDirectory(encrypt_path)
    return encrypt_path, decrypt_path


def main_test():
    passed_test = test_counter = count = 0
    passed_test += test_examples()
    for num in range(4, NUM_OF_TESTS):
        encryption_path, decryption_path = set_up(num)

        for elem in os.listdir(encryption_path):
            if elem.endswith(".enc"):
                shutil.copy(Path(encryption_path) / elem, Path(decryption_path) / elem)

        processDirectory(decryption_path)
        for elem in os.listdir(encryption_path):
            if elem.endswith(".txt"):
                count += 1
                test_counter += compare_files(str(Path(encryption_path, elem)), str(Path(decryption_path, elem)))

        if test_counter == count:
            passed_test += 1
            print("PASSED :)")

    return passed_test


# comment next lines to keep the output files.
def clean_up():
    for i in range(NUM_OF_TESTS):
        encrypted_dir_path = str(Path('tests') / f"test{i}e")
        decrypted_dir_path = str(Path('tests') / f"test{i}d")

        for file in os.listdir(encrypted_dir_path):
            path = Path(encrypted_dir_path, file)
            if file.endswith(".enc"):
                os.remove(path)
        for file in os.listdir(decrypted_dir_path):
            path = Path(decrypted_dir_path, file)
            if file.endswith(".json"):
                continue
            os.remove(path)
    print("deleting files succeeded...")


if __name__ == "__main__":
    tests_passed = main_test()
    if tests_passed == NUM_OF_TESTS:
        print("\n\nGood Job! You've PASSED all the tests ")
    else:
        print("\n\nYou've FAILED in {} tests... Keep going".format(NUM_OF_TESTS - tests_passed))

    clean_up()
