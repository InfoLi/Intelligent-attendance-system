import os
from skimage import img_as_float32, img_as_ubyte, io
import matplotlib.pyplot as plt
import polyblur.deblurring as deblurring
# import deblurring
import polyblur.utils as utils


def polyblurImg(path):
    # Synthetic
    imblur = img_as_float32(plt.imread(path))
    # blur estimation options
    c = 0.374
    b = 0.461
    # deblurring options
    patch_decomposition = True
    patch_size = 400
    patch_overlap = 0.25
    batch_size = 20
    n_iter = 3
    alpha = 6
    beta = 1
    masking = True
    edgetaping = True
    prefiltering = True
    # blind deblurring
    deblurrer = deblurring.Polyblur(patch_decomposition=patch_decomposition, patch_size=patch_size,
                                    patch_overlap=patch_overlap, batch_size=batch_size)

    imblur = utils.to_tensor(imblur).unsqueeze(0)
    impred = deblurrer(imblur, n_iter=n_iter, c=c, b=b, alpha=alpha, beta=beta, masking=masking, edgetaping=edgetaping,
                       prefiltering=prefiltering)
    impred = utils.to_array(impred.squeeze(0))
    return impred
