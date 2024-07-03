# Generating-Synthetic-Data-Using-AI-Agents-with-Claude-and-Docker

This project demonstrates how to create AI agents using Claude AI and Docker to generate synthetic data. It was developed as a learning exercise, following the tutorial by David Ondrej

## Project Overview

This project consists of two main AI agents:

1. Analyzer Agent: Analyzes the structure and patterns of a given CSV dataset.
2. Generator Agent: Generates new CSV rows based on the analysis results and sample data.

The agents are containerized using Docker for easy deployment and scalability.

## Prerequisites

- Docker
- Python 3.12
- Anthropic API key

## Project Structure

- `agents.py`: Main script containing the Analyzer and Generator agents.
- `prompts.py`: Contains the system and user prompts for the AI agents.
- `Dockerfile`: Instructions for building the Docker container.
- `requirements.txt`: List of Python dependencies.
- `.env`: Configuration file for storing the Anthropic API key. [Not a part of this Github Repo]
- `.dockerignore`: Specifies files and directories to be excluded from the Docker build.

## Setup and Installation

1. Create a `.env` file in the project root and add your Anthropic API key:

   ```powershell
   ANTHROPIC_API_KEY=your_api_key_here
   ```

## Building the Docker Image

Build the Docker image using the following command:

```powershell
docker build -t claude-docker-ai-agents .
```

## Running the Docker Container

To run the Docker container you can either provide the directory directly or create a docker volume to map to the image to your currect directory :

1. Mapping to absolute path: [Replace `"path/to/your/data/directory"` with the actual path to your data directory.]

```powershell
$path = "path/to/your/data/directory"
docker run -it `
    --rm `
    -v "${path}:/app/data" `
    -e ANTHROPIC_API_KEY `
    --name ai-agents-container `
    claude-docker-ai-agents
```

2. Mapping as a docker volume to current directory:

```powershell
docker run -it `
    --rm `
    -v "${PWD}/data:/app/data" `
    -e ANTHROPIC_API_KEY `
    --name ai-agents-container `
    claude-docker-ai-agents
```

## Usage

1. When prompted, enter your Anthropic API key.
2. Enter the name of your CSV file (which should be placed in the data directory you specified).
3. Specify the number of rows you want to generate.
4. The script will analyze your data and generate new rows based on the patterns it identifies.
5. The output will be saved in `/app/data/output.csv`.

## Publishing to Docker Hub

If you want to publish your Docker image to Docker Hub:

1. Log in to Docker Hub:

   ```powershell
   docker login
   ```
2. Tag your image:

   ```powershell
   docker tag claude-docker-ai-agents your-dockerhub-username/claude-data-gen-agent:latest
   ```
3. Push the image to Docker Hub:

   ```
   docker push your-dockerhub-username/claude-data-gen-agent:latest
   ```

## Using the Published Docker Image

To use the published Docker image:

1. Pull the image from Docker Hub:

   ```powershell
   docker pull your-dockerhub-username/claude-data-gen-agent:latest
   ```
2. Run the container:

   ```powershell
   $path = "path/to/your/data/directory"
   docker run -it `
       --rm `
       -v "${path}:/app/data" `
       -e ANTHROPIC_API_KEY `
       --name ai-agents-container `
       your-dockerhub-username/claude-data-gen-agent
   ```

## Refer Documentation folder for more details on working example

## Acknowledgements

This project was created following the tutorial by [David Ondrej](https://www.youtube.com/watch?v=AhPXGKG4RZ4).

## License

MIT License
