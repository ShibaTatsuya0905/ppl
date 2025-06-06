import tkinter as tk
from tkinter import scrolledtext, END
import spacy
import sys
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener

from ChoiceChatLexer import ChoiceChatLexer
from ChoiceChatParser import ChoiceChatParser
from ChoiceChatListener import ChoiceChatListener

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading language model 'en_core_web_sm' for spaCy...")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

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

knowledge_base_ppl = {
    "PROGRAMMING PARADIGMS": {
        "description": "Programming Paradigms: Overview of imperative, procedural, object-oriented, functional, logic, declarative, event-driven, agent-oriented, and concurrent/distributed programming.",
        "example": "Python is multi-paradigm, supporting object-oriented, imperative, and functional styles.",
        "related_topics": ["OOP", "FUNCTIONAL PROGRAMMING", "LOGIC PROGRAMMING", "DECLARATIVE PROGRAMMING"]
    },
    "HISTORY OF PROGRAMMING LANGUAGES": {
        "description": "History & Evolution of Programming Languages: Development from early languages (Assembly, Fortran, Lisp, COBOL) to modern ones (Python, Java, C#, JavaScript, Rust, Go, Swift, Kotlin) and the factors driving change.",
        "example": "LISP, developed in the late 1950s, was one of the earliest functional programming languages and heavily influenced AI research.",
    },
    "LANGUAGE EVALUATION CRITERIA": {
        "description": "Language Evaluation & Design Criteria: Readability, writability, reliability, cost, expressiveness, efficiency, orthogonality, simplicity, uniformity, extensibility, and portability.",
        "example": "Readability is a key criterion where Python often scores high due to its clean syntax.",
        "pros": ["Helps in choosing the right language for a task", "Guides language designers"],
        "cons": ["Criteria can be subjective", "Some criteria might conflict (e.g., efficiency vs. writability)"]
    },
    "INFLUENCE OF COMPUTER ARCHITECTURE": {
        "description": "Influence of Computer Architecture on Language Design: How Von Neumann and other architectures impact language features like variables, assignment, control structures, and parallel programming.",
        "example": "The Von Neumann architecture directly led to the concept of assignable variables and iterative control structures in imperative languages.",
        "related_topics": ["MEMORY MANAGEMENT"]
    },
    "VIRTUAL MACHINES AND RUNTIME ENVIRONMENTS": {
        "description": "Virtual Machines & Runtime Environments: Concepts of VMs (JVM, CLR, PVM), their role in portability, memory management, and code execution.",
        "example": "The Java Virtual Machine (JVM) allows Java code to run on any device that has a compatible JVM, achieving 'write once, run anywhere'.",
        "pros": ["Portability", "Security (sandboxing)", "Abstracts hardware differences"],
        "cons": ["Performance overhead compared to native code", "Increased memory footprint"]
    },
    "SYNTAX SPECIFICATION": {
        "description": "Formal Syntax Specification: BNF (Backus-Naur Form), EBNF (Extended BNF), syntax diagrams/railroad diagrams, and their role in documentation and development tools.",
        "example": "An EBNF rule for an identifier might be: `identifier ::= letter { letter | digit }`."
    },
    "LEXICAL ANALYSIS": {
        "description": "Lexical Analysis / Scanning: The process of converting a character stream into a sequence of tokens (keywords, identifiers, constants, operators, punctuation). Regular expressions and finite automata (DFA/NFA).",
        "example": "The input `var x = 10;` might be tokenized into: `KEYWORD(var)`, `IDENTIFIER(x)`, `OPERATOR(=)`, `INTEGER_LITERAL(10)`, `PUNCTUATION(;)`."
    },
    "SYNTAX ANALYSIS": {
        "description": "Syntax Analysis / Parsing: Constructing a parse tree or abstract syntax tree (AST) from a token stream. Parsing techniques: top-down (LL, predictive parsing, recursive descent) and bottom-up (LR, SLR, LALR, GLR).",
        "example": "A parser would check if the sequence of tokens from lexical analysis conforms to the language's grammar rules."
    },
    "SYNTAX ERROR HANDLING": {
        "description": "Syntax Error Handling: Techniques for detecting, reporting, and recovering from syntax errors during parsing, such as panic mode or phrase-level recovery.",
        "example": "When a compiler encounters a missing semicolon, it might report an error and attempt to continue parsing to find more errors."
    },
    "STATIC SEMANTICS": {
        "description": "Static Semantics: Semantic rules checked before execution (compile-time). Includes type checking, name resolution (ensuring variables are declared), and other context-sensitive constraints.",
        "example": "A static semantic check would ensure that a variable is declared before it is used, or that function arguments match parameter types."
    },
    "DYNAMIC SEMANTICS": {
        "description": "Dynamic Semantics: Defining the meaning of language constructs during program execution. Specification methods: operational semantics, axiomatic semantics, denotational semantics.",
        "example": "The dynamic semantics of a loop define how many times its body will execute based on the loop condition at runtime."
    },
    "ABSTRACT SYNTAX TREES": {
        "description": "Abstract Syntax Trees (ASTs): A tree representation of the abstract syntactic structure of source code. Each node denotes a construct occurring in the source code. It's a more compact and abstract representation than a parse tree.",
        "example": "For `a + b * c`, the AST would show `*` as a parent of `b` and `c`, and `+` as a parent of `a` and the `*` node, reflecting operator precedence."
    },
    "SYMBOL TABLES": {
        "description": "Symbol Tables: A data structure used by a language translator such as a compiler or interpreter, where each identifier in a program's source code is associated with information relating to its declaration or appearance in the source, such as its type, scope level, and sometimes its location.",
        "example": "When a variable `int count;` is declared, the symbol table stores 'count', its type 'int', its scope, and memory offset."
    },
    "PRIMITIVE DATA TYPES": {
        "description": "Primitive Data Types: Built-in types like integer, floating-point, decimal, boolean, character. Internal representation, value ranges, and related issues.",
        "example": "In Java, `int`, `float`, `boolean`, `char` are primitive data types.",
        "related_topics": ["DATA TYPES", "TYPE_SYSTEMS"]
    },
    "STRUCTURED DATA TYPES": {
        "description": "Structured Data Types: Types constructed from primitive types or other structured types. Examples include arrays, records (structs/objects), unions, strings, lists, and sets.",
        "example": "A `struct Point { int x; int y; }` in C is a structured data type."
    },
    "DATA ABSTRACTION AND ADTS": {
        "description": "Data Abstraction & Abstract Data Types (ADTs): Hiding implementation details of data structures, exposing only an interface of operations. Encapsulation is a key part. ADTs define a set of values and a set of operations on those values.",
        "example": "A Stack ADT is defined by operations like `push()`, `pop()`, `peek()`, `isEmpty()`, without specifying if it's implemented using an array or a linked list."
    },
    "TYPE SYSTEMS": {
        "description": "A Type System is a set of rules assigning a 'type' property to program constructs. Main categories: static (compile-time checks) vs. dynamic (run-time checks); strong vs. weak typing.",
        "example": "Java has a static, strong type system; Python has a dynamic, strong type system.",
        "related_topics": ["STATIC_TYPING", "DYNAMIC_TYPING", "TYPE_CHECKING", "DATA_TYPES"]
    },
    "TYPE CHECKING": {
        "description": "Type Checking: The process of verifying and enforcing the constraints of types. It can occur at compile-time (static) or run-time (dynamic). Ensures that operations are performed on compatible types.",
        "example": "A type checker would flag an error if you tried to add a string to an integer in a language that doesn't allow implicit coercion for that operation."
    },
    "POLYMORPHISM": {
        "description": "Polymorphism: The ability of an entity (e.g., a variable, function, or object) to take on multiple forms. Main types: ad-hoc (overloading), parametric (generics), subtype (inheritance).",
        "example": "A `print()` function that can print integers, strings, and floats is an example of ad-hoc polymorphism (overloading). A generic List<T> is parametric polymorphism."
    },
    "POINTERS AND REFERENCES": {
        "description": "Pointers & References: Pointers hold memory addresses. References are aliases for existing variables. They allow indirect data manipulation but can lead to issues like dangling pointers or aliasing problems.",
        "example": "C and C++ use pointers extensively (`int *p;`). Java uses references for all objects, but not explicit pointer arithmetic."
    },
    "EXPRESSIONS": {
        "description": "Expressions: Combinations of values, variables, operators, and function calls that are evaluated to produce a new value. Governed by operator precedence and associativity.",
        "example": "`a + (b * c) / d` is an arithmetic expression."
    },
    "ASSIGNMENT STATEMENTS": {
        "description": "Assignment Statements: Used to assign a value to a variable. Variations include simple assignment (`=`), compound assignment (`+=`, `-=`), and multiple assignment.",
        "example": "`x = 5;` or `count += 1;`."
    },
    "STATEMENT-LEVEL CONTROL FLOW": {
        "description": "Statement-Level Control Flow: Mechanisms to alter the sequential execution of statements. Includes selection (if, switch), iteration (for, while), and jumps (break, continue, goto).",
        "example": "An `if-else` statement selects one of two blocks of code to execute based on a condition."
    },
    "SUBPROGRAM DEFINITION AND ACTIVATION": {
        "description": "Subprogram Definition & Activation: Defining reusable blocks of code (functions, procedures, methods). Activation involves creating an activation record (stack frame) to store local variables, parameters, and return address.",
        "example": "Defining a function `def greet(name): print(f'Hello, {name}')` and calling it `greet('World')`."
    },
    "SCOPE AND LIFETIME": {
        "description": "Scope & Lifetime: Scope defines the visibility of an identifier. Lifetime is the duration a variable exists in memory. Static (lexical) scope is determined at compile-time; dynamic scope at run-time. Closures are functions that capture their lexical environment.",
        "example": "A variable declared inside a function typically has local scope and its lifetime is tied to the function's execution."
    },
    "PARAMETER PASSING MECHANISMS": {
        "description": "Parameter Passing Mechanisms: How arguments are passed to subprograms. Common methods: pass-by-value, pass-by-reference, pass-by-result, pass-by-value-result, pass-by-name, pass-by-sharing.",
        "example": "In pass-by-value, a copy of the argument's value is passed. In pass-by-reference, the subprogram gets direct access to the original argument's memory location."
    },
    "NESTED SUBPROGRAMS": {
        "description": "Nested Subprograms: The ability to define subprograms (functions or procedures) within other subprograms. Inner subprograms can often access variables of their enclosing subprograms (lexical scoping).",
        "example": "Python allows defining functions inside other functions."
    },
    "SUBPROGRAM OVERLOADING": {
        "description": "Subprogram Overloading: Allows multiple subprograms to have the same name but different parameter lists (signatures), distinguished by the number or types of their parameters.",
        "example": "In C++ or Java, you can have `int add(int a, int b)` and `float add(float a, float b)`."
    },
    "GENERIC SUBPROGRAMS": {
        "description": "Generic/Template Subprograms: Allow writing a single subprogram definition that can work with different data types, specified as parameters at compile-time or instantiation-time.",
        "example": "C++ templates (`template<typename T> T max(T a, T b)`) or Java generics (`List<String>`)."
    },
    "HIGHER-ORDER FUNCTIONS": {
        "description": "Higher-Order Functions: Functions that can take other functions as arguments or return functions as their results. A key feature of functional programming.",
        "example": "Python's `map()`, `filter()`, and `sorted()` (with a `key` function) are higher-order functions."
    },
    "COROUTINES AND GENERATORS": {
        "description": "Coroutines & Generators: Coroutines are subprograms that can suspend execution and resume later, allowing for cooperative multitasking. Generators are a type of coroutine that produce a sequence of values lazily.",
        "example": "Python's `async/await` for coroutines and `yield` keyword for generators."
    },
    "MEMORY MANAGEMENT AREAS": {
        "description": "Major Memory Areas: Programs typically use static memory (for global/static variables), stack memory (for local variables and function calls), and heap memory (for dynamically allocated data).",
        "example": "Global variables are in static memory, local variables of a function on the stack, objects created with `new` (Java/C++) or `malloc` (C) on the heap."
    },
    "STACK-BASED ALLOCATION": {
        "description": "Stack-Based Allocation: Memory for local variables and function parameters is allocated on a runtime stack when a subprogram is called and deallocated when it returns. Follows LIFO (Last-In, First-Out).",
        "example": "Each function call creates a new activation record (stack frame) on top of the stack."
    },
    "HEAP-BASED ALLOCATION": {
        "description": "Heap-Based Allocation: Memory allocated dynamically at runtime from a large pool of memory called the heap. Programmer (or runtime system) controls allocation and deallocation. Can lead to fragmentation.",
        "example": "Using `new` in Java or C++, or `malloc` in C, allocates memory on the heap."
    },
    "GARBAGE COLLECTION": {
        "description": "Automatic Garbage Collection (GC): A form of automatic memory management where the garbage collector attempts to reclaim memory occupied by objects that are no longer in use by the program. Algorithms include reference counting, mark-and-sweep, generational GC.",
        "example": "Java, Python, C#, Go, and Lisp all have garbage collection."
    },
    "MANUAL MEMORY MANAGEMENT": {
        "description": "Manual Memory Management: The programmer is responsible for explicitly allocating and deallocating memory. Requires careful management to avoid memory leaks and dangling pointers.",
        "example": "Using `malloc()`/`free()` in C and `new`/`delete` in C++."
    },
    "COMPILATION PROCESS": {
        "description": "Compilation Process: Translates source code from a high-level language into a lower-level language (e.g., machine code or bytecode). Stages include lexical analysis, syntax analysis, semantic analysis, intermediate code generation, optimization, and target code generation.",
        "example": "A C++ compiler (like g++) takes `.cpp` files and produces an executable file."
    },
    "INTERPRETATION PROCESS": {
        "description": "Interpretation Process: An interpreter directly executes instructions written in a programming or scripting language without previously converting them to an object code or machine code. Can be slower but offers more flexibility.",
        "example": "Python's default CPython implementation interprets bytecode. Many scripting languages are interpreted."
    },
    "LINKING AND LOADING": {
        "description": "Linking & Loading: Linking combines various pieces of object code and library code into a single executable image. Loading copies the executable image from disk into memory and prepares it for execution.",
        "example": "A linker resolves external references between different compiled modules."
    },
    "CODE OPTIMIZATION": {
        "description": "Code Optimization: The process of transforming a piece of code to make it more efficient (either in terms of execution time or memory usage) or smaller, without changing its output. Occurs at various compiler stages.",
        "example": "Constant folding, loop unrolling, dead code elimination, register allocation."
    },
    "OBJECT-ORIENTED PROGRAMMING": {
        "description": "Object-Oriented Programming (OOP): A paradigm based on 'objects', which contain data (attributes) and code (methods). Key principles: encapsulation, inheritance, polymorphism. Classes, objects, methods, constructors, destructors, access modifiers. Design patterns.",
        "example": "A `Dog` class inheriting from an `Animal` class, with `Dog` objects having specific behaviors like `bark()`.",
        "related_topics": ["OOP", "ENCAPSULATION", "INHERITANCE", "POLYMORPHISM"] # OOP key is already defined
    },
    "FUNCTIONAL PROGRAMMING DETAILED": {
        "description": "Functional Programming (FP): Pure functions, immutability, first-class and higher-order functions, recursion, lazy evaluation, monads, currying, function composition. FP languages: Haskell, Lisp, Scheme, Clojure, F#.",
        "example": "A pure function in FP always produces the same output for the same input and has no side effects." ,
        "related_topics": ["FUNCTIONAL PROGRAMMING", "IMMUTABILITY", "PURE FUNCTIONS"] # FP key is already defined
    },
    "LOGIC PROGRAMMING DETAILED": {
        "description": "Logic Programming (LP): Based on predicate logic. Facts, rules, queries, unification, resolution, backtracking. Prolog.",
        "example": "In Prolog, you can define `ancestor(X, Z) :- parent(X, Y), ancestor(Y, Z).` and query `?- ancestor(john, jim).`",
        "related_topics": ["LOGIC PROGRAMMING", "PROLOG", "DECLARATIVE PROGRAMMING"]
    },
    "DECLARATIVE PROGRAMMING DETAILED": {
        "description": 'Declarative Programming: Describes "what" to achieve rather than "how". Includes LP, FP, SQL, HTML.',
        "example": "CSS rules are declarative: `body { font-size: 16px; }` states the desired font size, not how to render it.",
        "related_topics": ["DECLARATIVE PROGRAMMING", "FUNCTIONAL PROGRAMMING", "LOGIC PROGRAMMING"]
    },
    "EVENT-DRIVEN PROGRAMMING": {
        "description": "Event-Driven Programming: The flow of the program is determined by events such as user actions (mouse clicks, key presses), sensor outputs, or messages from other programs/threads. Uses event handlers/callbacks.",
        "example": "GUI applications (like this Tkinter chatbot) are event-driven. Clicking a button triggers an event that calls a specific function."
    },
    "CONCURRENCY VS PARALLELISM": {
        "description": "Concurrency vs. Parallelism Concepts: Concurrency is about dealing with multiple tasks at once (can be interleaved on a single core). Parallelism is about doing multiple tasks at once (requires multiple cores).",
        "example": "A web server handling multiple client requests concurrently. A video encoding program using all CPU cores to process parts of a video in parallel."
    },
    "THREADS AND PROCESSES": {
        "description": "Threads & Processes: A process is an instance of a program with its own memory space. A thread is a lightweight unit of execution within a process, sharing the process's memory. Used for concurrency.",
        "example": "A word processor might use one thread for user input and another for background spell-checking."
    },
    "CONCURRENCY ISSUES": {
        "description": "Concurrency Issues: Problems arising from multiple threads/processes accessing shared resources. Includes race conditions, deadlocks, livelocks, starvation. Synchronization primitives (mutexes, semaphores, monitors, condition variables) are used to manage these.",
        "example": "A race condition occurs if two threads try to increment a shared counter simultaneously without proper locking, potentially leading to an incorrect final value."
    },
    "PARALLEL PROGRAMMING MODELS": {
        "description": "Parallel Programming Models: Frameworks for structuring parallel programs. Common models include shared memory (e.g., OpenMP), distributed memory (e.g., MPI), data parallelism, and task parallelism.",
        "example": "MPI is often used for large-scale scientific simulations on supercomputer clusters."
    },
    "LANGUAGE SUPPORT FOR CONCURRENCY": {
        "description": "Language Support for Concurrency: Built-in features or libraries in languages like Java (threads, `synchronized`), Python (GIL, `threading`, `asyncio`), Go (goroutines, channels), C++ (`<thread>`, `<atomic>`).",
        "example": "Go's goroutines and channels provide a high-level and efficient way to manage concurrent operations."
    },
    "DOMAIN-SPECIFIC LANGUAGES": {
        "description": "Domain-Specific Languages (DSLs): Languages designed for a specific problem domain, offering expressive power tailored to that domain (e.g., SQL for databases, HTML for web pages, R for statistics, Makefiles for build automation).",
        "example": "SQL is a DSL for querying and managing relational databases."
    },
    "METAPROGRAMMING": {
        "description": "Metaprogramming: Programs that write or manipulate other programs (or themselves) as their data, or that do part of the work at compile time that would otherwise be done at runtime. Examples include macros, reflection, decorators in Python.",
        "example": "Python decorators are a form of metaprogramming that can modify or enhance functions or classes."
    },
    "LANGUAGE INTEROPERABILITY": {
        "description": "Language Interoperability: Mechanisms allowing code written in different programming languages to work together (e.g., JNI in Java, P/Invoke in .NET, FFI - Foreign Function Interface in many languages).",
        "example": "Calling a C library function from a Python script using `ctypes` (an FFI)."
    },
    "FORMAL METHODS": {
        "description": "Formal Methods in Software Development: Using mathematically-based techniques for the specification, development, and verification of software and hardware systems to ensure correctness and reliability.",
        "example": "Using model checking to verify that a concurrent algorithm is free of deadlocks."
    },
    "SECURE CODING PRACTICES": {
        "description": "Secure Coding Practices in PLs: Language features and programming practices that help prevent security vulnerabilities (e.g., preventing buffer overflows, SQL injection, cross-site scripting).",
        "example": "Using prepared statements in SQL to prevent SQL injection, or bounds checking in languages to prevent buffer overflows."
    },
    "QUANTUM PROGRAMMING LANGUAGES": {
        "description": "Quantum Programming Languages: Emerging languages designed to describe quantum computations for quantum computers, dealing with concepts like qubits, superposition, and entanglement (e.g., Q#, Qiskit, Cirq).",
        "example": "Qiskit (Python library) allows users to design quantum circuits and run them on simulators or real quantum hardware."
    },
    "ETHICAL CONSIDERATIONS IN LANGUAGE DESIGN": {
        "description": "Ethical Considerations in Language Design & Use: How language design choices and their use can impact fairness, bias (e.g., in AI models trained with data processed by certain language tools), accessibility, privacy, and societal implications.",
        "example": "Ensuring that error messages are inclusive and understandable, or considering the potential for misuse of powerful language features in AI or autonomous systems."
    }
}


initial_display_options = {}
for i, key in enumerate(knowledge_base_ppl.keys()):
    char_code = ord('A') + i
    option_key_char = ""
    if char_code > ord('Z'):
        idx_beyond_z = i - 26
        first_char_offset = idx_beyond_z // 26 
        second_char_offset = idx_beyond_z % 26
        if first_char_offset > 25 : 
            option_key_char = f"Opt{i+1}" 
        else:
             option_key_char = chr(ord('A') + first_char_offset) + chr(ord('A') + second_char_offset)
    else:
        option_key_char = chr(char_code)
    initial_display_options[option_key_char] = key


def process_nlp_input(user_input, knowledge_base_local, initial_options_local):
    doc = nlp(user_input.lower())
    intent = None
    topic_key = None
    extracted_entities = [] 

    define_keywords = ["what is", "define", "explain", "tell me about", "describe", "meaning of"]
    example_keywords = ["example of", "give me an example", "show an example", "sample of"]
    pros_keywords = ["advantages of", "pros of", "benefits of", "good things about"]
    cons_keywords = ["disadvantages of", "cons of", "drawbacks of", "bad things about"]
    related_keywords = ["related to", "similar to", "connections with", "related topics for"]

    user_input_lower = user_input.lower()

    if any(phrase in user_input_lower for phrase in define_keywords):
        intent = "ask_definition"
    elif any(phrase in user_input_lower for phrase in example_keywords):
        intent = "ask_example"
    elif any(phrase in user_input_lower for phrase in pros_keywords):
        intent = "ask_pros"
    elif any(phrase in user_input_lower for phrase in cons_keywords):
        intent = "ask_cons"
    elif any(phrase in user_input_lower for phrase in related_keywords):
        intent = "ask_related"
    
    if not intent and ("what" in user_input_lower or "tell me" in user_input_lower or "how" in user_input_lower or "?" in user_input_lower):
        intent = "ask_definition"

    best_match_score = 0
    matched_kb_key_for_intent = None

    for kb_key_raw in knowledge_base_local.keys():
        kb_key_normalized = kb_key_raw.lower()
        score = 0
        
        if kb_key_normalized in user_input_lower:
            score = len(kb_key_normalized.split()) * 10 
        else:
            kb_key_words = set(kb_key_normalized.split())
            input_lemmas_set = set(token.lemma_ for token in doc if not token.is_stop and not token.is_punct)
            common_words = kb_key_words.intersection(input_lemmas_set)
            score = len(common_words)
            if "programming" in common_words and len(common_words)>1: score+=0.5 
            if "language" in common_words and len(common_words)>1: score+=0.5

        if score > best_match_score:
            best_match_score = score
            matched_kb_key_for_intent = kb_key_raw
    
    if matched_kb_key_for_intent:
        topic_key = matched_kb_key_for_intent
        if topic_key not in extracted_entities: extracted_entities.append(topic_key)
    
    if not intent and topic_key:
        intent = "ask_definition"
            
    if not topic_key:
        # SỬA DÒNG NÀY:
        # Bỏ "user_input_original=" và chỉ truyền giá trị của biến user_input
        raw_antlr_choice = get_user_choice_antlr(user_input) # user_input ở đây là biến chứa input của người dùng đã được truyền vào process_nlp_input
        
        if raw_antlr_choice and raw_antlr_choice in initial_options_local:
            topic_key = initial_options_local[raw_antlr_choice]
            if not intent: 
                intent = "ask_definition"
            if topic_key not in extracted_entities: extracted_entities.append(topic_key)


    if intent and topic_key:
        return intent, topic_key, extracted_entities 
    else:
        return None, None, []


class ChatApplication:
    TYPING_SPEED_MS = 30
    THINKING_TIME_MS = 600
    INDICATOR_ANIM_SPEED_MS = 300

    def __init__(self, master, get_antlr_func, initial_options_param, knowledge_base_param):
        self.master = master
        self.get_antlr_function = get_antlr_func 
        self.initial_display_options = initial_options_param
        self.knowledge_base = knowledge_base_param

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
        self.COLOR_BUTTON_DISABLED_BG = "#B0BEC5"
        self.COLOR_BUTTON_DISABLED_FG = "#ECEFF1"
        self.COLOR_INPUT_BG = "#FFFFFF"
        self.COLOR_INPUT_FG = self.COLOR_TEXT_PRIMARY
        self.COLOR_INPUT_BORDER = "#CFD8DC"
        self.COLOR_INPUT_BORDER_FOCUS = self.COLOR_BUTTON_NORMAL_BG

        master.title("Chatbot PPL Pro - NLP Enhanced")
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

        self.send_button = tk.Button(input_frame, text="Send", font=(self.font_family, 10, "bold"),
                                     bg=self.COLOR_BUTTON_NORMAL_BG, fg=self.COLOR_BUTTON_NORMAL_FG,
                                     activebackground=self.COLOR_BUTTON_HOVER_BG,
                                     activeforeground=self.COLOR_BUTTON_HOVER_FG,
                                     relief=tk.FLAT, borderwidth=0,
                                     padx=15, pady=6,
                                     command=self.send_message,
                                     cursor="hand2")
        self.send_button.pack(side=tk.RIGHT)
        self.send_button._enter_bind_id = self.send_button.bind("<Enter>", lambda e: self.send_button.config(bg=self.COLOR_BUTTON_HOVER_BG) if self.send_button['state'] == 'normal' else None)
        self.send_button._leave_bind_id = self.send_button.bind("<Leave>", lambda e: self.send_button.config(bg=self.COLOR_BUTTON_NORMAL_BG) if self.send_button['state'] == 'normal' else None)

        self.display_initial_message()
        self.input_field.focus_set()

    def _set_input_state(self, state):
        self.input_field.config(state=state)
        self.send_button.config(state=state)
        if state == 'disabled':
            self.send_button.config(bg=self.COLOR_BUTTON_DISABLED_BG, fg=self.COLOR_BUTTON_DISABLED_FG)
            if hasattr(self.send_button, "_enter_bind_id") and self.send_button._enter_bind_id: self.send_button.unbind("<Enter>", self.send_button._enter_bind_id)
            if hasattr(self.send_button, "_leave_bind_id") and self.send_button._leave_bind_id: self.send_button.unbind("<Leave>", self.send_button._leave_bind_id)
        else:
            self.send_button.config(bg=self.COLOR_BUTTON_NORMAL_BG, fg=self.COLOR_BUTTON_NORMAL_FG)
            self.send_button._enter_bind_id = self.send_button.bind("<Enter>", lambda e: self.send_button.config(bg=self.COLOR_BUTTON_HOVER_BG) if self.send_button['state'] == 'normal' else None)
            self.send_button._leave_bind_id = self.send_button.bind("<Leave>", lambda e: self.send_button.config(bg=self.COLOR_BUTTON_NORMAL_BG) if self.send_button['state'] == 'normal' else None)

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
            try: self.chat_area.delete(self.indicator_dots_start_index, tk.END + "-1l")
            except tk.TclError: pass
            self.chat_area.config(state='disabled')
            if self.current_indicator_job:
                self.master.after_cancel(self.current_indicator_job)
                self.current_indicator_job = None
            return

        self.chat_area.config(state='normal')
        try: self.chat_area.delete(self.indicator_dots_start_index, tk.END + "-1l")
        except tk.TclError: pass 
        
        dots = "." * ((dot_count % 3) + 1)
        try: self.chat_area.insert(self.indicator_dots_start_index, dots, ("bot_block", "bot_typing_indicator"))
        except tk.TclError: pass
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)
        
        self.current_indicator_job = self.master.after(self.INDICATOR_ANIM_SPEED_MS, lambda: self._animate_typing_indicator(dot_count + 1))

    def _begin_actual_typing(self, full_message_text):
        self.stop_indicator_animation = True
        if self.current_indicator_job:
             self.master.after_cancel(self.current_indicator_job)
             self.current_indicator_job = None
        self.chat_area.config(state='normal')
        try: self.chat_area.delete(self.indicator_dots_start_index, tk.END + "-1l")
        except tk.TclError: pass

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
        self.add_message_to_chat_immediately("Bot", "Hello! I'm your PPL (Principles of Programming Languages) Chatbot.", "bot_initial")
        self.add_message_to_chat_immediately(None, "Please select a topic you're interested in by typing its letter (e.g., A, B,...)\nor ask a question like 'What is [topic]?' or 'Example of [topic]'.", "bot_instruction")

        for option_char, topic_title_key in self.initial_display_options.items():
            kb_entry = self.knowledge_base.get(topic_title_key, {})
            desc_text = kb_entry.get("description", "Unknown Topic")
            topic_display_name = desc_text.split(":")[0].strip()
            if len(topic_display_name) > 50 :
                topic_display_name = topic_display_name[:47] + "..."
            self.add_message_to_chat_immediately(None, (option_char, topic_display_name), "bot_option")

        self.add_message_to_chat_immediately(None, "\nType 'exit' or 'quit' to end.", "bot_instruction")

    def send_message(self):
        if self.bot_is_processing: return
        user_text_original = self.input_field.get()
        if not user_text_original.strip():
            return

        self.add_message_to_chat_immediately("You", user_text_original, "user")
        self.input_field.delete(0, tk.END)

        if user_text_original.lower() in ['exit', 'quit', 'bye']:
            self._start_bot_processing("Goodbye! Have a great day.")
            self.master.after(self.THINKING_TIME_MS + len("Goodbye! Have a great day.") * self.TYPING_SPEED_MS + 1000, self.master.destroy)
            return

        intent, topic_key, extracted_entities = process_nlp_input(user_text_original, self.knowledge_base, self.initial_display_options)
        bot_response = ""

        if intent and topic_key:
            if topic_key in self.knowledge_base:
                topic_data = self.knowledge_base[topic_key]
                if intent == "ask_definition":
                    bot_response = topic_data.get("description", f"Sorry, I don't have a detailed description for {topic_key}.")
                elif intent == "ask_example":
                    bot_response = topic_data.get("example", f"Sorry, I don't have an example for {topic_key} right now.")
                elif intent == "ask_pros":
                    pros_list = topic_data.get("pros", [])
                    if pros_list: bot_response = f"Advantages of {topic_key}:\n- " + "\n- ".join(pros_list)
                    else: bot_response = f"I don't have a list of advantages for {topic_key} yet."
                elif intent == "ask_cons":
                    cons_list = topic_data.get("cons", [])
                    if cons_list: bot_response = f"Disadvantages of {topic_key}:\n- " + "\n- ".join(cons_list)
                    else: bot_response = f"I don't have a list of disadvantages for {topic_key} yet."
                elif intent == "ask_related":
                    related_list = topic_data.get("related_topics", [])
                    if related_list: bot_response = f"Topics related to {topic_key} include: {', '.join(related_list)}. You can ask me about them!"
                    else: bot_response = f"I don't have specific related topics listed for {topic_key} at the moment."
                else:
                    bot_response = topic_data.get("description", f"I have some information on {topic_key}, but I'm not sure about that specific question.")
            else:
                primary_entity_display = extracted_entities[0] if extracted_entities else "something"
                bot_response = f"I think you're asking about '{primary_entity_display}', but I don't have information on that specific topic."
        else:
            if not topic_key and extracted_entities:
                 bot_response = f"I see you mentioned '{extracted_entities[0]}'. Could you be more specific or choose from the list?"
            elif not topic_key:
                 bot_response = "I'm sorry, I didn't quite understand that. Could you try rephrasing or choosing from the list (e.g., A, B)?"
            elif topic_key and not intent:
                 bot_response = f"I see you mentioned {topic_key}. What would you like to know about it? (e.g., definition, example, pros, cons)"

        if not bot_response:
            bot_response = "I'm having a little trouble understanding. Please try asking in a different way or select an option from the list."
        
        self._start_bot_processing(bot_response)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApplication(root, get_user_choice_antlr, initial_display_options, knowledge_base_ppl)
    root.mainloop()