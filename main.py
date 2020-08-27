from math import ceil
from os import path

from Crypto.Cipher import AES
from PIL import Image

extra_char = '#'


def encode(img_path, msg, key):
    try:
        obj = AES.new(key)

        le = len(msg)

        msg = msg.ljust(ceil(le / 16) * 16, extra_char)

        ciphertext = obj.encrypt(msg)

        img = Image.open(img_path)

        new_image = Image.new(img.mode, img.size)

        ciphertext = ciphertext.hex()

        msg_len = len(ciphertext)

        if msg_len > img.size[0] * img.size[1]:
            raise ValueError(
                "Given message length exceeds the length of image. Please shorten the message and try again!!")
        li = []

        msg_char_index = 0
        msg_byte_index = 0

        for c in ciphertext:
            li.append(bin(ord(c))[2:].zfill(8))

        pixels = img.load()

        should_break = False

        for i in range(img.size[0]):

            for j in range(img.size[1]):

                if msg_char_index == msg_len:
                    should_break = True

                if should_break:
                    new_image.putpixel((i, j), pixels[i, j])
                    continue

                le = 0

                cur_tuple = ()

                for k in pixels[i, j]:
                    if msg_byte_index == 8:
                        cur_tuple = (cur_tuple[0], cur_tuple[1],)
                        if msg_char_index + 1 == msg_len:
                            cur_tuple += (1,)
                        else:
                            cur_tuple += (0,)

                        msg_byte_index = 0

                        msg_char_index += 1

                        break

                    if li[msg_char_index][msg_byte_index] == '0':
                        if k % 2 != 0:
                            cur_tuple += (pixels[i, j][le] - 1,)
                        else:
                            cur_tuple += (pixels[i, j][le],)
                    else:
                        if k % 2 == 0:
                            cur_tuple += (pixels[i, j][le] + 1,)
                        else:
                            cur_tuple += (pixels[i, j][le],)

                    le += 1
                    msg_byte_index += 1

                new_image.putpixel((i, j), cur_tuple)

        # Copy remaining Pixels
        for i1 in range(i, img.size[0]):
            for j1 in range(j, img.size[1]):
                new_image.putpixel((i1, j1), pixels[i1, j1])

        image_basename = path.basename(img_path).split(".")

        new_image.save(f"{image_basename[0]}_encoded.png")

        print(f"Image save as {image_basename[0]}_encoded.png in current directory..\n")

    except ValueError:
        raise ValueError


def decode(img_path, key):
    try:
        img = Image.open(img_path)

        pixels = img.load()
        cnt = 0

        should_break = False

        res = []
        cur_string = ""

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                for k in pixels[i, j]:
                    if cnt == 8:
                        res.append(cur_string)
                        cur_string = ""
                        cnt = 0
                        if k == 1:
                            should_break = True
                            break
                    else:
                        if k % 2 == 0:
                            cur_string += '0'
                        else:
                            cur_string += '1'

                        cnt += 1

                if should_break:
                    break

            if should_break:
                break
        result = ""

        for ele in res:
            result += chr(int(ele, 2))

        obj = AES.new(key)

        try:
            result = obj.decrypt(bytes.fromhex(result)).decode("utf-8")
            special_char_index = result.find("#")
            print(f"Decoded String is : {result[0:special_char_index]}")
        except ValueError:
            print("Entered Key is incorrect")

    except ValueError:
        raise ValueError


def main():
    print("Welcome to steganography.")
    steganography_type = int(input("1. Encode\n2. Decode\n3. Exit\n"))

    key_len = 32

    if steganography_type == 1 or steganography_type == 2:
        image_path = input("Enter Relative Path for Image: \n")
        if path.isfile(image_path):
            if not image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
                print("Not a valid image. Only .png,.jpg,.jpeg formats are accepted.\n")
                exit()

            if steganography_type == 1:
                key = input(
                    "Please Enter Secret Key to encode text(Maximum 32 characters long and don't add # in the key): \n")

                if len(key) > key_len:
                    print("Entered Key Length is greater than 32 characters")
                    exit()

                if '#' in key:
                    print("Key shouldn't contain # character")
                    exit()
                key = key.ljust(key_len, extra_char)

                msg = input("Enter Message to encode(Dont add # in the msg): \n")

                if '#' in msg:
                    print("Entered Message shouldn't contain # character")
                    exit()

                encode(image_path, msg, key)
            else:
                key = input("Please Enter Secret Key to decode text(Maximum 32 characters long): \n")
                if len(key) > key_len:
                    print("Entered Key Length is greater than 32 characters")
                    exit()
                if '#' in key:
                    print("Key shouldn't contain # character")
                    exit()
                key = key.ljust(key_len, extra_char)
                decode(image_path, key)
        else:
            print("Invalid File Path")
    else:
        exit()


if __name__ == "__main__":
    main()
