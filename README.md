# OptiMind_Chat

# Book Chatbot Project Using QLoRA and LLaMA-3.1-8B

This project develops a domain-specific **Book Chatbot** by fine-tuning the **Meta-LLaMA-3.1-8B** model using the **QLoRA** technique on content extracted from *The LLM Engineers Handbook – Master the Art of Engineering Large Language Models* by Paul Iusztin and Maxime Labonne.
The system is deployed through a **FastAPI backend** and a **React frontend** for interactive conversational use.










### Dataset Preparation

* Used *The LLM Engineers Handbook* as the main data source.
* Extracted raw text from the PDF using `pdfplumber`.
* Cleaned the text by removing extra whitespace, formatting symbols, and page numbers.
* Tokenized the content and split it into manageable text chunks of approximately 1000 tokens each.
* Organized the processed text into a training and validation dataset for supervised fine-tuning.

---

### Model Selection and Quantized Fine-Tuning (QLoRA)

* Selected **Meta-LLaMA-3.1-8B** as the base model.
* Applied **Quantized Low-Rank Adaptation (QLoRA)** to fine-tune the model efficiently on limited GPU memory.
* Enabled 4-bit quantization and trained only low-rank adapter parameters rather than full model weights.
* Configured the LoRA setup with specific ranks, alpha, dropout, and target transformer layers.
* Used the **Supervised Fine-Tuning (SFT)** procedure from the `trl` library to train on the handbook text for several epochs.
* Monitored training progress with gradient accumulation and mixed-precision optimization for stability and performance.

---

### Merging the Trained Model

* After fine-tuning, merged the LoRA adapter weights into the base LLaMA model to produce a unified model checkpoint.
* The merged model became a self-contained version suitable for inference without external adapters.

---

### Model Inference and Testing

* Conducted inference tests to verify output quality.
* Used book-related prompts such as summarization, explanation of key concepts, and moral lessons.
* The model generated coherent, context-aware responses that accurately reflected the contents and principles discussed in the book.



### Backend Development (FastAPI)

* Built a **FastAPI** application to serve the fine-tuned model through a REST API.
* Created an endpoint `/generate` that accepts a text prompt and returns the model’s generated response.
* Implemented request-response handling, tokenization, and text generation within an inference context for efficiency.
* Added CORS middleware to enable frontend access.
* Verified the API using the automatically generated Swagger UI documentation.



### Frontend Development (React)

* Designed a **React** web interface for real-time interaction with the chatbot.
* Developed a clean chat layout with user and assistant message bubbles.
* Implemented typing animations to indicate the model’s response generation.
* Added a custom title, favicon, and a bot avatar for branding consistency.
* Connected the frontend to the backend API using Axios for HTTP requests.

