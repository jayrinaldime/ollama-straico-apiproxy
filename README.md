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

## Installation

### 1. Install Docker

Follow the official Docker installation guide for your operating system:

- [Install Docker on Windows](https://docs.docker.com/desktop/install/windows-install/)
- [Install Docker on macOS](https://docs.docker.com/desktop/install/mac-install/)
- [Install Docker on Linux](https://docs.docker.com/engine/install/)

### 2. Install Docker Compose

Docker Compose is included with Docker Desktop for Windows and macOS. For Linux, follow the [official installation guide](https://docs.docker.com/compose/install/).

### 3. Clone the Repository

```bash
git clone https://github.com/jayrinaldime/OllamaStraicoAPIProxy.git
cd OllamaStraicoAPIProxy
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and add the necessary environment variables:

```
STRAICO_API_KEY=your_straico_api_key
```

### 5. Build and Run the Project

Use Docker Compose to build and run the project:

```bash
docker-compose up -d
```

This command will build the Docker image and start the container in detached mode.

## Usage

Once the container is running, you can use any Ollama-compatible application by pointing it to `http://localhost:3214` (or the appropriate host and port if you've modified the configuration).

## API Endpoints

List and describe the main API endpoints here.


## To-Do List 

1. Add Docker Image to GitHub Container Registry
   - Create a workflow to build and push the Docker image
   - Update readme with instructions to pull the image

2. Ensure integration with:
   - [continue.dev](https://www.continue.dev/)
   - [aider.chat](https://aider.chat/)

## Known Working Integrations

OllamaStraicoAPIProxy has been tested and confirmed to work with the following applications and integrations:

1. **Home Assistant**
   - Integration: [Ollama for Home Assistant](https://www.home-assistant.io/integrations/ollama/)
   - Description: Use OllamaStraicoAPIProxy with Home Assistant for AI-powered home automation tasks.

2. **Logseq**
   - Plugin: [ollama-logseq](https://github.com/omagdy7/ollama-logseq)
   - Description: Integrate OllamaStraicoAPIProxy with Logseq for enhanced note-taking and knowledge management.

3. **Obsidian**
   - Plugin: [obsidian-ollama](https://github.com/hinterdupfinger/obsidian-ollama)
   - Description: Use OllamaStraicoAPIProxy within Obsidian for AI-assisted note-taking and writing.

4. **Snippety**
   - Website: [https://snippety.app/](https://snippety.app/)
   - Description: Leverage OllamaStraicoAPIProxy with Snippety for improved code snippet management and generation.

Please note that while these integrations have been tested, you may need to adjust settings or configurations to point to your OllamaStraicoAPIProxy instance instead of a local Ollama installation.


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Ollama](https://github.com/ollama/ollama)
- [Straico](https://www.straico.com/)
