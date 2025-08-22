import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import json
from textblob import TextBlob
import spacy
import time 

INPUT_FILE = "local_stream.txt"
OUTPUT_CSV_FILE = "enriched_data.csv"

class AnalyzeTextDoFn(beam.DoFn):
    def __init__(self):
        self.nlp = None

    def setup(self):
        self.nlp = spacy.load("en_core_web_sm")

    def process(self, element):
        try:
            comment_data = json.loads(element)
            text = comment_data.get("text", "")
            created_at = comment_data.get("created_at", "")
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity

            doc = self.nlp(text)

            entities = ", ".join([f"{ent.text} ({ent.label})" for ent in doc.ents])

            yield {
                "created_at": created_at,
                "text": text,
                "polarity": polarity,
                "subjectivity": subjectivity,
                "entities": entities,
                "processing_timestamp": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            }

        except Exception as e:
            print(f"Error processing element: {e}")


def format_as_csv(element):
    text_cleaned = element['text'].replace('\n', ' ').replace('"', '""')
    entities_cleaned = element['entities'].replace('"', '""')

    return {
        f"{element['created_at']},"
        f"\"{text_cleaned}\","
        f"{element['polarity']},"
        f"{element['subjectivity']},"
        f"\"{entities_cleaned}\","
        f"{element['processing_timestamp']}"
    }

if __name__ == "__main__":
    print("Starting Apache Beam processing pipeline")

    options = PipelineOptions()

    csv_header = "created_at,text,polarity,subjectivity,entities,processing_timestamp"

    with beam.Pipeline(options=options) as p:
        (
            p
            | "ReadLines" >> beam.io.ReadFromText(INPUT_FILE)
            | "AnalyzeText" >> beam.ParDo(AnalyzeTextDoFn())
            | "FormatToCsv" >> beam.Map(format_as_csv)
            | "WriteCsv" >> beam.io.WriteToText(OUTPUT_CSV_FILE, header=csv_header, shard_name_template='')
        )
    print(f"Pipeline finished. Enriched data saved to {OUTPUT_CSV_FILE}")