# local-gpt

## Prerequisite

### Use AWS Bedrock

- Have a valid AWS credentials to invoke Bedrock model

### Use Local Model running on Ollama

- Run `llama3` model locally using Ollama
  - install Ollama from [here](https://ollama.com/download)
  - Execute `ollama run llama3` (Ensure to have enough storage space and RAM locally)

## Deployment Commands

```sh

# Install required packages
make install

# run llama model locally
make run
```