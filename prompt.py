# Question Prompt
# Python 2.7
import wolfram
import time


class Prompt(object):

    def __init__(self, write_action, error_action):
        self.write_action = write_action
        self.error_action = error_action

    def loop(self, exit=''):
        query = raw_input("What is your question? ")
        while(query != exit):
            response = wolfram.WolframRequest(query)
            if response.status:
                self.write_action(response)
            else:
                self.error_action(response)
            query = raw_input("What is your question?")

if __name__ == '__main__':
    answers = open("logs/{}.txt".format(str(time.time())), 'w')

    def log(response):
        answers.write("Query : {}\n".format(response.query))
        answers.write("Info : {}\n".format(response.prettify()))
        answers.write("\n" + "#" * 160 + "\n\n")

    def error(response):
        answers.write("Query : {}\n".format(response.query))
        answers.write("AN ERROR OCCURRED")
        answers.write("Info : {}\n".format(response.prettify()))
        answers.write("\n" + "#" * 160 + "\n\n")
    Prompt(log, error).loop()
    answers.close()
