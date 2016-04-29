"""
Copyright (c) 2016 Rodrigo Baravalle
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions
are met:
1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.
3. The name of the author may not be used to endorse or promote products
derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from imfractal import *

from pylab import *

import sys
import os

sys.path.append(os.path.join(os.path.dirname(sys.path[0]),'imfractal', 'imfractal',  "Algorithm"))

import qs3D


def do_test(_path):

    print "PATH: " + _path

    patients = ["32"]
    scans = ["1"]
    # amount of volumes of interest
    vois = 1
    dims = 10

    # BioAsset bone's multifractal spectra database

    aux = CSandbox3D(dims)

    #slices_str = "slice"
    #masks_str = "mask"

    params = {
        "zero": 1,
        "one": 0.75,
        "two": 3.7,
        "three": 1,
        "four": 15,
        "five": 0,
        "mask_filename": '',
        "seven": "no",
        "eight": 'S',
        "nine": 'M',
        "threshold": 200,
        "total_pixels":6000
    }

    from os import listdir
    from os.path import isfile, join
    mask_files = [f for f in listdir(_path) if isfile(join(_path, f)) and "Mask" in f]
    slice_files = [f for f in listdir(_path) if isfile(join(_path, f)) and "Slices" in f]

    mfss = np.zeros([len(mask_files), 2 * dims + 1])

    mask_files = sort(mask_files)
    slice_files = sort(slice_files)

    if len(mask_files) != len(slice_files):
        print "The directory should contain the same amount of slices and masks"
        exit()

    i = 0
    for mask_filename in mask_files:
        [patient_scan_str, _] = mask_filename.split("Mask")
        [first_str, scan_str] = patient_scan_str.split("_120_")
        [_, patient_str] = first_str.split("BA")

        mask_filename = _path + mask_filename

        params["five"] = 1 #fix me
        params["mask_filename"] = mask_filename

        # obviously we can directly use slice_files[i], but this adds robustness
        slice_filename = _path + "BA" + patient_str + "_120_" + scan_str + "Slices.mat"
        if slice_filename == _path + slice_files[i]:
            print "MASK: ", mask_filename
            print "SLICE: ", slice_filename
        else:
            print "Cannot process test: filename ", _path + slice_files[i], " should be ", slice_filename
            exit()

        aux.setDef(40, 1.02, True, params)
        mfss[i] = aux.getFDs(slice_filename)

        i += 1


    np.save("mfs_BioAsset",mfss)


    
