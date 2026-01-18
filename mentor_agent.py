import ast
import re

# -------------------
# PYTHON ANALYSIS
# -------------------
def analyze_python_code(code):
    errors = []
    suggestions = []

    lines = code.split("\n")

    # -------------------
    # Analyze each line separately for syntax errors
    # -------------------
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped:
            continue  # skip empty lines
        try:
            ast.parse(line)
        except SyntaxError as e:
            errors.append(f"❌ Syntax Error at line {i}: {e.msg}")
            errors.append(f"🔧 Check this line: {line}")

    # -------------------
    # Now analyze the full code for other issues if syntax allows
    # -------------------
    try:
        tree = ast.parse(code)
        suggestions.append("✅ Python syntax is valid for blocks that parsed successfully.")
    except SyntaxError:
        # cannot parse fully, skip AST-based checks
        tree = None

    if tree:
        # track variables
        defined_vars = set()
        list_defs = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                if isinstance(node.targets[0], ast.Name):
                    var_name = node.targets[0].id
                    defined_vars.add(var_name)
                if isinstance(node.targets[0], ast.Name) and isinstance(node.value, ast.List):
                    list_defs[node.targets[0].id] = len(node.value.elts)

        # list index checks
        for node in ast.walk(tree):
            if isinstance(node, ast.Subscript):
                if isinstance(node.value, ast.Name):
                    list_name = node.value.id
                    if isinstance(node.slice, ast.Constant) and list_name in list_defs:
                        idx = node.slice.value
                        max_idx = list_defs[list_name] - 1
                        if idx > max_idx:
                            errors.append(f"❌ Possible IndexError: '{list_name}[{idx}]' out of range (max index {max_idx})")
                            errors.append(f"🔧 Correct example: {list_name}[{max_idx}]")

        # undefined variables
        for node in ast.walk(tree):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                if node.id not in defined_vars and node.id not in dir(__builtins__):
                    errors.append(f"❌ Possible undefined variable: '{node.id}'")
                    errors.append(f"🔧 Suggestion: Define '{node.id}' before using it.")

        # functions
        functions = [n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        if functions:
            suggestions.append(f"✅ Functions detected: {', '.join(functions)}")
        else:
            suggestions.append("💡 Tip: Consider using functions for better structure.")
            suggestions.append("🔧 Example:\ndef greet(name):\n    print('Hello ' + name)")

        # loops
        loops = [n for n in ast.walk(tree) if isinstance(n, (ast.For, ast.While))]
        if loops:
            suggestions.append("✅ Loop(s) detected.")
        else:
            suggestions.append("💡 Tip: Add loops if repetition is needed.")
            suggestions.append("🔧 Example:\nfor i in range(5):\n    print(i)")

        # conditionals
        ifs = [n for n in ast.walk(tree) if isinstance(n, ast.If)]
        if ifs:
            suggestions.append("✅ Conditional logic detected.")
        else:
            suggestions.append("💡 Tip: Use if-else for decisions.")
            suggestions.append("🔧 Example:\nif x > 0:\n    print('Positive')")

        # print statements
        prints = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and getattr(n.func, 'id', '') == 'print']
        if prints:
            suggestions.append("✅ print() statements found (good for debugging).")

    feedback = ["📌 Errors:"] + errors + ["\n💡 Suggestions:"] + suggestions
    feedback.append("🎯 Overall: Review errors and try corrections to improve your code!")
    return "\n".join(feedback)


# -------------------
# JAVA ANALYSIS
# -------------------
def analyze_java_code(code):
    errors = []
    suggestions = []

    lines = code.split("\n")

    # 1️⃣ Check missing semicolons line-by-line
    for i, line in enumerate(lines, 1):
        line_strip = line.strip()
        if line_strip and not line_strip.endswith(";") and \
           not line_strip.endswith("{") and not line_strip.endswith("}") and \
           not line_strip.startswith("//") and \
           not re.match(r"(class|public|private|protected|if|for|while|else)", line_strip):
            errors.append(f"❌ Missing semicolon at line {i}")
            errors.append(f"🔧 Example fix:\n{line_strip};")

    # 2️⃣ Braces balance
    open_braces = code.count("{")
    close_braces = code.count("}")
    if open_braces != close_braces:
        errors.append(f"❌ Mismatched braces detected ({open_braces} '{{' vs {close_braces} '}}')")
        errors.append("🔧 Ensure every '{' has a matching '}'")

    # 3️⃣ Methods detection
    methods = re.findall(r'(public|private|protected)\s+\w+\s+(\w+)\s*\(.*\)', code)
    if methods:
        suggestions.append(f"✅ Methods detected: {', '.join([m[1] for m in methods])}")
    else:
        suggestions.append("💡 Tip: Consider adding methods for reusable code.")
        suggestions.append("🔧 Example:\npublic void greet(String name) {\n    System.out.println(\"Hello \" + name);\n}")

    # 4️⃣ Loops
    loops = re.findall(r"(for\s*\(.*\)|while\s*\(.*\))", code)
    if loops:
        suggestions.append("✅ Loop(s) detected.")
    else:
        suggestions.append("💡 Tip: Add loops if repetition is needed.")
        suggestions.append("🔧 Example:\nfor(int i=0;i<5;i++){\n    System.out.println(i);\n}")

    # 5️⃣ Print statements
    if "System.out.println" in code:
        suggestions.append("✅ Print statements found.")
    else:
        suggestions.append("💡 Tip: Use System.out.println for debugging.")
        suggestions.append("🔧 Example:\nSystem.out.println(\"Hello World\");")

    # 6️⃣ Array index check for simple literal arrays
    array_defs = {}
    for match in re.finditer(r'(\w+)\s*=\s*{\s*([\d,\s]+)\s*}', code):
        arr_name = match.group(1)
        arr_vals = match.group(2).split(",")
        array_defs[arr_name] = len(arr_vals)

    for match in re.finditer(r'(\w+)\s*\[\s*(\d+)\s*\]', code):
        arr_name = match.group(1)
        idx = int(match.group(2))
        if arr_name in array_defs and idx >= array_defs[arr_name]:
            errors.append(f"❌ Possible ArrayIndexOutOfBounds: '{arr_name}[{idx}]' out of range (max index {array_defs[arr_name]-1})")
            errors.append(f"🔧 Correct example: {arr_name}[{array_defs[arr_name]-1}]")

    feedback = ["📌 Errors:"] + errors + ["\n💡 Suggestions:"] + suggestions
    feedback.append("🎯 Overall: Review errors and try corrections to improve your code!")
    return "\n".join(feedback)


# -------------------
# MAIN FUNCTION
# -------------------
def analyze_code(code, language="python"):
    language = language.lower()
    if language == "python":
        return analyze_python_code(code)
    elif language == "java":
        return analyze_java_code(code)
    else:
        return "❌ Language not supported. Choose Python or Java."