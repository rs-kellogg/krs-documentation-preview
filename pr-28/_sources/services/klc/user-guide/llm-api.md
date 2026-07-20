# LLM API Usage

## What Are LLM APIs?

LLM (Large Language Model) APIs provide programmatic access to advanced language models via the web. This allows researchers to automate interactions with models without running them locally. APIs can be called from Python, R, or other programming environments to support reproducible, scalable workflows.

## Best Practices

* **Reproducibility**: Log all prompts, parameters, and responses for version control.
* **Data Privacy**: Avoid sending sensitive or identifiable information to third-party APIs unless explicitly allowed. <span style="color: purple;"><strong>Follow your IRB and data governance policies.</strong></span>
* **Cost Awareness**: LLM APIs are typically usage-based (e.g., token-based billing). Keep track of your usage to avoid unexpected costs. <span style="color: purple;"><strong>Set a max billing limit for your API key.</strong></span>
* **Model Versioning**: Document which version/model you used (e.g., GPT-4 vs GPT-3.5) to ensure consistent results over time.
* **Set Up Testing**: Have tests to validate LLM outputs. LLMs may introduce errors, hallucinations, or biases.

## Popular LLM API List
* **OpenAI - GPT** – [https://platform.openai.com/docs/overview](https://platform.openai.com/docs/overview)
* **Anthropic - Claude** – [https://docs.anthropic.com/en/docs/get-started](https://docs.anthropic.com/en/docs/get-started)
* **Google - Gemini** – [https://ai.google.dev/gemini-api/docs/models](https://ai.google.dev/gemini-api/docs/models)
* **Groq - Cloud for AI Inference with Open Source Models** - [https://console.groq.com/docs/libraries](https://console.groq.com/docs/libraries) 

## API Workflow on KLC
- Step 1: Create a Conda Environment  
Start by creating an isolated Python environment using Conda to manage dependencies cleanly. See instructions [here](./klc-software.md).

- Step 2: Install Required API Packages  
Install the Python client libraries for the LLM API provider you’re using. 

- Step 3: Obtain and Store Your API Key Securely  
Avoid hardcoding your API key in scripts. Use environment variables or store it in a text file and load it in your script.

- Step 4: Write Your API Call Script

- Step 5: Run Script on the Cluster

- Step 6: Monitor and Log Responses  
Save outputs to files for reproducibility.

