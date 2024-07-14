# OllamaStraicoAPIProxy

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Supported-brightgreen.svg)

## Project Description

OllamaStraicoAPIProxy implements the same Ollama API endpoints but redirects the requests to the Straico API Server. 
This allows you to use any application that supports Ollama while leveraging Straico's available cloud LLM models instead of running a local LLM.

**Disclaimer:** This is not an official Ollama or Straico product.

## Prerequisites

- Docker
- Docker Compose

### 1. Install Docker

Follow the official Docker installation guide for your operating system:

- [Install Docker on Windows](https://docs.docker.com/desktop/install/windows-install/)
- [Install Docker on macOS](https://docs.docker.com/desktop/install/mac-install/)
- [Install Docker on Linux](https://docs.docker.com/engine/install/)

### 2. Install Docker Compose

Docker Compose is included with Docker Desktop for Windows and macOS. For Linux, follow the [official installation guide](https://docs.docker.com/compose/install/).


## Deploy

### Standalone

Open command prompt or terminal app and execute the command below.

Please change the `K0-1111111111111111` with your actual straico api key. 
``` bash
$ docker container run -e STRAICO_API_KEY=K0-1111111111111111 -p 3214:3214 -d ghcr.io/jayrinaldime/ollama-straico-apiproxy:latest
```
This code runs a Docker container with the following specifications:

1. Sets an environment variable STRAICO_API_KEY with the value K0-1111111111111111
2. Maps port 3214 on the host to port 3214 in the container
3. Runs the container in detached mode
4. Uses the image ghcr.io/jayrinaldime/ollama-straico-apiproxy:latest

### Docker Compose 

1. Create a folder anywhere 
1. Inside the folder create a file named **docker-compose.yml**
1. In docker-compose.yml file set the following content 
   
   ``` yaml
   ---
   services:
      straico_proxy:
         image: ghcr.io/jayrinaldime/ollama-straico-apiproxy
         ports:
            - 3214:3214
         environment:
            STRAICO_API_KEY: K0-1111111111111111
         restart: always

   ```
   * Please change the `K0-1111111111111111` with your actual straico api key. 
1. open console / terminal app and navigate to the created folder in step #1 
1. Execute command
   
   ```bash
   docker-compose up -d
    ```

   * This command will download docker image and start the container in detached mode.

## Usage

Once the container is running, you can use any Ollama-compatible application by pointing it to `http://localhost:3214` (or the appropriate host and port if you've modified the configuration).

## API Endpoints

List and describe the main API endpoints here.

### Ollama 
   1. /api/generate
   1. /api/chat
   1. /api/tags

### LM Studio
   1. /v1/chat/completions 
      * alias: /chat/completions
   1. /v1/completions
   1. /v1/models 

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

Please note that while these integrations have been tested, you may need to adjust settings or configurations to point to your OllamaStraicoAPIProxy instance instead of a local Ollama installation.

## To-Do List 

1. Ensure integration with:
   - [aider.chat](https://aider.chat/)
   
## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Ollama](https://github.com/ollama/ollama)
- [Straico](https://www.straico.com/)
