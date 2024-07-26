import cv2

def main():
    # Load an image
    image = cv2.imread("/home/nvidia/Pictures/1.png")

    # Check if the image was loaded successfully
    if image is None:
        print("Error: Unable to load image")
        return

    # Display the image
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

