#!/usr/bin/env python3
"""
Empathetic Code Reviewer - Streamlit Web Interface

A web-based interface for the Empathetic Code Reviewer using Streamlit.
Provides an easy-to-use GUI for transforming harsh code review comments
into empathetic, constructive feedback.

Usage:
    streamlit run streamlit_app.py
"""

import streamlit as st
import json
import os
from typing import Dict, Any, List
from dotenv import load_dotenv

from code_reviewer import EmpatheticCodeReviewer


def load_example_files() -> Dict[str, Dict[str, Any]]:
    """Load all example JSON files for the dropdown."""
    examples = {}
    example_dir = "examples"
    
    if os.path.exists(example_dir):
        for filename in os.listdir(example_dir):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(example_dir, filename), 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        examples[filename] = data
                except Exception as e:
                    st.error(f"Error loading {filename}: {e}")
    
    return examples


def main():
    """Main Streamlit application."""
    # Page configuration
    st.set_page_config(
        page_title="🤖 Empathetic Code Reviewer",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load environment variables
    load_dotenv()
    
    # Header
    st.title("🤖 Empathetic Code Reviewer")
    st.markdown("**Transform harsh code review comments into constructive, empathetic feedback**")
    st.markdown("---")
    
    # Sidebar configuration
    st.sidebar.header("⚙️ Configuration")
    
    # Mock mode toggle
    use_mock = st.sidebar.checkbox(
        "🧪 Mock Mode", 
        value=True,
        help="Use mock responses instead of Azure OpenAI (recommended for testing)"
    )
    
    if not use_mock:
        st.sidebar.warning("⚠️ Azure OpenAI mode requires environment variables to be set")
        
        # Check environment variables
        required_vars = [
            'AZURE_OPENAI_API_KEY',
            'AZURE_OPENAI_ENDPOINT', 
            'AZURE_OPENAI_API_VERSION',
            'AZURE_OPENAI_DEPLOYMENT_NAME'
        ]
        
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            st.sidebar.error(f"Missing environment variables: {', '.join(missing_vars)}")
            st.sidebar.info("💡 Enable Mock Mode or configure your .env file")
    
    # Load example files
    examples = load_example_files()
    
    # Main interface
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 Input")
        
        # Example selector
        if examples:
            st.subheader("🔍 Quick Start - Load Example")
            selected_example = st.selectbox(
                "Choose an example:",
                options=[""] + list(examples.keys()),
                format_func=lambda x: "Select an example..." if x == "" else x.replace('.json', '').replace('_', ' ').title()
            )
            
            if selected_example and selected_example in examples:
                example_data = examples[selected_example]
                st.success(f"✅ Loaded: {selected_example}")
                
                # Auto-populate fields
                code_snippet = example_data.get("code_snippet", "")
                review_comments = example_data.get("review_comments", [])
            else:
                code_snippet = ""
                review_comments = []
        else:
            code_snippet = ""
            review_comments = []
        
        st.subheader("💻 Code Snippet")
        code_input = st.text_area(
            "Enter your code snippet:",
            value=code_snippet,
            height=200,
            help="Paste the code that was reviewed"
        )
        
        st.subheader("💬 Review Comments")
        st.write("Add the original review comments (one per line):")
        
        # Dynamic comment input
        if 'comments' not in st.session_state:
            st.session_state.comments = review_comments if review_comments else [""]
        
        # Display comment inputs
        for i, comment in enumerate(st.session_state.comments):
            col_comment, col_remove = st.columns([4, 1])
            with col_comment:
                st.session_state.comments[i] = st.text_input(
                    f"Comment {i+1}:",
                    value=comment,
                    key=f"comment_{i}"
                )
            with col_remove:
                if len(st.session_state.comments) > 1:
                    if st.button("🗑️", key=f"remove_{i}", help="Remove this comment"):
                        st.session_state.comments.pop(i)
                        st.rerun()
        
        # Add/Remove comment buttons
        col_add, col_clear = st.columns(2)
        with col_add:
            if st.button("➕ Add Comment"):
                st.session_state.comments.append("")
                st.rerun()
        
        with col_clear:
            if st.button("🗑️ Clear All"):
                st.session_state.comments = [""]
                st.rerun()
    
    with col2:
        st.header("📊 Empathetic Review")
        
        # Generate review button
        if st.button("🚀 Generate Empathetic Review", type="primary", use_container_width=True):
            # Validation
            if not code_input.strip():
                st.error("❌ Please enter a code snippet")
                return
            
            # Filter out empty comments
            filtered_comments = [c.strip() for c in st.session_state.comments if c.strip()]
            
            if not filtered_comments:
                st.error("❌ Please enter at least one review comment")
                return
            
            # Prepare input data
            input_data = {
                "code_snippet": code_input,
                "review_comments": filtered_comments
            }
            
            try:
                with st.spinner("🔄 Generating empathetic review..."):
                    reviewer = EmpatheticCodeReviewer(use_mock=use_mock)
                    result = reviewer.generate_empathetic_review(input_data)
                
                # Display result
                st.success("✅ Review generated successfully!")
                st.markdown("### 📝 Generated Review")
                st.markdown(result)
                
                # Download button
                st.download_button(
                    label="💾 Download Review",
                    data=result,
                    file_name="empathetic_review.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"❌ Error generating review: {str(e)}")
                if not use_mock:
                    st.info("💡 Try enabling Mock Mode for local testing")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>🤖 <strong>Empathetic Code Reviewer</strong> - Transforming Critical Feedback into Constructive Growth</p>
            <p>Built for hackathon • <a href='https://github.com' target='_blank'>View Source</a></p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
