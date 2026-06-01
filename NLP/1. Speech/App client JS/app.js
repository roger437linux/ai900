async function textoParaAudio  (texto) {
    const SPEECH_KEY=''
    const SPEECH_REGION=''
    const url = `https://${SPEECH_REGION}.tts.speech.microsoft.com/cognitiveservices/v1`


    const data = `
        <speak version='1.0' xml:lang='pt-BR'>
            <voice xml:lang='pt-BR' xml:gender='Female' name='pt-BR-GiovannaNeural'>
                ${texto}
            </voice>
        </speak>
    `

    const options = {
        method: 'POST',
        headers: {
            'Ocp-Apim-Subscription-Key': SPEECH_KEY,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'audio-16khz-128kbitrate-mono-mp3'
          },
        body: data,

    }
    
    const response  = await fetch(url, options)
    const datablob = await response.blob()

    return datablob


}

const playAudio = async () => {

    const audioPlayer = document.getElementById('player');
    const texto = document.getElementById('texto').value


    const blobAudio = await textoParaAudio(texto)

    const objectURL = URL.createObjectURL(blobAudio);
    audioPlayer.src = objectURL;
    

}

document.getElementById('converter')
        .addEventListener('click', () => playAudio())