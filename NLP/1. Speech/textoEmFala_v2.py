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

speech_config = speechsdk.SpeechConfig(subscription=chave1, region=regiao)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)


#***************************************************************************************
# Vozes disponíveis
#
# https://play.ht/text-to-speech-voices/microsoft-azure/
#
# English  (US) --> Guy, Amber, Ana, Aria, Ashley, ...
#
# Portguês (BR) --> Francisca, Antonio, ...
#
#***************************************************************************************


# Função para execução com chamada no próprio arquivo
def menu():
    
    print('\n*** Qual voz deseja? ***\n')
    print('1. Francica [default]')
    print('2. Antônio')
    
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
    
    # Get text from the console and synthesize to the default speaker.    
    print("\nDigite um texto para ouvi-lo >\n")
    texto = input()
    idioma = 'pt-BR'    
    transcreverTextoEmFala(texto, nome, idioma, True)


def transcreverTextoEmFala(text, nome, idioma, proprioArquivo=False):
    
    voz = idioma + '-' + nome + 'Neural'
    
    speech_config.speech_synthesis_voice_name = voz
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)   
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        if proprioArquivo:
            print("\nSpeech synthesized for text [{}]\n".format(text))        
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("\nSpeech synthesis canceled: {}\n".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("\nError details: {}\n".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")



if __name__ == '__main__':
    menu()