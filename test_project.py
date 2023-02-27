import project
import pickle
import cv2
import numpy as np


def test_draw_lines():
    assert np.array_equal(project.draw_lines(cv2.imread("Rickrolling.webp"), cv2.Canny(cv2.imread("Rickrolling.webp"), 100, 200), 100), pickle.load(open("pickles/draw_lines.pickle", "rb")))

def test_reduce_image():
    assert np.array_equal(project.reduce_image(cv2.imread("Rickrolling.webp"), 10), pickle.load(open("pickles/reduce_image.pickle", "rb")))

def test_cartoonify():
    assert np.array_equal(project.cartoonify(cv2.imread("Rickrolling.webp"), 10, "-n"), pickle.load(open("pickles/cartoonify.pickle", "rb")))