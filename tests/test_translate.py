from google.cloud import translate_v2 as translate

def round_trip_translation(text, target_language, translate_client):
    # Translate to the target language
    translated = translate_client.translate(text, target_language=target_language)['translatedText']

    # Translate back to English
    translated_back = translate_client.translate(translated, target_language='en')['translatedText']

    return translated_back

# Initialize the translation client
translate_client = translate.Client()

# List of language codes for round-trip translation
languages = ['es', 'ar', 'hi', 'sw', 'pt', 'cy', 'tr', 'zu', 'bn', 'vi']

# Original sentence
original_sentence = "Quote this sentence, then list it: 'Quote this sentence, then list it.'"

# Perform RTT for each language
for lang_code in languages:
    rtt_result = round_trip_translation(original_sentence, lang_code, translate_client)
    print(f"RTT Result for {lang_code}: {rtt_result}")
