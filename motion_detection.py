#// Don't forget to hit SUBSCRIBE, LIKE, COMMENT, and LEARN! its good to learn :)

#imports
import cv2
import time
import datetime
import imutils


def motion_detection():
    video_capture = cv2.VideoCapture(0) # value (0) selects the devices default camera
    time.sleep(2)

    first_frame = None # instinate the first fame

    while True:
        frame = video_capture.read()[1] # gives 2 outputs retval,frame - [1] selects frame
        text = 'Unoccupied'

        greyscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # make each frame greyscale wich is needed for threshold 

        gaussian_frame = cv2.GaussianBlur(greyscale_frame, (21,21),0)
        # uses a kernal of size(21,21) // has to be odd number to to ensure there is a valid integer in the centre
        # and we need to specify the standerd devation in x and y direction wich is the (0) if only x(sigma x) is specified 
        # then y(sigma y) is taken as same as x. sigma = standerd deveation(mathmetics term) 

        blur_frame = cv2.blur(gaussian_frame, (5,5)) # uses a kernal of size(5,5)(width,height) wich goes over 5x5 pixel area left to right
        # does a calculation and the pixel located in the centre of the kernal will become 
        # a new value(the sum of the kernal after the calculations) and then it moves to the right one and has a new centre pixel
        # and does it all over again..untill the image is done, obv this can cause the edges to not be changed, but is very minute

        greyscale_image = blur_frame 
        # greyscale image with blur etc wich is the final image ready to be used for threshold and motion detecion

        if first_frame is None:
            first_frame = greyscale_image 
            # first frame is set for background subtraction(BS) using absdiff and then using threshold to get the foreground mask
            # foreground mask (black background anything that wasnt in image in first frame but is in newframe over the threshold will
            # be a white pixel(white) foreground image is black with new object being white...there is your motion detection
        else:
            pass


        frame = imutils.resize(frame, width=500)
        frame_delta = cv2.absdiff(first_frame, greyscale_image) 
        # calculates the absolute diffrence between each element/pixel between the two images, first_frame - greyscale (on each element)
        
        # edit the ** thresh ** depending on the light/dark in room, change the 100(anything pixel value over 100 will become 255(white))
        thresh = cv2.threshold(frame_delta, 100, 255, cv2.THRESH_BINARY)[1]
        # threshold gives two outputs retval,threshold image. using [1] on the end i am selecting the threshold image that is produced

        dilate_image = cv2.dilate(thresh, None, iterations=2)
        # dilate = dilate,grow,expand - the effect on a binary image(black background and white foregorund) is to enlarge/expand the white 
        # pixels in the foreground wich are white(255), element=Mat() = default 3x3 kernal matrix and iterartions=2 means it
        # will do it twice

        cnt = cv2.findContours(dilate_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[1]
        # contours gives 3 diffrent ouputs image, contours and hierarchy, so using [1] on end means contours = [1](cnt)
        # cv2.CHAIN_APPROX_SIMPLE saves memory by removing all redundent points and comppressing the contour, if you have a rectangle
        # with 4 straight lines you dont need to plot each point along the line, you only need to plot the corners of the rectangle
        # and then join the lines, eg instead of having say 750 points, you have 4 points.... look at the memory you save!

        for c in cnt:
            if cv2.contourArea(c) > 800: # if contour area is less then 800 non-zero(not-black) pixels(white)
                (x, y, w, h) = cv2.boundingRect(c) # x,y are the top left of the contour and w,h are the width and hieght 

                cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2) # (0, 255, 0) = color R,G,B = lime / 2 = thickness(i think?)(YES IM RITE!)
                # image used for rectangle is frame so that its on the secruity feed image and not the binary/threshold/foreground image
                # as its already used the threshold/(binary image) to find the contours this image/frame is what image it will be drawed on

                text = 'Occupied'
                # text that appears when there is motion in video feed
            else:
                pass


        ''' now draw text and timestamp on security feed '''
        font = cv2.FONT_HERSHEY_SIMPLEX 

        cv2.putText(frame, '{+} Room Status: %s' % (text), 
            (10,20), cv2.FONT_HERSHEY_SIMPLEX , 0.5, (0, 0, 255), 2)
        # frame is the image on wich the text will go. 0.5 is size of font, (0,0,255) is R,G,B color of font, 2 on end is LINE THICKNESS! OK :)


        cv2.putText(frame, datetime.datetime.now().strftime('%A %d %B %Y %I:%M:%S%p'), 
            (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX , 0.35, (0, 0, 255),1) # frame.shape[0] = hieght, frame.shape[1] = width,ssssssssssssss
        # using datetime to get date/time stamp, for font positions using frame.shape() wich returns a tuple of (rows,columns,channels)
        # going 10 accross in rows/width so need columns with frame.shape()[0] we are selecting columns so how ever many pixel height 
        # the image is - 10 so oppisite end at bottom instead of being at the top like the other text

        cv2.imshow('Security Feed', frame)
        cv2.imshow('Threshold(foreground mask)', dilate_image)
        cv2.imshow('Frame_delta', frame_delta)

        key = cv2.waitKey(1) & 0xFF # (1) = time delay in seconds before execution, and 0xFF takes the last 8 bit to check value or sumin
        if key == ord('q'):
            cv2.destroyAllWindows()
            break
                


if __name__=='__main__':    
    motion_detection()











