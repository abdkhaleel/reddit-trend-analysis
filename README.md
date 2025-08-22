# Local Real-time Social Media Trend Analysis Pipeline

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Apache Beam](https://img.shields.io/badge/Apache%20Beam-2.52.0-orange?style=for-the-badge&logo=apache)
![spaCy](https://img.shields.io/badge/spaCy-3.7.2-brightgreen?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI2ZmZiIgZD0iTTEyIDJDNi40OCAMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyem0wIDE4Yy00LjQxIDAtOC0zLjU5LTgtOHMzLjU5LTggOC04IDggMy41OSA4IDgtMy41OSA4LTggOHptLTUuNS04YzAtLjgyLjgxLTEuNSAxLjgxLTEuNXMyLjE5LjY4IDIuMTkgMS41YzAgLjY1LS40NCAxLjE5LTEuMDUgMS40bC0xLjA0LjM1Yy0xLjU1LjUzLTEuNTIgMi4xMi0xLjUyIDIuMjVoMS41YzAtLjQxLjA2LTEuMDUtLjA5LTEuMTZsMS4xNi0uMzljLjgyLS4yOCAxLjQ4LS45NSAxLjQ4LTEuODVjMC0xLjM4LTEuNDYtMi41LTMuMjUtMi41UzYuNSAxMC42MiA2LjUgMTJ6bTYuNzUgNC4yNWMwIC40MS0uMzQgLjc1LS43NS43NVMxMS43NSAxNi42NiAxMS43NSAxNi4yNXYtMS41YzAtLjQxLjM0LS43NS43NS0uNzVzLjc1LjM0Ljc1Ljc1djEuNXoiLz48L3N2Zz4=)
![Pandas](https://img.shields.io/badge/Pandas-2.1.3-yellow?style=for-the-badge&logo=pandas)

> A complete, end-to-end data pipeline that runs entirely on a local machine. This project serves as a hands-on guide to understand the entire lifecycle of data—from ingestion and processing to analysis and visualization—without requiring any cloud services.

## 🏛️ Project Architecture

The pipeline is composed of three distinct stages, each simulating a component of a modern cloud-based data stack.



1.  **The Producer (`stream_to_file.py`)**
    *   **Action:** Ingests a real-time stream of comments from Reddit.
    *   **Output:** Writes raw data into `local_stream.txt`.
    *   **Simulates:** A message queue producer (Kafka, Pub/Sub).

2.  **The Processor (`process_stream.py`)**
    *   **Action:** Runs an Apache Beam pipeline locally to read the raw data, perform NLP enrichment (Sentiment & Entity Analysis), and filter out noise.
    *   **Output:** Writes structured, enriched data into `enriched_data.csv`.
    *   **Simulates:** A distributed ETL job (Spark, Dataflow) and a data warehouse (BigQuery).

3.  **The Analyzer & Visualizer (`visualize_trends.py`)**
    *   **Action:** Uses pandas to analyze the structured data and Matplotlib/Seaborn to generate visualizations.
    *   **Output:** Generates and displays three charts (`.png` files) revealing key trends.
    *   **Simulates:** A Business Intelligence (BI) tool (Looker Studio, Tableau).

---

## 🛠️ Tech Stack

| Category                | Technology / Library      |
| ----------------------- | ------------------------- |
| **Data Ingestion**      | `praw`                    |
| **Data Processing**     | `apache-beam`             |
| **NLP**                 | `spacy` & `textblob`      |
| **Data Analysis**       | `pandas`                  |
| **Data Visualization**  | `matplotlib` & `seaborn`  |
| **Environment Mgmt**    | `python-dotenv`           |

---

## 🚀 Get Started

Follow these steps to set up your local environment and run the pipeline.

### Prerequisites

*   Python 3.8 or higher
*   `pip` package installer

### 1. Clone and Set Up Environment

```bash
# Clone the repository
git clone https://github.com/abdkhaleel/reddit-trend-analysis.git
cd reddit-trend-analysis

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

Install all required Python libraries and the spaCy NLP model.

```bash
# Install libraries
pip install praw apache-beam spacy textblob pandas matplotlib seaborn python-dotenv

# Download spaCy model
python3 -m spacy download en_core_web_sm
```
> **Linux Users Note:** Matplotlib's interactive plots may require the `tkinter` library. If you encounter issues, install it with: `sudo apt-get install python3-tk`

---

## ⚙️ Configuration

To stream data from Reddit, you must provide your own API credentials.

1.  Go to **[Reddit's App Preferences](https://www.reddit.com/prefs/apps)** and create a new `script` type app. Use `http://localhost:8080` for the `redirect uri`.
2.  Create a file named **`.env`** in the project's root directory.
3.  Add your credentials to the file as shown below:

```ini
# .env file
REDDIT_CLIENT_ID="YOUR_CLIENT_ID_HERE"
REDDIT_CLIENT_SECRET="YOUR_CLIENT_SECRET_HERE"
REDDIT_USER_AGENT="Python:TrendAnalysis:v0.1 by u/YourUsername"
```
*(Remember to replace the placeholders with your actual credentials and username).*

---

## ▶️ How to Run the Pipeline

Execute the scripts sequentially in your terminal.

### Step 1: Run the Producer
This script will collect real-time data from Reddit.
```bash
python3 stream_to_file.py
```
Let it run for a few minutes to collect data, then stop it with `Ctrl+C`.
*   **Input:** Reddit API Stream
*   **Output:** `local_stream.txt`

### Step 2: Run the Processor
This script cleans, enriches, and structures the raw data.
```bash
python3 process_stream.py
```
*   **Input:** `local_stream.txt`
*   **Output:** `enriched_data.csv`

### Step 3: Run the Analyzer & Visualizer
This script analyzes the final data and generates plots.
```bash
python3 visualize_trends.py
```
*   **Input:** `enriched_data.csv`
*   **Output:** Three `.png` image files and interactive plot windows.

---

## 📊 Example Output

The final output consists of three insightful charts that tell a story about the data:

1.  **`sentiment_distribution.png`**: A histogram showing the overall public mood.
2.  **`top_entities.png`**: A bar chart of the most frequently mentioned topics.
3.  **`top_entities_sentiment.png`**: A bar chart revealing the average sentiment for each top topic.

---

## 🌟 Future Improvements

*   **Real Message Queue:** Replace the `.txt` file with a local Docker instance of Kafka or RabbitMQ.
*   **Real Database:** Replace the `.csv` output with a local SQLite or PostgreSQL database.
*   **Interactive Dashboard:** Rebuild the visualizer using Streamlit or Dash for a web-based, interactive experience.

## 📜 License

This project is licensed under the MIT License.
