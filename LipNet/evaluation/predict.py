import sys
sys.path.append('C:\\Users\\Matthew\\Documents\\silent_speaking\\SilentSpeaking\\LipNet')
sys.path.append('C:\\Users\\Matthew\\Documents\\silent_speaking\\SilentSpeaking')
from cog_services import cognitive
import lipnet
from lipnet.lipreading.videos import Video
from lipnet.lipreading.visualization import show_video_subtitle
from lipnet.core.decoders import Decoder
from lipnet.lipreading.helpers import labels_to_text
from lipnet.utils.spell import Spell
from lipnet.model2 import LipNet
from keras.optimizers import Adam
from keras import backend as K
import numpy as np
import os



np.random.seed(55)

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

FACE_PREDICTOR_PATH = os.path.join(CURRENT_PATH,'..','common','predictors','shape_predictor_68_face_landmarks.dat')

PREDICT_GREEDY      = False
PREDICT_BEAM_WIDTH  = 200
PREDICT_DICTIONARY  = os.path.join(CURRENT_PATH,'..','common','dictionaries','grid.txt')

class Prebuilt_model:
    def __init__(self, weight_path, video_path, lipnet, absolute_max_string_len=32, output_size=28):
        self.lipnet = lipnet
        self.adam = Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
        self.lipnet.model.compile(loss={'ctc': lambda y_true, y_pred: y_pred}, optimizer=self.adam)
        self.lipnet.model.load_weights(weight_path)
        self.spell = Spell(path=PREDICT_DICTIONARY)
        self.decoder = Decoder(greedy=PREDICT_GREEDY, beam_width=PREDICT_BEAM_WIDTH,
                      postprocessors=[labels_to_text])


class MODEL:
    model = None




def predict(weight_path, video_path, absolute_max_string_len=32, output_size=28):
    #print("\nLoading data from disk...")
    video = Video(vtype='face', face_predictor_path=FACE_PREDICTOR_PATH)
    if os.path.isfile(video_path):
        video.from_video(video_path)
    else:
        video.from_frames(video_path)
    #print("Data loaded.\n")

    if K.image_data_format() == 'channels_first':
        img_c, frames_n, img_w, img_h = video.data.shape
    else:
        frames_n, img_w, img_h, img_c = video.data.shape

    lipnet = LipNet(img_c=img_c, img_w=img_w, img_h=img_h, frames_n=frames_n,
                absolute_max_string_len=absolute_max_string_len, output_size=output_size)

    if not MODEL.model:
        #lipnet = LipNet(img_c=img_c, img_w=img_w, img_h=img_h, frames_n=frames_n,
        #            absolute_max_string_len=absolute_max_string_len, output_size=output_size)
        #adam = Adam(lr=0.0001, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
        #lipnet.model.compile(loss={'ctc': lambda y_true, y_pred: y_pred}, optimizer=adam)
        #lipnet.model.load_weights(weight_path)

        #print("Built Model.") 
        #spell = Spell(path=PREDICT_DICTIONARY)
        #decoder = Decoder(greedy=PREDICT_GREEDY, beam_width=PREDICT_BEAM_WIDTH,
        #              postprocessors=[labels_to_text])#, spell.sentence])
        MODEL.model = Prebuilt_model(weight_path, video_path, lipnet, absolute_max_string_len, output_size)

    X_data       = np.array([video.data]).astype(np.float32) / 255
    input_length = np.array([len(video.data)])

    y_pred         = MODEL.model.lipnet.predict(X_data)
    results         = MODEL.model.decoder.decode(y_pred, input_length)
    print("Before cognitive services: " + results[0])
    cog = cognitive()
    cog_result = cog.speech_to_text(cog.text_to_speech(results[0]))
    print("after cognitive services: " + cog_result) 

    return (video, cog_result)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        video, result = predict(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4:
        video, result = predict(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 5:
        video, result = predict(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        video, result = None, ""

    #if video is not None:
        #show_video_subtitle(video.face, result)

    stripe = "-" * len(result)
    #print("")
    #print(" __                   __  __          __      ")
    #print("/\\ \\       __        /\\ \\/\\ \\        /\\ \\__   ")
    #print("\\ \\ \\     /\\_\\  _____\\ \\ `\\\\ \\     __\\ \\ ,_\\  ")
    #print(" \\ \\ \\  __\\/\\ \\/\\ '__`\\ \\ , ` \\  /'__`\\ \\ \\/  ")
    #print("  \\ \\ \\L\\ \\\\ \\ \\ \\ \\L\\ \\ \\ \\`\\ \\/\\  __/\\ \\ \\_ ")
    #print("   \\ \\____/ \\ \\_\\ \\ ,__/\\ \\_\\ \\_\\ \\____\\\\ \\__\\")
    #print("    \\/___/   \\/_/\\ \\ \\/  \\/_/\\/_/\\/____/ \\/__/")
    #print("                  \\ \\_\\                       ")
    #print("                   \\/_/                       ")
    #print("")
    #print("             --{}- ".format(stripe))
    #print("[ DECODED ] |> {} |".format(result))
    #print("             --{}- ".format(stripe))
