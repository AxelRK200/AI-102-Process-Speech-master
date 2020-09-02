import azure.cognitiveservices.speech as speechsdk

speech_key, service_region = "e8fb934b094144d19c9a388061c236f3", "eastus"

def translate_speech_to_speech():

    # Creates an instance of a speech translation config with specified subscription key and service region.
    # Replace with your own subscription key and region identifier from here: https://aka.ms/speech/sdkregion
    translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=speech_key, region=service_region)
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

    # Creates a speech synthesizer using the configured voice for audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Sets source and target languages.
    # In this example, the service will translate a US English spoken input, to French and Indonesian language spoken output
    # Replace with the languages of your choice, from list found here: https://aka.ms/speech/sttt-languages
    fromLanguage = 'fr-FR'
    translation_config.speech_recognition_language = fromLanguage

    # Add more than one language to the collection.
    # using the add_target_language() method
    translation_config.add_target_language("zh-Hans")
    translation_config.add_target_language("ru")

    # Creates a translation recognizer using and audio file as input.
    recognizer = speechsdk.translation.TranslationRecognizer(translation_config=translation_config)

    # Starts translation, and returns after a single utterance is recognized. The end of a
    # single utterance is determined by listening for silence at the end or until a maximum of 15
    # seconds of audio is processed. It returns the recognized text as well as the translation.
    # Note: Since recognize_once() returns only a single utterance, it is suitable only for single
    # shot recognition like command or query.
    # For long-running multi-utterance recognition, use start_continuous_recognition() instead.
    print("Je vous écoute ...")
    result = recognizer.recognize_once()

# Check the result
    if result.reason == speechsdk.ResultReason.TranslatedSpeech:
        # Output the text for the recognized speech input
        print("Pris en compte '{}': {}".format(fromLanguage, result.text))

        # Loop through the returned translation results
        for key in result.translations:

        # Using the Key and Value components of the returned dictionary for the translated results
        # The first portion gets the key (language code) while the second gets the Value
        # which is the translated text for the language specified
        # Output the language and then the translated text
            print("Traduit en {}: {}".format(key, result.translations[key]))

            # If the language code is 'zh-CN' for Chinese Traditional, then use the Neural Chinese Voice
            if key == "zh-Hans":
                speech_config.speech_synthesis_voice_name = "zh-CN-XiaoxiaoNeural"

                # Update the speech synthesizer to use the proper voice
                speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

                # Use the proper voice, from the speech synthesizer configuration, to narrate the translated result
                speech_synthesizer.speak_text_async(result.translations[key]).get()
            else: # Otherwise, use the voice for the Russian translation
                speech_config.speech_synthesis_voice_name = "ru-RU-DariyaNeural"

                # Update the speech synthesizer to use the proper voice
                speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

                # Use the proper voice, from the speech synthesizer configuration, to narrate the translated result
                speech_synthesizer.speak_text_async(result.translations[key]).get()

    elif result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Pris en compte: {} (Le texte n'a pas pu être traduit)".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("NO MATCH: L'enregistrement n'a pas été compris: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        print("Annulé: Reason={}".format(result.cancellation_details.reason))
        if result.cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Annulé: ErrorDetails={}".format(result.cancellation_details.error_details))

translate_speech_to_speech()