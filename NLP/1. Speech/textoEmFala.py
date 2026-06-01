chave1 = ""
regiao = ""

############################################
# Speech service
#
# Sintese ==> Converte texto em fala
# pip install azure-cognitiveservices-speech
############################################

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

speech_config = speechsdk.SpeechConfig(subscription=chave1, region=regiao)

audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)


#***************************************************************************************
# Vozes disponíveis

# https://azure.microsoft.com/en-us/products/cognitive-services/text-to-speech/#features

# English (US) --> Guy, Amber, Ana, Aria, Ashley, ...

# Portguês (BR) --> Francisca, Antonio, ...

#***************************************************************************************

# The language of the voice that speaks.
# speech_config.speech_synthesis_voice_name='en-US-JennyNeural'

# idioma = 'en-US'
# nome = 'Ashley'

print('\n*** Qual voz deseja? ***\n')
print('1. Francica [default]')
print('2. Antônio')

nome = ''

while True:
    op = input("\nOpção:  ")
    if op == '' or op == '1':
        nome = 'Francisca'
        break
    elif  op == '2':
        nome = 'Antonio'
        break    
    else:
        print('\nOpção inválida')

idioma = 'pt-BR'
voz = idioma + '-' + nome + 'Neural'

speech_config.speech_synthesis_voice_name=voz

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# Get text from the console and synthesize to the default speaker.
print("\nDigite um texto para ouvi-lo >\n")
text = input()

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
			
			