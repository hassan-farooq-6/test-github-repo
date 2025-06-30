import openai
import sys
import json

openai.api_key = "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"  # Replace with your actual API key

def analyze_code(file_path):
    with open(file_path, "r") as f:
        code = f.read()

    if not code.strip():
        print("No code found. Skipping AI review.")
        return None

    # Send code to GPT-4o Mini
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert code reviewer. Only report critical issues like syntax errors, security flaws, and logical bugs. Ignore best practices and suggestions unless they indicate a serious problem."},
            {"role": "user", "content": f"Review the following code:\n\n{code}"}
        ]
    )

    return response["choices"][0]["message"]["content"]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No file provided for analysis.")
        sys.exit(0)

    file_path = sys.argv[1]
    ai_suggestions = analyze_code(file_path)

    if ai_suggestions:
        print("\n=== AI SUGGESTIONS ===\n")
        print(ai_suggestions)
        print("\n======================\n")

        with open("ai_suggestions.json", "w") as f:
            json.dump({"suggestions": ai_suggestions}, f, indent=4)

        # **🔹 Block only if real issues exist**
        # Check for actual problems, not just mentions of the word "critical"
        blocking_phrases = [
            "syntax error", "security flaw", "logical issue", 
            "critical bug", "crash", "will cause", "vulnerability",
            "error on line", "bug in", "problem with"
        ]
        
        # Don't block if AI says "no critical issues" or "no issues found"
        safe_phrases = [
            "no critical issues", "no issues found", "no syntax errors", 
            "no security flaws", "does not contain any critical issues",
            "free of critical issues", "appears to be functioning as intended",
            "everything appears to be", "no changes are necessary"
        ]
        
        is_safe = any(phrase in ai_suggestions.lower() for phrase in safe_phrases)
        has_issues = any(phrase in ai_suggestions.lower() for phrase in blocking_phrases)
        
        if has_issues and not is_safe:
            print("AI found critical issues. Blocking commit.")
            sys.exit(1)
        else:
            print("No critical issues found. Proceeding with commit.")
            sys.exit(0)
    else:
        print("No issues found by AI. Proceeding with commit.")
        sys.exit(0)