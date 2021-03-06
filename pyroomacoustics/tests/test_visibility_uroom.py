# @version: 1.0  date: 05/06/2015 by Sidney Barthe
# @author: robin.scheibler@epfl.ch, ivan.dokmanic@epfl.ch, sidney.barthe@epfl.ch
# @copyright: EPFL-IC-LCAV 2015

from unittest import TestCase
import numpy as np

import pyroomacoustics as pra

fs = 8000
t0 = 1./(fs*np.pi*1e-2)
absorption = 0.90
max_order_sim = 2
sigma2_n = 5e-7

corners = np.array([[0,5,5,3,3,2,2,0], [0,0,5,5,2,2,5,5]])
room = pra.Room.from_corners(
    corners,
    absorption,
    fs,
    t0,
    max_order_sim,
    sigma2_n)
    
room.add_source([1, 4], None, 0)

# place 3 microphones in the room
mics = pra.MicrophoneArray(np.array([[4, 2.5, 2.5,],
                                     [4, 1,   4   ]]), fs)
room.add_microphone_array(mics)

# run the image source model
room.image_source_model()

# we order the sources lexicographically
ordering = np.lexsort(room.sources[0].images)
images_found = room.sources[0].images[:,ordering]
visibilities = room.visibility[0][:,ordering]

# This should be all visible sources, from the 3 mic locations
sources = np.array([[ 1., -1.,  1., -3., -1., -1.,  1.],
                    [-6., -4., -4.,  4.,  4.,  6.,  8.]])

# These are the visibilities for each individual microphone
visible_opposite_side = [0, 0, 1, 0, 0, 0, 0]
visible_middle = [1, 1, 1, 1, 1, 1, 1]
visible_outside = [0, 0, 0, 0, 0, 0, 0]

class TestVisibilityURoom(TestCase):

    def test_sources(self):
        self.assertTrue(np.allclose(images_found, sources))

    def test_visibility_oppositeSide(self):
        self.assertTrue(all(visibilities[0] == visible_opposite_side))

    def test_visibility_middle(self):
        self.assertTrue(all(visibilities[1] == visible_middle))

    def test_visibility_outside(self):
        self.assertTrue(all(visibilities[2] == visible_outside))
