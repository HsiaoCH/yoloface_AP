# *******************************************************************
#
# Author : Thanh Nguyen, 2018
# Email  : sthanhng@gmail.com
# Github : https://github.com/sthanhng
#
# BAP, AI Team
# Face detection using the YOLOv3 algorithm
#
# Description : yoloface.py
# The main code of the Face detection using the YOLOv3 algorithm
#
# *******************************************************************

# Usage example:  python yoloface.py --image samples/outside_000001.jpg \
#                                    --output-dir outputs/
#                 python yoloface.py --video samples/subway.mp4 \
#                                    --output-dir outputs/
#                 python yoloface.py --src 1 --output-dir outputs/


import argparse
import sys
import os

from utilss import *

#####################################################################
parser = argparse.ArgumentParser()
parser.add_argument('--model-cfg', type=str, default='./cfg/yolov3-face.cfg',
                    help='path to config file')
parser.add_argument('--model-weights', type=str,
                    default='./model-weights/yolov3-wider_16000.weights',
                    help='path to weights of model')
parser.add_argument('--image', type=str, default='',
                    help='path to image file')
parser.add_argument('--video', type=str, default='',
                    help='path to video file')
parser.add_argument('--src', type=int, default=0,
                    help='source of the camera')
parser.add_argument('--output-dir', type=str, default='outputs/',
                    help='path to the output directory')
args = parser.parse_args()

#####################################################################
# print the arguments
def _main():
    # Give the configuration and weight files for the model and load the network
    # using them.
    net = cv2.dnn.readNetFromDarknet(args.model_cfg, args.model_weights)
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    Folders = os.listdir(args.image)
    for Folder in Folders:
        print(Folder)
        imgs = os.listdir('WIDER_val/' + Folder)
        if os.path.isdir('./wider_out/' + Folder):
            print('good')
        else:
            os.mkdir('./wider_out/' + Folder)
        # check outputs directory
        if not os.path.exists(args.output_dir):
            print('==> Creating the {} directory...'.format(args.output_dir))
            os.makedirs(args.output_dir)
        else:
            print('==> Skipping create the {} directory...'.format(args.output_dir))
        for img in imgs:
            names = img
            fp = open('wider_out/'+ Folder + '/' + names.rstrip('.jpg')+".txt", "w")
            fp.write(img+"\n")
            img = 'WIDER_val/' + Folder + '/' + img
            print('----- info -----')
            print('[i] The config file: ', args.model_cfg)
            print('[i] The weights of model file: ', args.model_weights)
            print('[i] Path to image file: ', img)
            print('[i] Path to video file: ', args.video)
            print('###########################################################\n')

            #wind_name = 'face detection using YOLOv3'
            #cv2.namedWindow(wind_name, cv2.WINDOW_NORMAL)
            output_file = ''

            if img:
                if not os.path.isfile(img):
                    print("[!] ==> Input image file {} doesn't exist".format(img))
                    sys.exit(1)
                cap = cv2.VideoCapture(img)
                #output_file = img[:-4].rsplit('/')[-1] + '_yoloface.jpg'
            elif args.video:
                if not os.path.isfile(args.video):
                    print("[!] ==> Input video file {} doesn't exist".format(args.video))
                    sys.exit(1)
                cap = cv2.VideoCapture(args.video)
                #output_file = args.video[:-4].rsplit('/')[-1] + '_yoloface.avi'
            else:
                # Get data from the camera
                cap = cv2.VideoCapture(args.src)

            # Get the video writer initialized to save the output video
            if not img:
                video_writer = cv2.VideoWriter(os.path.join(args.output_dir, output_file),
                                               cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'),
                                               cap.get(cv2.CAP_PROP_FPS), (
                                                   round(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                                                   round(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))

            while True:

                has_frame, frame = cap.read()

                # Stop the program if reached end of video
                if not has_frame:
                    print('[i] ==> Done processing!!!')
                    print('[i] ==> Output file is stored at', os.path.join(args.output_dir, output_file))
                    cv2.waitKey(1000)
                    break

                # Create a 4D blob from a frame.
                blob = cv2.dnn.blobFromImage(frame, 1 / 255, (IMG_WIDTH, IMG_HEIGHT),
                                             [0, 0, 0], 1, crop=False)

                # Sets the input to the network
                net.setInput(blob)

                # Runs the forward pass to get output of the output layers
                outs = net.forward(get_outputs_names(net))

                # Remove the bounding boxes with low confidence

                faces , scer = post_process(frame, outs, CONF_THRESHOLD, NMS_THRESHOLD)
                print(scer)
                #print(boxs)
                #cv2.imshow(wind_name, frame)
                print(faces)
                print('[i] ==> # detected faces: {}'.format(len(faces)))
                print('#' * 60)
                fp.write(str(len(faces))+"\n")

                i = 0
                for face in faces:
                    fp.write(str(face[0]) + " " + str(face[1]) + " " + str(face[2]) + " " + str(face[3]) + " " + str(scer[i]) + "\n")
                    i = i + 1
                # initialize the set of information we'll displaying on the frame

                info = [
                    ('number of faces detected', '{}'.format(len(faces)))
                ]

                for (i, (txt, val)) in enumerate(info):
                    text = '{}: {}'.format(txt, val)
                    cv2.putText(frame, text, (10, (i * 20) + 20),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLOR_RED, 2)

                # Save the output video to file
                if img:
                    print("==")
                    #cv2.imwrite(os.path.join(args.output_dir, output_file), frame.astype(np.uint8))
                else:
                    video_writer.write(frame.astype(np.uint8))



                key = cv2.waitKey(1)
                if key == 27 or key == ord('q'):
                    print('[i] ==> Interrupted by user!')

            cap.release()
            cv2.destroyAllWindows()
            fp.close()



    print('==> All done!')
    print('***********************************************************')





if __name__ == '__main__':
    _main()
