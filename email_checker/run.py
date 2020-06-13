import os
import argparse
from logger import log

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--inline-emails', type=str, nargs='+', default=[], help="Additional emails to check")
parser.add_argument('-e', '--email-file', type=str, default='', help="Location of emails.txt file")
parser.add_argument('-p', '--param-file', type=str, default='', help="Destination of parameters.txt file")


def main(args):
	log.info('Starting email check with arguments...')
	log.info('[param file] - {}'.format(os.path.abspath(args.param_file)))
	log.info('[email file] - {}'.format(os.path.abspath(args.email_file)))
	log.info('[additional emails] - {}'.format(', '.join(args.inline_emails)))


if __name__ == '__main__':
	args = parser.parse_args()
	main(args)