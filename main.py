# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from tkinter import *
import re

def CutOneLineTokens(input_line):
    #our completed string to build after processing our rules will be held here
    formatted_tokens = []
    token_types = []
    token_values = []
    while input_line != "":             #run through whole string
        initial_length = len(input_line)

        #clean string before processing
        foundToken = re.match(r"\s+", input_line)
        if foundToken:
            token = foundToken.group()
            input_line = input_line.replace(token, "", 1)
            continue

        # checking for keywords
        foundToken = re.match(r"\b(if|else|int|float)\b", input_line)
        if foundToken:
            token = foundToken.group()
            formatted_tokens.append("<keyword, " + str(token) + ">")
            token_types.append("keyword")
            token_values.append(str(token))
            input_line = input_line.replace(token, "", 1)
            continue

        # checking for identifiers
        foundToken = re.match(r"[A-Za-z_][A-Za-z_0-9]*", input_line)
        if foundToken:
            token = foundToken.group()
            formatted_tokens.append("<identifier, " + str(token) + ">")
            token_types.append("identifier")
            token_values.append(str(token))
            input_line = input_line.replace(token, "", 1)
            continue

        # op/sep check
        foundToken = re.match(r"=", input_line)
        if foundToken:
            token = foundToken.group()
            formatted_tokens.append("<operator, " + str(token) + ">")
            token_types.append("operator")
            token_values.append(str(token))
            input_line = input_line.replace(token, "", 1)
        foundToken = re.match(r"\+", input_line)
        if foundToken:
            token = foundToken.group()
            formatted_tokens.append("<operator, " + str(token) + ">")
            token_types.append("operator")
            token_values.append(str(token))
            input_line = input_line.replace(token, "", 1)
        foundToken = re.match(r">", input_line)
        if foundToken:
            token = foundToken.group()
            formatted_tokens.append("<operator, " + str(token) + ">")
            token_types.append("operator")
            token_values.append(str(token))
            input_line = input_line.replace(token, "", 1)
        foundToken = re.match(r"\*", input_line)
        if foundToken:
            token = foundToken.group()
            formatted_tokens.append("<operator, " + str(token) + ">")
            token_types.append("operator")
            token_values.append(str(token))
            input_line = input_line.replace(token, "", 1)
        foundToken = re.match(r"\(", input_line)
        if foundToken:
            token = foundToken.group()
            formatted_tokens.append("<separator, " + str(token) + ">")
            token_types.append("separator")
            token_values.append(str(token))
            input_line = input_line.replace(token, "", 1)
        foundToken = re.match(r"\)", input_line)
        if foundToken:
            token = foundToken.group()
            formatted_tokens.append("<separator, " + str(token) + ">")
            token_types.append("separator")
            token_values.append(str(token))
            input_line = input_line.replace(token, "", 1)
        foundToken = re.match(r":", input_line)
        if foundToken:
            token = foundToken.group()
            formatted_tokens.append("<separator, " + str(token) + ">")
            token_types.append("separator")
            token_values.append(str(token))
            input_line = input_line.replace(token, "", 1)
        foundToken = re.match(r";", input_line)
        if foundToken:
            token = foundToken.group()
            formatted_tokens.append("<separator, " + str(token) + ">")
            token_types.append("separator")
            token_values.append(str(token))
            input_line = input_line.replace(token, "", 1)

        # checking for separators / str lit
        foundToken = re.match(r'([“""])(.*?)([”""])', input_line, re.DOTALL)
        if foundToken:
            # Opening quote
            formatted_tokens.append("<separator, " + foundToken.group(1) + ">")
            token_types.append("separator")
            token_values.append(foundToken.group(1))
            # String literal content
            formatted_tokens.append("<String_literal, " + foundToken.group(2) + ">")
            token_types.append("String_literal")
            token_values.append(foundToken.group(2))
            # Closing quote
            formatted_tokens.append("<separator, " + foundToken.group(3) + ">")
            token_types.append("separator")
            token_values.append(foundToken.group(3))
            # Updating the input line
            input_line = input_line.replace(token, "", 1)

        # checking for int/float lit
        foundToken = re.match(r"\d+\.\d*|\.\d+", input_line)
        if foundToken:
            token = foundToken.group()
            formatted_tokens.append("<Float_literal, " + str(token) + ">")
            token_types.append("Float_literal")
            token_values.append(str(token))
            input_line = input_line.replace(token, "", 1)
            continue
        foundToken = re.match(r"\d+", input_line)
        if foundToken:
            token = foundToken.group()
            formatted_tokens.append("<Int_literal, " + str(token) + ">")  # Update here
            token_types.append("Int_literal")
            token_values.append(str(token))
            input_line = input_line.replace(token, "", 1)
            continue

        # No token matched if we reach this condition
        if len(input_line) == initial_length:
            # For debugging
            formatted_tokens.append(f"<unknown, {input_line}>")
            token_types.append("unknown")
            token_values.append(input_line)

            break

    # Zip the new lists together into a single list of tuples
    token_data = list(zip(token_types, token_values))

    # Return the three lists as a tuple
    return formatted_tokens, token_types, token_values

class GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Lexical Analyzer for TinyPie")

        #source code for input
        self.source_label = Label(self.root, text="Source Code Input:")
        self.source_label.grid(row=0, column=0)

        self.source_text = Text(self.root, height=10, width=40)
        self.source_text.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        #process current line
        self.current_line_label = Label(self.root, text="Current Processing Line:")
        self.current_line_label.grid(row=2, column=0)

        self.current_line_value = StringVar(value="0")
        self.current_line_entry = Entry(self.root, state='readonly', textvariable=self.current_line_value, width=5)
        self.current_line_entry.grid(row=3, column=0)

        #button for next line
        self.button_next_line = Button(self.root, text="Next Line", command=self.output_next_line)
        self.button_next_line.grid(row=4, column=0, pady=10)

        #lexical analyzer result
        self.lexical_result_label = Label(self.root, text="Lexical Analyzed Result:")
        self.lexical_result_label.grid(row=0, column=1)

        self.lexical_result_text = Text(self.root, height=10, width=40)
        self.lexical_result_text.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        self.parseLabel = Label(self.root, text="Parse Tree:")
        self.parseLabel.grid(row=0, column=2, sticky=W, padx=30)
        self.parseTreeOutput = Text(self.root, width=40, height=10, font=("Times", 14))
        self.parseTreeOutput.grid(row=1, column=2, sticky=E, padx=30)

        #Quit button
        self.quit_button = Button(self.root, text="Quit", command=self.root.quit)
        self.quit_button.grid(row=4, column=2, padx=30)

        self.line_count = 0

    def output_next_line(self):
        #remove previous tag line
        if self.line_count >0:
            self.source_text.tag_remove("highlight", f"{self.line_count}.0", f"{self.line_count}.end")

        self.line_count += 1

        # Update the current line number
        self.current_line_value.set("     " + str(self.line_count))

        # Get the current line text
        current_line = self.source_text.get(str(self.line_count) + ".0", str(self.line_count) + ".end")
        print([ord(char) for char in current_line])
        if not current_line.strip():
            return

        # Process the current line
        formatted_tokens, token_types, token_values = CutOneLineTokens(current_line.strip())

        # Insert lexer output to lexical_result_text text widget
        self.lexical_result_text.insert('end', "####Lexer Line " + str(self.line_count) + "####\n")
        for token in formatted_tokens:
            self.lexical_result_text.insert('end', token + '\n')

        # Insert parse tree header to parseTreeOutput Text widget
        self.parseTreeOutput.insert('end', "####Parse Tree Line " + str(self.line_count) + "####\n")

        # Calling parser method
        token_data = list(zip(token_types, token_values))
        print("Tokens after lexing line {}: {}".format(self.line_count, token_data))
        self.parser(token_data)

        # Highlight the current line in the source_text Text widget
        self.source_text.tag_add("highlight", f"{self.line_count}.0", f"{self.line_count}.end")
        self.source_text.tag_config("highlight", font=('TkDefaultFont', 10, 'bold'))

    def parser(self, Mytokens):
        if not Mytokens:
            return
        global inToken
        inToken = ("empty", "empty")
        inToken = Mytokens.pop(0)

        def accept_token():
            global inToken
            self.parseTreeOutput.insert("end", "     accept token from the list:" + inToken[1] + "\n")
            if (Mytokens):
                inToken = Mytokens.pop(0)

        def comparison_exp():
            self.parseTreeOutput.insert("end", "\n----parent node comparison_exp, finding children nodes:\n")
            global inToken
            if (inToken[0] == "identifier"):
                self.parseTreeOutput.insert("end", "child node (internal): identifier" + "\n")
                self.parseTreeOutput.insert("end", "   identifier has child node (token):" + inToken[1] + "\n")
                accept_token()
                if (inToken[1] == ">"):
                    self.parseTreeOutput.insert("end", "child node (internal): seperator" + "\n")
                    self.parseTreeOutput.insert("end", "   seperator has child node (token):" + inToken[1] + "\n")
                    accept_token()
                    if (inToken[0] == "identifier"):
                        self.parseTreeOutput.insert("end", "child node (internal): identifier" + "\n")
                        self.parseTreeOutput.insert("end", "   identifier has child node (token):" + inToken[1] + "\n")
                        accept_token()
                    else:
                        print("Error, missing identifier in comparison expression.")
                        return
                else:
                    print("Error, missing \'>\' in comparison expression.")
                    return
            else:
                print("Error, missing identifier in comparison expression.")
                return

        def if_exp():
            self.parseTreeOutput.insert("end", "\n----parent node if_exp, finding children nodes:" + "\n")
            global inToken
            if (inToken[1] == "if"):
                self.parseTreeOutput.insert("end", "child node (internal): keyword" + "\n")
                self.parseTreeOutput.insert("end", "   keyword has child node (token):" + inToken[1] + "\n")
                accept_token()
                if (inToken[1] == "("):
                    self.parseTreeOutput.insert("end", "child node (internal): seperator" + "\n")
                    self.parseTreeOutput.insert("end", "   separator has child node (token):" + inToken[1] + "\n")
                    accept_token()
                    if (inToken[0] == "identifier"):
                        comparison_exp()
                        if (inToken[1] == ")"):
                            self.parseTreeOutput.insert("end",
                                                        "\n----parent node if_exp, finding children nodes:" + "\n")
                            self.parseTreeOutput.insert("end", "child node (internal): seperator" + "\n")
                            self.parseTreeOutput.insert("end",
                                                        "   separator has child node (token):" + inToken[1] + "\n")
                            accept_token()
                            if (inToken[1] == ":"):
                                self.parseTreeOutput.insert("end", "child node (internal): seperator" + "\n")
                                self.parseTreeOutput.insert("end",
                                                            "   separator has child node (token):" + inToken[1] + "\n")
                                return
                            else:
                                print("Error, missing \':\' as fifth expression.")
                                return
                        else:
                            print("Error, missing \')\' as fourth expression.")
                            return
                    else:
                        print("Error, missing \'comparison expression\' as third expression.")
                        return
                else:
                    print("Error, missing \'(\' as second expression.")
                    return
            else:
                print("Error, missing \'if\' as first expression.")
                return

        def multi():
            self.parseTreeOutput.insert("end", "\n----parent node multi, finding children nodes:" + "\n")
            global inToken
            if (inToken[0] == "Int_literal"):
                self.parseTreeOutput.insert("end", "child node (internal): int" + "\n")
                self.parseTreeOutput.insert("end", "   int has child node (token):" + inToken[1] + "\n")
                accept_token()
                if (inToken[1] == "*"):
                    self.parseTreeOutput.insert("end", "child node (token):" + inToken[1] + "\n")
                    accept_token()
                    self.parseTreeOutput.insert("end", "child node (internal): multi" + "\n")
                    multi()
            elif (inToken[0] == "Float_literal"):
                self.parseTreeOutput.insert("end", "child node (internal): float" + "\n")
                self.parseTreeOutput.insert("end", "   float has child node (token):" + inToken[1] + "\n")
                accept_token()
            else:
                print("Error, invalid syntax.")
                return

        def math():
            self.parseTreeOutput.insert("end", "\n----parent node math, finding children nodes:" + "\n")
            global inToken
            if (inToken[0] == "Float_literal" or inToken[0] == "Int_literal"):
                self.parseTreeOutput.insert("end", "child node (internal): multi" + "\n")
                multi()
                if (inToken[1] == "+"):
                    self.parseTreeOutput.insert("end", "\n----parent node math, finding children nodes:" + "\n")
                    self.parseTreeOutput.insert("end", "child node (internal):+" + "\n")
                    accept_token()
                    self.parseTreeOutput.insert("end", "child node (internal): multi" + "\n")
                    multi()
                else:
                    print("Error, invalid syntax.")
                    return
            else:
                print("Error, invalid syntax.")
                return

        def exp():
            global inToken
            self.parseTreeOutput.insert("end", "\n----parent node key_exp, finding children nodes:" + "\n")
            self.parseTreeOutput.insert("end", "child node (internal): keyword" + "\n")
            self.parseTreeOutput.insert("end", "  Keyword has child node(token):" + inToken[1] + "\n")
            accept_token()
            self.parseTreeOutput.insert("end", "\n----parent node exp, finding children nodes:" + "\n")
            if (inToken[0] == "identifier"):
                self.parseTreeOutput.insert("end", "child node (internal): identifier" + "\n")
                self.parseTreeOutput.insert("end", "   identifier has child node (token):" + inToken[1] + "\n")
                accept_token()
            else:
                print("expect identifier as the second element of the expression!\n")
                return
            if (inToken[1] == "="):
                self.parseTreeOutput.insert("end", "child node (token):" + inToken[1] + "\n")
                accept_token()
            else:
                print("expect = as the third element of the expression!")
                return
            self.parseTreeOutput.insert("end", "Child node (internal): math" + "\n")
            math()
            if (inToken[1] == ";"):
                self.parseTreeOutput.insert("end", "\n----parent node key_exp, finding children nodes:" + "\n")
                self.parseTreeOutput.insert("end", "child node (internal): seperator" + "\n")
                self.parseTreeOutput.insert("end", "   seperator has child node (token):" + inToken[1] + "\n")
                accept_token()

        def print_exp():
            global inToken
            self.parseTreeOutput.insert("end", "\n----parent node print_exp, finding children nodes:" + "\n")
            self.parseTreeOutput.insert("end", "child node (internal): keyword" + "\n")
            self.parseTreeOutput.insert("end", "   keyword has child node (token):" + inToken[1] + "\n")
            accept_token()
            if (inToken[1] == "("):
                self.parseTreeOutput.insert("end", "child node (internal): seperator" + "\n")
                self.parseTreeOutput.insert("end", "   separator has child node (token):" + inToken[1] + "\n")
                accept_token()
                if (inToken[1] in ["“", "\""]):
                    self.parseTreeOutput.insert("end", "child node (internal): seperator" + "\n")
                    self.parseTreeOutput.insert("end", "   separator has child node (token):" + inToken[1] + "\n")
                    accept_token()
                    if (inToken[0] == "String_literal"):
                        self.parseTreeOutput.insert("end", "child node (internal): String" + "\n")
                        self.parseTreeOutput.insert("end", "   String has child node (token):" + inToken[1] + "\n")
                        accept_token()
                        if (inToken[1] in ["”", "\""]):
                            self.parseTreeOutput.insert("end", "child node (internal): seperator" + "\n")
                            self.parseTreeOutput.insert("end",
                                                        "   separator has child node (token):" + inToken[1] + "\n")
                            accept_token()
                            if (inToken[1] == ")"):
                                self.parseTreeOutput.insert("end", "child node (internal): seperator" + "\n")
                                self.parseTreeOutput.insert("end",
                                                            "   separator has child node (token):" + inToken[1] + "\n")
                                accept_token()
                                if (inToken[1] == ";"):
                                    self.parseTreeOutput.insert("end", "child node (internal): seperator" + "\n")
                                    self.parseTreeOutput.insert("end", "   separator has child node (token):" + inToken[
                                        1] + "\n")
                                    accept_token()

                                else:
                                    print("Error, missing \';\' as seventh expression.")
                                    return
                            else:
                                print("Error, missing \')\' as sixth expression.")
                                return
                        else:
                            print("Error, missing \'\"\' as fifth expression.")
                            return
                    else:
                        print("Error, missing \'String\' as fourth expression.")
                        return
                else:
                    print("Error, missing \'\"\' as third expression.")
                    return
            else:
                print("Error, missing \'(\' as second expression.")
                return

        if (inToken[0] == "keyword"):
            if (inToken[1] == "float"):
                exp()
            elif (inToken[1] == "if"):
                if_exp()
            elif (inToken[1] == "print"):
                print_exp()
            else:
                print("Error, invalid syntax.")
        else:
            print("Error, invalid syntax.")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = Tk()

    # enlarge window when user enlarges
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    lexer_gui = GUI(root)
    root.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
