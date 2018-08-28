#!/usr/bin/env python2

from gimpfu import *


def resize_layer_width(layer, width):
    pass


def resize_layer_height(layer, width):
    pass


def setup_picture(image, drawable):

    if len(image.layers) == 1:
        pdb.gimp_message("You shall not use a single layer group as a root for all layers")
        return

    if image.height % 12 != 0:
        pdb.gimp_message("Setting the height of the image as a multiple of 12")
        pdb.gimp_image_resize(
            image, 
            image.width, 
            image.height + (12 - image.height % 12),
            0,
            0,
        )

    if image.width % 12 != 0:
        pdb.gimp_message("Setting the width of the image as a multiple of 12")
        pdb.gimp_image_resize(
            image, 
            image.width + (12 - image.width % 12), 
            image.height,
            0,
            0,
        )

    for layer in image.layers:
        if type(layer) is gimp.GroupLayer:
            
            for sublayer in layer.children:
                xdifftotwelve = (12 - layer.width % 12) % 12
                ydifftotwelve = (12 - layer.height % 12) % 12
                xsizediff = layer.width - sublayer.width
                ysizediff = layer.height - sublayer.height
                xoffset = layer.offsets[0] - sublayer.offsets[0]
                yoffset = layer.offsets[1] - sublayer.offsets[1]
                pdb.gimp_message(
                    "Resizing layer {} size:({}, {}) " \
                    "pos: ({}, {}) to fit its " \
                    "parent size ({}, {}), pos ({}, {}) " \
                    "diff: size ({}, {}), pos ({}, {})".format(
                        sublayer.name,
                        sublayer.width,
                        sublayer.height,
                        sublayer.offsets[0],
                        sublayer.offsets[1],
                        layer.width,
                        layer.height,
                        layer.offsets[0],
                        layer.offsets[1],
                        xsizediff,
                        ysizediff,
                        xoffset,
                        yoffset,
                    )
                )
                pdb.gimp_layer_resize(
                    sublayer,
                    layer.width + xdifftotwelve,
                    layer.height + ydifftotwelve,
                    - xoffset,
                    - yoffset,
                )
                pdb.gimp_message(
                    "New layer size: ({}, {}), position: ({}, {})".format(
                        layer.width,
                        layer.height,
                        layer.offsets[0],
                        layer.offsets[1]
                    )
                )
            
            #position the layer group to a 12 position
            xoffset = (layer.offsets[0] % 12) % 12
            yoffset = (layer.offsets[1] % 12) % 12
            for sublayer in layer.children:
                pdb.gimp_layer_resize(
                    sublayer,
                    sublayer.width + xoffset,
                    sublayer.height + yoffset,
                    xoffset,
                    yoffset,
                )

                pdb.gimp_item_set_visible(sublayer, False)

            pdb.gimp_message(
                "New layer pos after move: ({}, {}), position: ({}, {})".format(
                    xoffset,
                    yoffset,
                    layer.offsets[0],
                    layer.offsets[1]
                )
            )

        pdb.gimp_item_set_visible(layer, False)




register(
    proc_name = "setup_picture",
    blurb = "Sets the picture layers correctly",
    help = "Sets layers of the picture in a way that can be used in 4k pictures",
    author = "https://github.com/Meithal",
    copyright = "2018 https://github.com/Meithal",
    date = "2018",
    label = "Set layers for 4k export",
    imagetypes = "*",
    params = [ 
        (PF_IMAGE, "image", "Input image", None),
        (PF_DRAWABLE, "drawable", "Input drawable", None),
    ],
    results = [ ],
    function = setup_picture,
    menu = "<Image>/Layer"
)

main()