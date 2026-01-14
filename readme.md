Cornell Dialog Sentiment Annotator

A Full-Stack Data Pipeline & Annotation Tool

📌 Project Overview

This project is a comprehensive end-to-end pipeline designed to create a high-quality, granular sentiment dataset based on the Cornell Movie-Dialogs Corpus.

Unlike standard sentiment analysis (which classifies text as simply "Positive" or "Negative"), this tool facilitates the annotation of interpersonal dynamics on a continuous scale from -1.0 (Hostile/Disengagement) to +1.0 (Supportive/Engagement).

The project consists of two main components:

The ETL Pipeline: A robust backend (DataCleaner, DataProvider) that ingests raw, unstructured corpus data, repairs integrity errors, and restructures it for analysis.

The Annotation Interface: A PySide6-based GUI optimized for high-throughput manual annotation, featuring context-aware visualization and I/O optimization.

🚀 Key Features & Technical Highlights

1. Robust Data Pipeline (ETL)

Automated Cleaning: The DataCleaner class handles parsing errors common in raw text corpora (e.g., bad delimiters, missing fields) and performs referential integrity checks between movie_lines and movie_conversations.A

Structured Storage: Converts monolithic raw files into a file-per-conversation structure. This architecture allows for:

Lazy Loading: Only required data is loaded into RAM.

Scalability: Can handle datasets larger than available memory.

Parallelism: Future-proofed for multiple annotators working on different files.

2. Advanced Annotation GUI

Context-Aware: Displays a rolling window of 4 dialogue lines with distinct character color-coding, ensuring annotators understand the flow of conversation, not just isolated sentences.

Granular Annotation: Uses a slider-based interface for precise float-point annotation (-1.0 to +1.0).

State Management: Implements a "Dirty Flag" architecture to track unsaved changes, ensuring zero data loss while preventing redundant file writes.

3. Performance Optimization

Differential Saving (Delta Updates): The application tracks exactly which sliders have been modified using NumPy boolean masks. When saving, only the specific changed rows are written to the disk.

Impact: Reduces disk I/O by up to 75% during typical usage.

Gatekeeper Pattern: Navigation functions (Next/Previous) automatically trigger valid saves only when necessary, creating a seamless, lag-free user experience.

🛠️ Architecture

Directory Structure

├── raw_data/              # Original Cornell Movie-Dialogs Corpus
├── data_set/              # Processed Structured Data
│   ├── conversations/     # Individual conversation TSVs
│   ├── stats/             # Corresponding annotation metadata
│   └── data_stat.tsv      # Global index and progress tracker
├── src/
│   ├── data_loading.py    # Backend: DataProvider & DataCleaner logic
│   ├── main.py            # Frontend: PySide6 Application Controller
│   ├── conversation_page.py # UI Component: Message rendering logic
│   └── ...
├── requirements.txt       # Project dependencies
└── README.md              # Project documentation



The Pipeline Flow

Ingestion: DataCleaner reads raw .txt files, repairing malformed lines.

Transformation: DataProvider joins lines with conversation metadata and creates a normalized schema.

Annotation: The GUI loads a conversation chunk. User inputs are captured in memory.

Persistence: On navigation, the save_current() method filters for modified data and performs a batch update to the specific stats_X.tsv file.

💻 Installation & Usage

Prerequisites

Python 3.8+

Setup

Clone the repository:

git clone [https://github.com/yourusername/cornell-sentiment-annotator.git](https://github.com/yourusername/cornell-sentiment-annotator.git)



Install the required dependencies:

pip install -r requirements.txt



Place the Cornell Movie-Dialogs Corpus files in ./raw_data/archive/.

Running the Tool

python main.py



First Run: The tool will automatically detect raw data, run the cleaning pipeline (this may take a moment), and generate the structured dataset.

Subsequent Runs: The tool launches instantly, loading the last saved state.

📊 Data Format

The output annotations are stored in tab-separated values (TSV) with the following schema:

Column          Type    Description
-----------------------------------------------------------
id              int     Conversation ID
lines_index     int     Index of the line within the conversation
connotation     float   Annotated value (-1.0 to 1.0)


📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

Built to demonstrate advanced data handling patterns and efficient GUI application architecture in Python.