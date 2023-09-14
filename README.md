# Triangle Code

![GitHub](https://img.shields.io/github/license/ElRapt/trianglecode)
![Language](https://img.shields.io/badge/Language-Python-blue)
![Size](https://img.shields.io/badge/Size-1MB-lime)

## Overview

Triangle Code is an innovative and unique approach to encoding and decoding data within a visually meaningful and aesthetically appealing structure. It was developed as a project during my Computer Science undergraduate studies.

> **Disclaimer**: This project is largely conceptual and has certain limitations, particularly regarding the decoding process. It is not recommended for production use.

## Concept

The concept of Triangle Code is to represent data as triangles within an image. A binary '0' is represented by a black triangle and a binary '1' by a white triangle. 

The triangles are read from top to bottom, level by level. Each level contains one more triangle than the previous one. 

## Error Correction

The Triangle Code protocol integrates Reed-Solomon error correction. This means that even if a certain percentage of the data is corrupted, the original message can still be recovered. 

## Operation of Encoding and Decoding

In the Triangle Code protocol, a message goes through two significant phases – encoding and decoding. 

### Encoding
The process begins by encoding the original message. This is done by converting each character in the message into its binary form, each character being represented by an 8-bit binary number corresponding to its ASCII value. For instance, the letter 'A' would be translated into '01000001'. 

After this, the message is further encoded using Reed-Solomon error correction to add redundancy. Reed-Solomon code is a type of systematic code, meaning that the original message is still present in the encoded message, but extra redundant information is appended to the end. This redundancy helps in detecting and correcting errors that might occur during transmission or storage.

Each binary digit (bit) is then represented by a triangular cell in the image – a white triangle represents a '1', while a black triangle represents a '0'. The bits are read from left to right, starting at the top of the triangle and working down each level.

### Decoding
Decoding follows the reverse process of encoding. The triangular cells are read from the top down, left to right, and the color of each cell is converted back into a bit – white cells become '1', black cells become '0'. 

These bits are then grouped into bytes (8 bits per byte), which are then fed into the Reed-Solomon decoder. The Reed-Solomon decoder uses the redundant information encoded earlier to detect and correct any errors that might have occurred.

Finally, each corrected byte is converted back into its corresponding character using the ASCII standard, resulting in the original message being retrieved.

This operation of encoding and decoding allows the Triangle Code to effectively store information in a visual format, while also providing resilience against errors.


## Implementation

The repository contains two main methods, one for encoding a message into an image and another for decoding a message from an image.

`encode_message_in_triangle(message, img, cell_size)`: This function encodes a given message into an image. The message is first encoded with Reed-Solomon for error correction, then converted into a sequence of binary digits which are drawn as triangles in the image.

`decode_message_from_triangle(img, cell_size)`: This function decodes a message from an image. It reads the triangles from the image, converts them back into binary digits, and then decodes the Reed-Solomon encoding to recover the original message.

## Example

Below is the image generated with the message `Hello world` encoded with 10 bytes of redundancy with Reed-Solomon.

![Capture d’écran 2023-05-18 125117](https://github.com/ElRapt/trianglecode/assets/102360910/7a661ad6-6d4b-49cc-871c-f9d93561dfbb)


## Limitations and Potential Improvements

While the Triangle Code protocol presents unique features such as its simplicity, visibility and integration of Reed-Solomon error correction, it also has certain limitations, particularly concerning its resilience to distortion and information density. Future improvements could include increasing the data density, improving the resilience to distortion, and optimizing the Reed-Solomon error correction process.

## Skills Gained

This project allowed me to gain a deep understanding of error correction codes and practical experience in bit and byte manipulation, error handling, and image manipulation.

## Contributions and Future Development

This is an open-source project and contributions are welcome. Please read the contributing guidelines before making a pull request.

## License

Please see the `LICENSE` file for details.



