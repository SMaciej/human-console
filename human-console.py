import os, sys, re, random, shlex

class HumanConsole():
    verbs = {'run':('run',), 'shutdown':('shutdown', 'exit', 'stop'), 'open':('open', 'show'), 'search':('search', 'find'), 
             'simple_calculation':('add', 'substract', 'divide', 'multiply'), 'help':('help', 'wtf'), }
    helpers = {'and':('and', '&', '&&'), 'or':('or', '||')}
    ignores = ('me', 'some', 'lots of', 'of', 'a', 'the', 'an', 'with', 'for', 'can', 'you', 'in', 'it', 'using', 'is', 'to', 'from', 'by')

    help_text = ("With my help you can run apps, open and search for files and even do math!\n"
                 "If you want me to RUN something, simply ask me to run given application. I can run two applications, or choose one of given two for you, if you can't decide.\n"
                 "Don't be afraid to OPEN files. I can do that.\n"
                 "Don't hesitate if you want to FIND something, remember that you can give me a directory to search in.\n"
                 "If you want me to calculate something just say a word.")

    def welcomeText(self):
        print("Welcome to the human console.\n"
              "If you need help you can always ask me for it.\n"
              "If you want to get rid of me, just tell me to stop.")

    def ask(self):
        user_input = self.getInput()
        return self.parseInput(user_input)

    def getInput(self):
        """Waits for user input, then prepares it for parsing."""
        print("\nPlease, tell me what can I do for you:")
        user_input = raw_input()
        return self.prepareText(user_input)

    def prepareText(self, text):
        """Prepares text for parsing."""
        if text.endswith(('.', '?', '!', ',')):
            text = text[:-1]
        text = shlex.split(text.lower().replace(',', ' ').replace("'", ''))
        text = [word for word in text if word not in self.ignores]
        return text

    def parseInput(self, user_input):
        app = app2 = file = next_word = path = first = second = None

        if __debug__ == True:
            print('DEBUG Parsed text: %s' % user_input)

        for index, word in enumerate(user_input):

            # open a file
            if word in self.verbs['open']:
                if index-1 >= 0:
                    print user_input
                    app = user_input[index-1]
                else:
                    try:
                        app = user_input[index+2]
                    except IndexError:
                        print("I'm sorry, but to open a file you need to specify an app you want to open it with. Please, give me that app name:")
                        app = raw_input()
                try:
                    file = user_input[index+1]
                except IndexError:
                    print("You have to specify a file. Please, give me a file:")
                    file = raw_input()
                print("I'm running %s with %s." % (file, app))
                if __debug__ == True:
                    print('DEBUG Command: %s %s' % (app, file))
                os.system('%s %s' % (app, file))
                return None

            # run a program
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
                if __debug__ == True:
                    print('DEBUG Command: xfce4-terminal -e %s' % app)
                os.system('xfce4-terminal -e %s' % app)
                if app2: 
                    print("After that I'm running %s." % app2)
                    if __debug__ == True:
                        print('DEBUG Command: xfce4-terminal -e %s' % app2)
                    os.system('xfce4-terminal -e %s' % app2)
                return None

            # search for something
            elif word in self.verbs['search']:
                path = None
                file = user_input[index+1]
                for word in user_input:
                    if '/' in word:
                        path = word
                if path:
                    if __debug__ == True:
                        print('DEBUG Command: find %s -name "%s"' % (path, file))
                    print("Look what I've found:")
                    os.system('find %s -name "%s"' % (path, file))
                else:
                    if __debug__ == True:
                        print('DEBUG Command: xfce4-terminal -e find . -name "%s"' % file)
                    print("Look what I've found:")
                    os.system('find -name "%s"' % file)
                return None

            # simple calculation
            elif word in self.verbs['simple_calculation']:
                operations = self.verbs['simple_calculation']
                first = self.text2int(user_input[index+1])
                second = self.text2int(user_input[index+2])
                if __debug__:
                    print('DEBUG Converted numbers: %s %s' % (first, second))
                if word == operations[0]:
                    print('The result of adding is: %s' % str(first+second))
                if word == operations[1]:
                    print('The result of substraction is: %s' % str(first-second))
                if word == operations[2]:
                    print('The result is: %s' % str(first/second))
                if word == operations[3]:
                    print('The result is: %s' % str(first*second))
                return None

            # show help
            elif word in self.verbs['help']:
                print(self.help_text)
                return None

            # exit human-console
            elif word in self.verbs['shutdown']:
                print('It was nice meeting you, hope to see you soon.')
                sys.exit()

        # not understandable
        print("What a shame. I don't understand you. We all know it's my developer's fault, not mine. Anyway, I can always show you the help file.")

    def text2int(self, textnum, numwords={}):
        """ Text to int conversion function, made by StackOverflow user "recursive". """
        if not numwords:
          units = [
            "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
            "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen",
            "sixteen", "seventeen", "eighteen", "nineteen",
          ]

          tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

          scales = ["hundred", "thousand", "million", "billion", "trillion"]

          numwords["and"] = (1, 0)
          for idx, word in enumerate(units):    numwords[word] = (1, idx)
          for idx, word in enumerate(tens):     numwords[word] = (1, idx * 10)
          for idx, word in enumerate(scales):   numwords[word] = (10 ** (idx * 3 or 2), 0)

        current = result = 0
        for word in textnum.split():
            if word not in numwords:
              raise Exception("Illegal word: " + word)

            scale, increment = numwords[word]
            current = current * scale + increment
            if scale > 100:
                result += current
                current = 0

        return result + current



console = HumanConsole()
console.welcomeText()

while True:
    console.ask()
