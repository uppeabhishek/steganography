**Visual Cryptography Steganography**

Cryptography is the process of encryption and decryption of text data.

Steganography is the process of hiding text data inside images, audio, video.

So we can mix both Cryptography and Steganography and achieve good level of security while transmitting images or videos.

I have used AES algorithm for text encryption and decryption.

There are several algorithms for achieving steganography.

In this project I have implemented LST(Least Significant Bit) algorithm on Steganography.

Features

1. **Encoding**: Users need to enter an image path, secret key and text to be encoded.
    
    **Result**: Image with encrypted text hidden inside image.
  
2. **Decoding**: Users need to enter an image path and secret key to decode text.
    
    **Result**: Decrypted Text decoded from image.
