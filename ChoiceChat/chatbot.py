import tkinter as tk
from tkinter import scrolledtext, PhotoImage, END
import time 
import sys
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener

from ChoiceChatLexer import ChoiceChatLexer
from ChoiceChatParser import ChoiceChatParser
from ChoiceChatListener import ChoiceChatListener

class NoOpErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e): pass
    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs): pass
    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs): pass
    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs): pass

class ChoiceExtractorListener(ChoiceChatListener):
    def __init__(self): self.selected_choice = None
    def enterSelectedChoice(self, ctx:ChoiceChatParser.SelectedChoiceContext):
        if ctx.CHOICE_TOKEN(): self.selected_choice = ctx.CHOICE_TOKEN().getText().upper()

def get_user_choice_antlr(user_input_str: str):
    input_stream = InputStream(user_input_str)
    lexer = ChoiceChatLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ChoiceChatParser(stream)
    lexer.removeErrorListeners()
    parser.removeErrorListeners()
    tree = parser.chatInput()
    listener = ChoiceExtractorListener()
    walker = ParseTreeWalker()
    walker.walk(listener, tree)
    return listener.selected_choice

available_options_for_ui = {
    # === FOUNDATIONS & CORE CONCEPTS ===
    "A": "Programming Paradigms: Overview of imperative, procedural, object-oriented, functional, logic, declarative, event-driven, agent-oriented, and concurrent/distributed programming.",
    "B": "History & Evolution of Programming Languages: Development from early languages (Assembly, Fortran, Lisp, COBOL) to modern ones (Python, Java, C#, JavaScript, Rust, Go, Swift, Kotlin) and the factors driving change.",
    "C": "Language Evaluation & Design Criteria: Readability, writability, reliability, cost, expressiveness, efficiency, orthogonality, simplicity, uniformity, extensibility, and portability.",
    "D": "Influence of Computer Architecture on Language Design: How Von Neumann and other architectures impact language features like variables, assignment, control structures, and parallel programming.",
    "E": "Virtual Machines & Runtime Environments: Concepts of VMs (JVM, CLR, PVM), their role in portability, memory management, and code execution.",

    # === SYNTAX ===
    "F": "Formal Syntax Specification: BNF (Backus-Naur Form), EBNF (Extended BNF), syntax diagrams/railroad diagrams, and their role in documentation and development tools.",
    "G": "Lexical Analysis / Scanning: The process of converting a character stream into a sequence of tokens (keywords, identifiers, constants, operators, punctuation). Regular expressions and finite automata (DFA/NFA).",
    "H": "Syntax Analysis / Parsing: Constructing a parse tree or abstract syntax tree (AST) from a token stream. Parsing techniques: top-down (LL, predictive parsing, recursive descent) and bottom-up (LR, SLR, LALR, GLR).",
    "I": "Syntax Error Handling: Techniques for detecting, reporting, and recovering from syntax errors during parsing.",

    # === SEMANTICS ===
    "J": "Static Semantics: Semantic rules checked before execution (compile-time). Includes type checking, name resolution, and other context-sensitive constraints.",
    "K": "Dynamic Semantics: Defining the meaning of language constructs during program execution. Specification methods: operational semantics, axiomatic semantics, denotational semantics.",
    "L": "Abstract Syntax Trees (ASTs): Intermediate data structure representing the hierarchical structure of a program, used in semantic analysis, optimization, and code generation.",
    "M": "Symbol Tables: Data structures used by compilers to store information about identifiers (names of variables, functions, types) and their attributes (type, scope, address).",

    # === DATA TYPES ===
    "N": "Primitive Data Types: Built-in types like integer, floating-point, decimal, boolean, character. Internal representation, value ranges, and related issues.",
    "O": "Structured Data Types: Arrays (static, dynamic, jagged), records/structs, unions (discriminated, free), strings, pointers, and references.",
    "P": "Data Abstraction & Abstract Data Types (ADTs): Hiding implementation details, exposing only an interface. Encapsulation. Examples: stack, queue, list defined as ADTs.",
    "Q": "Type Systems: Classification: static vs. dynamic, strong vs. weak, explicit vs. implicit/inferred. Pros and cons of each.",
    "R": "Type Checking: The process of verifying type compatibility of operands in expressions and function parameters. Type compatibility, type coercion/conversion, type equivalence (name vs. structural).",
    "S": "Polymorphism: The ability of an entity (function, object) to take on many forms. Parametric polymorphism (generics), ad-hoc polymorphism (overloading), subtype/inclusion polymorphism (inheritance), coercion polymorphism.",
    "T": "Pointers & References: Concepts, usage, issues (dangling pointers, memory leaks), and their differences in various languages.",

    # === EXPRESSIONS & STATEMENTS ===
    "U": "Expressions: Arithmetic, relational, logical, bitwise, assignment operators. Operator precedence and associativity. Short-circuit evaluation. Side effects.",
    "V": "Assignment Statements: Variations of assignment (basic, compound, multiple). Copy semantics vs. reference semantics.",
    "W": "Statement-Level Control Flow: Selection (if-then-else, switch/case/select), iteration (while, for, do-while, loop-exit), conditional and unconditional jumps (break, continue, goto, return).",

    # === SUBPROGRAMS (FUNCTIONS / PROCEDURES) ===
    "X": "Subprogram Definition & Activation: Declaration, definition, invocation. Activation records / stack frames and their structure.",
    "Y": "Scope & Lifetime: Static (lexical) scope vs. dynamic scope. Local, global, static variables. Closures.",
    "Z": "Parameter Passing Mechanisms: Pass-by-value, pass-by-result, pass-by-value-result, pass-by-reference, pass-by-name, pass-by-sharing (object references).",
    "AA": "Nested Subprograms: The ability to define subprograms within other subprograms and scope access rules.",
    "AB": "Subprogram Overloading: Allowing multiple subprograms with the same name but different signatures (number or types of parameters).",
    "AC": "Generic/Template Subprograms: Creating subprograms that can operate on multiple data types without rewriting code.",
    "AD": "Higher-Order Functions: Functions that can take other functions as parameters or return a function. A concept in functional programming.",
    "AE": "Coroutines & Generators: Special subprogram forms allowing suspension and resumption of execution, useful for asynchronous programming and lazy data sequence generation.",

    # === MEMORY MANAGEMENT ===
    "AF": "Major Memory Areas: Static, stack, heap. Characteristics and usage of each area.",
    "AG": "Stack-Based Allocation: How local variables and activation records are managed on the program stack.",
    "AH": "Heap-Based Allocation: Dynamic allocation for objects with an unknown lifetime. Fragmentation issues.",
    "AI": "Automatic Garbage Collection (GC): GC algorithms: reference counting, mark-and-sweep, stop-and-copy, generational GC. Pros and cons.",
    "AJ": "Manual Memory Management: `malloc`/`free` in C, `new`/`delete` in C++. Issues like dangling pointers, memory leaks, double free.",

    # === PROGRAM EXECUTION ===
    "AK": "Compilation Process: Stages: lexical analysis, syntax analysis, semantic analysis, intermediate code generation, optimization, target code generation.",
    "AL": "Interpretation Process: Direct execution of source code or bytecode. Pros and cons compared to compilation.",
    "AM": "Linking & Loading: The process of combining compiled modules and loading the program into memory for execution.",
    "AN": "Code Optimization: Optimization techniques at various levels (local, global, loop, inter-procedural) to improve performance or code size.",

    # === DETAILED PROGRAMMING PARADIGMS ===
    "AO": "Object-Oriented Programming (OOP): Encapsulation, inheritance (single, multiple, interface), polymorphism (dynamic dispatch). Classes, objects, methods, constructors, destructors, access modifiers. Design patterns.",
    "AP": "Functional Programming (FP): Pure functions, immutability, first-class and higher-order functions, recursion, lazy evaluation, monads, currying, function composition. FP languages: Haskell, Lisp, Scheme, Clojure, F#.",
    "AQ": "Logic Programming (LP): Based on predicate logic. Facts, rules, queries, unification, resolution, backtracking. Prolog as a prime example.",
    "AR": 'Declarative Programming: Describing "what" to achieve rather than "how". Includes LP, FP, SQL, HTML.',
    "AS": "Event-Driven Programming: Flow of execution is determined by events (user actions, system events). Callbacks, event loops. Common in GUI, web applications.",

    # === CONCURRENCY & PARALLELISM ===
    "AT": "Concurrency vs. Parallelism Concepts: Differences and their relationship.",
    "AU": "Threads & Processes: Creation, management, communication, and synchronization between threads/processes.",
    "AV": "Concurrency Issues: Race conditions, deadlocks, livelocks, starvation. Synchronization primitives (mutexes, semaphores, monitors, condition variables).",
    "AW": "Parallel Programming Models: Shared memory (e.g., OpenMP), distributed memory (e.g., MPI), data parallelism, task parallelism.",
    "AX": "Language Support for Concurrency: Built-in features or libraries in languages like Java (threads, `synchronized`), Python (GIL, `threading`, `asyncio`), Go (goroutines, channels), C++ ( `<thread>`, `<atomic>`).",

    # === ADVANCED & SPECIALIZED TOPICS ===
    "AY": "Domain-Specific Languages (DSLs): Languages designed for a specific problem domain (e.g., SQL for databases, HTML for web pages, R for statistics).",
    "AZ": "Metaprogramming: Programs that write or manipulate other programs (or themselves) as their data, or that do part of the work at compile time that would otherwise be done at runtime. Macros, reflection.",
    "BA": "Language Interoperability: Mechanisms allowing code written in different programming languages to work together (e.g., JNI, P/Invoke, FFI).",
    "BB": "Formal Methods in Software Development: Using mathematical techniques for the specification, development, and verification of software and hardware systems.",
    "BC": "Secure Coding Practices in PLs: Language features and programming practices that help prevent security vulnerabilities (e.g., buffer overflows, injection attacks).",
    "BD": "Quantum Programming Languages: Emerging languages designed to describe quantum computations for quantum computers (e.g., Q#, Qiskit).",
    "BE": "Ethical Considerations in Language Design: How language design choices can impact fairness, bias, accessibility, and societal implications."
}

class ChatApplication:
    TYPING_SPEED_MS = 10 
    THINKING_TIME_MS = 700 
    INDICATOR_ANIM_SPEED_MS = 300 

    def __init__(self, master, get_choice_function, options_data):
        self.master = master
        self.get_choice_function = get_choice_function
        self.options_data = options_data
        self.bot_is_processing = False 
        self.stop_indicator_animation = False
        self.current_indicator_job = None

        self.font_family = "Segoe UI"
        self.font_normal = (self.font_family, 10)
        self.font_bold = (self.font_family, 10, "bold")
        self.font_small = (self.font_family, 9)

        self.COLOR_BG_MAIN = "#F4F6F8"
        self.COLOR_BG_CHAT_AREA = "#FFFFFF"
        self.COLOR_TEXT_PRIMARY = "#263238"
        self.COLOR_TEXT_SECONDARY = "#546E7A"
        self.COLOR_USER_BG = "#E1F5FE"
        self.COLOR_USER_SENDER = "#0277BD"
        self.COLOR_BOT_BG = "#E8F5E9"
        self.COLOR_BOT_SENDER = "#2E7D32"
        self.COLOR_BOT_OPTION_KEY = self.COLOR_BOT_SENDER
        self.COLOR_BUTTON_NORMAL_BG = "#007BFF"
        self.COLOR_BUTTON_NORMAL_FG = "#FFFFFF"
        self.COLOR_BUTTON_HOVER_BG = "#0056b3"
        self.COLOR_BUTTON_HOVER_FG = "#FFFFFF"
        self.COLOR_BUTTON_DISABLED_BG = "#2F8FBE"
        self.COLOR_BUTTON_DISABLED_FG = "#ECEFF1"
        self.COLOR_INPUT_BG = "#FFFFFF"
        self.COLOR_INPUT_FG = self.COLOR_TEXT_PRIMARY
        self.COLOR_INPUT_BORDER = "#CFD8DC"
        self.COLOR_INPUT_BORDER_FOCUS = self.COLOR_BUTTON_NORMAL_BG

        master.title("Chatbot PPL Pro - Advanced Effects")
        master.geometry("800x700")
        master.configure(bg=self.COLOR_BG_MAIN)

        main_frame = tk.Frame(master, bg=self.COLOR_BG_MAIN, padx=15, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.chat_area = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, state='disabled',
                                                   font=self.font_normal,
                                                   bg=self.COLOR_BG_CHAT_AREA,
                                                   fg=self.COLOR_TEXT_PRIMARY,
                                                   relief=tk.FLAT, borderwidth=1,
                                                   padx=10, pady=10)
        self.chat_area.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        self.chat_area.tag_configure("user_block", background=self.COLOR_USER_BG, relief=tk.FLAT)
        self.chat_area.tag_configure("user_sender", foreground=self.COLOR_USER_SENDER, font=self.font_bold)

        self.chat_area.tag_configure("bot_block", background=self.COLOR_BOT_BG, relief=tk.FLAT)
        self.chat_area.tag_configure("bot_sender", foreground=self.COLOR_BOT_SENDER, font=self.font_bold)
        self.chat_area.tag_configure("bot_text_typed", font=self.font_normal)
        self.chat_area.tag_configure("bot_typing_indicator", font=self.font_normal)


        self.chat_area.tag_configure("bot_option_list_block")
        self.chat_area.tag_configure("bot_option_key", foreground=self.COLOR_BOT_OPTION_KEY, font=self.font_bold)
        self.chat_area.tag_configure("bot_option_text", foreground=self.COLOR_TEXT_SECONDARY, font=self.font_normal)
        self.chat_area.tag_configure("bot_instruction", foreground=self.COLOR_TEXT_SECONDARY, font=self.font_small)

        input_frame = tk.Frame(main_frame, bg=self.COLOR_BG_MAIN, pady=5)
        input_frame.pack(fill=tk.X)

        self.input_field = tk.Entry(input_frame, font=self.font_normal,
                                    bg=self.COLOR_INPUT_BG, fg=self.COLOR_INPUT_FG,
                                    relief=tk.SOLID, borderwidth=1,
                                    insertbackground=self.COLOR_TEXT_PRIMARY,
                                    highlightthickness=2,
                                    highlightbackground=self.COLOR_INPUT_BORDER,
                                    highlightcolor=self.COLOR_INPUT_BORDER_FOCUS)
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=8, padx=(0, 10))
        self.input_field.bind("<Return>", self.send_message_event)
        self.input_field.bind("<FocusIn>", lambda e: self.input_field.config(highlightbackground=self.COLOR_INPUT_BORDER_FOCUS))
        self.input_field.bind("<FocusOut>", lambda e: self.input_field.config(highlightbackground=self.COLOR_INPUT_BORDER))

        self.send_button = tk.Button(input_frame, text="Gửi", font=(self.font_family, 10, "bold"),
                                     bg=self.COLOR_BUTTON_NORMAL_BG, fg=self.COLOR_BUTTON_NORMAL_FG,
                                     activebackground=self.COLOR_BUTTON_HOVER_BG,
                                     activeforeground=self.COLOR_BUTTON_HOVER_FG,
                                     relief=tk.FLAT, borderwidth=0,
                                     padx=15, pady=6,
                                     command=self.send_message,
                                     cursor="hand2")
        self.send_button.pack(side=tk.RIGHT)
        self.send_button.bind("<Enter>", lambda e: self.send_button.config(bg=self.COLOR_BUTTON_HOVER_BG) if self.send_button['state'] == 'normal' else None)
        self.send_button.bind("<Leave>", lambda e: self.send_button.config(bg=self.COLOR_BUTTON_NORMAL_BG) if self.send_button['state'] == 'normal' else None)

        self.display_initial_message()
        self.input_field.focus_set()

    def _set_input_state(self, state):
        self.input_field.config(state=state)
        self.send_button.config(state=state)
        if state == 'disabled':
            self.send_button.config(bg=self.COLOR_BUTTON_DISABLED_BG, fg=self.COLOR_BUTTON_DISABLED_FG)
            self.send_button.unbind("<Enter>")
            self.send_button.unbind("<Leave>")
        else:
            self.send_button.config(bg=self.COLOR_BUTTON_NORMAL_BG, fg=self.COLOR_BUTTON_NORMAL_FG)
            self.send_button.bind("<Enter>", lambda e: self.send_button.config(bg=self.COLOR_BUTTON_HOVER_BG) if self.send_button['state'] == 'normal' else None)
            self.send_button.bind("<Leave>", lambda e: self.send_button.config(bg=self.COLOR_BUTTON_NORMAL_BG) if self.send_button['state'] == 'normal' else None)

    def send_message_event(self, event):
        if not self.bot_is_processing:
            self.send_message()

    def add_message_to_chat_immediately(self, sender_name, message_text, sender_type):
        self.chat_area.config(state='normal')
        prefix = ""
        block_tag_tuple = ()

        if sender_type == "user":
            block_tag_tuple = ("user_block", "user_sender")
            prefix = f"{sender_name}: "
        elif sender_type == "bot_option":
            block_tag_tuple = ("bot_option_list_block", "bot_option_key")
            key, topic = message_text
            prefix = f"  {key}: "
            message_text = topic
        elif sender_type == "bot_instruction":
            block_tag_tuple = ("bot_instruction",)
        elif sender_type == "bot_initial":
            block_tag_tuple = ("bot_block", "bot_sender")
            prefix = f"{sender_name}: "

        start_index_marker = self.chat_area.index(tk.END + "-1c")
        if start_index_marker != "1.0": self.chat_area.insert(tk.END, "\n\n")
        else: self.chat_area.insert(tk.END, "\n")
        
        line_start_index = self.chat_area.index(tk.END + "-1c")
        line_content = prefix + message_text + "\n"
        self.chat_area.insert(tk.END, line_content, block_tag_tuple[0])

        if len(block_tag_tuple) > 1 and prefix:
            self.chat_area.tag_add(block_tag_tuple[1], line_start_index, f"{line_start_index}+{len(prefix)}c")

        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def _start_bot_processing(self, full_message_text_to_type):
        if self.bot_is_processing: return
        self.bot_is_processing = True
        self._set_input_state('disabled')
        self.chat_area.config(state='normal')

        self.sender_prefix_for_bot = "Bot: "
        start_index_marker = self.chat_area.index(tk.END + "-1c")
        if start_index_marker != "1.0": self.chat_area.insert(tk.END, "\n\n")
        else: self.chat_area.insert(tk.END, "\n")

        self.current_bot_message_start_index = self.chat_area.index(tk.END + "-1c")
        self.chat_area.insert(tk.END, self.sender_prefix_for_bot, ("bot_block", "bot_sender"))
        
        self.indicator_dots_start_index = self.chat_area.index(tk.END + "-1c")
        self.stop_indicator_animation = False
        self._animate_typing_indicator()

        self.master.after(self.THINKING_TIME_MS, lambda: self._begin_actual_typing(full_message_text_to_type))

    def _animate_typing_indicator(self, dot_count=0):
        if self.stop_indicator_animation:
            self.chat_area.config(state='normal')
            self.chat_area.delete(self.indicator_dots_start_index, tk.END + "-1l") # Delete from start of dots to end of that line
            self.chat_area.config(state='disabled')
            if self.current_indicator_job:
                self.master.after_cancel(self.current_indicator_job)
                self.current_indicator_job = None
            return

        self.chat_area.config(state='normal')
        self.chat_area.delete(self.indicator_dots_start_index, tk.END + "-1l") # Delete old dots
        
        dots = "." * ((dot_count % 3) + 1)
        self.chat_area.insert(self.indicator_dots_start_index, dots, ("bot_block", "bot_typing_indicator"))
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)
        
        self.current_indicator_job = self.master.after(self.INDICATOR_ANIM_SPEED_MS, lambda: self._animate_typing_indicator(dot_count + 1))

    def _begin_actual_typing(self, full_message_text):
        self.stop_indicator_animation = True 
        if self.current_indicator_job:
             self.master.after_cancel(self.current_indicator_job)
             self.current_indicator_job = None
        self.chat_area.config(state='normal')
        self.chat_area.delete(self.indicator_dots_start_index, tk.END + "-1l") 
        self._char_index_typing = 0
        self._full_text_to_type = full_message_text
        self.typing_start_index_for_actual_text = self.chat_area.index(tk.END + "-1c") 
        self._type_next_char_recursive()


    def _type_next_char_recursive(self):
        if self._char_index_typing < len(self._full_text_to_type):
            char = self._full_text_to_type[self._char_index_typing]
            self.chat_area.config(state='normal')
            self.chat_area.insert(tk.END, char, ("bot_block", "bot_text_typed"))
            self.chat_area.config(state='disabled')
            self.chat_area.see(tk.END)
            self._char_index_typing += 1
            self.master.after(self.TYPING_SPEED_MS, self._type_next_char_recursive)
        else:
            self.chat_area.config(state='normal')
            self.chat_area.insert(tk.END, "\n", "bot_block") 
            self.chat_area.config(state='disabled')
            self.chat_area.see(tk.END)
            self.bot_is_processing = False
            self._set_input_state('normal')
            self.input_field.focus_set()

    def display_initial_message(self):
        self.add_message_to_chat_immediately("Bot", "Chào bạn! Tôi là chatbot về Nguyên lý Ngôn ngữ Lập trình (PPL).", "bot_initial")
        self.add_message_to_chat_immediately(None, "Vui lòng chọn một chủ đề bạn quan tâm:", "bot_instruction")

        for key_option, text_option_full in self.options_data.items():
            topic_name = text_option_full.split(":")[0].strip()
            self.add_message_to_chat_immediately(None, (key_option, topic_name), "bot_option")

        self.add_message_to_chat_immediately(None, "\nBạn cũng có thể gõ 'chọn A', 'lấy B', v.v.", "bot_instruction")
        self.add_message_to_chat_immediately(None, "Gõ 'thoát' để kết thúc.", "bot_instruction")

    def send_message(self):
        if self.bot_is_processing: return
        user_text = self.input_field.get()
        if not user_text.strip():
            return

        self.add_message_to_chat_immediately("Bạn", user_text, "user")
        self.input_field.delete(0, tk.END)

        if user_text.lower() in ['thoát', 'exit', 'quit']:
            self._start_bot_processing("Tạm biệt! Hẹn gặp lại.")
          
            self.master.after(self.THINKING_TIME_MS + len("Tạm biệt! Hẹn gặp lại.") * self.TYPING_SPEED_MS + 1000, self.master.destroy)
            return

        extracted_choice = self.get_choice_function(user_text)
        bot_response = ""

        if extracted_choice and extracted_choice in self.options_data:
            bot_response = self.options_data[extracted_choice]
        elif extracted_choice:
            bot_response = f"Lựa chọn '{extracted_choice}' không có trong danh sách. Vui lòng chọn lại."
        else:
            bot_response = "Tôi không hiểu lựa chọn của bạn. Vui lòng thử lại (ví dụ: 'A', 'chọn B')."
        
        self._start_bot_processing(bot_response)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApplication(root, get_user_choice_antlr, available_options_for_ui)
    root.mainloop()