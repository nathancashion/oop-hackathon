# Rad Report to Plain Language Converter

This repository is a fork of an [Out of Pocket Hackathon project](https://github.com/danielsamfdo/oop-hackathon) by Daniel Sam Pete Thiyago, shared with me by [James Leonard](https://github.com/Jleona12).

## Basics
The project uses OpenAI's GPT-3.5-turbo model to convert radiology reports into plain language summaries that are easier for patients to understand.

## Changes Made
I have updated the code to use either the OpenAI API or run locally with various models via Ollama. The user can choose the model to use by specifying it in the `model` variable.

I have also added error handling to manage potential issues during API calls or local model execution.

Finally, I have included new PDF examples of radiology reports. The intent is to be able to indicate the report file path as a command-line argument when running the script.

### Disclosure
The changes in this fork were vibe-coded using AI assistance from [Warp AI](https://app.warp.dev/referral/2RXNPM) and other AI tools in VS Code. Please review the code carefully to ensure it meets your requirements and standards.

