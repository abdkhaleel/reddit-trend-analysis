import spacy

def check_entity_logic():
    print("Loading spaCy model 'en_core_web_sm'...")
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("Error: Model 'en_core_web_sm' not found.")
        print("Please run 'python -m spacy download en_core_web_sm' in your terminal.")
        return
        
    print("Model loaded successfully.\n")

    sample_sentences = [
        "Apple is releasing the first iPhone 15 in September for $999.",
        "The top two companies are Google and Microsoft.",
        "One of the best programming languages is Python.",
        "The event is happening today at 4pm.",
        "Khaleel is learning about data pipelines in Germany.",
    ]

    UNWANTED_ENTITY_LABELS = {
        "CARDINAL", "ORDINAL", "DATE", "TIME", "MONEY", "PERCENT", "QUANTITY"
    }
    
    for i, sentence in enumerate(sample_sentences):
        print(f"--- Processing Sentence {i+1} ---")
        print(f"Text: \"{sentence}\"")
        
        doc = nlp(sentence)
        
        print("\n  1. All Entities Found by spaCy:")
        if not doc.ents:
            print("     - No entities found.")
        else:
            for ent in doc.ents:
                print(f"     - Found: '{ent.text}'  (Label: {ent.label_})")

        good_entities = [ent for ent in doc.ents if ent.label_ not in UNWANTED_ENTITY_LABELS]

        print("\n  2. Filtered Entities (Our 'Good Topics'):")
        if not good_entities:
            print("     - No good topics found after filtering.")
        else:
            for ent in good_entities:
                print(f"     - Kept: '{ent.text}'  (Label: {ent.label_})")
        
        print("-" * (len(sentence) + 4) + "\n")


if __name__ == "__main__":
    check_entity_logic()