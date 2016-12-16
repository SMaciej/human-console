import os, re, random


class HumanConsole():

    verbs = {'run':('run',), 'shutdown':('shutdown', 'exit', 'stop'), 'show':('show', 'give'), 'open':('open',), 'search':('search', 'find'), 'help':('help', 'wtf'),}
    helpers = {'and':('and',), 'or':('or',)}
    nouns = {}
    ignores = ('me', 'some', 'lots of', 'of', 'a', 'the', 'an', 'with', 'for')

    def welcomeText(self):
        print("Welcome to the human console.\n"
              "If you need help you can always ask me for it.\n"
              "If you want to get rid of me, just tell me to stop.")

    def prepareText(self, text):
        """Prepares text for parsing."""
        text = text.lower().replace(',', ' ').split()
        text = [word for word in text if word not in self.ignores]
        for index, word in enumerate(text):
            if word not in self.verbs['open']:
                try:
                    text[index+1] = text[index+1].replace('.', '')
                except IndexError:
                    if text[index-1] not in self.verbs['open']:
                        text[index] = text[index].replace('.', '')
                    else:
                        pass

        return text

    def getInput(self):
        """Waits for user input, then prepares it for parsing."""
        print("\nPlease, tell me what can I do for you:")
        user_input = raw_input()
        return self.prepareText(user_input)

    def parseInput(self, user_input):
        for index, word in enumerate(user_input):

            if word in self.verbs:

                # Opening file.
                if word in self.verbs['open']:
                    if index-1 >= 0:
                        app = user_input[index-1]
                    else:
                        print("I'm sorry, but to open a file you need to specify an app you want to open it with. Please, give me that app name:")
                        app = raw_input()
                    try:
                        file = user_input[index+1]
                    except IndexError:
                        print("You have to specify a file. Please, give me a file:")
                        file = raw_input()
                    print("I'm running %s with %s." % (file, app))
                    os.system('%s %s' % (app, file))

                elif word in self.verbs['run']:
                    app2 = None
                    try:
                        app = user_input[index+1]
                    except IndexError:
                        print('Tell me, what do you want me to run?')
                        app = raw_input()
                    try:
                        next_word = user_input[index+2]
                        if next_word in self.helpers['and']:
                            app2 = user_input[index+3]
                        elif next_word in self.helpers['or']:
                            app = random.choice([app, user_input[index+3]])
                    except IndexError:
                        pass
                    print("I'm running %s." % app)
                    os.system('xfce4-terminal -e %s' % app)
                    if app2: 
                        print("After that I'm running %s." % app2)
                        os.system('xfce4-terminal -e %s' % app2)

                elif word in self.verbs['search']:


                elif word in self.verbs['shutdown']:
                    print('It was nice meeting you, hope to see you soon.')

            # else:
            #     print("What a shame. I don't understand you. It's developer's fault, not mine. But I can always show you the help file.")

                return None


    def ask(self):
        user_input = self.getInput()
        return self.parseInput(user_input)



console = HumanConsole()
console.welcomeText()

while True:
    console.ask()
