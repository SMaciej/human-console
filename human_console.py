import os, re, random


class HumanConsole():

    verbs = {'run':('run',), 'shutdown':('shutdown', 'exit', 'stop'), 'restart':('restart',), 'show':('show', 'give')}
    logical = {'and':('and',), 'or':('or',),}
    nouns = ('')
    ignores = ('me', 'some', 'lots of', 'of', 'a', 'the', 'an')

    def welcomeText(self):
        print("Welcome to human console.\n"
              "If you need help you can always ask me for it.\n"
              "If you want to get rid of me, just tell me to stop.")

    def prepareText(self, text):
        """Prepares text for parsing."""
        text = text.lower().replace('.', '').replace(',', ' ').split()
        text = [word for word in text if word not in self.ignores]
        return text

    def getInput(self):
        """Waits for user input, then prepares it for parsing."""
        print("\nPlease, tell me what can I do for you:")
        user_input = raw_input()
        return self.prepareText(user_input)

    def parseInput(self, user_input):
        for index, word in enumerate(user_input):

            if word in self.verbs:
                if word in self.verbs['run']:
                    app = user_input[index+1]
                    app2 = None
                    try:
                        next_word = user_input[index+2]
                        if next_word in self.logical['and']:
                            app2 = user_input[index+3]
                        elif next_word in self.logical['or']:
                            app = random.choice([app, user_input[index+3]])
                    except IndexError:
                        pass

                    print("I'm running %s." % app)
                    os.system('xfce4-terminal -e %s' % app)
                    if app2: 
                        print("After that I'm running %s." % app2)
                        os.system('xfce4-terminal -e %s' % app2)

    def ask(self):
        user_input = self.getInput()
        return self.parseInput(user_input)





console = HumanConsole()
console.welcomeText()

while True:
    console.ask()
