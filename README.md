<!-- markdownlint-disable-file MD033 -->

# MCP Goodnews

---

[![CodeQL](https://github.com/VectorInstitute/mcp-goodnews/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/VectorInstitute/mcp-goodnews/actions/workflows/github-code-scanning/codeql)
[![Linting](https://github.com/VectorInstitute/mcp-goodnews/actions/workflows/lint.yml/badge.svg)](https://github.com/VectorInstitute/mcp-goodnews/actions/workflows/lint.yml)
[![Unit Testing and Upload Coverage](https://github.com/VectorInstitute/mcp-goodnews/actions/workflows/unit_test.yml/badge.svg)](https://github.com/VectorInstitute/mcp-goodnews/actions/workflows/unit_test.yml)
[![codecov](https://codecov.io/github/VectorInstitute/mcp-goodnews/graph/badge.svg?token=KvwFM5bQiH)](https://codecov.io/github/VectorInstitute/mcp-goodnews)
[![Release](https://github.com/VectorInstitute/mcp-goodnews/actions/workflows/release.yml/badge.svg)](https://github.com/VectorInstitute/mcp-goodnews/actions/workflows/release.yml)
![GitHub License](https://img.shields.io/github/license/VectorInstitute/mcp-goodnews)

<p align="center">
  <img src="https://d3ddy8balm3goa.cloudfront.net/vector-mcp-goodnews/logo.svg" alt="MCP Goodnews Logo" width="400"/>
</p>

MCP Goodnews is a simple Model Context Protocol (MCP) application that features
a server for getting good, positive, and uplifting news. This tool fetches news
articles from the [NewsAPI](https://newsapi.org/) and uses a Cohere LLM to rank
and return the top news articles based on positive sentiment.

## Motivation

In a world where negative news often dominates headlines, Goodnews MCP aims to
shine a light on more positive and uplifting news stories. This project was
inspired by an earlier initiative called GoodnewsFirst, which delivered positive
news daily to email subscribers — it was a really awesome project! While GoodnewsFirst
predated recent breakthroughs in Large Language Models (LLMs) and relied on
traditional methods for sentiment ranking, Goodnews MCP leverages modern LLMs to
perform sentiment analysis in a zero-shot setting.

## Example Usage: MCP Goodnews with Claude Desktop

<img width="1112" alt="image" src="https://github.com/user-attachments/assets/fe204338-7505-4ce5-91b8-0b0b611099e1" />

### Requirements

- [Cohere API Key](https://dashboard.cohere.com/)
- [NewsAPI Key](https://newsapi.org/)
- [Claude Desktop Application](https://claude.ai/download)
- [uv Python Project and Package Manager](https://docs.astral.sh/uv/getting-started/installation/)

### Clone `mcp-goodnews`

```bash
# Clone the repository
git clone https://github.com/username/mcp-goodnews.git
```

In the next step, we'll need to provide the absolute path to the location of this
cloned repository.

### Update Claude Desktop Config to find mcp-goodnews

#### For Mac/Linux

```bash
# Navigate to the configuration directory
cd ~/Library/Application\ Support/Claude/config

# Edit the claude_desktop_config.json file
nano claude_desktop_config.json
```

#### For Windows

```bash
# Navigate to the configuration directory
cd %APPDATA%\Claude\config

# Edit the claude_desktop_config.json file
notepad claude_desktop_config.json
```

And you'll want to add an entry under `mcpServers` for `Goodnews`:

```json
{
  "mcpServers": {
    "Goodnews": {
      "command": "<absolute-path-to-bin>/uv",
      "args": [
        "--directory",
        "<absolute-path-to-cloned-repo>/mcp-goodnews/src/mcp_goodnews",
        "run",
        "server.py"
      ],
      "env": {
        "NEWS_API_KEY": "<newsapi-api-key>",
        "COHERE_API_KEY": "<cohere-api-key>"
      }
    }
  }
}
```

### Start or Restart Claude Desktop

Claude Desktop will use the updated config to build and run the mcp-goodnews server.
If successful, you will see the hammer tool in the bottom-right corner of the chat
dialogue window.

<img width="749" alt="image" src="https://github.com/user-attachments/assets/f871451b-cd66-4a75-bdde-35220e485203" />

Clicking the hammer tool icon will bring up a modal that lists available MCP tools.
You should see `fetch_list_of_goodnews` listed there.

<img width="505" alt="image" src="https://github.com/user-attachments/assets/d68bef03-0926-4ae9-8b4a-00a003097169" />


### Ask Claude for Good News!

Example prompts:

- "Show me some good news from today."
- "What positive things happened in the world this week?"
- "Give me uplifting news stories about science."

## How It Works

1. When you request good news, the application queries the NewsAPI for recent articles
2. The Cohere LLM analyzes the sentiment of each article
3. Articles are ranked based on positive sentiment score
4. The top-ranking good news stories are returned to you through Claude

## License

[Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0)

---

_Stay positive with Goodnews MCP!_
