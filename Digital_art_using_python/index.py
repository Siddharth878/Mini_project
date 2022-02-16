from audioop import findfactor
from math import factorial
import random
from PIL import Image, ImageDraw,ImageChops
import colorsys

def random_colors(): # this is modified to hsv and then to rgb
    h = random.random() # will return value between 0 and 1
    s = 1 # ie.. maximum
    v = 1 # ie.. maximum
    
    float_rgb = colorsys.hsv_to_rgb(h,s,v)
    rgb = [int(x*255) for x in float_rgb]
    
    return tuple(rgb)

# this here is for gradient


def interpolate(sc, ec, factor: float):

    reciprocal = 1-factor
    return (
        int(sc[0]*reciprocal + ec[0]*factor),
        int(sc[1]*reciprocal + ec[1]*factor),
        int(sc[2]*reciprocal + ec[2]*factor)
    )


def generateArt(path:str):
    print("Generating art ")
    
    scale_factor = 2
    target_size_px = 256
    img_size_px=target_size_px*scale_factor

    # colors

    start_color=random_colors()
    end_color=random_colors()
    bg_color=(0, 0, 0)
    image=Image.new("RGB",
    size = (img_size_px, img_size_px),
    color = bg_color)    # size and color and not necessary to write

    # let's set padding pixels
    pad_px=16*scale_factor

    # To draw lines we have to import ImageDraw
    draw=ImageDraw.Draw(image)  # So Draw is the object we can intereact with


   # Generate the points
    points=[]
    for i in range(0, 10):
        randompnt=(random.randint(pad_px, img_size_px-pad_px),
        random.randint(pad_px, img_size_px-pad_px))
        points.append(randompnt)


   
    min_x = min([p[0] for p in points])
    max_x = max([p[0] for p in points])
    min_y = min([p[1] for p in points])
    max_y = max([p[1] for p in points])

    delta_x = min_x -(img_size_px-max_x)
    delta_y = min_y - (img_size_px-max_y)
   
    
    # draw.rectangle((min_x,min_y,max_x,max_y),outline = (0,0,0))

    for i,point in enumerate(points):
        points[i] = (point[0]-delta_x//2,point[1]-delta_y//2)
        
    
    # min_x = min([p[0] for p in points])
    # max_x = max([p[0] for p in points])
    # min_y = min([p[1] for p in points])
    # max_y = max([p[1] for p in points])
    # draw.rectangle((min_x,min_y,max_x,max_y),outline = (230,230,230))




    thick=1*scale_factor

    # this is the main function
    n_points=len(points)-1

      
    for i,point in enumerate(points): # this is tuple unpacking
        # randompnt = (random.randint(0,img_size_px),random.randint(0,img_size_px)) # This is a point therefore it should have two points stored in tuple
        # randompnt2 = (random.randint(0,img_size_px),random.randint(0,img_size_px)) # and also we need a 2nd point to connect the line
        # print(i)
        


        # Overlay_canvas

        overlay_image = Image.new("RGB",
        size = (img_size_px, img_size_px),
        color = bg_color)
        overlay_draw = ImageDraw.Draw(overlay_image)
        

        # Search for random points but still connnected from the previous one
        rp1=point
        if i == n_points:
            rp2=points[0]
        else:
            rp2=points[i+1]


        line_xy=(rp1, rp2)
        color_factor=i/n_points
        default_line_C=interpolate(start_color, end_color, color_factor)

        overlay_draw.line(line_xy, fill = (default_line_C), width = thick)
        thick += scale_factor
        image = ImageChops.add(image,overlay_image)
    
    image = image.resize((target_size_px,target_size_px),resample=Image.ANTIALIAS)
    image.save(path)




if __name__ == '__main__':

    for i in range(10):
        generateArt(f'test_image{i}.png')
