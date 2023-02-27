from colorthief import ColorThief
import cv2
import numpy as np
from scipy import ndimage
import progressbar
import pickle
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from PIL import Image
import warnings
import sys
from skimage import img_as_ubyte
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeVideoClip
import os

warnings.filterwarnings("ignore")


def main():
    # open Rick_Astley_Never_Gonna_Give_You_Up.mp4, for each frame, convert it to a cartoon, and save it to a new video

    if len(sys.argv) < 6:
        sys.exit("Usage: python3 projectfinal.py <photo/video> <input file> <output file> <colordepth> <flags>")

    if sys.argv[1] == "video":
        video = sys.argv[2]
        cap = cv2.VideoCapture(video)

        # get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # create video writer
        fourcc = cv2.VideoWriter_fourcc(*'avc1')
        out = cv2.VideoWriter('temp.mp4', fourcc, fps, (width, height))

        # process each frame
        for i in progressbar.progressbar(range(num_frames)):
            # read frame
            ret, frame = cap.read()

            # convert to cartoon
            cartoon = cartoonify(frame, sys.argv[4], sys.argv[5:])

            cartoon = img_as_ubyte(cartoon)

            out.write(cartoon)

        # release video
        cap.release()
        out.release()   

        audio_clip = AudioFileClip(video)
        video_clip = VideoFileClip('temp.mp4')
        final_clip = CompositeVideoClip([video_clip.set_audio(audio_clip)])
        final_clip.write_videofile(sys.argv[3], fps=fps)

        # remove temp.mp4
        os.remove("temp.mp4")

    elif  sys.argv[1] == "photo":
        # open image
        im = cv2.imread(sys.argv[2])

        # convert to cartoon
        cartoon = cartoonify(im, sys.argv[4], sys.argv[5:][0])

        # save cartoonified image
        cv2.imwrite(sys.argv[3], cartoon)

    else:
        sys.exit("Usage: python3 projectfinal.py <photo/video> <input file> <output file> <colordepth> <flags>")


def draw_lines(im, edges, threshold):
    # assume edges and im are numpy arrays with the same shape

    # find indices of white pixels in edges
    white_pixel_indices = np.where(edges > threshold)

    # set corresponding pixels in im to black
    black_value = np.array([0, 0, 0]) # create a 1D array of the desired color
    for i in range(len(white_pixel_indices[0])):
        idx = (white_pixel_indices[0][i], white_pixel_indices[1][i])
        im[idx] = black_value

    return im

def reduce_image(im, color_depth):
    color_thief = ColorThief("Rickrolling.webp")
    color_thief.image = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB))
    palette = color_thief.get_palette(color_count=color_depth)

    # Reshape the image into a 2D array of pixels
    im_pixels = im.reshape((-1, 3))

    # Cluster the colors using k-means
    kmeans = KMeans(n_clusters=len(palette), init=np.array(palette), n_init=1, max_iter=1, algorithm='full').fit(im_pixels)

    # Find the closest color in the palette for each pixel
    distances = cdist(kmeans.cluster_centers_, palette)
    closest_colors = np.argmin(distances, axis=1)

    # Replace each pixel with the closest color
    new_im_pixels = np.array([palette[closest_colors[label]] for label in kmeans.labels_])
    new_im = new_im_pixels.reshape(im.shape)

    return new_im

def cartoonify(im, color_depth, flags):
    if "-c" in flags:
        edges = cv2.Canny(im, 100, 200)
    elif "-n" in flags:
        # set edges to all black
        edges = np.zeros(im.shape)
    else:
        copy = np.copy(im).astype('int32')
        dx = ndimage.sobel(copy, 1)  # horizontal derivative
        dy = ndimage.sobel(copy, 0)  # vertical derivative
        edges = np.hypot(dx, dy)  # magnitude
        edges *= 255.0 / np.max(edges)  # normalize (Q&D)

    threshold = 50
    if "-s" in flags:
        threshold = int(flags[flags.index("-s") + 2:])

    return draw_lines(reduce_image(im, int(color_depth)), edges, threshold)
     

if __name__ == "__main__":
    main()