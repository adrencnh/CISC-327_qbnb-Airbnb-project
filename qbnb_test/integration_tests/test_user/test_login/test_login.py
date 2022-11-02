from os import popen
import sys
from pathlib import Path
import subprocess
from qbnb.models import user_register
from qbnb.models import User
# get expected input/output file
current_folder = Path(__file__).parent


# read expected in/out
expected_in_both_invalid = open(current_folder.joinpath(
    'test_login_invalid_email_password.in'))
expected_in_invalid_email = open(current_folder.joinpath(
    'test_login_invalid_email.in'))
expected_in_invalid_password = open(current_folder.joinpath(
    'test_login_invalid_password.in'))
expected_in_valid = open(current_folder.joinpath(
    'test_login_valid.in'))

expected_out_invalid = open(current_folder.joinpath(
    'test_login_invalid.out')).read()
expected_out_valid = open(current_folder.joinpath(
    'test_login_valid.out')).read()


# Input partition method with the input divided into four part

def test_login_invalid_email_password():
    """
    Input partition test for input with both invalid
    passowrd and email
    """

    output = subprocess.run(
        ['python', '-m', 'qbnb'],
        stdin=expected_in_both_invalid,
        capture_output=True,
    ).stdout.decode()
    
    output = output.replace('\r', '')
    expected = expected_out_invalid.replace('\r', '')
    
    assert output.strip() == expected.strip()

  
def test_login_invalid_email():
    """
    Input partition test for input with only 
    invalid email and valid password
    """
    
    user_register('test0@test.com', 'Aa123456!', 'testuser')
    
    output = subprocess.run(
        ['python', '-m', 'qbnb'],
        stdin=expected_in_invalid_email,
        capture_output=True,
    ).stdout.decode()
    
    output = output.replace('\r', '')
    expected = expected_out_invalid.replace('\r', '')

    assert output.strip() == expected.strip()
    
    user = User.objects(email='test0@test.com')
    user[0].delete()


def test_login_invalid_password():
    """
    Input partition test for input that has invalid
    password and valid email
    """
    user_register('test0@test.com', 'Aa123456!', 'testuser')
    output = subprocess.run(
        ['python', '-m', 'qbnb'],
        stdin=expected_in_invalid_password,
        capture_output=True,
    ).stdout.decode()
    
    output = output.replace('\r', '')
    expected = expected_out_invalid.replace('\r', '')
    
    assert output.strip() == expected.strip()

    user = User.objects(email='test0@test.com')
    user[0].delete()


def test_login_valid():
    """
    Input partition test for valid input.
    """
    user_register('test0@test.com', 'Aa123456!', 'testuser')
    output = subprocess.run(
        ['python', '-m', 'qbnb'],
        stdin=expected_in_valid,
        capture_output=True,
    ).stdout.decode()
    user = User.objects(email='test0@test.com')
    user[0].delete()
    output = output.replace('\r', '')
    expected = expected_out_valid.replace('\r', '')

    assert output.strip() == expected.strip()


