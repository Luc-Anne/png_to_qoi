#!/bin/python3.10.4

from PIL import Image
from struct import *
import sys

def convert_png_into_qoi(file_input, file_output):
    
    # Input file datas
    img = Image.open(file_input, 'r')
    list_pixels = img.getdata()

    width = img.width
    height = img.height
    bands = 4 if img.getbands() == ('R', 'G', 'B', 'A') else 3
    """
    exif = img._getexif() or {}
    if exif.get(0xA001) == 1 or exif.get(0x0001) == 'R98':
        colorspace = 0
    else:
        colorspace = 1
    """
    colorspace = 0

    qoi_data = encode_qoi(list_pixels, width, height, bands, colorspace)

    # Write on file
    with open(file_output, "wb") as output:
        output.write(qoi_data)

def encode_qoi(list_pixels, width, height, bands, colorspace):

    # Init
    bits_buffer = bytearray()
    
    # HEADER
    bits_buffer += bytes('qoif', "ASCII")
    bits_buffer += (width).to_bytes(4, "big")
    bits_buffer += (height).to_bytes(4, "big")
    bits_buffer += (bands).to_bytes(1, "big")
    bits_buffer += (colorspace).to_bytes(1, "big")
    
    bits_buffer += encode_qoi_pixels(list_pixels, bands)
    
    # FOOTER
    bits_buffer += bytes(7) + b'\x01'
    
    return bits_buffer
    
def encode_qoi_pixels(list_pixels, bands):

    # Init
    bits_buffer_chunks = bytearray()
    
    previous_pixel = (0, 0, 0, 255)
    
    index = list()
    for i in range(64):
        index.append((0,0,0,0))
    if bands == 4 and list_pixels[0] == previous_pixel:
        # 53 is the index position of previous_pixel
        # In case of it is the first pixel, add in index to speed up encode pixels
        # by avoiding change value in running index during runs
        index[53] = (0,0,0,255)
    
    run_len = -1
    
    # ENCODE PIXELS
    for current_pixel in list_pixels:

        if current_pixel == previous_pixel:
            # Start/go on run
            run_len += 1
        else:
            # Close run if exists before working on current pixel
            if not run_len == -1:
                bits_buffer_chunks += QOI_OP_RUN(run_len) #QOI_OP_RUN
                run_len = -1

            # Retrieve detail datas
            r = current_pixel[0]
            g = current_pixel[1]
            b = current_pixel[2]
            a = current_pixel[3] if bands == 4 else 255

            # Working with running index
            index_position = (r * 3 + g * 5 + b * 7 + a * 11) % 64
            
            if index[index_position] == current_pixel:
                bits_buffer_chunks += index_position.to_bytes(1, "big") #QOI_OP_INDEX
            else:
                # Change value in running index
                index[index_position] = current_pixel
                
                # Others possible chunks
                if bands == 4 and current_pixel[3] != previous_pixel[3]:
                    bits_buffer_chunks += pack("BBBBB", 255, r, g, b, a) #QOI_OP_RGBA
                else:
                    dr = (current_pixel[0] - previous_pixel[0] + 2) % 256
                    dg = (current_pixel[1] - previous_pixel[1] + 2) % 256
                    db = (current_pixel[2] - previous_pixel[2] + 2) % 256
                    if dr < 4 and dg < 4 and db < 4 :
                        bits_buffer_chunks += pack('B', 64 + dr * 16 + dg * 4 + db) #QOI_OP_DIFF
                    else:
                        dg_trivial = current_pixel[1] - previous_pixel[1]
                        dg = (dg_trivial + 32) % 256
                        dr_dg = (current_pixel[0] - previous_pixel[0] - dg_trivial + 8) % 256
                        db_dg = (current_pixel[2] - previous_pixel[2] - dg_trivial + 8) % 256
                        if dg < 64 and dr_dg < 16 and db_dg < 16 :
                            bits_buffer_chunks += pack('BB', 128 + dg, dr_dg * 16 + db_dg) #QOI_OP_LUMA
                        else:
                            bits_buffer_chunks += pack("BBBB", 254, r, g, b) #QOI_OP_RGB
    
        previous_pixel = current_pixel

    if not run_len == -1:
        # Close run if still running
        bits_buffer_chunks += QOI_OP_RUN(run_len) #QOI_OP_RUN
    
    return bits_buffer_chunks

def QOI_OP_RUN(run_len):
    
    bits_buffer_chunks_QOI_OP_RUN = bytearray()
    
    for i in range(run_len // 62):
        bits_buffer_chunks_QOI_OP_RUN += (253).to_bytes(1, "big") #QOI_OP_RUN
    bits_buffer_chunks_QOI_OP_RUN += pack('B', 192 + (run_len % 62)) #QOI_OP_RUN
    
    return bits_buffer_chunks_QOI_OP_RUN

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "-h" or sys.argv[1] == "--help":
            print("qoi_convertion.py source.png destination.qoi")
        elif len(sys.argv) == 3:
            convert_png_into_qoi(sys.argv[1], sys.argv[2])
        else:
            print('qoi_convertion.py -h for help')
    else:
        print('qoi_convertion.py -h for help')
