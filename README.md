# Ollama Straico API Proxy

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Supported-brightgreen.svg)
[![Build and Push Docker Images](https://github.com/jayrinaldime/ollama-straico-apiproxy/actions/workflows/docker-image.yml/badge.svg)](https://github.com/jayrinaldime/ollama-straico-apiproxy/actions/workflows/docker-image.yml)

## Project Description

StraicoAPIProxy implements the same API endpoints but redirects the requests to the Straico API Server. 
We now support Ollama, LMStudio/OpenAI and Anthropic Claude API Endpoints.

This allows you to use any application that supports Ollama, LMStudio/OpenAI and Anthropic Claude while leveraging Straico's available cloud LLM models instead of running a local LLM.

**Disclaimer:** This is not an official Ollama or Straico product.

## Setup 

Please follow the [Setup Guide](https://github.com/jayrinaldime/ollama-straico-apiproxy/wiki/Deployment-Ollama%E2%80%90straico%E2%80%90apiproxy#basic-deployment).

## Usage

Once the container is running, you can use any Ollama-compatible application by pointing it to `http://localhost:11434` (or the appropriate host and port if you've modified the configuration).

## API Endpoints

List and describe the main API endpoints here.

### Ollama 
   1. /api/generate
   1. /api/chat
   1. /api/tags
   1. /api/embeddings
### LM Studio
   1. /v1/chat/completions 
      * alias: /chat/completions
   1. /v1/completions
   1. /v1/models 
   1. /v1/embeddings
### OpenAI
   1. /v1/chat/completions 
   1. /v1/audio/speech
   1. /v1/images/generations
### Anthopic Claude
   1. /v1/messages
      
## Known Working Integrations

OllamaStraicoAPIProxy has been tested and confirmed to work with the following applications and integrations:

1. **Home Assistant**
   - Integration: [Ollama for Home Assistant](https://www.home-assistant.io/integrations/ollama/)
   - Description: Use OllamaStraicoAPIProxy with Home Assistant for AI-powered home automation tasks.

1. **Logseq**
   - Plugin: [ollama-logseq](https://github.com/omagdy7/ollama-logseq)
   - Description: Integrate OllamaStraicoAPIProxy with Logseq for enhanced note-taking and knowledge management.

1. **Obsidian**
   - Plugin: [obsidian-ollama](https://github.com/hinterdupfinger/obsidian-ollama)
   - Description: Use OllamaStraicoAPIProxy within Obsidian for AI-assisted note-taking and writing.

1. **Snippety**
   - Website: [https://snippety.app/](https://snippety.app/)
   - Description: Leverage OllamaStraicoAPIProxy with Snippety for AI assisted snippet management and generation.

1. **Rivet** 
   - Website: [https://rivet.ironcladapp.com/](https://rivet.ironcladapp.com/)
   - Description: Allows using Ollama Chat and OpenAI Chat (via LM Studio)

1. **Continue.dev** 
   - Website: [https://www.continue.dev/](https://www.continue.dev/)
   - Description: Generate code using Ollama and LM Studio

1. **Open WebUI** 
   - Website: [https://docs.openwebui.com/](https://docs.openwebui.com/)
   - Description: Allows using Ollama with Open WebUI 
   - Sample Configuration: [docker-compose.yaml](https://gist.github.com/jayrinaldime/2f4442ded08c283249fbd3c568234173)

1. **Flowise** 
   - Website: [https://flowiseai.com/](https://flowiseai.com/)
   - Description: Allows using Ollama with Flowise
   - Sample Configuration: [docker-compose.yaml](https://gist.github.com/jayrinaldime/f17c8eec1fe75573d06147ffb7199535)

1. **Aider Chat** 
  - Website: [https://aider.chat/](https://aider.chat/)
  - Description: Pair Programming / Coding Assistant. 

1. **Cline** 
  - Website: [https://github.com/cline/cline](https://github.com/cline/cline)
  - Description: Pair Programming / Coding Assistant. 

1. **Enconvo** 
  - Website: [https://www.enconvo.com/](https://www.enconvo.com/)
  - Description: Desktop app

Please note that while these integrations have been tested, you may need to adjust settings or configurations to point to your OllamaStraicoAPIProxy instance instead of a local Ollama installation.

## To-Do List 

1. Add Tests
2. Add Documentation 
   
## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Ollama](https://github.com/ollama/ollama)
- [Straico](https://www.straico.com/)


## Referal Link to digitalocean 

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%201.svg)](https://www.digitalocean.com/?refcode=a2a1e461053d&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)
