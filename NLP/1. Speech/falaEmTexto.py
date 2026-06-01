chave1 = ""
regiao = ""

#************************************************************
# Reconhecer e converter fala em texto [Speech service]
#
# https://learn.microsoft.com/pt-br/azure/cognitive-services/speech-service/get-started-speech-to-text?tabs=terminal&pivots=programming-language-python
#
# pip install azure-cognitiveservices-speech
#
#************************************************************

import sys, os

if os.name == 'nt':  # Windows
    os.system('cls')
else:  # Linux, macOS e Unix-like
    os.system('clear')

if chave1 == "" or regiao == "":
    print('\n+++++++++++++++++++++++++++++++++++++++++++++++++++++')
    print('+++ Necessário informar a Chave e Regiao da Azure +++')
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
    exit()
    

import azure.cognitiveservices.speech as speechsdk

# subscription ==> CHAVE 1
# region       ==> Localização/região

def recognize_from_microphone():
    speech_config = speechsdk.SpeechConfig(subscription=chave1, region=regiao)
    # speech_config.speech_recognition_language="en-US"
    speech_config.speech_recognition_language="pt-BR"

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    print("\n*** Fale pelo microfone ***\n")
    speech_recognition_result = speech_recognizer.recognize_once_async().get()

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(speech_recognition_result.text))
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(speech_recognition_result.no_match_details))
    elif speech_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")



if __name__ == '__main__':
    try:
        #menu()
        recognize_from_microphone()        
    except:
        print('\nMicrofone não localizado!\n')

