from tkinter import *
import re

from treelib import Tree
import pydot
from PIL import Image, ImageTk
import os

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

        # Configure the grid layout
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        #source code for input
        self.source_label = Label(self.root, text="Source Code Input:")
        self.source_label.grid(row=0, column=0)

        self.source_text = Text(self.root, height=10, width=40)
        self.source_text.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        #process current line
        self.current_line_label = Label(self.root, text="Current Processing Line:")
        self.current_line_label.grid(row=4, column=0, sticky=W, padx=(10, 2)) #move current processing line to the bottom

        self.current_line_value = StringVar(value="0")
        self.current_line_entry = Entry(self.root, state='readonly', textvariable=self.current_line_value, width=5)
        self.current_line_entry.grid(row=4, column=1, sticky=W, padx=(2, 10)) #Move current processing line to the bottom

        #button for next line
        self.button_next_line = Button(self.root, text="Next Line", command=self.output_next_line)
        self.button_next_line.grid(row=5, column=0, padx=(10, 5), pady=10, sticky=W) #move button to bottom

        #lexical analyzer result
        self.lexical_result_label = Label(self.root, text="Lexical Analyzed Result:")
        self.lexical_result_label.grid(row=0, column=1)

        self.lexical_result_text = Text(self.root, height=10, width=40)
        self.lexical_result_text.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        self.parseLabel = Label(self.root, text="Parse Tree:")
        self.parseLabel.grid(row=0, column=2, sticky=W, padx=30)
        self.parseTreeOutput = Text(self.root, width=40, height=10, font=("Times", 14))
        self.parseTreeOutput.grid(row=1, column=2, sticky=E, padx=30)

        #Adding new tree visualization text box and label
        self.tree_visualization_label = Label(self.root, text="Tree Visualization:")
        self.tree_visualization_label.grid(row=2, column=0, columnspan=3, sticky=W)

        self.tree_visualization_output = Text(self.root, height=10, width=80)
        self.tree_visualization_output.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        #Quit button
        self.quit_button = Button(self.root, text="Quit", command=self.root.quit)
        self.quit_button.grid(row=5, column=2, padx=(5, 10), pady=10, sticky=E)

        self.line_count = 0

        # Creation of a the tree portion starter
        self.numberFloat = 0
        self.numberInteger = 0
        self.countMulti = 0
        self.myTree = Tree()


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

        # Initialize the root node of the parse tree
        if not self.myTree.contains('root'):
            self.myTree.create_node("Root", "root")

        # Calling parser method
        token_data = list(zip(token_types, token_values))
        print("Tokens after lexing line {}: {}".format(self.line_count, token_data))
        self.parser(token_data, 'root')

        # Highlight the current line in the source_text Text widget
        self.source_text.tag_add("highlight", f"{self.line_count}.0", f"{self.line_count}.end")
        self.source_text.tag_config("highlight", font=('TkDefaultFont', 10, 'bold'))

        # Generate a Graphviz dot file from the tree
        self.myTree.to_graphviz("graph.dot", shape='box', sorting=False)
        (graph,) = pydot.graph_from_dot_file('graph.dot')
        graph.write_jpg('graph.jpg')

        # Resize the image and convert
        self.graphImageIntial = Image.open("graph.jpg")
        self.graphImageIntial = self.graphImageIntial.resize((700, 300))
        self.ImageGraph = ImageTk.PhotoImage(self.graphImageIntial)

        # Display the image in the Tree Visualization GUI box
        if hasattr(self, 'imgLabel'):
            self.imgLabel.configure(image=self.ImageGraph)
        else:
            self.imgLabel = Label(self.tree_visualization_output, image=self.ImageGraph)
            self.imgLabel.image = self.ImageGraph  # Keep a reference
            self.imgLabel.pack()

        # Clean up temporary files
        os.remove("graph.jpg")
        os.remove("graph.dot")

        self.myTree = Tree()

    identify_inputToken = ("empty", "empty")

    def parser(self, Mytokens, parent_id):
        if not Mytokens:
            return

        # Initialize the root node of the parse tree
        if not self.myTree.contains('root'):
            self.myTree.create_node("Root", "root")

        global inToken
        inToken = ("empty", "empty")
        inToken = Mytokens.pop(0)

        def accept_token(self, parent_id):
            global inToken
            self.parseTreeOutput.insert("end", "     accept token from the list:" + inToken[1] + "\n")

            # Add token to the parse tree
            token_node_id = parent_id + "_token_" + inToken[1]
            self.myTree.create_node("Token: " + inToken[1], token_node_id, parent=parent_id)

            if (Mytokens):
                inToken = Mytokens.pop(0)

        def comparison_exp(self, parent_id):

            # Create a node for the comparison expression
            comparison_id = "comparison_" + str(self.line_count)
            self.myTree.create_node("Comparison Expression", comparison_id, parent=parent_id)

            self.parseTreeOutput.insert("end", "\n----parent node comparison_exp, finding children nodes:\n")
            global inToken
            if (inToken[0] == "identifier"):
                # Process the first identifier
                identifier1_id = comparison_id + "_identifier1"
                self.myTree.create_node("Identifier: " + inToken[1], identifier1_id, parent=comparison_id)

                self.parseTreeOutput.insert("end", "child node (internal): identifier" + "\n")
                self.parseTreeOutput.insert("end", "   identifier has child node (token):" + inToken[1] + "\n")
                accept_token(self, identifier1_id)
                if (inToken[1] == ">"):
                    self.parseTreeOutput.insert("end", "child node (internal): seperator" + "\n")
                    self.parseTreeOutput.insert("end", "   seperator has child node (token):" + inToken[1] + "\n")

                    # Process the '>' token
                    separator_id = comparison_id + "_separator"
                    self.myTree.create_node("Separator: " + inToken[1], separator_id, parent=comparison_id)
                    accept_token(self, separator_id) #was just accept_token(self) for both

                    if (inToken[0] == "identifier"):
                        self.parseTreeOutput.insert("end", "child node (internal): identifier" + "\n")
                        self.parseTreeOutput.insert("end", "   identifier has child node (token):" + inToken[1] + "\n")

                        # Process the second identifier
                        identifier2_id = comparison_id + "_identifier2"
                        self.myTree.create_node("Identifier: " + inToken[1], identifier2_id, parent=comparison_id)
                        accept_token(self, identifier2_id)
                    else:
                        print("Error, missing identifier in comparison expression.")
                        return
                else:
                    print("Error, missing \'>\' in comparison expression.")
                    return
            else:
                print("Error, missing identifier in comparison expression.")
                return

        def if_exp(self, parent_id):
            self.parseTreeOutput.insert("end", "\n----parent node if_exp, finding children nodes:" + "\n")
            global inToken

            # Create a node for the if expression
            if_exp_id = "if_exp_" + str(self.line_count)  # Ensure unique ID for the if expression
            self.myTree.create_node("If Expression", if_exp_id, parent=parent_id)

            if (inToken[1] == "if"):
                self.parseTreeOutput.insert("end", "child node (internal): keyword" + "\n")
                self.parseTreeOutput.insert("end", "   keyword has child node (token):" + inToken[1] + "\n")

                # Create a node for the 'if' keyword
                if_keyword_id = if_exp_id + "_keyword"
                self.myTree.create_node("Keyword: " + inToken[1], if_keyword_id, parent=if_exp_id)
                accept_token(self, if_keyword_id)  # Pass the new node ID as parent_id

                #accept_token(self, parent_id)
                if (inToken[1] == "("):
                    self.parseTreeOutput.insert("end", "child node (internal): seperator" + "\n")
                    self.parseTreeOutput.insert("end", "   separator has child node (token):" + inToken[1] + "\n")

                    # Create a node for the '(' separator
                    left_paren_id = if_exp_id + "_leftparen"
                    self.myTree.create_node("Separator: " + inToken[1], left_paren_id, parent=if_exp_id)
                    accept_token(self, left_paren_id)

                    #accept_token(self, parent_id)
                    if (inToken[0] == "identifier"):
                        # Call comparison_exp with the parent_id for the if expression
                        comparison_exp_id = if_exp_id + "_comparison"
                        self.myTree.create_node("Comparison", comparison_exp_id, parent=if_exp_id)
                        comparison_exp(self, comparison_exp_id)  # The comparison_exp will build its own subtree
                        #comparison_exp(self, parent_id)
                        if (inToken[1] == ")"):
                            self.parseTreeOutput.insert("end",
                                                        "\n----parent node if_exp, finding children nodes:" + "\n")
                            self.parseTreeOutput.insert("end", "child node (internal): seperator" + "\n")
                            self.parseTreeOutput.insert("end",
                                                        "   separator has child node (token):" + inToken[1] + "\n")

                            # Create a node for the ')' separator
                            right_paren_id = if_exp_id + "_rightparen"
                            self.myTree.create_node("Separator: " + inToken[1], right_paren_id, parent=if_exp_id)
                            accept_token(self, right_paren_id)

                            #accept_token(self, parent_id)
                            if (inToken[1] == ":"):
                                self.parseTreeOutput.insert("end", "child node (internal): seperator" + "\n")
                                self.parseTreeOutput.insert("end",
                                                            "   separator has child node (token):" + inToken[1] + "\n")

                                # Create a node for the ':' separator
                                colon_id = if_exp_id + "_colon"
                                self.myTree.create_node("Separator: " + inToken[1], colon_id, parent=if_exp_id)
                                accept_token(self, colon_id)

                               # return
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

        def multi(self, parent_id):
            self.parseTreeOutput.insert("end", "\n----parent node multi, finding children nodes:" + "\n")
            global inToken

            # Create a node for the multiplication expression
            self.line_count += 1
            multi_id = "multi_" + str(self.line_count)  # Ensure unique ID for the multiplication expression
            self.myTree.create_node("Multiplication", multi_id, parent=parent_id)

            # Process the first part of the multiplication (an integer or a float)
            if inToken[0] in ["Int_literal", "Float_literal"]:
                literal_id = f"{multi_id}_{inToken[1]}"
                literal_type = "Integer" if inToken[0] == "Int_literal" else "Float"
                self.myTree.create_node(f"{literal_type}: {inToken[1]}", literal_id, parent=multi_id)
                self.parseTreeOutput.insert("end", f"child node (internal): {literal_type}\n")
                self.parseTreeOutput.insert("end", f"   {literal_type} has child node (token): {inToken[1]}\n")
                accept_token(self, literal_id)

                # If there's a multiplication operator, process the next part of the multiplication
                if inToken[1] == "*":
                    operator_id = f"{multi_id}_operator_{inToken[1]}"
                    self.myTree.create_node(f"Operator: {inToken[1]}", operator_id, parent=multi_id)
                    self.parseTreeOutput.insert("end", f"child node (token): {inToken[1]}\n")
                    accept_token(self, operator_id)

                    # Recursively call multi for the right operand of the multiplication
                    self.parseTreeOutput.insert("end", "child node (internal): multi\n")
                    multi(self, multi_id)  # Note that we pass multi_id again as the parent_id
            else:
                print("Error, invalid syntax.")
                return

        def math(self, parent_id):
            self.parseTreeOutput.insert("end", "\n----parent node math, finding children nodes:" + "\n")
            global inToken

            # Increment line_count to ensure a unique node ID
            self.line_count += 1
            math_id = "math_" + str(self.line_count)
            self.myTree.create_node("Arithmetic Expression", math_id, parent=parent_id)

            if (inToken[0] == "Float_literal" or inToken[0] == "Int_literal"):
                self.parseTreeOutput.insert("end", "child node (internal): multi" + "\n")
                multi(self, parent_id)
                if (inToken[1] == "+"):
                    self.parseTreeOutput.insert("end", "\n----parent node math, finding children nodes:" + "\n")
                    self.parseTreeOutput.insert("end", "child node (internal):+" + "\n")
                    accept_token(self, parent_id)
                    self.parseTreeOutput.insert("end", "child node (internal): multi" + "\n")
                    multi(self, parent_id)
                else:
                    print("Error, invalid syntax.")
                    return
            else:
                print("Error, invalid syntax.")
                return

        def exp(self, parent_id):
            global inToken
            self.parseTreeOutput.insert("end", "\n----parent node key_exp, finding children nodes:" + "\n")
            self.parseTreeOutput.insert("end", "child node (internal): keyword" + "\n")
            self.parseTreeOutput.insert("end", "  Keyword has child node(token):" + inToken[1] + "\n")
            accept_token(self, parent_id)
            self.parseTreeOutput.insert("end", "\n----parent node exp, finding children nodes:" + "\n")
            if (inToken[0] == "identifier"):
                self.parseTreeOutput.insert("end", "child node (internal): identifier" + "\n")
                self.parseTreeOutput.insert("end", "   identifier has child node (token):" + inToken[1] + "\n")
                accept_token(self, parent_id)
            else:
                print("expect identifier as the second element of the expression!\n")
                return
            if (inToken[1] == "="):
                self.parseTreeOutput.insert("end", "child node (token):" + inToken[1] + "\n")
                accept_token(self, parent_id)
            else:
                print("expect = as the third element of the expression!")
                return
            self.parseTreeOutput.insert("end", "Child node (internal): math" + "\n")
            math(self, parent_id)
            if (inToken[1] == ";"):
                self.parseTreeOutput.insert("end", "\n----parent node key_exp, finding children nodes:" + "\n")
                self.parseTreeOutput.insert("end", "child node (internal): seperator" + "\n")
                self.parseTreeOutput.insert("end", "   seperator has child node (token):" + inToken[1] + "\n")
                accept_token(self, parent_id)

        def print_exp(self, parent_id):
            global inToken
            self.parseTreeOutput.insert("end", "\n----parent node print_exp, finding children nodes:" + "\n")
            self.parseTreeOutput.insert("end", "child node (internal): keyword" + "\n")
            self.parseTreeOutput.insert("end", "   keyword has child node (token):" + inToken[1] + "\n")
            accept_token(self, parent_id)
            if (inToken[1] == "("):
                self.parseTreeOutput.insert("end", "child node (internal): seperator" + "\n")
                self.parseTreeOutput.insert("end", "   separator has child node (token):" + inToken[1] + "\n")
                accept_token(self, parent_id)
                if (inToken[1] in ["“", "\""]):
                    self.parseTreeOutput.insert("end", "child node (internal): seperator" + "\n")
                    self.parseTreeOutput.insert("end", "   separator has child node (token):" + inToken[1] + "\n")
                    accept_token(self, parent_id)
                    if (inToken[0] == "String_literal"):
                        self.parseTreeOutput.insert("end", "child node (internal): String" + "\n")
                        self.parseTreeOutput.insert("end", "   String has child node (token):" + inToken[1] + "\n")
                        accept_token(self, parent_id)
                        if (inToken[1] in ["”", "\""]):
                            self.parseTreeOutput.insert("end", "child node (internal): seperator" + "\n")
                            self.parseTreeOutput.insert("end",
                                                        "   separator has child node (token):" + inToken[1] + "\n")
                            accept_token(self, parent_id)
                            if (inToken[1] == ")"):
                                self.parseTreeOutput.insert("end", "child node (internal): seperator" + "\n")
                                self.parseTreeOutput.insert("end",
                                                            "   separator has child node (token):" + inToken[1] + "\n")
                                accept_token(self, parent_id)
                                if (inToken[1] == ";"):
                                    self.parseTreeOutput.insert("end", "child node (internal): seperator" + "\n")
                                    self.parseTreeOutput.insert("end", "   separator has child node (token):" + inToken[
                                        1] + "\n")
                                    accept_token(self, parent_id)

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
                exp(self, parent_id)
            elif (inToken[1] == "if"):
                if_exp(self, parent_id)
            elif (inToken[1] == "print"):
                print_exp(self)
            else:
                print("Error, invalid syntax.")
        else:
            print("Error, invalid syntax.")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = Tk()

    root.grid_rowconfigure(3, weight=1)  # Make new Tree Visualization box expandable
    root.grid_columnconfigure(1, weight=1)

    # enlarge window when user enlarges
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)

    lexer_gui = GUI(root)
    root.mainloop()
