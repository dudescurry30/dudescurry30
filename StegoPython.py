# Raymond Mwangi
# ITT-111 Topic 5
# Date: 2/3/2025
# References: www.youtube.com/watch?v-sc7uBxuwwYg (https://github.com/I-Am-Jakoby/hak5-submissions/blob/main/Assets/logo-170-px.png?raw=true)
# Python program implementing Image Steganography


from PIL import Image

# Convert encoding data into 8-bit binary form using ASCII value of characters
def genData(data):
    return [format(ord(i), '08b') for i in data]

# Pixels are modified according to the 8-bit binary data and finally returned
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)

    for i in range(lendata):
        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
                            imdata.__next__()[:3] +
                            imdata.__next__()[:3]]

        # Pixel value should be made odd for 1 and even for 0
        for j in range(8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                pix[j] = pix[j] - 1 if pix[j] != 0 else pix[j] + 1

        # Eighth pixel of every set tells whether to stop or read further.
        if i == lendata - 1:
            if pix[-1] % 2 == 0:
                pix[-1] = pix[-1] - 1 if pix[-1] != 0 else pix[-1] + 1
        else:
            if pix[-1] % 2 != 0:
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)

    for pixel in modPix(newimg.getdata(), data):
        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if x == w - 1:
            x = 0
            y += 1
        else:
            x += 1

# Encode data into image
def encode():
    img = input("Enter image name (with extension): ")
    image = Image.open(img, 'r')

    data = input("Enter data to be encoded: ")
    if len(data) == 0:
        raise ValueError('Data is empty')

    newimg = image.copy()
    encode_enc(newimg, data)

    new_img_name = input("Enter the name of the new image (with extension, e.g., image.png): ")

    # Validate file name and extension
    if "." not in new_img_name or len(new_img_name.split(".")) < 2:
        raise ValueError("Invalid file name! Please include a valid file extension (e.g., .png, .jpg).")

    # Extract file format and handle 'jpg' case
    file_format = new_img_name.split(".")[1].upper()
    if file_format == 'JPG':
        file_format = 'JPEG'

    # Save the image with the correct format
    newimg.save(new_img_name, file_format)


# Decode the data in the image
def decode():
    img = input("Enter image name (with extension): ")
    try:
        image = Image.open(img, 'r')
    except FileNotFoundError:
        print("Image not found. Please try again.")
        return

    data = ''
    imgdata = iter(image.getdata())

    while True:
        pixels = [value for value in imgdata.__next__()[:3] +
                            imgdata.__next__()[:3] +
                            imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            binstr += '0' if i % 2 == 0 else '1'

        data += chr(int(binstr, 2))
        if pixels[-1] % 2 != 0:
            return data

# Main Function
def __main__():
    while True:
        user_input = input(":: Welcome to Steganography ::\n1. Encode\n2. Decode\nEnter your choice: ")
        if user_input.strip():  # Ensure input is not empty or only spaces
            try:
                a = int(user_input)
                if a in [1, 2]:  # Check for valid options
                    break
                else:
                    print("Please enter 1 or 2.")
            except ValueError:
                print("Please enter a valid number.")
        else:
            print("Input cannot be empty. Please enter a valid number.")

    if a == 1:
        print("Encoding selected.")
        encode()
    elif a == 2:
        print("Decoding selected.")
        decoded_data = decode()
        if decoded_data:
            print("Decoded data:", decoded_data)

if __name__ == "__main__":
    __main__()

