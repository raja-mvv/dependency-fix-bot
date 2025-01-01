# Node.js Dependency Upgrade & AI Error Fixer

**Automate your Node.js dependency upgrades and build error resolution using AI-powered suggestions.**  
This script upgrades outdated dependencies in your Node.js project, runs the build process, logs errors, and provides AI-driven recommendations for fixing build issues.


## Features

- **Automate Dependency Upgrades:**  
  The script updates outdated dependencies in your `package.json` to their latest versions.

- **Build Error Detection:**  
  After upgrading dependencies, it runs the build process and captures any errors that occur.

- **AI-Powered Error Resolution:**  
  It uses AI models (such as CodeLlama or Google Gemini) to analyze build errors and suggest potential fixes.

- **Example Node.js Project:**  
  Includes a sample Node.js project to demonstrate how the script works.


## Prerequisites

Before running the script, you need to ensure the following:

- **Node.js** installed on your machine (version 14.x or higher recommended).
- **Python** installed (for running the script).
- **pip** to install Python dependencies.

Additionally, this script uses AI models, so you'll need an API key for **Google Gemini** or a pre-trained local model (e.g., CodeLlama).

---

## Setup Instructions

### 1. Clone the repository

First, clone this repository to your local machine:

### 2. Install Node.js dependencies for the example project

Navigate to the example Node.js project directory and install dependencies:

```bash
cd sample-nodejs
npm install
```

### 3. Install Python dependencies

This script requires Python packages for interacting with AI models. Install them using `pip`:

```bash
pip install transformers google-generativeai
```

### 4. Configure Google Gemini API Key (Optional)

If you're using the **Google Gemini** API for AI-powered suggestions, you will need to set up your API key.

Create a `.env` file in the root directory of the repository with the following content:

```
GEMINI_API_KEY=your_google_gemini_api_key
```

Alternatively, you can set the environment variable manually:

```bash
export GEMINI_API_KEY="your_google_gemini_api_key"
```

### 5. (Optional) Configure a Local AI Model

If you prefer to use a **local AI model** (such as CodeLlama), make sure to download the model and update the `use_local_model` variable in the script accordingly.

---

## Usage

Once you have everything set up, you can run the script to automatically upgrade dependencies and resolve any build errors.

### 1. Run the script

In the root directory of the repository, run the Python script as follows:

```bash
python upgrade_and_fix.py
```

This will:

- Upgrade outdated dependencies in your `package.json`.
- Run the build process (`npm run build`).
- If the build fails, it will analyze the errors and provide AI-powered suggestions for fixing them.

### 2. Example output

After running the script, you’ll see output like this:

```shell
➜  python upgrade_me.py

up to date, audited 84 packages in 496ms

14 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
Build failed! Errors:

> sample-nodejs@1.0.0 build
> npx tsc

src/server.ts(15,3): error TS2339: Property 'pluck' does not exist on type 'LoDashStatic'.

🟡 Suggestion for: src/server.ts(15,3): error TS2339: Property 'pluck' does not exist on type 'LoDashStatic'.
🟢 Prompt: 
                **Error:** src/server.ts(15,3): error TS2339: Property 'pluck' does not exist on type 'LoDashStatic'.
                **Code Snippet:**
                ```typescript
                app.listen(port, () => {
  var objects = [{ 'a': 1 }, { 'a': 2 }];

// in 3.10.1
_.pluck(objects, 'a'); // ➜ [1, 2]

  console.log(`Server listening on port ${port}`);
}); 
                ```
                **Instruction:** How can I resolve this error? 
                
✨ Suggestion: The error "Property 'pluck' does not exist on type 'LoDashStatic'" means you're using a Lodash version where `pluck` has been removed.  `pluck` was deprecated in Lodash 4.0 and removed entirely in later versions.

To resolve this, you need to replace `_.pluck` with the modern equivalent: `_.map`.

Here's the corrected code:
....
```

---

## Example Node.js Project

An example Node.js project is included in the `sample-nodejs` directory. You can modify this project, test the script, and see how it handles dependencies and build errors.

---

## How It Works

1. **Upgrade Dependencies:**  
   The script uses `npm outdated` to get a list of outdated dependencies and updates the `package.json` with their latest versions. Then it runs `npm install` to fetch the updated packages.

2. **Build Process:**  
   The script runs `npm run build` to build your project. If the build fails, the error logs are captured.

3. **AI Error Analysis:**  
   If build errors occur, the script sends them to an AI model (like CodeLlama or Google Gemini) for analysis. It generates possible fixes based on the error message and the surrounding code.

4. **Suggested Fixes:**  
   The AI provides suggestions such as code fixes or additional npm commands (e.g., `npm install` for missing dependencies).

---

## Next Steps

While this solution automates dependency upgrades and error analysis, there are many ways it could be improved:

1. **CI/CD Pipeline Integration:**  
   Integrate this script into your CI/CD pipeline to automatically open pull requests (PRs) with dependency upgrades and suggested fixes.

2. **AI-Powered Auto Fixing:**  
   In the future, you could enhance the script to automatically apply suggested fixes and create pull requests, streamlining the process even further.

3. **Model Customization:**  
   Fine-tune the AI model on your specific project to improve accuracy in error resolution and suggestions.

---

## Alternative Tools

There are other tools like **Dependabot** that automate dependency updates. However, this solution is different in that it doesn’t stop at upgrading libraries. It takes it a step further by identifying build issues and providing AI-driven suggestions for resolving those errors, making it a more comprehensive solution for maintaining your Node.js projects.

---

## Contributing

If you want to contribute to this project, feel free to fork the repository, submit issues, and create pull requests. Contributions are always welcome!

