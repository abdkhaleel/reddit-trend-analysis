import pandas as pd
from collections import Counter
import re

INPUT_CSV_FILE = "enriched_data.csv"
NUMBER_OF_TOP_ENTITIES = 15

def main():
    print("--- Starting data analysis ---")
    try:
        df = pd.read_csv("enriched_data.csv")
        print(f"Successfully loaded {len(df)} rows from {INPUT_CSV_FILE}.")
    except FileNotFoundError:
        print(f"File {INPUT_CSV_FILE} not found. Please ensure the file exists.")
        return

    df['created_at'] = pd.to_datetime(df['created_at'], format='%Y-%m-%dT%H:%M:%SZ', errors='coerce')
    df['entities'].fillna('', inplace=True)
    df.dropna(subset=['created_at', 'text', 'polarity'], inplace=True)
    print(f"After cleaning, we are analyzing {len(df)} rows.")

    all_entities = []
    for entity_list in df['entities']:
        if isinstance(entity_list, str):
            entities = entity_list.split(', ')
            for entity in entities:
                if not entity: continue
                cleaned_entity = re.sub(r'\s*\(.*?\)', '', entity).strip().lower()
                if len(cleaned_entity) > 2 and not cleaned_entity.isnumeric():
                    all_entities.append(cleaned_entity)
    
    top_entities = Counter(all_entities).most_common(NUMBER_OF_TOP_ENTITIES)
    print(f"Found {len(top_entities)} unique top entities.")

    import matplotlib
    matplotlib.use('TkAgg')
    import matplotlib.pyplot as plt
    import seaborn as sns

    plt.figure(1, figsize=(10, 6))
    sns.set_style("whitegrid")
    sns.histplot(df['polarity'], bins=30, kde=True)
    plt.title('Overall Sentiment Distribution of Comments')
    plt.savefig('sentiment_distribution.png', dpi=300)

    df_top_entities = pd.DataFrame(top_entities, columns=['Entity', 'Count'])
    plt.figure(2, figsize=(12, 8))
    sns.barplot(x='Count', y='Entity', data=df_top_entities, palette='viridis')
    plt.title(f'Top {NUMBER_OF_TOP_ENTITIES} Most Mentioned Entities')
    plt.tight_layout()
    plt.savefig('top_entities.png', dpi=300)

    top_entity_names = [entity for entity, count in top_entities]
    entity_sentiments = {entity: [] for entity in top_entity_names}
    if top_entity_names:
        for index, row in df.iterrows():
            text_lower = row['text'].lower()
            polarity = row['polarity']
            for entity in top_entity_names:
                if entity in text_lower:
                    entity_sentiments[entity].append(polarity)
    avg_sentiments = {entity: sum(s) / len(s) for entity, s in entity_sentiments.items() if s}
    df_avg_sentiments = pd.DataFrame(list(avg_sentiments.items()), columns=['Entity', 'AveragePolarity']).sort_values(by='AveragePolarity', ascending=False)
    
    plt.figure(3, figsize=(12, 8))
    sns.barplot(x='AveragePolarity', y='Entity', data=df_avg_sentiments, palette='RdBu_r')
    plt.title(f'Average Sentiment of Top {NUMBER_OF_TOP_ENTITIES} Entities')
    plt.tight_layout()
    plt.savefig('top_entities_sentiment.png', dpi=300)

    print("\nVisualizations prepared. Displaying all plots now.")
    plt.show()
    
    input("Press ENTER in this terminal to close the plots and exit.")

if __name__ == "__main__":
    main()