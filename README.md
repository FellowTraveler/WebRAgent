# 🔍 WebRAgent

A Retrieval-Augmented Generation (RAG) web application built with Flask and Qdrant.

© 2024 Dennis Kruyt. All rights reserved.

## 📋 Overview

This application implements a RAG system that combines the power of Large Language Models (LLMs) with a vector database (Qdrant) to provide context-enhanced responses to user queries. It features:

- 💬 User query interface for asking questions
- 🔐 Admin interface for managing document collections
- 📄 Document processing and embedding
- 🤖 Integration with multiple LLM providers (OpenAI, Claude, Ollama)

## ✨ Features

- 🖥️ **User Interface**: Clean, intuitive interface to submit queries and receive LLM responses
- 🌐 **Web Search**: Search the web directly using SearXNG integration with LLM result interpretation
- 🤖 **Agent Search**: Break down complex questions into sub-queries for more comprehensive answers
- 🧠 **Mind Maps**: Visualize response concepts with automatically generated mind maps
- 🔎 **Vector Search**: Retrieve relevant document snippets based on semantic similarity
- 👤 **Admin Interface**: Securely manage collections and upload documents
- 📝 **Document Processing**: Automatically extract text, chunk, embed, and store documents
- 🧠 **Multiple LLM Support**: Configure your preferred LLM provider (OpenAI, Claude, Ollama)
- 🔍 **Dynamic Embedding Models**: Automatically detects and uses available embedding models from all configured providers

## 📋 Prerequisites

- 🐍 Python 3.8+
- 🗄️ [Qdrant](https://qdrant.tech/documentation/quick-start/) running locally or remotely
- 🔑 API keys for your chosen LLM provider

## 🚀 Installation

### 💻 Option 1: Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dkruyt/WebRAgent.git
   cd WebRAgent
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the example environment file and configure it with your settings:
   ```bash
   cp .env.example .env
   ```

   Then edit the `.env` file with your preferred settings. Here are the key settings to configure:
   ```
   # API Keys for LLM Providers (uncomment and add your keys for the providers you want to use)
   # At least one provider should be configured
   #OPENAI_API_KEY=your_openai_api_key_here
   #CLAUDE_API_KEY=your_claude_api_key_here
   
   # Ollama Configuration (uncomment to use Ollama)
   #OLLAMA_HOST=http://localhost:11434
   
   # Qdrant Configuration
   QDRANT_HOST=localhost
   QDRANT_PORT=6333
   
   # SearXNG Configuration
   SEARXNG_URL=http://searxng:8080
   
   # Flask Secret Key (generate a secure random key for production)
   FLASK_SECRET_KEY=change_me_in_production
   
   # Admin User Configuration
   ADMIN_USERNAME=admin
   ADMIN_PASSWORD=change_me_in_production
   ```

   Note: The system will automatically detect and use models from the providers you've configured:
   
   - If you set OPENAI_API_KEY, it will use OpenAI models for both LLM and embeddings
   - If you set CLAUDE_API_KEY, it will use Claude models for LLM
   - If you set OLLAMA_HOST, it will use Ollama models for both LLM and embeddings
   - Sentence Transformers will be used as fallback embedding models
   
   There's no need to manually specify which models to use - the system dynamically detects available models.

5. Make sure you have Qdrant running locally or specify a remote instance in the `.env` file.

6. If using Ollama, make sure it's running locally or specify a remote instance in the `.env` file.

7. Start the application:
   ```bash
   python run.py
   ```

8. Access the application at `http://localhost:5000`

### 🐳 Option 2: Docker Installation

This project includes Docker and Docker Compose configurations for easy deployment.

1. Clone the repository:
   ```bash
   git clone https://github.com/dkruyt/WebRAgent.git
   cd WebRAgent
   ```

2. Start the application with Docker Compose:
   ```bash
   docker-compose up -d
   ```

3. The following services will be available:
   - 🌐 RAG Web Application: http://localhost:5000
   - 📊 Qdrant Dashboard: http://localhost:6333/dashboard
   - 🔍 SearXNG Search Engine: http://localhost:8080

4. To shut down the application:
   ```bash
   docker-compose down
   ```

### 📥 Pre-downloading Ollama Models

If you want to pre-download the Ollama models before starting the application:

```bash
# For main LLM models
ollama pull llama2
ollama pull mistral
ollama pull gemma

# For embedding models
ollama pull nomic-embed-text
ollama pull all-minilm
```

The system will automatically detect these models if they're available in your Ollama installation.

## 📖 Usage

### 🔍 User Interface
1. Navigate to the home page
2. Choose your search method:
   - **Document Search**: Select a collection from the dropdown
   - **Web Search**: Toggle the "Web Search" option
3. Enter your query in the text box
4. Configure additional options (optional):
   - **Generate Mind Map**: Toggle to visualize concepts related to your query
   - **Agent Search**: Enable for complex questions that benefit from being broken down
   - **Number of Results**: Adjust how many results to retrieve
5. Submit your query and view the response
6. Explore source documents or web sources that informed the answer

### 🌐 Web Search
1. Toggle the "Web Search" option on the main interface
2. Enter your query
3. The system will:
   - Search the web using SearXNG
   - Use an LLM to interpret and synthesize the search results
   - Present a comprehensive answer along with source links

### 🤖 Agent Search
1. Enable the "Agent Search" checkbox
2. Choose a strategy:
   - **Direct Decomposition**: Breaks down your question into targeted sub-queries
   - **Informed Decomposition**: Gets initial results first, then creates follow-up queries
3. Submit your query to receive a comprehensive answer synthesized from multiple search operations

### 👤 Admin Interface
1. Login with admin credentials (default: username `admin`, password `admin123`)
2. Create new collections from the admin dashboard
3. Upload documents to collections
4. Documents are automatically processed and made available for retrieval

## 🛠️ Technical Implementation

- 🌐 **Flask**: Web framework for the application
- 🗄️ **Qdrant**: Vector database for storing and retrieving document embeddings
- 🔍 **SearXNG**: Self-hosted search engine for web search capabilities
- 🤖 **Agent Framework**: Custom implementation for query decomposition and synthesis
- 🧠 **Mind Map Generation**: Visualization system for query responses
- 🔤 **Embedding Models**:
  - **SentenceTransformers**: Local embedding models (always available as fallback)
  - **OpenAI Embeddings**: High-quality embeddings when API key is configured
  - **Ollama Embeddings**: Local embedding models when Ollama is configured
- 🔌 **Model Management**: Dynamic provider detection and configuration based on available environment variables
- 🔐 **Flask-Login**: For admin authentication
- 📚 **Python Libraries**: For document processing (PyPDF2, BeautifulSoup, etc.)
- 📄 **Docling**: Advanced document processing capability for extracting text from various file formats

## 📂 Project Structure

```
WebRAgent/
├── app/
│   ├── models/             # Data models
│   │   ├── chat.py         # Chat session models
│   │   ├── collection.py   # Document collection models
│   │   ├── document.py     # Document models and metadata
│   │   └── user.py         # User authentication models
│   ├── routes/             # Route handlers
│   │   ├── admin.py        # Admin interface routes
│   │   ├── auth.py         # Authentication routes
│   │   ├── chat.py         # Chat interface routes
│   │   └── main.py         # Main application routes
│   ├── services/           # Business logic
│   │   ├── agent_search_service.py     # Query decomposition and agent search
│   │   ├── chat_service.py             # Chat session management
│   │   ├── claude_service.py           # Anthropic Claude integration
│   │   ├── document_service.py         # Document processing
│   │   ├── llm_service.py              # LLM provider abstraction
│   │   ├── mindmap_service.py          # Mind map generation
│   │   ├── model_service.py            # Dynamic model management
│   │   ├── ollama_service.py           # Ollama integration
│   │   ├── openai_service.py           # OpenAI integration
│   │   ├── qdrant_service.py           # Vector database operations
│   │   ├── rag_service.py              # Core RAG functionality
│   │   ├── searxng_service.py          # Web search integration
│   │   └── web_search_agent_service.py # Web search with agent capabilities
│   ├── static/             # CSS, JS, and other static files
│   ├── templates/          # Jinja2 templates
│   └── __init__.py         # Flask application factory
├── data/                   # Created at runtime for data storage
│   ├── collections/        # Collection metadata storage
│   ├── documents/          # Document metadata storage
│   ├── models/             # Model configuration storage
│   │   ├── config.json     # Dynamic model configuration
│   │   └── dimensions.json # Embedding model dimensions
│   └── uploads/            # Uploaded document files
├── searxng/                # SearXNG configuration
├── .dockerignore           # Files to exclude from Docker build
├── .env                    # Environment variables
├── .env.example            # Example environment file
├── .gitignore              # Git ignore patterns
├── docker-compose.yml      # Docker Compose config
├── docker-compose.gpu.yml  # Docker Compose config with GPU support
├── Dockerfile              # Docker build instructions
├── requirements.txt        # Project dependencies
├── README.md               # Project documentation
└── run.py                  # Application entry point
```

## 🔒 Security Notes

- ⚠️ This application uses a simple in-memory user store for demo purposes
- 🛡️ In a production environment, use a proper database with password hashing
- 🔐 Configure HTTPS for secure communication
- 🔑 Set a strong, unique `FLASK_SECRET_KEY`
- 🚫 Do not expose admin routes to the public internet without proper security

## 📜 License

MIT

## 📝 Copyright

© 2024 Dennis Kruyt. All rights reserved.

## 🙏 Acknowledgements

- 🗄️ [Qdrant](https://qdrant.tech/)
- 🔤 [SentenceTransformers](https://www.sbert.net/)
- 🌐 [Flask](https://flask.palletsprojects.com/)
- 📄 [Docling](https://github.com/doclingjs/docling)
- 🔍 [SearXNG](https://docs.searxng.org/)
- 🤖 [OpenAI](https://openai.com/)
- 🧠 [Anthropic](https://www.anthropic.com/)
- 🦙 [Ollama](https://ollama.ai/)