# 🤖 Empathetic Code Reviewer

**Transforming Critical Feedback into Constructive Growth**

An AI-powered tool that transforms harsh, direct code review comments into empathetic, educational, and constructive feedback using Azure OpenAI.

## 🎯 The Problem

Code reviews are essential for maintaining code quality, but harsh feedback can be discouraging and unhelpful. Comments like:
- "This is terrible code"
- "Variable names are awful" 
- "This is inefficient and wrong"

...leave developers feeling demoralized without understanding **how** to improve.

## 💡 The Solution

This project transforms critical feedback into empathetic, educational guidance. Instead of harsh comments, developers receive:
- **Positive reinforcement** that acknowledges their effort
- **Clear explanations** of the underlying principles
- **Concrete examples** showing exactly how to improve
- **Learning resources** for continued growth

## ✨ Features

- **🔄 Comment Transformation**: Converts harsh review comments into empathetic, constructive feedback
- **📚 Educational Focus**: Explains the underlying software principles behind each suggestion
- **💡 Code Improvements**: Provides concrete code examples demonstrating recommended fixes
- **🎨 Multiple Languages**: Supports Python, JavaScript, Java, C++, Go, and more
- **📊 Severity Assessment**: Adjusts tone based on the harshness of original comments
- **🔗 Resource Links**: References relevant documentation and best practices
- **📝 Markdown Output**: Generates well-formatted reports ready for sharing

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Azure OpenAI account with a deployed model (optional - use mock mode for testing)
- Virtual environment (recommended)

### Installation

1. **Clone and setup the project:**
   ```bash
   cd Dar_Hack
   source venv/bin/activate  # Your virtual environment is already created
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.template .env
   # Edit .env with your Azure OpenAI credentials
   ```

3. **Test the installation (no Azure required):**
   ```bash
   python main.py examples/sample_input.json --mock
   ```

## 📖 Usage

### 🌐 Web Interface (Recommended)

Launch the Streamlit web app for an easy-to-use GUI:

```bash
streamlit run streamlit_app.py
```

Then open http://localhost:8501 in your browser. Features include:
- 🎯 Load example files with one click
- 📝 Interactive code and comment input
- 🧪 Mock mode toggle (no Azure setup required)
- 💾 Download generated reviews as Markdown
- 🎨 Clean, professional interface

### Command Line Interface

```bash
# Process a JSON file (mock mode)
python main.py examples/sample_input.json --mock

# Save output to file (mock mode)
python main.py examples/sample_input.json -o report.md --mock

# Interactive mode (mock mode)
python main.py --interactive --mock

# Show help
python main.py --help
```

### Input Format

Create a JSON file with your code snippet and review comments:

```json
{
  "code_snippet": "def get_active_users(users):\\n    results = []\\n    for u in users:\\n        if u.is_active == True:\\n            results.append(u)\\n    return results",
  "review_comments": [
    "This is inefficient. Don't loop twice conceptually.",
    "Variable 'u' is a bad name.",
    "Boolean comparison '== True' is redundant."
  ]
}
```

### Example Output

```markdown
---
### Analysis of Comment: "Variable 'u' is a bad name."

* **Positive Rephrasing:** "Great job on the logic flow! For better code readability, consider using a more descriptive variable name that clearly indicates what the variable represents."

* **The 'Why':** Clear, descriptive variable names make code self-documenting and easier for team members to understand. When other developers (including your future self) read this code, they'll immediately understand what each variable represents without having to trace through the logic.

* **Suggested Improvement:**
```python
def get_active_users(users):
    results = []
    for user in users:  # 'user' is more descriptive than 'u'
        if user.is_active and user.profile_complete:
            results.append(user)
    return results
```

* **Learn More:** Check out PEP 8's naming conventions: https://pep8.org/#naming-conventions
---
```

## 📁 Project Structure

```
Dar_Hack/
├── main.py                 # Main application entry point
├── code_reviewer.py        # Core AI reviewer logic
├── streamlit_app.py        # Web interface (Streamlit)
├── requirements.txt        # Python dependencies
├── .gitignore             # Git ignore patterns
├── .env                   # Environment variables (your config)
├── README.md              # This file
└── examples/              # Sample input files
    ├── sample_input.json      # Basic Python example
    ├── javascript_example.json # JavaScript example
    └── harsh_comments.json    # Example with harsh comments
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `AZURE_OPENAI_API_KEY` | Your Azure OpenAI API key | `abc123...` |
| `AZURE_OPENAI_ENDPOINT` | Your Azure OpenAI endpoint | `https://your-resource.openai.azure.com/` |
| `AZURE_OPENAI_API_VERSION` | API version | `2024-02-15-preview` |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Your model deployment name | `gpt-4` |

You can also enable mock mode via environment variable:

```bash
export USE_MOCK=1
python main.py examples/sample_input.json
```

## 🎨 Advanced Features

### Severity-Based Tone Adjustment
The AI automatically detects the harshness of original comments and adjusts its tone accordingly:
- **Harsh comments**: Extra gentle and encouraging
- **Critical comments**: Supportive but educational  
- **Mild comments**: Friendly and collaborative

### Multi-Language Support
Automatically detects and handles multiple programming languages:
- Python
- JavaScript
- Java
- C++
- Go
- And more...

### Interactive Mode
Run `python main.py --interactive` for a guided experience where you can:
- Enter code snippets directly
- Add multiple review comments
- Save results to files

## 🧪 Examples

Try these example files:

```bash
# Basic Python example (mock mode)
python main.py examples/sample_input.json --mock

# JavaScript with modern practices (mock mode)
python main.py examples/javascript_example.json --mock

# Handling harsh comments (mock mode)
python main.py examples/harsh_comments.json --mock
```

## 🛠️ Development

### Running Tests
```bash
python -m pytest tests/  # When tests are added
```

### Code Style
```bash
black *.py  # Format code
flake8 *.py  # Check style
```

## 🎯 Hackathon Features

This project includes several advanced features designed to stand out:

1. **🎭 Contextual Tone Adjustment**: AI adapts its empathy level based on comment severity
2. **📚 Educational Resources**: Links to relevant documentation and style guides
3. **🔍 Language Detection**: Automatically identifies programming languages
4. **📊 Comprehensive Analysis**: Detailed breakdown of each review point
5. **💬 Interactive Mode**: User-friendly command-line interface
6. **📝 Professional Output**: Publication-ready Markdown reports

## 🤝 Contributing

This is a hackathon project, but contributions are welcome! Areas for improvement:
- Additional programming language support
- Integration with popular code review platforms (GitHub, GitLab, etc.)
- Enhanced AI prompting strategies
- Unit tests and automated testing

## 📄 License

MIT License - feel free to use this project for learning and development.

## 🙏 Acknowledgments

Built for the hackathon challenge: "The Empathetic Code Reviewer - Transforming Critical Feedback into Constructive Growth."

---

**Happy coding! 🚀**
