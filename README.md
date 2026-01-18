🔹 Description
AI LogicMedic Agent is an offline intelligent coding mentor that helps developers identify and fix errors in their code. It detects syntax mistakes, runtime issues like index errors, undefined variables, and provides line-by-line suggestions and corrected examples, acting like a real human mentor.
It’s perfect for students, developers, or anyone learning Python/Java, and works without requiring any API keys or internet connection.
🔹 Features
Detects syntax errors and indentation issues
Identifies Python list/Java array index errors
Detects undefined variables in Python
Provides corrected examples and mentor-style suggestions
Detects loops, functions, conditionals, and print statements
Supports Python and Java
Fully offline; no API key needed
Interactive Streamlit interface for easy testing
🔹 Tech Stack
Python 3.x
AST for Python static analysis
Regex for Java static analysis
Streamlit for interactive web UI
🔹 Installation
Clone the repository:
Copy code
Bash
git clone https://github.com/yourusername/AI-LogicMedic-Agent.git
cd AI-LogicMedic-Agent
Install required packages:
Copy code
Bash
pip install streamlit
🔹 Usage
Run the Streamlit app:
Copy code
Bash
streamlit run app.py
Select your language (Python or Java) from the dropdown.
Paste your code into the text area.
Click Analyze to get line-by-line mentor feedback.
🔹 Example Output
Python Input:
Copy code
Python
for i in range(5)
print(i)

numbers = [1, 2, 3]
print(numbers[5])
Mentor Feedback:
Copy code

📌 Errors:
❌ Syntax Error at line 1: expected ':'
❌ Possible IndexError: 'numbers[5]' out of range (max index 2)

💡 Suggestions:
✅ Loop(s) detected
✅ print() statements found (good for debugging)
🎯 Overall: Review errors and try corrections to improve your code!
🔹 Future Improvements
Add more advanced runtime error detection
Support other programming languages
Integrate AI-powered suggestions for better explanations
🔹 License
This project is open-source and free to use.
