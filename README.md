NOTE: Project Euler changed their CAPTCHA so this script no longer works.

This script is for bulk solving captchas / submitting answers on projecteuler.net. See [blog post](http://franklinta.com/2014/08/24/solving-captchas-on-project-euler) for details.

To run, fill in USERNAME and PASSWORD in submitter.py and populate answers.txt with `<problem_num> <answer>` per line for each problem number and answer you want the script to submit, then run `python submitter.py`. There will be a 30 second delay between each submission attempt.

The images in `labeled_images/` were generated with `curl "https://projecteuler.net/captcha/show_captcha.php?[00-19]" -o "#1.png"` and then manually labeled.

The images in `test_images/` were obtained in the same way and were only used during development. Run `python solver.py` to see the solver's solution for those images.

Requires scipy, mechanize, and beautifulsoup.
