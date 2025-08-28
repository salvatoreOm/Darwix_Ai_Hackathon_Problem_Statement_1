#!/usr/bin/env python3
"""
Empathetic Code Reviewer - Main Application

This is the main entry point for the Empathetic Code Reviewer application.
It processes JSON input containing code snippets and review comments,
then generates empathetic, constructive feedback using Azure OpenAI.

Usage:
    python main.py <input_json_file>
    python main.py --interactive
    python main.py --help

Examples:
    python main.py examples/sample_input.json
    python main.py --interactive
"""

import argparse
import json
import sys
import os
from typing import Dict, Any
from dotenv import load_dotenv

from code_reviewer import EmpatheticCodeReviewer


def load_json_input(file_path: str) -> Dict[str, Any]:
    """
    Load and validate JSON input file.
    
    Args:
        file_path: Path to the JSON input file
        
    Returns:
        Parsed JSON data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
        ValueError: If required keys are missing
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Input file not found: {file_path}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Invalid JSON in file {file_path}: {e}", e.doc, e.pos)
    
    # Validate required keys
    required_keys = ['code_snippet', 'review_comments']
    missing_keys = [key for key in required_keys if key not in data]
    
    if missing_keys:
        raise ValueError(f"Missing required keys in JSON: {missing_keys}")
    
    if not isinstance(data['review_comments'], list):
        raise ValueError("'review_comments' must be a list")
    
    if not data['review_comments']:
        raise ValueError("'review_comments' list cannot be empty")
    
    return data


def interactive_mode(use_mock: bool = False):
    """Run the application in interactive mode."""
    print("🤖 Empathetic Code Reviewer - Interactive Mode")
    print("=" * 50)
    
    # Get code snippet
    print("\nPlease enter your code snippet (press Enter twice when done):")
    code_lines = []
    empty_line_count = 0
    
    while empty_line_count < 2:
        line = input()
        if line.strip() == "":
            empty_line_count += 1
        else:
            empty_line_count = 0
        code_lines.append(line)
    
    # Remove the last two empty lines
    code_snippet = '\n'.join(code_lines[:-2])
    
    if not code_snippet.strip():
        print("❌ Error: Code snippet cannot be empty")
        return
    
    # Get review comments
    print("\nPlease enter review comments (one per line, press Enter on empty line to finish):")
    review_comments = []
    
    while True:
        comment = input(f"Comment {len(review_comments) + 1}: ").strip()
        if not comment:
            break
        review_comments.append(comment)
    
    if not review_comments:
        print("❌ Error: At least one review comment is required")
        return
    
    # Create input data
    input_data = {
        "code_snippet": code_snippet,
        "review_comments": review_comments
    }
    
    # Process the review
    try:
        print("\n🔄 Generating empathetic review...")
        reviewer = EmpatheticCodeReviewer(use_mock=use_mock)
        result = reviewer.generate_empathetic_review(input_data)
        
        print("\n" + "=" * 60)
        print("📝 EMPATHETIC CODE REVIEW REPORT")
        print("=" * 60)
        print(result)
        
        # Ask if user wants to save the result
        save_choice = input("\n💾 Would you like to save this report to a file? (y/n): ").lower()
        if save_choice in ['y', 'yes']:
            filename = input("Enter filename (default: review_report.md): ").strip()
            if not filename:
                filename = "review_report.md"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"✅ Report saved to {filename}")
        
    except Exception as e:
        print(f"❌ Error generating review: {e}")


def process_file_mode(input_file: str, output_file: str = None, use_mock: bool = False):
    """Process a JSON input file and generate the empathetic review."""
    try:
        # Load and validate input
        print(f"📂 Loading input from: {input_file}")
        input_data = load_json_input(input_file)
        
        # Generate review
        print("🔄 Generating empathetic review...")
        reviewer = EmpatheticCodeReviewer(use_mock=use_mock)
        result = reviewer.generate_empathetic_review(input_data)
        
        # Output result
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"✅ Report saved to: {output_file}")
        else:
            print("\n" + "=" * 60)
            print("📝 EMPATHETIC CODE REVIEW REPORT")
            print("=" * 60)
            print(result)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="Transform harsh code review comments into empathetic, constructive feedback",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py examples/sample_input.json
  python main.py input.json -o report.md
  python main.py --interactive
        """
    )
    
    parser.add_argument(
        'input_file',
        nargs='?',
        help='JSON file containing code_snippet and review_comments'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file for the generated report (default: print to stdout)'
    )
    
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )

    parser.add_argument(
        '--mock',
        action='store_true',
        help='Use mock mode (no Azure calls) for quick local testing'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Empathetic Code Reviewer 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Check for environment variables unless in mock mode
    if not args.mock:
        required_env_vars = [
            'AZURE_OPENAI_API_KEY',
            'AZURE_OPENAI_ENDPOINT',
            'AZURE_OPENAI_API_VERSION',
            'AZURE_OPENAI_DEPLOYMENT_NAME'
        ]
        missing_env_vars = [var for var in required_env_vars if not os.getenv(var)]
        if missing_env_vars:
            print("❌ Error: Missing required environment variables:")
            for var in missing_env_vars:
                print(f"   - {var}")
            print("\nTip: Run with --mock to skip Azure setup for local testing.")
            print("Please check your .env file or set these environment variables.")
            sys.exit(1)
    
    # Handle different modes
    if args.interactive:
        interactive_mode(use_mock=args.mock)
    elif args.input_file:
        process_file_mode(args.input_file, args.output, use_mock=args.mock)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
