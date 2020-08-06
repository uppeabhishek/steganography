from os import path

from PIL import Image


def encode(img_path, msg):
    try:
        given_img = Image.open(img_path)

        img = given_img.copy()

        msg_len = len(msg)

        if msg_len > img.size[0] * img.size[1]:
            raise ValueError(
                "Given message length exceeds the length of image. Please shorten the message and try again!!")
        li = []

        msg_char_index = 0
        msg_byte_index = 0

        for c in msg:
            li.append(bin(ord(c))[2:].zfill(8))

        pixels = img.load()

        for i in range(img.size[0]):
            for j in range(img.size[1]):

                if msg_char_index == msg_len:
                    break

                le = 0
                cur_tuple = ()
                for k in pixels[i, j]:
                    if msg_byte_index == 8:
                        cur_tuple = (pixels[i, j][0], pixels[i, j][1],)
                        if msg_char_index + 1 == msg_len:
                            cur_tuple += (1,)
                        else:
                            cur_tuple += (0,)

                        msg_byte_index = 0

                        msg_char_index += 1

                        break

                    if li[msg_char_index][msg_byte_index] == '1':
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

                pixels[i, j] = cur_tuple

        image_basename = path.basename(img_path).split(".")

        img.save(f"{image_basename[0]}_encoded.{image_basename[1]}")

    except ValueError:
        raise ValueError


def decode(img_path):
    try:
        img = Image.open(img_path)

        pixels = img.load()

        for c in "hello":
            print(bin(ord(c)-ord('a'))[2].zfill(8))

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                pass
                # print(pixels[i, j], end=" ")


        msg_char_index = 0
        msg_byte_index = 0

        pass
    except ValueError:
        raise ValueError


def main():
    encode("test.jpeg", "hello")
    # decode("test_encoded.jpeg")
    # decode("test.jpeg")
    # print("Welcome to steganography.")
    # steganography_type = int(input("1. Encode\n2. Decode\n3. Exit\n"))
    #
    # if steganography_type == 1 or steganography_type == 2:
    #     image_path = input("Enter Relative Path for Image: ")
    #     if path.isfile(image_path):
    #
    #         if not image_path.lower().endswith(('.png', '.jpg', '.jpeg')):
    #             print("Not a image")
    #             exit()
    #
    #         if steganography_type == 1:
    #             msg = input("Enter Message to encode: ")
    #             encode(image_path, msg)
    #         else:
    #             decode(image_path)
    #     else:
    #         print("Invalid File Path")
    # else:
    #     exit()


if __name__ == "__main__":
    main()
