import os
import shutil
import filecmp
import difflib
from pathlib import Path
from ex5 import processDirectory
import json

# to keep the output files comment the last block of code in the file.
# Change it for the number of test you want. (up to 1001).
NUM_OF_TESTS = 1001


def get_mode(dir_path):
    is_caesar = False
    with open(Path(dir_path) / 'config.json', 'r') as config_file:
        config_dict = json.load(config_file)
        class_type = config_dict["type"]
        if class_type == "Caesar":
            is_caesar = True

    return is_caesar


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


def test_encryption(encrypt_dir_to_test, decryption_dir, test_num, is_caesar):
    fails = 0
    for elem in os.listdir(encrypt_dir_to_test):
        if elem.endswith(".enc"):
            out_file = Path(encrypt_dir_to_test) / elem
            dst_file = Path(decryption_dir) / elem
            shutil.copy(out_file, dst_file)
            if test_num in range(4) or is_caesar:
                if not compare_files(str(out_file), str(out_file.with_suffix(".out"))):
                    fails += 1

    return fails


def test_decryption(encryption_path, decrypt_dir_to_test):
    fails = 0
    for elem in os.listdir(encryption_path):
        if elem.endswith('.txt'):
            out_file = Path(encryption_path) / elem
            dst_file = Path(decrypt_dir_to_test) / elem
            if not compare_files(dst_file.with_suffix('.txt'), out_file.with_suffix('.txt')):
                fails += 1

    return fails


def test_examples():
    passed_tests = fails = 0
    for i in range(NUM_OF_TESTS):
        encryption_path, decryption_path = set_up(i)
        is_caesar = get_mode(encryption_path)
        fails += test_encryption(encryption_path, decryption_path, i, is_caesar)

        processDirectory(decryption_path)
        fails += test_decryption(encryption_path, decryption_path)

        if fails == 0:
            print("PASSED :)")
            passed_tests += 1

    return passed_tests


def set_up(num):
    encrypt_path = str(Path('tests') / f"test{num}e")
    decrypt_path = str(Path('tests') / f"test{num}d")
    print("____________________________________")
    print(f"test no.{num}:", end=" ")

    processDirectory(encrypt_path)
    return encrypt_path, decrypt_path


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
    tests_passed = test_examples()
    if tests_passed == NUM_OF_TESTS:
        print("\n\nGood Job! You've PASSED all the tests ")
    else:
        print("\n\nYou've FAILED in {} tests... Keep going".format(NUM_OF_TESTS - tests_passed))

    clean_up()
