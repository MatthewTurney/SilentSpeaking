import requests
import json
from time import gmtime, strftime

class cognitive:
    def get_token(self):
        key = '1974b9e52e5d4a66a5b461eff442d429'
        url = 'https://westus.api.cognitive.microsoft.com/sts/v1.0/issueToken'
        headers = {'Content-type': 'application/x-www-form-urlencoded', 'Content-Length': '0',
                   'Ocp-Apim-Subscription-Key': key}
        response = requests.post(url, headers=headers)
        self.token = 'Bearer ' + response.content.decode('UTF-8')

    def text_to_speech(self, message):
        self.get_token()
        url = 'https://westus.tts.speech.microsoft.com/cognitiveservices/v1'
        headers = {'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm', 'Authorization': self.token,
                   'Content-type': 'application/ssml+xml', 'Connection': 'Keep-Alive'}
        xmlstring = "<speak version='1.0' xmlns=\"http://www.w3.org/2001/10/synthesis\" xml:lang='en-US'><voice  name='Microsoft Server Speech Text to Speech Voice (en-US, JessaRUS)'>" + message +"</voice> </speak>"
        response = requests.post(url, data=xmlstring, headers=headers)
        sound_output = response.content
        output_file = "C:\\Users\\Matthew\\Documents\\silent_speaking\\SilentSpeaking\\sound_files\\{}.wav".format(strftime("%Y-%m-%d_%H-%M-%S", gmtime()))
        with open(output_file, mode='wb') as file:
            file.write(sound_output)
        return sound_output


    def speech_to_text(self, input):
        url = 'https://westus.stt.speech.microsoft.com/speech/recognition/conversation/cognitiveservices/v1?language=en-US'
        headers = {'Content-type': 'audio/wav; codec=audio/pcm; samplerate=16000',
                   'Ocp-Apim-Subscription-Key': '1974b9e52e5d4a66a5b461eff442d429'}
        response = requests.post(url, data=input, headers=headers)
        text = json.loads(response.content.decode('UTF-8'))['DisplayText']
        return text


if __name__ == "__main__":
    test = cognitive()
    output = test.text_to_speech("peter is the best")
    text = test.speech_to_text(output)
    print(text)