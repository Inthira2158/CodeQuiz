"""
seed_data.py - Populates CodeQuiz with comprehensive programming questions,
topics, achievements, and realistic leaderboard demo data.
"""

import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'codequiz.db')

TOPICS = [
    {
        'slug': 'python',
        'name': 'Python',
        'description': 'Core syntax, list comprehensions, OOP, decorators, generators, and data structures.',
        'icon': 'fa-brands fa-python',
        'color': '#3776AB',
        'gradient': 'linear-gradient(135deg, #3776AB 0%, #FFD43B 100%)',
        'code_lang': 'python'
    },
    {
        'slug': 'java',
        'name': 'Java',
        'description': 'Object-Oriented Programming, collections, streams, memory management, and threads.',
        'icon': 'fa-brands fa-java',
        'color': '#ED8B00',
        'gradient': 'linear-gradient(135deg, #E76F00 0%, #5382A1 100%)',
        'code_lang': 'java'
    },
    {
        'slug': 'sql',
        'name': 'SQL',
        'description': 'Database queries, relational JOINs, aggregations, subqueries, and indexing.',
        'icon': 'fa-solid fa-database',
        'color': '#00758F',
        'gradient': 'linear-gradient(135deg, #00758F 0%, #F29111 100%)',
        'code_lang': 'sql'
    },
    {
        'slug': 'html',
        'name': 'HTML',
        'description': 'Semantic markup, modern HTML5 elements, accessibility, forms, and document structure.',
        'icon': 'fa-brands fa-html5',
        'color': '#E34F26',
        'gradient': 'linear-gradient(135deg, #E34F26 0%, #F06529 100%)',
        'code_lang': 'html'
    },
    {
        'slug': 'css',
        'name': 'CSS',
        'description': 'Flexbox, CSS Grid, responsive design, animations, specificity, and modern layouts.',
        'icon': 'fa-brands fa-css3-alt',
        'color': '#1572B6',
        'gradient': 'linear-gradient(135deg, #1572B6 0%, #33A9DC 100%)',
        'code_lang': 'css'
    },
    {
        'slug': 'javascript',
        'name': 'JavaScript',
        'description': 'ES6+ modern features, async/await, closures, prototypes, DOM, and event loop.',
        'icon': 'fa-brands fa-js',
        'color': '#F7DF1E',
        'gradient': 'linear-gradient(135deg, #F7DF1E 0%, #E5A823 100%)',
        'code_lang': 'javascript'
    }
]

ACHIEVEMENTS = [
    {
        'slug': 'first_blood',
        'title': 'First Steps',
        'description': 'Complete your first quiz on CodeQuiz.',
        'icon': 'fa-solid fa-play',
        'badge_color': 'primary',
        'points': 50
    },
    {
        'slug': 'flawless_victory',
        'title': 'Flawless Victory',
        'description': 'Score a perfect 100% on any topic quiz.',
        'icon': 'fa-solid fa-trophy',
        'badge_color': 'warning',
        'points': 150
    },
    {
        'slug': 'speed_demon',
        'title': 'Speed Demon',
        'description': 'Complete a quiz in under 60 seconds with at least 80% accuracy.',
        'icon': 'fa-solid fa-bolt',
        'badge_color': 'danger',
        'points': 100
    },
    {
        'slug': 'polyglot',
        'title': 'The Polyglot',
        'description': 'Attempt quizzes across 3 or more different programming topics.',
        'icon': 'fa-solid fa-globe',
        'badge_color': 'info',
        'points': 120
    },
    {
        'slug': 'grandmaster',
        'title': 'Grandmaster',
        'description': 'Accumulate over 500 total points on the platform.',
        'icon': 'fa-solid fa-crown',
        'badge_color': 'warning',
        'points': 200
    },
    {
        'slug': 'pythonista',
        'title': 'True Pythonista',
        'description': 'Achieve 80%+ score on an Advanced Python quiz.',
        'icon': 'fa-brands fa-python',
        'badge_color': 'success',
        'points': 80
    },
    {
        'slug': 'sql_ninja',
        'title': 'SQL Query Ninja',
        'description': 'Complete an SQL quiz with zero mistakes.',
        'icon': 'fa-solid fa-database',
        'badge_color': 'primary',
        'points': 80
    }
]

QUESTIONS = [
    # ==========================================
    # PYTHON QUESTIONS
    # ==========================================
    {
        'topic_slug': 'python',
        'difficulty': 'Beginner',
        'question_text': 'What is the output of the following list slice operation in Python?',
        'code_snippet': 'numbers = [10, 20, 30, 40, 50]\nprint(numbers[1:4])',
        'code_lang': 'python',
        'option_a': '[10, 20, 30]',
        'option_b': '[20, 30, 40]',
        'option_c': '[20, 30, 40, 50]',
        'option_d': '[10, 20, 30, 40]',
        'correct_option': 'B',
        'explanation': 'Slicing syntax [start:stop] is zero-indexed and exclusive of the stop index. Index 1 is 20, index 2 is 30, index 3 is 40. Index 4 (50) is excluded.'
    },
    {
        'topic_slug': 'python',
        'difficulty': 'Beginner',
        'question_text': 'Which keyword is used in Python to define an anonymous / inline function?',
        'code_snippet': 'multiply = _____ x, y: x * y\nprint(multiply(3, 4))',
        'code_lang': 'python',
        'option_a': 'def',
        'option_b': 'inline',
        'option_c': 'lambda',
        'option_d': 'func',
        'correct_option': 'C',
        'explanation': 'In Python, anonymous one-line functions are defined using the `lambda` keyword.'
    },
    {
        'topic_slug': 'python',
        'difficulty': 'Intermediate',
        'question_text': 'What does the following list comprehension evaluate to?',
        'code_snippet': 'matrix = [[1, 2], [3, 4]]\nflat = [val for row in matrix for val in row if val % 2 == 0]\nprint(flat)',
        'code_lang': 'python',
        'option_a': '[1, 3]',
        'option_b': '[2, 4]',
        'option_c': '[[2], [4]]',
        'option_d': '[1, 2, 3, 4]',
        'correct_option': 'B',
        'explanation': 'The nested comprehension flattens the matrix into values 1, 2, 3, 4, then the filter `if val % 2 == 0` keeps only even numbers [2, 4].'
    },
    {
        'topic_slug': 'python',
        'difficulty': 'Intermediate',
        'question_text': 'What will be printed by this dictionary update code?',
        'code_snippet': 'd = {"a": 1}\nd.setdefault("a", 100)\nd.setdefault("b", 200)\nprint(d["a"], d["b"])',
        'code_lang': 'python',
        'option_a': '100 200',
        'option_b': '1 200',
        'option_c': '1 None',
        'option_d': 'KeyError',
        'correct_option': 'B',
        'explanation': '`setdefault(key, default)` returns the key value if the key is already in the dictionary without modifying it. If the key is not found, it sets key to default. Thus, "a" stays 1 and "b" becomes 200.'
    },
    {
        'topic_slug': 'python',
        'difficulty': 'Advanced',
        'question_text': 'What will be output when using a mutable default argument in Python?',
        'code_snippet': 'def append_item(val, items=[]):\n    items.append(val)\n    return items\n\nprint(append_item(1))\nprint(append_item(2))',
        'code_lang': 'python',
        'option_a': '[1] then [2]',
        'option_b': '[1] then [1, 2]',
        'option_c': '[1, 2] then [1, 2]',
        'option_d': 'TypeError',
        'correct_option': 'B',
        'explanation': 'Default arguments in Python are evaluated once when the function definition is executed, not at each call. Hence, the same list instance is reused across invocations, resulting in [1] and [1, 2].'
    },
    {
        'topic_slug': 'python',
        'difficulty': 'Advanced',
        'question_text': 'What does `yield` do in a Python generator function?',
        'code_snippet': 'def counter():\n    yield 1\n    yield 2',
        'code_lang': 'python',
        'option_a': 'Terminates execution and discards the function state',
        'option_b': 'Pauses function execution, yielding a value, and saves state for the next call',
        'option_c': 'Creates an asynchronous subprocess thread',
        'option_d': 'Converts the output into a JSON serialized object',
        'correct_option': 'B',
        'explanation': '`yield` suspends the generator function execution, yields the specified value to the caller, and remembers all local variables so execution resumes right after the yield when `next()` is called.'
    },
    {
        'topic_slug': 'python',
        'difficulty': 'Beginner',
        'question_text': 'Which of the following data types in Python is IMMUTABLE?',
        'code_snippet': '# Python Built-in Collections',
        'code_lang': 'python',
        'option_a': 'list',
        'option_b': 'set',
        'option_c': 'tuple',
        'option_d': 'dict',
        'correct_option': 'C',
        'explanation': 'Tuples (along with strings, ints, floats, and frozensets) are immutable. Lists, sets, and dictionaries can have their contents modified in-place.'
    },
    {
        'topic_slug': 'python',
        'difficulty': 'Intermediate',
        'question_text': 'What is the purpose of the `*args` and `**kwargs` syntax in Python function signatures?',
        'code_snippet': 'def custom_func(*args, **kwargs):\n    pass',
        'code_lang': 'python',
        'option_a': 'To enforce static typing on arguments',
        'option_b': 'To accept variable positional arguments (tuple) and keyword arguments (dictionary)',
        'option_c': 'To define private instance attributes',
        'option_d': 'To specify memory pointer addresses',
        'correct_option': 'B',
        'explanation': '`*args` gathers arbitrary positional arguments into a tuple, while `**kwargs` collects arbitrary keyword arguments into a dictionary.'
    },
    {
        'topic_slug': 'python',
        'difficulty': 'Advanced',
        'question_text': 'What is the output of this decorator wrapper execution?',
        'code_snippet': 'def deco(func):\n    def wrapper(*args):\n        return func(*args).upper()\n    return wrapper\n\n@deco\ndef greet(name):\n    return f"hello {name}"\n\nprint(greet("alice"))',
        'code_lang': 'python',
        'option_a': 'hello alice',
        'option_b': 'HELLO ALICE',
        'option_c': 'deco: hello alice',
        'option_d': 'AttributeError',
        'correct_option': 'B',
        'explanation': 'The decorator wraps `greet`, intercepts its return string "hello alice", and applies `.upper()` returning "HELLO ALICE".'
    },
    {
        'topic_slug': 'python',
        'difficulty': 'Beginner',
        'question_text': 'What does `bool([])` evaluate to in Python?',
        'code_snippet': 'result = bool([])\nprint(result)',
        'code_lang': 'python',
        'option_a': 'True',
        'option_b': 'False',
        'option_c': 'None',
        'option_d': 'TypeError',
        'correct_option': 'B',
        'explanation': 'In Python, empty collections (empty list `[]`, dict `{}`, tuple `()`, set, string `""`) are considered falsy, evaluating to `False`.'
    },
    {
        'topic_slug': 'python',
        'difficulty': 'Intermediate',
        'question_text': 'Which built-in module provides heap-based priority queue implementation in Python?',
        'code_snippet': 'import heapq\n# heapq.heappush, heapq.heappop',
        'code_lang': 'python',
        'option_a': 'queue',
        'option_b': 'heapq',
        'option_c': 'collections',
        'option_d': 'priority',
        'correct_option': 'B',
        'explanation': '`heapq` provides min-heap operations (heappush, heappop, heapify) over standard Python lists.'
    },
    {
        'topic_slug': 'python',
        'difficulty': 'Advanced',
        'question_text': 'What is the difference between `is` and `==` in Python?',
        'code_snippet': 'a = [1, 2, 3]\nb = [1, 2, 3]\nprint(a == b, a is b)',
        'code_lang': 'python',
        'option_a': '`==` checks identity; `is` checks equality',
        'option_b': '`==` checks equality of values; `is` checks reference identity in memory',
        'option_c': 'There is no difference; they are aliases',
        'option_d': '`is` only works on primitives like integers',
        'correct_option': 'B',
        'explanation': '`==` tests if values are equivalent (value equality), whereas `is` tests whether both variables point to the exact same object in memory (`id(a) == id(b)`).'
    },

    # ==========================================
    # JAVA QUESTIONS
    # ==========================================
    {
        'topic_slug': 'java',
        'difficulty': 'Beginner',
        'question_text': 'What is the default value of an uninitialized boolean instance variable in Java?',
        'code_snippet': 'public class Test {\n    boolean flag;\n}',
        'code_lang': 'java',
        'option_a': 'true',
        'option_b': 'false',
        'option_c': 'null',
        'option_d': '0',
        'correct_option': 'B',
        'explanation': 'In Java, instance boolean variables default to `false` when not explicitly initialized.'
    },
    {
        'topic_slug': 'java',
        'difficulty': 'Beginner',
        'question_text': 'Which keyword is used to prevent a method from being overridden by subclasses?',
        'code_snippet': 'public _____ void secureAction() {\n    // cannot be overridden\n}',
        'code_lang': 'java',
        'option_a': 'static',
        'option_b': 'abstract',
        'option_c': 'final',
        'option_d': 'const',
        'correct_option': 'C',
        'explanation': 'The `final` keyword when applied to a method prevents subclasses from overriding it.'
    },
    {
        'topic_slug': 'java',
        'difficulty': 'Intermediate',
        'question_text': 'What is the output of the following String comparison in Java?',
        'code_snippet': 'String s1 = "Hello";\nString s2 = new String("Hello");\nSystem.out.println((s1 == s2) + " " + s1.equals(s2));',
        'code_lang': 'java',
        'option_a': 'true true',
        'option_b': 'false false',
        'option_c': 'false true',
        'option_d': 'true false',
        'correct_option': 'C',
        'explanation': '`s1 == s2` evaluates to false because `new String()` allocates a new object on the heap outside the String pool. `s1.equals(s2)` evaluates to true because their character contents are identical.'
    },
    {
        'topic_slug': 'java',
        'difficulty': 'Intermediate',
        'question_text': 'Which Java Collection implementation ensures unique elements and maintains insertion order?',
        'code_snippet': 'Set<String> set = new _____<>();',
        'code_lang': 'java',
        'option_a': 'HashSet',
        'option_b': 'TreeSet',
        'option_c': 'LinkedHashSet',
        'option_d': 'ArrayList',
        'correct_option': 'C',
        'explanation': '`LinkedHashSet` maintains a doubly-linked list through all its entries, guaranteeing elements are stored uniquely and iterated in the order they were inserted.'
    },
    {
        'topic_slug': 'java',
        'difficulty': 'Advanced',
        'question_text': 'What does Java 8 Stream `.filter().map().reduce()` do in this code?',
        'code_snippet': 'List<Integer> nums = Arrays.asList(1, 2, 3, 4, 5);\nint result = nums.stream()\n    .filter(n -> n % 2 != 0)\n    .map(n -> n * 2)\n    .reduce(0, Integer::sum);\nSystem.out.println(result);',
        'code_lang': 'java',
        'option_a': '18',
        'option_b': '12',
        'option_c': '20',
        'option_d': '9',
        'correct_option': 'A',
        'explanation': 'Odd numbers are 1, 3, 5. Doubling them gives 2, 6, 10. Summing them (2 + 6 + 10) yields 18.'
    },
    {
        'topic_slug': 'java',
        'difficulty': 'Advanced',
        'question_text': 'What is the purpose of the `volatile` keyword in Java multi-threading?',
        'code_snippet': 'private volatile boolean running = true;',
        'code_lang': 'java',
        'option_a': 'Locks the variable with an atomic synchronized monitor',
        'option_b': 'Guarantees that reads and writes are always read directly from main memory rather than thread CPU caches',
        'option_c': 'Prevents garbage collection from cleaning the object',
        'option_d': 'Makes the variable immutable across all threads',
        'correct_option': 'B',
        'explanation': '`volatile` ensures visibility of changes to variables across threads by forcing reads and writes directly to main memory, avoiding CPU cache staleness.'
    },
    {
        'topic_slug': 'java',
        'difficulty': 'Beginner',
        'question_text': 'Which of these is NOT a primitive data type in Java?',
        'code_snippet': '// Java Types',
        'code_lang': 'java',
        'option_a': 'byte',
        'option_b': 'int',
        'option_c': 'String',
        'option_d': 'float',
        'correct_option': 'C',
        'explanation': '`String` is a reference class type in Java, whereas `byte`, `int`, and `float` are primitives.'
    },
    {
        'topic_slug': 'java',
        'difficulty': 'Intermediate',
        'question_text': 'What happens if you do NOT provide an explicit constructor in a Java class?',
        'code_snippet': 'public class User {\n    private String name;\n}',
        'code_lang': 'java',
        'option_a': 'The code fails to compile',
        'option_b': 'The Java compiler automatically provides a default no-argument constructor',
        'option_c': 'The class can only be instantiated via static factory methods',
        'option_d': 'The compiler creates a constructor requiring arguments for all fields',
        'correct_option': 'B',
        'explanation': 'If no constructor is explicitly declared, the Java compiler creates a default public no-argument constructor.'
    },
    {
        'topic_slug': 'java',
        'difficulty': 'Advanced',
        'question_text': 'How does `ConcurrentHashMap` achieve high concurrency compared to `Hashtable`?',
        'code_snippet': 'Map<String, String> map = new ConcurrentHashMap<>();',
        'code_lang': 'java',
        'option_a': 'It locks the entire table on every read and write operation',
        'option_b': 'It uses bucket-level locking (CAS operations and synchronized on tree/node bins) instead of locking the entire map',
        'option_c': 'It spawns a background thread per key access',
        'option_d': 'It stores all entries in flat unmodifiable arrays',
        'correct_option': 'B',
        'explanation': '`ConcurrentHashMap` allows concurrent reads without locking and uses fine-grained node-level synchronization and Compare-And-Swap (CAS) instructions rather than locking the entire data structure.'
    },
    {
        'topic_slug': 'java',
        'difficulty': 'Beginner',
        'question_text': 'Which access modifier allows access only within the same class?',
        'code_snippet': 'public class Bank {\n    _____ double balance;\n}',
        'code_lang': 'java',
        'option_a': 'protected',
        'option_b': 'public',
        'option_c': 'private',
        'option_d': 'default (package-private)',
        'correct_option': 'C',
        'explanation': '`private` specifies that members are only accessible within the body of the declaring class.'
    },
    {
        'topic_slug': 'java',
        'difficulty': 'Intermediate',
        'question_text': 'Which interface in Java is a Functional Interface suitable for lambdas taking 1 argument and returning a boolean?',
        'code_snippet': '// java.util.function',
        'code_lang': 'java',
        'option_a': 'Consumer<T>',
        'option_b': 'Supplier<T>',
        'option_c': 'Predicate<T>',
        'option_d': 'Function<T, R>',
        'correct_option': 'C',
        'explanation': '`Predicate<T>` represents a boolean-valued function of one argument with the abstract method `boolean test(T t)`.'
    },
    {
        'topic_slug': 'java',
        'difficulty': 'Advanced',
        'question_text': 'What is the output of this code with inheritance and polymorphism?',
        'code_snippet': 'class Parent {\n    void print() { System.out.print("P "); }\n}\nclass Child extends Parent {\n    void print() { System.out.print("C "); }\n}\nParent obj = new Child();\nobj.print();',
        'code_lang': 'java',
        'option_a': 'P',
        'option_b': 'C',
        'option_c': 'P C',
        'option_d': 'Compilation Error',
        'correct_option': 'B',
        'explanation': 'In Java, non-static methods are resolved at runtime based on the actual object type (`Child`), dynamic method dispatch invokes the overridden `Child.print()`.'
    },

    # ==========================================
    # SQL QUESTIONS
    # ==========================================
    {
        'topic_slug': 'sql',
        'difficulty': 'Beginner',
        'question_text': 'Which clause is used in SQL to filter rows before any groupings are applied?',
        'code_snippet': 'SELECT department, AVG(salary)\nFROM employees\n_____ status = "Active"\nGROUP BY department;',
        'code_lang': 'sql',
        'option_a': 'HAVING',
        'option_b': 'WHERE',
        'option_c': 'FILTER',
        'option_d': 'ORDER BY',
        'correct_option': 'B',
        'explanation': '`WHERE` filters individual rows before aggregation. `HAVING` is applied after `GROUP BY` to filter aggregated groups.'
    },
    {
        'topic_slug': 'sql',
        'difficulty': 'Beginner',
        'question_text': 'What SQL command is used to remove all records from a table without deleting the table structure?',
        'code_snippet': '_____ TABLE employees;',
        'code_lang': 'sql',
        'option_a': 'DROP',
        'option_b': 'TRUNCATE',
        'option_c': 'ALTER',
        'option_d': 'REMOVE',
        'correct_option': 'B',
        'explanation': '`TRUNCATE TABLE` empties all rows from a table while keeping the table definition and schema intact.'
    },
    {
        'topic_slug': 'sql',
        'difficulty': 'Intermediate',
        'question_text': 'What is the key difference between INNER JOIN and LEFT JOIN?',
        'code_snippet': 'SELECT u.name, o.id\nFROM users u\nLEFT JOIN orders o ON u.id = o.user_id;',
        'code_lang': 'sql',
        'option_a': 'INNER JOIN returns all rows from left table; LEFT JOIN only matching rows',
        'option_b': 'LEFT JOIN returns all rows from left table plus matching rows from right; unmatched right fields are NULL',
        'option_c': 'LEFT JOIN automatically sorts results in ascending order',
        'option_d': 'There is no difference in standard SQL',
        'correct_option': 'B',
        'explanation': '`LEFT JOIN` returns every row from the left table regardless of whether there is a match in the right table. Non-matching columns from the right table are filled with `NULL`.'
    },
    {
        'topic_slug': 'sql',
        'difficulty': 'Intermediate',
        'question_text': 'What is the output of COUNT(column_name) vs COUNT(*)?',
        'code_snippet': '-- employees has 10 rows, but bonus is NULL in 3 rows\nSELECT COUNT(*), COUNT(bonus) FROM employees;',
        'code_lang': 'sql',
        'option_a': '10 and 10',
        'option_b': '10 and 7',
        'option_c': '7 and 7',
        'option_d': '7 and 10',
        'correct_option': 'B',
        'explanation': '`COUNT(*)` counts total rows including NULLs (10), while `COUNT(column_name)` ignores NULL values in that specific column (10 - 3 = 7).'
    },
    {
        'topic_slug': 'sql',
        'difficulty': 'Advanced',
        'question_text': 'Which SQL window function assigns a unique sequential integer to rows without gaps, even when values are identical?',
        'code_snippet': 'SELECT id, salary,\n       _____ OVER (ORDER BY salary DESC) AS pos\nFROM employees;',
        'code_lang': 'sql',
        'option_a': 'RANK()',
        'option_b': 'DENSE_RANK()',
        'option_c': 'ROW_NUMBER()',
        'option_d': 'NTILE()',
        'correct_option': 'C',
        'explanation': '`ROW_NUMBER()` always assigns a strictly unique sequential integer starting from 1 with no ties or duplicates.'
    },
    {
        'topic_slug': 'sql',
        'difficulty': 'Advanced',
        'question_text': 'What is a Correlated Subquery in SQL?',
        'code_snippet': 'SELECT e1.name, e1.salary\nFROM employees e1\nWHERE e1.salary > (\n    SELECT AVG(e2.salary)\n    FROM employees e2\n    WHERE e2.dept_id = e1.dept_id\n);',
        'code_lang': 'sql',
        'option_a': 'A subquery that executes once before the outer query runs',
        'option_b': 'A subquery that references columns from the outer query and re-evaluates for each outer row',
        'option_c': 'A subquery that runs in parallel across multiple CPU cores',
        'option_d': 'A subquery that only returns scalar booleans',
        'correct_option': 'B',
        'explanation': 'A correlated subquery references columns from the enclosing query (e.g. `e1.dept_id`) and must be evaluated repeatedly for each candidate row processed by the outer query.'
    },
    {
        'topic_slug': 'sql',
        'difficulty': 'Beginner',
        'question_text': 'Which keyword is used to eliminate duplicate rows from the query output?',
        'code_snippet': 'SELECT _____ country FROM customers;',
        'code_lang': 'sql',
        'option_a': 'UNIQUE',
        'option_b': 'DISTINCT',
        'option_c': 'FILTERED',
        'option_d': 'GROUP',
        'correct_option': 'B',
        'explanation': '`SELECT DISTINCT` removes duplicate rows from the result set, returning only unique values.'
    },
    {
        'topic_slug': 'sql',
        'difficulty': 'Intermediate',
        'question_text': 'What is the purpose of the HAVING clause in SQL?',
        'code_snippet': 'SELECT dept_id, COUNT(*)\nFROM employees\nGROUP BY dept_id\n_____ COUNT(*) > 5;',
        'code_lang': 'sql',
        'option_a': 'To filter records before aggregation',
        'option_b': 'To filter grouped records based on aggregate functions',
        'option_c': 'To specify primary key constraints',
        'option_d': 'To sort rows in ascending order',
        'correct_option': 'B',
        'explanation': '`HAVING` filters results after the `GROUP BY` clause has aggregated the rows, enabling conditions on aggregate functions like `COUNT(*)`, `SUM()`, or `AVG()`.'
    },
    {
        'topic_slug': 'sql',
        'difficulty': 'Advanced',
        'question_text': 'Which index type is best suited for equality lookups on high-cardinality primary keys in relational databases?',
        'code_snippet': 'CREATE INDEX idx_user_id ON users(user_id);',
        'code_lang': 'sql',
        'option_a': 'Bitmap Index',
        'option_b': 'B-Tree Index',
        'option_c': 'Full-Text Index',
        'option_d': 'Spatial R-Tree Index',
        'correct_option': 'B',
        'explanation': 'B-Tree (Balanced Tree) is the default and most efficient general-purpose index for range and equality lookups on high-cardinality keys.'
    },
    {
        'topic_slug': 'sql',
        'difficulty': 'Beginner',
        'question_text': 'What wildcard character matches zero or more characters in an SQL `LIKE` operator?',
        'code_snippet': 'SELECT * FROM users WHERE email LIKE "%@gmail.com";',
        'code_lang': 'sql',
        'option_a': '*',
        'option_b': '%',
        'option_c': '_',
        'option_d': '?',
        'correct_option': 'B',
        'explanation': 'In SQL `LIKE` patterns, `%` represents zero or more characters, while `_` represents exactly one single character.'
    },
    {
        'topic_slug': 'sql',
        'difficulty': 'Intermediate',
        'question_text': 'What does ACID stand for in database management systems?',
        'code_snippet': '-- Transaction Properties',
        'code_lang': 'sql',
        'option_a': 'Atomicity, Consistency, Isolation, Durability',
        'option_b': 'Accuracy, Completeness, Integrity, Dependability',
        'option_c': 'Association, Concurrency, Indexing, Decoupling',
        'option_d': 'Allocation, Cache, Iteration, Data',
        'correct_option': 'A',
        'explanation': 'ACID guarantees database transactions are processed reliably: Atomicity, Consistency, Isolation, and Durability.'
    },
    {
        'topic_slug': 'sql',
        'difficulty': 'Advanced',
        'question_text': 'What happens if you perform a `UNION` vs a `UNION ALL` between two queries?',
        'code_snippet': 'SELECT id FROM tableA\nUNION\nSELECT id FROM tableB;',
        'code_lang': 'sql',
        'option_a': '`UNION` retains duplicates; `UNION ALL` strips duplicates',
        'option_b': '`UNION` strips duplicate rows (distinct); `UNION ALL` preserves all rows including duplicates and is faster',
        'option_c': '`UNION` joins columns horizontally; `UNION ALL` stacks vertically',
        'option_d': '`UNION ALL` throws an error if schemas differ by column names',
        'correct_option': 'B',
        'explanation': '`UNION` performs an implicit `DISTINCT` sort operation to eliminate duplicates, whereas `UNION ALL` simply concatenates both result sets directly without sorting.'
    },

    # ==========================================
    # HTML QUESTIONS
    # ==========================================
    {
        'topic_slug': 'html',
        'difficulty': 'Beginner',
        'question_text': 'Which semantic HTML5 tag represents independent, self-contained content such as a blog post or news story?',
        'code_snippet': '<_____>\n  <h2>Breaking Tech News</h2>\n  <p>Details here...</p>\n</_____>',
        'code_lang': 'html',
        'option_a': '<section>',
        'option_b': '<article>',
        'option_c': '<aside>',
        'option_d': '<div>',
        'correct_option': 'B',
        'explanation': 'The `<article>` element represents a complete, self-contained composition in a document, page, application, or site that is independently distributable or reusable.'
    },
    {
        'topic_slug': 'html',
        'difficulty': 'Beginner',
        'question_text': 'What attribute on an `<input>` field makes it mandatory for the user before form submission?',
        'code_snippet': '<input type="email" name="user_email" _____>',
        'code_lang': 'html',
        'option_a': 'validate',
        'option_b': 'mandatory',
        'option_c': 'required',
        'option_d': 'strict',
        'correct_option': 'C',
        'explanation': 'The boolean attribute `required` specifies that an input field must be filled out before submitting the form.'
    },
    {
        'topic_slug': 'html',
        'difficulty': 'Intermediate',
        'question_text': 'What is the purpose of the `<meta name="viewport" content="...">` tag in HTML documents?',
        'code_snippet': '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        'code_lang': 'html',
        'option_a': 'Sets browser cookie policies',
        'option_b': 'Controls the layout viewport dimensions and scaling on mobile devices for responsiveness',
        'option_c': 'Pre-renders search engine snippets',
        'option_d': 'Locks the screen orientation to portrait mode only',
        'correct_option': 'B',
        'explanation': 'The viewport meta tag informs the mobile browser how to adjust the dimensions and scaling of the page to match the device screen width.'
    },
    {
        'topic_slug': 'html',
        'difficulty': 'Intermediate',
        'question_text': 'Which tag should be used to display preformatted programming code preserving whitespace and line breaks?',
        'code_snippet': '<_____><code>console.log("Hello\nWorld");</code></_____>',
        'code_lang': 'html',
        'option_a': '<pre>',
        'option_b': '<format>',
        'option_c': '<block>',
        'option_d': '<span>',
        'correct_option': 'A',
        'explanation': 'The `<pre>` element displays text in a fixed-width font exactly as written in the HTML source, preserving spaces and line breaks.'
    },
    {
        'topic_slug': 'html',
        'difficulty': 'Advanced',
        'question_text': 'What is the key difference between `<canvas>` and `<svg>` in HTML5?',
        'code_snippet': '<!-- Canvas vs SVG -->',
        'code_lang': 'html',
        'option_a': '`<canvas>` is vector-based; `<svg>` is pixel/raster-based',
        'option_b': '`<canvas>` renders via raster pixel scripts (immediate mode); `<svg>` renders XML-based vector shapes retained in the DOM',
        'option_c': '`<svg>` cannot be styled with CSS, whereas `<canvas>` can',
        'option_d': '`<canvas>` works only in Chrome; `<svg>` works in all browsers',
        'correct_option': 'B',
        'explanation': '`<canvas>` uses JavaScript to draw bitmap pixels (immediate mode graphics with no individual DOM nodes). `<svg>` describes scalable vector graphics in XML format where each shape is a separate DOM node capable of handling events and CSS styling.'
    },
    {
        'topic_slug': 'html',
        'difficulty': 'Advanced',
        'question_text': 'Which attribute improves accessibility by defining the relationship between an `<input>` and its `<label>` when not nesting?',
        'code_snippet': '<label _____="user-name">Your Name</label>\n<input type="text" id="user-name">',
        'code_lang': 'html',
        'option_a': 'target',
        'option_b': 'for',
        'option_c': 'connect',
        'option_d': 'ref',
        'correct_option': 'B',
        'explanation': 'The `for` attribute of a `<label>` must match the `id` of the related form element, binding them together for screen readers and click targeting.'
    },
    {
        'topic_slug': 'html',
        'difficulty': 'Beginner',
        'question_text': 'What does `target="_blank"` on an `<a>` tag achieve?',
        'code_snippet': '<a href="https://example.com" target="_blank">Visit</a>',
        'code_lang': 'html',
        'option_a': 'Downloads the target file directly to disk',
        'option_b': 'Opens the linked document in a new window or tab',
        'option_c': 'Opens the page in an invisible iframe',
        'option_d': 'Refreshes the current tab with clear cache',
        'correct_option': 'B',
        'explanation': '`target="_blank"` instructs the browser to open the linked destination in a new browsing context (usually a new tab).'
    },
    {
        'topic_slug': 'html',
        'difficulty': 'Intermediate',
        'question_text': 'Which HTML5 element is used to group media content together with an optional caption?',
        'code_snippet': '<_____>\n  <img src="chart.png" alt="Sales graph">\n  <figcaption>Figure 1: Quarterly Sales</figcaption>\n</_____>',
        'code_lang': 'html',
        'option_a': '<picture>',
        'option_b': '<figure>',
        'option_c': '<aside>',
        'option_d': '<media>',
        'correct_option': 'B',
        'explanation': 'The `<figure>` element encapsulates self-contained content, often with a `<figcaption>` representing a caption.'
    },
    {
        'topic_slug': 'html',
        'difficulty': 'Advanced',
        'question_text': 'What is the role of the `rel="noopener noreferrer"` attribute when using `target="_blank"`?',
        'code_snippet': '<a href="https://external.site" target="_blank" rel="noopener noreferrer">External</a>',
        'code_lang': 'html',
        'option_a': 'Speeds up image preloading on the page',
        'option_b': 'Prevents tabnabbing security attacks by ensuring `window.opener` is null and strips the Referer header',
        'option_c': 'Enforces HTTPS encryption on the destination link',
        'option_d': 'Tells search engines not to index the destination',
        'correct_option': 'B',
        'explanation': '`noopener` prevents the newly opened page from gaining access to the original page through `window.opener`, protecting against malicious tab hijacking (tabnabbing). `noreferrer` additionally suppresses the Referer HTTP header.'
    },
    {
        'topic_slug': 'html',
        'difficulty': 'Beginner',
        'question_text': 'Which HTML element represents the highest level header in a document hierarchy?',
        'code_snippet': '<_____>Platform Overview</_____>',
        'code_lang': 'html',
        'option_a': '<head>',
        'option_b': '<header>',
        'option_c': '<h1>',
        'option_d': '<h0>',
        'correct_option': 'C',
        'explanation': '`<h1>` denotes the most important / top-level heading in HTML document outlines.'
    },
    {
        'topic_slug': 'html',
        'difficulty': 'Intermediate',
        'question_text': 'Which tag is used to create a drop-down selection list in an HTML form?',
        'code_snippet': '<_____ name="language">\n  <option value="py">Python</option>\n  <option value="js">JavaScript</option>\n</_____>',
        'code_lang': 'html',
        'option_a': '<dropdown>',
        'option_b': '<list>',
        'option_c': '<select>',
        'option_d': '<picker>',
        'correct_option': 'C',
        'explanation': 'The `<select>` element is used to create a drop-down list of selectable `<option>` elements.'
    },
    {
        'topic_slug': 'html',
        'difficulty': 'Advanced',
        'question_text': 'What does the `defer` attribute do when loading external scripts in HTML?',
        'code_snippet': '<script src="app.js" defer></script>',
        'code_lang': 'html',
        'option_a': 'Loads and executes the script immediately, blocking HTML parsing',
        'option_b': 'Downloads the script asynchronously in parallel with HTML parsing, but executes only after HTML parsing is complete and preserves script execution order',
        'option_c': 'Delays execution until the user clicks on the page',
        'option_d': 'Prevents the script from executing if cookies are disabled',
        'correct_option': 'B',
        'explanation': '`defer` downloads the script in the background without blocking DOM parsing, then executes it in source order after the document has been fully parsed (just before DOMContentLoaded).'
    },

    # ==========================================
    # CSS QUESTIONS
    # ==========================================
    {
        'topic_slug': 'css',
        'difficulty': 'Beginner',
        'question_text': 'In the standard CSS Box Model, which layer is located immediately outside the padding?',
        'code_snippet': '/* CSS Box Model */\n.card {\n    margin: 10px;\n    border: 2px solid #333;\n    padding: 15px;\n}',
        'code_lang': 'css',
        'option_a': 'Margin',
        'option_b': 'Content',
        'option_c': 'Border',
        'option_d': 'Outline',
        'correct_option': 'C',
        'explanation': 'From inside out: Content -> Padding -> Border -> Margin. Border sits directly outside Padding.'
    },
    {
        'topic_slug': 'css',
        'difficulty': 'Beginner',
        'question_text': 'Which property is used in CSS Flexbox to align flex items along the main axis?',
        'code_snippet': '.container {\n    display: flex;\n    _____: center;\n}',
        'code_lang': 'css',
        'option_a': 'align-items',
        'option_b': 'justify-content',
        'option_c': 'align-content',
        'option_d': 'flex-direction',
        'correct_option': 'B',
        'explanation': '`justify-content` aligns items along the main axis (horizontal by default), while `align-items` aligns along the cross axis.'
    },
    {
        'topic_slug': 'css',
        'difficulty': 'Intermediate',
        'question_text': 'What does `box-sizing: border-box;` do in CSS?',
        'code_snippet': '* {\n    box-sizing: border-box;\n}',
        'code_lang': 'css',
        'option_a': 'Adds an extra 10px shadow to every element border',
        'option_b': 'Includes padding and border within the specified width and height of an element',
        'option_c': 'Calculates margins from the window viewport boundary',
        'option_d': 'Restricts boxes to square aspect ratios',
        'correct_option': 'B',
        'explanation': 'With `box-sizing: border-box`, an element’s width and height encompass its content, padding, and border, preventing layout blowouts when padding is added.'
    },
    {
        'topic_slug': 'css',
        'difficulty': 'Intermediate',
        'question_text': 'Which CSS selector has the HIGHEST specificity according to the CSS cascade rules?',
        'code_snippet': '/* Specificity hierarchy */',
        'code_lang': 'css',
        'option_a': '`div.nav-item > a`',
        'option_b': '`#main-header`',
        'option_c': '`.btn.btn-primary.active`',
        'option_d': '`header nav ul li a`',
        'correct_option': 'B',
        'explanation': 'An ID selector `#main-header` has a specificity of (1, 0, 0), which overrides any number of classes (0, 1, 0) or element tags (0, 0, 1).'
    },
    {
        'topic_slug': 'css',
        'difficulty': 'Advanced',
        'question_text': 'What is the effect of setting an element’s position to `sticky`?',
        'code_snippet': '.nav-bar {\n    position: sticky;\n    top: 0;\n}',
        'code_lang': 'css',
        'option_a': 'The element is fixed to the window bottom permanently',
        'option_b': 'The element is treated as relative until its scroll offset reaches the threshold, where it behaves like fixed within its parent container',
        'option_c': 'The element ignores flex container constraints',
        'option_d': 'The element is removed from normal flow and centered on screen',
        'correct_option': 'B',
        'explanation': '`position: sticky` toggles between relative and fixed positioning based on scroll position, sticking at the specified offset within its scrolling parent container.'
    },
    {
        'topic_slug': 'css',
        'difficulty': 'Advanced',
        'question_text': 'What does the CSS Grid declaration `grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));` achieve?',
        'code_snippet': '.grid-container {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));\n    gap: 1rem;\n}',
        'code_lang': 'css',
        'option_a': 'Creates fixed 250px columns with no responsiveness',
        'option_b': 'Creates a responsive column layout that automatically fits as many columns of at least 250px as possible without media queries',
        'option_c': 'Creates an infinite horizontal carousel',
        'option_d': 'Splits columns evenly into 4 fixed cells',
        'correct_option': 'B',
        'explanation': 'This classic responsive CSS Grid pattern automatically fits as many columns as will fit at >= 250px, expanding each fractionally (`1fr`) to fill remaining space, completely eliminating the need for media queries.'
    },
    {
        'topic_slug': 'css',
        'difficulty': 'Beginner',
        'question_text': 'Which property is used to change the text color in CSS?',
        'code_snippet': 'h1 {\n    _____: #ffffff;\n}',
        'code_lang': 'css',
        'option_a': 'font-color',
        'option_b': 'text-color',
        'option_c': 'color',
        'option_d': 'foreground',
        'correct_option': 'C',
        'explanation': 'The CSS `color` property specifies the foreground color of text content.'
    },
    {
        'topic_slug': 'css',
        'difficulty': 'Intermediate',
        'question_text': 'Which pseudo-class targets an element when the user points to it with a cursor device?',
        'code_snippet': '.button:_____ {\n    background-color: #4CAF50;\n}',
        'code_lang': 'css',
        'option_a': ':active',
        'option_b': ':focus',
        'option_c': ':hover',
        'option_d': ':visited',
        'correct_option': 'C',
        'explanation': 'The `:hover` pseudo-class applies styles when the user hovers over an element with a pointer without activating it.'
    },
    {
        'topic_slug': 'css',
        'difficulty': 'Advanced',
        'question_text': 'When does the `z-index` property take effect on an element?',
        'code_snippet': '.modal-backdrop {\n    z-index: 1050;\n}',
        'code_lang': 'css',
        'option_a': 'On any element regardless of display or position',
        'option_b': 'Only on positioned elements (position relative, absolute, fixed, sticky) or flex/grid direct children',
        'option_c': 'Only on elements that have display: inline-block',
        'option_d': 'Only when paired with transform3d',
        'correct_option': 'B',
        'explanation': '`z-index` only functions on elements that create or participate in a stacking context, requiring `position` other than `static`, or on direct children of a flex or grid container.'
    },
    {
        'topic_slug': 'css',
        'difficulty': 'Beginner',
        'question_text': 'How do you center an inline or inline-block element horizontally inside its parent container?',
        'code_snippet': '.parent {\n    _____: center;\n}',
        'code_lang': 'css',
        'option_a': 'align: center;',
        'option_b': 'margin: 0 auto;',
        'option_c': 'text-align: center;',
        'option_d': 'float: center;',
        'correct_option': 'C',
        'explanation': 'Setting `text-align: center;` on the parent container centers all nested inline and inline-block children horizontally.'
    },
    {
        'topic_slug': 'css',
        'difficulty': 'Intermediate',
        'question_text': 'What does `rem` unit represent in CSS sizing?',
        'code_snippet': 'body {\n    font-size: 16px;\n}\nh1 {\n    font-size: 2rem;\n}',
        'code_lang': 'css',
        'option_a': 'Relative to the immediate parent element’s font size',
        'option_b': 'Relative to the root (`<html>`) element’s font size',
        'option_c': 'Relative to the viewport width percentage',
        'option_d': 'Responsive em measure based on screen DPI',
        'correct_option': 'B',
        'explanation': '`rem` stands for "root em" and is always calculated relative to the font-size of the root element (`<html>`), making it more predictable than `em`.'
    },
    {
        'topic_slug': 'css',
        'difficulty': 'Advanced',
        'question_text': 'What is the purpose of the `@supports` CSS rule?',
        'code_snippet': '@supports (display: subgrid) {\n    .layout { display: subgrid; }\n}',
        'code_lang': 'css',
        'option_a': 'Detects user operating system platform',
        'option_b': 'Feature query that tests whether the browser supports a specific CSS property-value pair before applying rules',
        'option_c': 'Verifies internet bandwidth connectivity speed',
        'option_d': 'Loads polyfills for older browsers',
        'correct_option': 'B',
        'explanation': '`@supports` allows developers to perform feature queries, applying conditional CSS rules only if the rendering engine supports the declared CSS feature.'
    },

    # ==========================================
    # JAVASCRIPT QUESTIONS
    # ==========================================
    {
        'topic_slug': 'javascript',
        'difficulty': 'Beginner',
        'question_text': 'What is the output of `typeof NaN` in JavaScript?',
        'code_snippet': 'console.log(typeof NaN);',
        'code_lang': 'javascript',
        'option_a': '"undefined"',
        'option_b': '"number"',
        'option_c': '"nan"',
        'option_d': '"object"',
        'correct_option': 'B',
        'explanation': 'In JavaScript, `NaN` stands for "Not-a-Number", but according to IEEE 754 floating-point specifications, its primitive type is officially `"number"`.'
    },
    {
        'topic_slug': 'javascript',
        'difficulty': 'Beginner',
        'question_text': 'Which method creates a new array populated with the results of calling a provided function on every element in the calling array?',
        'code_snippet': 'const numbers = [1, 2, 3];\nconst doubled = numbers._____(x => x * 2);',
        'code_lang': 'javascript',
        'option_a': 'forEach',
        'option_b': 'map',
        'option_c': 'filter',
        'option_d': 'reduce',
        'correct_option': 'B',
        'explanation': '`Array.prototype.map()` creates a new transformed array containing the return value of invoking the callback on each element.'
    },
    {
        'topic_slug': 'javascript',
        'difficulty': 'Intermediate',
        'question_text': 'What will be printed to the console due to JavaScript closures?',
        'code_snippet': 'function createCounter() {\n    let count = 0;\n    return function() {\n        count++;\n        return count;\n    };\n}\nconst c1 = createCounter();\nc1();\nconsole.log(c1());',
        'code_lang': 'javascript',
        'option_a': '1',
        'option_b': '2',
        'option_c': 'undefined',
        'option_d': 'ReferenceError',
        'correct_option': 'B',
        'explanation': 'The returned inner function forms a closure over `count`. The first call `c1()` increments `count` to 1, and the second call increments it to 2 and returns 2.'
    },
    {
        'topic_slug': 'javascript',
        'difficulty': 'Intermediate',
        'question_text': 'What is the output of comparing values with `==` vs `===`?',
        'code_snippet': 'console.log(0 == false, 0 === false);',
        'code_lang': 'javascript',
        'option_a': 'true true',
        'option_b': 'false false',
        'option_c': 'true false',
        'option_d': 'false true',
        'correct_option': 'C',
        'explanation': '`0 == false` performs type coercion and evaluates to `true` (since false coerces to number 0). `0 === false` checks both value and type without coercion, yielding `false`.'
    },
    {
        'topic_slug': 'javascript',
        'difficulty': 'Advanced',
        'question_text': 'In what order will the numbers be logged by the JavaScript Event Loop?',
        'code_snippet': 'console.log(1);\nsetTimeout(() => console.log(2), 0);\nPromise.resolve().then(() => console.log(3));\nconsole.log(4);',
        'code_lang': 'javascript',
        'option_a': '1, 2, 3, 4',
        'option_b': '1, 4, 3, 2',
        'option_c': '1, 4, 2, 3',
        'option_d': '3, 1, 4, 2',
        'correct_option': 'B',
        'explanation': 'Synchronous code runs first (1, then 4). Microtasks (`Promise.then`) run next before any macrotasks (3). Finally macrotasks (`setTimeout`) in the timer queue execute (2). Output: 1, 4, 3, 2.'
    },
    {
        'topic_slug': 'javascript',
        'difficulty': 'Advanced',
        'question_text': 'What happens when `const obj = Object.freeze({ a: 1, nested: { b: 2 } });` is modified?',
        'code_snippet': 'const obj = Object.freeze({ a: 1, nested: { b: 2 } });\nobj.a = 99;\nobj.nested.b = 99;\nconsole.log(obj.a, obj.nested.b);',
        'code_lang': 'javascript',
        'option_a': '1 2',
        'option_b': '99 99',
        'option_c': '1 99',
        'option_d': 'TypeError thrown for both',
        'correct_option': 'C',
        'explanation': '`Object.freeze()` performs a shallow freeze only on the immediate top-level properties of the target object. `obj.a` cannot be mutated (remains 1), but nested child objects remain mutable unless deeply frozen, so `obj.nested.b` becomes 99.'
    },
    {
        'topic_slug': 'javascript',
        'difficulty': 'Beginner',
        'question_text': 'Which keyword declares a block-scoped variable that CANNOT be reassigned in JavaScript?',
        'code_snippet': '_____ MAX_USERS = 100;',
        'code_lang': 'javascript',
        'option_a': 'var',
        'option_b': 'let',
        'option_c': 'const',
        'option_d': 'static',
        'correct_option': 'C',
        'explanation': '`const` declares a block-scoped variable whose identifier reference cannot be reassigned.'
    },
    {
        'topic_slug': 'javascript',
        'difficulty': 'Intermediate',
        'question_text': 'What does `Array.prototype.reduce()` return in this snippet?',
        'code_snippet': 'const nums = [1, 2, 3, 4];\nconst sum = nums.reduce((acc, curr) => acc + curr, 10);\nconsole.log(sum);',
        'code_lang': 'javascript',
        'option_a': '10',
        'option_b': '20',
        'option_c': '14',
        'option_d': '24',
        'correct_option': 'B',
        'explanation': 'The initial accumulator value is 10. Adding 1 + 2 + 3 + 4 = 10. Total sum = 10 + 10 = 20.'
    },
    {
        'topic_slug': 'javascript',
        'difficulty': 'Advanced',
        'question_text': 'What is the binding of `this` inside an arrow function?',
        'code_snippet': 'const obj = {\n    name: "CodeQuiz",\n    getName: () => this.name\n};',
        'code_lang': 'javascript',
        'option_a': 'Bound dynamically to `obj` at invocation time',
        'option_b': 'Arrow functions do not have their own `this`; they lexically capture `this` from the surrounding enclosing scope',
        'option_c': 'Bound to the prototype object of `Function`',
        'option_d': 'Throws a SyntaxError',
        'correct_option': 'B',
        'explanation': 'Arrow functions retain the `this` value of the enclosing lexical execution context at the time they are created, and cannot be rebound using `.bind()`, `.call()`, or `.apply()`.'
    },
    {
        'topic_slug': 'javascript',
        'difficulty': 'Beginner',
        'question_text': 'What is the method used to convert a JavaScript object into a JSON string?',
        'code_snippet': 'const user = { id: 1, name: "Sam" };\nconst json = JSON._____(user);',
        'code_lang': 'javascript',
        'option_a': 'parse',
        'option_b': 'stringify',
        'option_c': 'encode',
        'option_d': 'toText',
        'correct_option': 'B',
        'explanation': '`JSON.stringify()` serializes a JavaScript value/object to a JSON-formatted string.'
    },
    {
        'topic_slug': 'javascript',
        'difficulty': 'Intermediate',
        'question_text': 'What is the output of the optional chaining operator `?.` in JavaScript?',
        'code_snippet': 'const user = { profile: null };\nconsole.log(user?.profile?.name ?? "Guest");',
        'code_lang': 'javascript',
        'option_a': 'TypeError: Cannot read properties of null',
        'option_b': 'null',
        'option_c': '"Guest"',
        'option_d': 'undefined',
        'correct_option': 'C',
        'explanation': '`user?.profile?.name` safely short-circuits to `undefined` because `profile` is null. The nullish coalescing operator `??` falls back to the default value `"Guest"`.'
    },
    {
        'topic_slug': 'javascript',
        'difficulty': 'Advanced',
        'question_text': 'What does `Promise.allSettled()` do when one of the input promises rejects?',
        'code_snippet': 'Promise.allSettled([\n    Promise.resolve(42),\n    Promise.reject("Error")\n]).then(results => console.log(results));',
        'code_lang': 'javascript',
        'option_a': 'Immediately rejects with "Error"',
        'option_b': 'Waits for all promises to finish and returns an array of outcome objects with `{ status: "fulfilled" | "rejected" }`',
        'option_c': 'Retries the rejected promise up to 3 times',
        'option_d': 'Throws an UnhandledPromiseRejectionException',
        'correct_option': 'B',
        'explanation': 'Unlike `Promise.all` which rejects immediately upon any failure, `Promise.allSettled` waits until every promise either fulfills or rejects and returns descriptors of all results.'
    }
]

DEMO_USERS = [
    {
        'username': 'AlexDev',
        'email': 'alex@example.com',
        'password': 'password123',
        'avatar': 'avatar-1',
        'bio': 'Full-stack software engineer & competitive programmer.',
        'total_points': 1420
    },
    {
        'username': 'Sara_Coder',
        'email': 'sara@example.com',
        'password': 'password123',
        'avatar': 'avatar-2',
        'bio': 'Python enthusiast, data engineer & SQL query optimizer.',
        'total_points': 1280
    },
    {
        'username': 'David_JS',
        'email': 'david@example.com',
        'password': 'password123',
        'avatar': 'avatar-3',
        'bio': 'Frontend wizard mastering modern JavaScript & CSS grid.',
        'total_points': 960
    },
    {
        'username': 'Priya_Java',
        'email': 'priya@example.com',
        'password': 'password123',
        'avatar': 'avatar-4',
        'bio': 'Java backend developer building enterprise microservices.',
        'total_points': 810
    },
    {
        'username': 'WebCraft_Dan',
        'email': 'dan@example.com',
        'password': 'password123',
        'avatar': 'avatar-5',
        'bio': 'HTML5 & CSS architect passionate about clean semantic UI.',
        'total_points': 690
    }
]

DEMO_ATTEMPTS = [
    # user_index, topic, difficulty, total, correct, wrong, skipped, score_pct, points, time_sec
    (0, 'python', 'Advanced', 10, 10, 0, 0, 100.0, 300, 145),
    (0, 'javascript', 'Intermediate', 10, 9, 1, 0, 90.0, 240, 160),
    (0, 'sql', 'Intermediate', 10, 10, 0, 0, 100.0, 280, 130),
    (1, 'sql', 'Advanced', 10, 10, 0, 0, 100.0, 320, 115),
    (1, 'python', 'Intermediate', 10, 9, 1, 0, 90.0, 250, 140),
    (1, 'java', 'Intermediate', 10, 8, 2, 0, 80.0, 210, 185),
    (2, 'javascript', 'Advanced', 10, 9, 1, 0, 90.0, 270, 125),
    (2, 'css', 'Intermediate', 10, 10, 0, 0, 100.0, 260, 110),
    (2, 'html', 'Intermediate', 10, 10, 0, 0, 100.0, 230, 95),
    (3, 'java', 'Advanced', 10, 9, 1, 0, 90.0, 280, 175),
    (3, 'sql', 'Intermediate', 10, 8, 2, 0, 80.0, 200, 190),
    (4, 'html', 'Beginner', 10, 10, 0, 0, 100.0, 220, 90),
    (4, 'css', 'Advanced', 10, 9, 1, 0, 90.0, 250, 155),
]


def seed_database():
    print(f"Connecting to database at {DB_PATH}...")
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    # 1. Read and apply schema
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    print("Schema applied successfully.")

    # 2. Insert Topics
    for t in TOPICS:
        cursor.execute("""
            INSERT INTO topics (slug, name, description, icon, color, gradient, code_lang)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (t['slug'], t['name'], t['description'], t['icon'], t['color'], t['gradient'], t['code_lang']))
    print(f"Inserted {len(TOPICS)} topics.")

    # 3. Insert Achievements
    for a in ACHIEVEMENTS:
        cursor.execute("""
            INSERT INTO achievements (slug, title, description, icon, badge_color, points)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (a['slug'], a['title'], a['description'], a['icon'], a['badge_color'], a['points']))
    print(f"Inserted {len(ACHIEVEMENTS)} achievements.")

    # 4. Insert Questions
    for q in QUESTIONS:
        cursor.execute("""
            INSERT INTO questions (
                topic_slug, difficulty, question_text, code_snippet, code_lang,
                option_a, option_b, option_c, option_d, correct_option, explanation, time_limit_sec
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            q['topic_slug'], q['difficulty'], q['question_text'], q['code_snippet'], q['code_lang'],
            q['option_a'], q['option_b'], q['option_c'], q['option_d'], q['correct_option'], q['explanation'], 30
        ))
    print(f"Inserted {len(QUESTIONS)} rich programming questions across all topics.")

    # 5. Insert Demo Users
    user_ids = []
    for u in DEMO_USERS:
        pwd_hash = generate_password_hash(u['password'])
        cursor.execute("""
            INSERT INTO users (username, email, password_hash, avatar, bio, total_points)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (u['username'], u['email'], pwd_hash, u['avatar'], u['bio'], u['total_points']))
        user_ids.append(cursor.lastrowid)
    print(f"Inserted {len(DEMO_USERS)} demo users with competitive leaderboards.")

    # 6. Insert Demo Quiz Attempts & User Topic Stats
    for attempt in DEMO_ATTEMPTS:
        u_idx, topic, diff, total, corr, wrong, skip, pct, pts, time_sec = attempt
        uid = user_ids[u_idx]
        cursor.execute("""
            INSERT INTO quiz_attempts (
                user_id, topic_slug, difficulty, total_questions, correct_answers,
                wrong_answers, skipped_answers, score_percentage, points_earned, time_taken_sec
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (uid, topic, diff, total, corr, wrong, skip, pct, pts, time_sec))

        # Update or Insert user_topic_stats
        cursor.execute("SELECT id, quizzes_taken, total_questions_attempted, total_correct, best_score, total_time_spent_sec FROM user_topic_stats WHERE user_id = ? AND topic_slug = ?", (uid, topic))
        stat_row = cursor.fetchone()
        if stat_row:
            new_taken = stat_row[1] + 1
            new_attempted = stat_row[2] + total
            new_correct = stat_row[3] + corr
            new_best = max(stat_row[4], pct)
            new_time = stat_row[5] + time_sec
            mastery = 'Master' if new_best >= 90 else ('Skilled' if new_best >= 70 else 'Apprentice')
            cursor.execute("""
                UPDATE user_topic_stats
                SET quizzes_taken = ?, total_questions_attempted = ?, total_correct = ?, best_score = ?, total_time_spent_sec = ?, mastery_level = ?
                WHERE user_id = ? AND topic_slug = ?
            """, (new_taken, new_attempted, new_correct, new_best, new_time, mastery, uid, topic))
        else:
            mastery = 'Master' if pct >= 90 else ('Skilled' if pct >= 70 else 'Apprentice')
            cursor.execute("""
                INSERT INTO user_topic_stats (
                    user_id, topic_slug, quizzes_taken, total_questions_attempted,
                    total_correct, best_score, total_time_spent_sec, mastery_level
                ) VALUES (?, ?, 1, ?, ?, ?, ?, ?)
            """, (uid, topic, total, corr, pct, time_sec, mastery))

    # Give demo achievements
    for i, uid in enumerate(user_ids):
        # Give first blood to everyone
        cursor.execute("INSERT OR IGNORE INTO user_achievements (user_id, achievement_id) VALUES (?, 1)", (uid,))
        if i in [0, 1, 2]:
            cursor.execute("INSERT OR IGNORE INTO user_achievements (user_id, achievement_id) VALUES (?, 2)", (uid,)) # Flawless
            cursor.execute("INSERT OR IGNORE INTO user_achievements (user_id, achievement_id) VALUES (?, 3)", (uid,)) # Speed Demon
            cursor.execute("INSERT OR IGNORE INTO user_achievements (user_id, achievement_id) VALUES (?, 5)", (uid,)) # Grandmaster

    conn.commit()
    conn.close()
    print("Database initialization and seeding completed successfully!")


if __name__ == '__main__':
    seed_database()
