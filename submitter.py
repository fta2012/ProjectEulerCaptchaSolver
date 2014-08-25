from bs4 import BeautifulSoup
from mechanize import Browser
from os import remove
from solver import solve_for_filename
from time import sleep

import sys

USERNAME = ''
PASSWORD = ''

if not USERNAME or not PASSWORD:
    print 'Fill in USERNAME and PASSWORD first'
    sys.exit()

# Login
browser = Browser()
browser.open('https://projecteuler.net/sign_in')
browser.select_form(nr=0)
browser.form['username'] = USERNAME
browser.form['password'] = PASSWORD
resp = browser.submit()

# Submit each answer from answers.txt
# Each line of answers.txt should be in the form "<problem number> <answer>"
answers = [line.split() for line in open('answers.txt').read().strip().split('\n')]
for problem_num, answer in answers:
    print problem_num + ':'
    # Keep retrying the submission until it succeeds 
    while True:
        resp = browser.open('https://projecteuler.net/problem=' + problem_num)
        soup = BeautifulSoup(resp)
        if not soup.find(id='captcha_image'):
            # Assume that if you don't see a captcha then this problem was already solved
            print 'Solved'
            break
        
        # Fetch the captcha image and solve it
        browser.retrieve('https://projecteuler.net/captcha/show_captcha.php', 'temp.png')
        captcha_answer = solve_for_filename('temp.png')
        if not captcha_answer:
            print 'Failed to solve captcha, refreshing for a new image'
            continue
        
        # Submit answer and captcha
        browser.select_form(nr=0)
        browser.form['guess_' + str(problem_num)] = answer
        browser.form['captcha'] = captcha_answer
        resp = browser.submit()
        soup = BeautifulSoup(resp)
        message = soup.find(id='message') or soup.select('#content p')
        print message

        # Wait 30 seconds
        sleep(30)

remove('temp.png')
