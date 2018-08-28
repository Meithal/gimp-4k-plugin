#!/usr/bin/env python2

from gimpfu import *


def setup_picture(image, drawable):

    if len(image.layers) == 1:
        pdb.gimp_message("You shall not use a single layer group as a root for all layers")
        return

    pdb.gimp_image_undo_group_start(image)

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

            # resize if needed
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
                    "New group layer size: ({}, {}), position: ({}, {})".format(
                        layer.width,
                        layer.height,
                        layer.offsets[0],
                        layer.offsets[1]
                    )
                )

                pdb.gimp_item_set_visible(sublayer, False)

            pdb.gimp_message(
                "New layer {} pos after move: ({}, {}), position: ({}, {})".format(
                    layer.name,
                    xoffset,
                    yoffset,
                    layer.offsets[0],
                    layer.offsets[1]
                )
            )

        else:
            xoffset = layer.offsets[0] % 12
            yoffset = layer.offsets[1] % 12

            pdb.gimp_message(
                "Master layer {} padding, ({}, {}) to ({}, {})".format(
                    layer.name,
                    layer.width,
                    layer.height,
                    layer.width + xoffset,
                    layer.height + yoffset
                )
            )

            # padding
            pdb.gimp_layer_resize(
                layer,
                layer.width + xoffset,
                layer.height + yoffset,
                xoffset,
                yoffset,
            )

            #size
            xdifftotwelve = (12 - layer.width % 12) % 12
            ydifftotwelve = (12 - layer.height % 12) % 12
            pdb.gimp_layer_resize(
                layer,
                layer.width + xdifftotwelve,
                layer.height + ydifftotwelve,
                0,
                0,
            )
            pdb.gimp_message(
                "New layer {} size: ({}, {}), position: ({}, {})".format(
                    layer.name,
                    layer.width,
                    layer.height,
                    layer.offsets[0],
                    layer.offsets[1]
                )
            )

            pdb.gimp_item_set_visible(layer, False)

        pdb.gimp_item_set_visible(layer, False)

    pdb.gimp_image_undo_group_end(image)
    pdb.gimp_image_undo_group_start(image)

    pdb.gimp_message(
        "Starting exporting"
    )


    for layer in image.layers:

        pdb.gimp_item_set_visible(layer, True)

        if layer.children:
            pass
        else:

            # nimage = gimp.Image(image.width, image.height, RGB)
            # nlayer = nimage.new_layer()
            
            pdb.gimp_edit_copy(layer)

            nimage = pdb.gimp_edit_paste_as_new_image()
            ndisplay = gimp.Display(nimage)
            gimp.displays_flush()

            # floating = pdb.gimp_edit_paste(nlayer)
            # pdb.gimp_sel_floating_anchor(floating)
            # nimage.add_layer(nlayer)
            # nlayer = layer.copy()
            # nlayer = gimp.Layer(nimage, layer.name, layer.width, layer.height, RGB_IMAGE, 100, NORMAL_MODE)
            # nimage.resize_to_layers()
            # ndisplay = pdb.gimp_display_new(nimage)

            # pdb.file_png_save(
            #     RUN_INTERACTIVE,
            #     nimage,
            #     nimage.layers[0],
            #     layer.name,
            #     layer.name,
            #     False,
            #     5,
            #     False,
            #     False,
            #     False,
            #     False,
            #     False
            # )

    pdb.gimp_image_undo_group_end(image)

def open_image_save_and_close():
    pass


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