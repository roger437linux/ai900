chave1 = ""
regiao = ""

#########################################################################
# Speech service
#
# Reconhecer e converter uma fala em texto com tradução para outro idioma
#
# Vozes
# https://play.ht/text-to-speech-voices/microsoft-azure/
#
# https://learn.microsoft.com/pt-br/azure/cognitive-services/speech-service/get-started-speech-translation?tabs=terminal&pivots=programming-language-python
#
# pip install azure-cognitiveservices-speech
#########################################################################

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

# Texto em fala
speech_config = speechsdk.SpeechConfig(subscription=chave1, region=regiao)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
###


def recognize_from_microphone():
    speech_translation_config = speechsdk.translation.SpeechTranslationConfig(subscription=chave1, region=regiao)

    print('\n*** Idioma de origem para voz? ***\n')
    print('1. Português [default]')
    print('2. Espanhol')
    print('3. Italiano')
    print('4. Inglês')

    idiomaOrigem = ''
    while True:
        op = input("\nOpção:  ")
        if op == '' or op == '1':
            idiomaOrigem = 'pt-BR'
            break
        elif  op == '2':
            idiomaOrigem = 'es-ES'
            break
        elif op == '3':
            idiomaOrigem = 'it-IT'
            break
        elif op == '4':
            idiomaOrigem = 'en-US'
            break
        else:
            print('\nOpção inválida')
   
    # speech_translation_config.speech_recognition_language="en-US"
    speech_translation_config.speech_recognition_language=idiomaOrigem

    print('\n*** Idioma para texto traduzido? ***\n')
    print('1. Inglês [default]')
    print('2. Espanhol')
    print('3. Italiano')
    print('4. Frances')
    print('5. Alemão')
    print('6. Catalão')
    print('7. Galego')
    print('8. Português')

    idiomaDest = ''
    while True:
        op = input("\nOpção:  ")
        if op == '' or op == '1':
            idiomaDest = 'en'
            break
        elif  op == '2':
            idiomaDest = 'es'
            break
        elif op == '3':
            idiomaDest = 'it'
            break
        elif op == '4':
            idiomaDest = 'fr'
            break
        elif op == '5':
            idiomaDest = 'de'
            break
        elif op == '6':
            idiomaDest = 'ca'
            break
        elif op == '7':
            idiomaDest = 'gl'
            break
        elif op == '8':
            idiomaDest = 'pt'
            break
        else:
            print('\nOpção inválida')

    # target_language="it"
    target_language = idiomaDest

    speech_translation_config.add_target_language(target_language)

    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    translation_recognizer = speechsdk.translation.TranslationRecognizer(translation_config=speech_translation_config, audio_config=audio_config)

    print("\n*** Fale pelo microfone ***\n")
    translation_recognition_result = translation_recognizer.recognize_once_async().get()

    if translation_recognition_result.reason == speechsdk.ResultReason.TranslatedSpeech:
        print("Fala reconhecida: {}".format(translation_recognition_result.text))

        idiomaAlvo = ''
        if target_language == 'en':
            idiomaAlvo = 'Inglês'
        elif target_language == 'es':
            idiomaAlvo = 'Espanhol'
        elif target_language == 'it':
            idiomaAlvo = 'Italiano'
        elif target_language == 'fr':
            idiomaAlvo = 'Frances'
        elif target_language == 'de':
            idiomaAlvo = 'Alemão' 
        elif target_language == 'ca':
            idiomaAlvo = 'Catalão' 
        elif target_language == 'gl':
            idiomaAlvo = 'Galego'  
        elif target_language == 'pt':
            idiomaAlvo = 'Português'        

        print("""\nTraduzido para '{}': {}\n""".format(
            idiomaAlvo, #target_language, 
            translation_recognition_result.translations[target_language]))
    elif translation_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(translation_recognition_result.no_match_details))
    elif translation_recognition_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = translation_recognition_result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and region values?")
                 
        
    texto_em_fala(translation_recognition_result.translations[target_language], idiomaDest)    
    
    
def texto_em_fala(fala, idiomaDest):
    
    match idiomaDest:
        case 'en': 
            nome = 'Cora'
            #nome = 'Davis'
            idioma = 'en-US'
        case 'es':
            nome = 'Alonso'
            #nome = 'Paloma'
            idioma = 'es-US'
        case 'it':
            nome = 'Benigno'
            #nome = 'Irma'
            idioma = 'it-IT'
        case 'fr':
            nome = 'Alain'
            #nome = 'Yvette'
            idioma = 'fr-FR'
        case 'pt':
            nome = 'Giovanna'
            #nome = 'Nicolau'
            idioma = 'pt-BR'
        case _:
            print("\nAinda não implementada voz nesse idioma!\n")
            return
                        
    
    voz = idioma + '-' + nome + 'Neural'

    speech_config.speech_synthesis_voice_name=voz

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    # Get text from the console and synthesize to the default speaker.
    
    text = fala

    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("\nSpeech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("\nSpeech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("\nError details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")
        
    

try:
    recognize_from_microphone()
except:
    print("\nNão foi encontrado microfone!\n")