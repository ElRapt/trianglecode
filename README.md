# Triangle Code

## Overview

Triangle Code is an innovative and unique approach to encoding and decoding data within a visually meaningful and aesthetically appealing structure. It was developed as a project during my Computer Science undergraduate studies.

> **Disclaimer**: This project is largely conceptual and has certain limitations, particularly regarding the decoding process. It is not recommended for production use.

## Concept

The concept of Triangle Code is to represent data as triangles within an image. A binary '0' is represented by a black triangle and a binary '1' by a white triangle. 

The triangles are read from top to bottom, level by level. Each level contains one more triangle than the previous one. 

## Error Correction

The Triangle Code protocol integrates Reed-Solomon error correction. This means that even if a certain percentage of the data is corrupted, the original message can still be recovered. 

## Implementation

The repository contains two main methods, one for encoding a message into an image and another for decoding a message from an image.

`encode_message_in_triangle(message, img, cell_size)`: This function encodes a given message into an image. The message is first encoded with Reed-Solomon for error correction, then converted into a sequence of binary digits which are drawn as triangles in the image.

`decode_message_from_triangle(img, cell_size)`: This function decodes a message from an image. It reads the triangles from the image, converts them back into binary digits, and then decodes the Reed-Solomon encoding to recover the original message.

## Limitations and Potential Improvements

While the Triangle Code protocol presents unique features such as its simplicity, visibility and integration of Reed-Solomon error correction, it also has certain limitations, particularly concerning its resilience to distortion and information density. Future improvements could include increasing the data density, improving the resilience to distortion, and optimizing the Reed-Solomon error correction process.

## Skills Gained

This project allowed me to gain a deep understanding of error correction codes and practical experience in bit and byte manipulation, error handling, and image manipulation.

## Contributions and Future Development

This is an open-source project and contributions are welcome. Please read the contributing guidelines before making a pull request.

## License

Please see the `LICENSE` file for details.
