import json
import subprocess
import re
import os
from transformers import AutoModelForCausalLM, AutoTokenizer
import google.generativeai as genai

def upgrade_dependencies(project_dir):
    """
    Upgrades dependencies in the specified Node.js project.

    Args:
        project_dir: Path to the root directory of the Node.js project.

    Returns:
        True if the upgrade was successful, False otherwise.
    """
    try:
        # Get outdated packages in JSON format
        result = subprocess.run(
            ["npm", "outdated", "--json"],
            cwd=project_dir,
            capture_output=True,
            text=True
        )

        outdated_packages = json.loads(result.stdout)

        # Update package.json
        with open(f"{project_dir}/package.json", "r") as f:
            package_json = json.load(f)

        for package_name, package_info in outdated_packages.items():
            if package_name in package_json.get("dependencies", {}):
                package_json["dependencies"][package_name] = package_info["latest"]

        with open(f"{project_dir}/package.json", "w") as f:
            json.dump(package_json, f, indent=2)

        # Install updated packages
        subprocess.run(["npm", "install"], cwd=project_dir, check=True)

        return True
    except Exception as e:
        print(f"Error upgrading dependencies: {e}")
        return False
    
def build_project(project_dir):
    """
    Builds the Node.js project and captures errors.

    Args:
        project_dir: Path to the root directory of the Node.js project.

    Returns:
        True if the build was successful, False otherwise.
        Errors (if any) are stored in the `build_errors` variable.
    """

    try:
        build_result = subprocess.run(
            ["npm", "run", "build"],
            cwd=project_dir,
            capture_output=True, 
            text=True 
        )

        if build_result.returncode == 0:
            print("Build successful!")
            return False
        else:
            # Build failed, capture errors
            # print(f'{build_result}')
            build_errors = build_result.stdout 
            print("Build failed! Errors:")
            print(build_errors)

            # Optionally write errors to a file (modify path as needed)
            with open(f"{project_dir}/build_errors.log", "w") as f:
                f.write(build_errors)

            return True

    except Exception as e:
        print(f"Error building project: {e}")
        return False
    
def analyze_build_errors(error_log, project_dir):
    """
    Analyzes build errors using an open-source AI model.

    Args:
        error_log: Path to the build error log file.
        project_dir: Path to the root directory of the Node.js project.

    Returns:
        A list of suggested fixes.
    """
    try:
        with open(error_log, "r") as f:
            errors = f.read()

        # Load an open-source code generation model (e.g., flan-t5-small)
        # model_name = "google/flan-t5-small" 
        # model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        # tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        if use_local_model:
            model_name = "codellama/CodeLlama-7b-hf"  # Choose the appropriate size (7B, 13B, 34B)
            model = AutoModelForCausalLM.from_pretrained(model_name)
            tokenizer = AutoTokenizer.from_pretrained(model_name)

        suggestions = []
        for error in errors.splitlines():
            if 'error' in error:
                print(f'🟡 Suggestion for: {error}')
                code_snippet = get_code_snippet_around_error(project_dir, error)  # Function to get code snippet
                prompt = f"""
                **Error:** {error}
                **Code Snippet:**
                ```typescript
                {code_snippet} 
                ```
                **Instruction:** How can I resolve this error? 
                """
                print(f'🟢 Prompt: {prompt}')

                if use_local_model:

                    inputs = tokenizer(prompt, return_tensors="pt")
                    input_ids = inputs["input_ids"]
                    attention_mask = inputs["attention_mask"] 

                    output = model.generate(
                        input_ids=input_ids, 
                        attention_mask=attention_mask, 
                        max_new_tokens=100,  # Reduce for faster generation
                        num_beams=1,        # Reduce for faster generation
                        do_sample=True, 
                        temperature=0.1,   # Lower temperature for more focused output
                        top_p=0.9,         # Focus on higher probability tokens
                        # early_stopping=True 
                    )

                    suggestion = tokenizer.decode(output[0], skip_special_tokens=True)
                else:
                    try:
                        # Use GenerateText from google.cloud.ai_generativetext
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        response = model.generate_content(prompt)

                        suggestion = response.text
                        # ...
                    except Exception as e:
                        print(f"Error generating text with Gemini API: {e}")
                        suggestion = "Error generating suggestion from Gemini API."

                print(f'✨ Suggestion: {suggestion}')
                suggestions.append(suggestion)

        return suggestions

    except Exception as e:
        print(f"Error analyzing build errors: {e}")
        return []

def get_code_snippet_around_error(project_dir, error):
    """
    Extracts a relevant code snippet from the project files based on the error message.

    This is a simplified example and may need to be adapted based on your project's structure and error messages.

    Args:
        project_dir: Path to the root directory of the Node.js project.
        error: The error message.

    Returns:
        A code snippet related to the error.
    """
    try:
        # Extract the file path from the error message (e.g., "src/server.ts(15,3)")
        # file_path = error.split(":")[0].strip().split("(")[0]
        match = re.search(r'([^\s(]+)\(', error)
        file_path = match.group(1)


        # Read the contents of the file
        with open(f"{project_dir}/{file_path}", "r") as f:
            file_content = f.read()

        # Extract a code snippet around the line number (e.g., 5 lines before and after)
        match = re.search(r'\(([\d]+)', error)
        line_number = int(match.group(1))
        # line_number = int(error.split(":")[1].split(",")[0])
        start_line = max(0, line_number - 5)
        end_line = min(line_number + 5, len(file_content.splitlines()))
        lines = file_content.splitlines()[start_line:end_line]

        return "\n".join(lines)

    except Exception as e:
        print(f"Error extracting code snippet: {e}")
        return "" 

def update_package_json(project_dir):
  """
  Updates the package.json file with the latest versions of dependencies.

  Args:
      project_dir: Path to the root directory of the Node.js project.

  Returns:
      True if the update was successful, False otherwise.
  """
  try:
    with open(f"{project_dir}/package.json", "r") as f:
      package_json = json.load(f)

    # Get a list of all dependencies
    dependencies = package_json.get("dependencies", {})

    # Use `npm outdated` to get the latest versions in JSON format
    result = subprocess.run(
        ["npm", "outdated", "--json"],
        cwd=project_dir,
        capture_output=True,
        text=True
    )

    # Parse the output of `npm outdated`
    outdated_packages = json.loads(result.stdout)

    # Update dependencies with the latest versions
    for package_name, package_info in outdated_packages.items():
      if package_name in dependencies:
        dependencies[package_name] = package_info["latest"]

    # Write the updated dependencies back to package.json
    with open(f"{project_dir}/package.json", "w") as f:
      package_json["dependencies"] = dependencies
      json.dump(package_json, f, indent=2)

    return True
  except Exception as e:
    print(f"Error updating package.json: {e}")
    return False


# Set your Gemini API key
os.environ["GEMINI_API_KEY"] = "YOUR_GEMINI_API_KEY" 

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

project_dir = "../sample-nodejs"  # Replace with the actual project directory
use_local_model = False

if upgrade_dependencies(project_dir):
    if build_project(project_dir):
        # Assuming the build generates an error log file named "build_errors.log"
        error_log = f"{project_dir}/build_errors.log"
        suggestions = analyze_build_errors(error_log, project_dir)

        # Print or apply the suggested fixes (e.g., modify code files)
        for suggestion in suggestions:
            print(suggestion)