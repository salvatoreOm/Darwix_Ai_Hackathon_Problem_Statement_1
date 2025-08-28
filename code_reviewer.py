"""
Empathetic Code Reviewer - Core Module

This module provides the main functionality for transforming harsh code review 
comments into empathetic, constructive feedback using Azure OpenAI.
"""

import os
import requests
from typing import Dict, List, Any


class EmpatheticCodeReviewer:
    """
    A class that transforms harsh code review comments into empathetic, 
    constructive feedback using Azure OpenAI.
    """
    
    def __init__(self, use_mock: bool = False):
        """Initialize the reviewer with Azure OpenAI configuration.

        Args:
            use_mock: If True, bypass Azure API and return a deterministic mock report
        """
        self.use_mock = bool(use_mock or os.getenv("USE_MOCK", "").lower() in {"1", "true", "yes"})

        # Store Azure OpenAI configuration (only required when not mocking)
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

        if not self.use_mock:
            required_vars = [
                "AZURE_OPENAI_API_KEY",
                "AZURE_OPENAI_ENDPOINT",
                "AZURE_OPENAI_API_VERSION",
                "AZURE_OPENAI_DEPLOYMENT_NAME",
            ]
            missing_vars = [var for var in required_vars if not os.getenv(var)]
            if missing_vars:
                raise ValueError(
                    f"Missing required environment variables: {', '.join(missing_vars)}"
                )
    
    def generate_empathetic_review(self, input_data: Dict[str, Any]) -> str:
        """
        Generate an empathetic code review report from input data.
        
        Args:
            input_data: Dictionary containing 'code_snippet' and 'review_comments'
            
        Returns:
            Markdown formatted empathetic review report
        """
        code_snippet = input_data.get("code_snippet", "")
        review_comments = input_data.get("review_comments", [])
        
        if not code_snippet:
            raise ValueError("code_snippet is required")
        
        if not review_comments:
            raise ValueError("review_comments list cannot be empty")
        
        # Detect programming language
        language = self._detect_language(code_snippet)
        
        # Assess severity of comments
        severity_levels = [self._assess_comment_severity(comment) for comment in review_comments]
        
        # Generate the empathetic review
        prompt = self._create_detailed_prompt(code_snippet, review_comments, language, severity_levels)

        if self.use_mock:
            return self._create_mock_report(code_snippet, review_comments, language, severity_levels)

        try:
            response = self._call_azure_openai(prompt)
            return response.strip()
        except Exception as e:
            raise RuntimeError(f"Failed to generate review: {str(e)}")
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for the AI."""
        return """You are an empathetic senior software developer and mentor with years of experience. 
        Your role is to transform harsh, direct code review comments into constructive, educational, 
        and encouraging feedback. You understand that learning happens best in a supportive environment.

        Key principles:
        - Always start with something positive
        - Explain the 'why' behind suggestions with clear reasoning
        - Provide concrete, actionable improvements
        - Use encouraging, supportive language
        - Reference best practices and documentation when relevant
        - Tailor your tone to the severity of the original comment
        - End with motivational, growth-oriented language"""
    
    def _detect_language(self, code_snippet: str) -> str:
        """Detect the programming language from the code snippet."""
        # Simple language detection based on common patterns
        if 'def ' in code_snippet and ':' in code_snippet:
            return 'Python'
        elif 'function' in code_snippet and '{' in code_snippet:
            return 'JavaScript'
        elif 'public class' in code_snippet or 'private ' in code_snippet:
            return 'Java'
        elif '#include' in code_snippet or 'int main' in code_snippet:
            return 'C++'
        elif 'func ' in code_snippet and '{' in code_snippet:
            return 'Go'
        else:
            return 'Unknown'
    
    def _assess_comment_severity(self, comment: str) -> str:
        """Assess the severity/harshness of a review comment."""
        harsh_words = ['bad', 'terrible', 'wrong', 'stupid', 'awful', 'horrible', 'useless']
        critical_words = ['inefficient', 'redundant', 'unnecessary', 'poor', 'weak']
        
        comment_lower = comment.lower()
        
        if any(word in comment_lower for word in harsh_words):
            return 'harsh'
        elif any(word in comment_lower for word in critical_words):
            return 'critical'
        else:
            return 'mild'
    
    def _create_detailed_prompt(self, code_snippet: str, review_comments: List[str], 
                              language: str, severity_levels: List[str]) -> str:
        """Create a detailed prompt for the AI."""
        
        # Create comment analysis
        comment_analysis = []
        for i, (comment, severity) in enumerate(zip(review_comments, severity_levels)):
            comment_analysis.append(f"{i+1}. \"{comment}\" (Severity: {severity})")
        
        prompt = f"""
Please transform the following code review into an empathetic, educational report.

**Code Snippet ({language}):**
```{language.lower()}
{code_snippet}
```

**Original Review Comments:**
{chr(10).join(comment_analysis)}

**Instructions:**
For each original comment, create a markdown section with the following structure:

---
### Analysis of Comment: "[original comment]"

* **Positive Rephrasing:** [Rewrite the comment in an encouraging, supportive way that acknowledges effort while suggesting improvement]

* **The 'Why':** [Explain the underlying software engineering principle, performance concern, or best practice. Include specific technical reasoning]

* **Suggested Improvement:**
```{language.lower()}
[Provide concrete code example showing the recommended fix]
```

* **Learn More:** [If applicable, mention relevant documentation, style guides, or resources (e.g., PEP 8 for Python, MDN for JavaScript)]

---

**Additional Requirements:**
1. Adjust your tone based on the severity of each original comment
2. For harsh comments, be extra gentle and encouraging
3. For critical comments, be supportive but educational
4. For mild comments, be friendly and collaborative

5. End with a "**Overall Summary**" section that:
   - Acknowledges the developer's effort
   - Summarizes the key improvements
   - Encourages continued learning and growth
   - Maintains a positive, motivational tone

Please ensure the response is well-formatted markdown and maintains a consistently empathetic tone throughout.
"""
        return prompt

    def _create_mock_report(
        self,
        code_snippet: str,
        review_comments: List[str],
        language: str,
        severity_levels: List[str],
    ) -> str:
        """Create a deterministic mock review report suitable for local testing."""
        lines: List[str] = []
        lines.append("---")
        for i, (comment, severity) in enumerate(zip(review_comments, severity_levels), start=1):
            lines.append(f"### Analysis of Comment {i}: \"{comment}\"")
            lines.append("")
            lines.append("* **Positive Rephrasing:** Nice progress here! Let's refine this area for clarity and performance.")
            lines.append("")
            if severity == "harsh":
                why = "The suggestion aims to improve reliability and readability while keeping your original intent."
            elif severity == "critical":
                why = "This change balances readability and efficiency based on common best practices."
            else:
                why = "A small tweak can improve maintainability without changing behavior."
            lines.append(f"* **The 'Why':** {why}")
            lines.append("")
            lines.append("* **Suggested Improvement:**")
            lines.append(f"```{language.lower()}")
            lines.append("# Example improvement (mock)\n# Replace with a specific change based on context")
            lines.append(code_snippet.splitlines()[0] if code_snippet else "# (no code provided)")
            lines.append("```")
            lines.append("")
            lines.append("* **Learn More:** Consider consulting your team's style guide or official docs.")
            lines.append("\n---\n")

        lines.append("**Overall Summary**\n")
        lines.append(
            "Great work pushing this forward! With a few focused adjustments, "
            "your code will be clearer and easier to maintain. Keep iterating—you're on the right track!"
        )
        return "\n".join(lines)

    def _call_azure_openai(self, prompt: str) -> str:
        """
        Make a direct HTTP request to Azure OpenAI API.
        
        Args:
            prompt: The user prompt to send to the API
            
        Returns:
            The AI response content
        """
        # Construct the API URL
        url = f"{self.endpoint}openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"
        
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }
        
        data = {
            "messages": [
                {
                    "role": "system", 
                    "content": self._get_system_prompt()
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": 3000,
            "top_p": 0.9
        }
        
        # Make the HTTP request
        response = requests.post(url, headers=headers, json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            raise RuntimeError(f"Azure OpenAI API error: {response.status_code} - {response.text}")


def main():
    """Main function for testing the reviewer."""
    # Example usage
    sample_data = {
        "code_snippet": """def get_active_users(users):
    results = []
    for u in users:
        if u.is_active == True and u.profile_complete == True:
            results.append(u)
    return results""",
        "review_comments": [
            "This is inefficient. Don't loop twice conceptually.",
            "Variable 'u' is a bad name.",
            "Boolean comparison '== True' is redundant."
        ]
    }
    
    try:
        reviewer = EmpatheticCodeReviewer(use_mock=True)
        result = reviewer.generate_empathetic_review(sample_data)
        print(result)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
