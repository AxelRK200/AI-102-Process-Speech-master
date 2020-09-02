import azure.cognitiveservices.speech as speechsdk

# Creates an instance of a speech config with specified subscription key and service region.
speech_key, service_region = "e8fb934b094144d19c9a388061c236f3", "eastus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
#Neural voices pas disponibles dans toutes les régions de création du service Speech
speech_config.speech_synthesis_voice_name = "fr-FR-DeniseNeural"

#Création d'un fichier .wav en sortie du texte synthétisé
audio_filename = "synthesize_text_to_speech/media/synthese-vocale.wav"
audio_output = speechsdk.audio.AudioOutputConfig(filename=audio_filename)

# Creates a speech synthesizer using the default speaker as audio output.
speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)

# Receives a text from console input.
print("Texte à synthétiser")
text = input()

# Synthesizes the received text to speech.
# The synthesized speech is expected to be heard on the speaker with this line executed.
result = speech_synthesizer.speak_text_async(text).get()

# Checks result.
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Synthèse vocale effectée pour le texte suivant [{}]".format(text))
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print("Synthèse vocale annulée: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print("Error details: {}".format(cancellation_details.error_details))
    print("Vérifier clé et région")