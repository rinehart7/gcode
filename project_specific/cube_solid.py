''' Generates gcode for a solid cube. The raster pattern for this code iteration is with the scan paths parallel to the 
    edges of the cube with a 90 degree rotation each layer. The code is set up so each scan path on the interior of the 
    part is deposited in the same direction, with the laser returning to one side after each track. The interior tracks 
    are printed first, then a contour pass is performed. '''

''' Fix from previous version so the core hatches only extend to the total distance minus the hatch distance. This ensures
    there is enough room for a contour pass. Also, fixes the code so it resets the x AND y position after each layer before
    the contour pass '''

# Note that the coordinates in this code are based on absolute coordinates, so the welder must be set to X7.5 Y2 approximately
# and then zeroed to ensure the deposition pattern is correct.

printingFeed=15 # printing feed speed within G-code
movingFeed=200 # feed speed when moving the welder to different locations
x_distance=4 # size of part in x direction
x_step=0.25 # hatch distance when depositing parallel to the y-axis
x_hatch_end_pt=x_distance-x_step # calculates location to stop hatching in x-direction
y_distance=4 # size of part in y direction
y_step=0.25 # hatch distance when depositing parallel to the x-axis
y_hatch_end_pt=y_distance-y_step # calculates location to stop hatching in y-direction
z_height=4 # height of the part
z_step=.25 # height to raise between layers
layers_for_dwell=10 # number of layers before dweel time is added
dwell_time=60 # dwell time in seconds

''' First Layer '''

print("G90 G20 F{}".format(printingFeed), file=open('cube.tap','w')) # set absolute coordinates and inch units
print("G1 Z{}".format(z_step), file=open('cube.tap','a')) # move welder off baseplate to start printing

# core hatching
layer_number=1
x_position=0
y_position=0
z_position=z_step
while layer_number <= (z_height/z_step):
    if layer_number % 2 == 0: # do this hatch pattern if the layer number is divisible by 2
        x_position=-x_step # set initial x to be one hatch away from boundary
        y_init_pos=-y_step # sets the original scan position when rastering along the y-axis
        print("G1 X{} Y{} F{}".format(x_position,y_init_pos,movingFeed), file=open('cube.tap','a')) # set initial position before hatching
        while x_position > -x_distance:
           print("m08", file=open('cube.tap','a')) # turn welder on
           print("G1 Y-{} F{}".format(y_hatch_end_pt,printingFeed), file=open('cube.tap','a')) # print track parallel to y-axis
           print("m09", file=open('cube.tap','a')) # turn welder off
           x_position-=x_step # add hatch distance to current x position
           print("G1 X{} F{}".format(x_position,movingFeed), file=open('cube.tap','a')) # move back to original x position + hatch distance
           print("G1 Y{} F{}".format(y_init_pos,movingFeed), file=open('cube.tap','a')) # additional reset step for y position
        print("G1 X0 Y0 F{}".format(movingFeed), file=open('cube.tap','a')) # move back to origin
    else: # do this hatch pattern for odd layers
        y_position=-y_step # set initial x to be one hatch away from boundary
        x_init_pos=-x_step # sets the original scan position when rastering along the x-axis
        print("G1 X{} Y{} F{}".format(y_position,x_init_pos,movingFeed), file=open('cube.tap','a')) # set initial position before hatching
        while y_position > -y_distance:
            print("m08", file=open('cube.tap','a')) # turn welder on
            print("G1 X-{} F{}".format(x_hatch_end_pt,printingFeed), file=open('cube.tap','a')) # print track parallel to x-axis
            print("m09", file=open('cube.tap','a')) # turn welder off
            y_position-=y_step # add hatch distance to current x position
            print("G1 Y{} F{}".format(y_position,movingFeed), file=open('cube.tap','a')) # move back to original y position + hatch distance
            print("G1 X{} F{}".format(x_init_pos,movingFeed), file=open('cube.tap','a')) # additional reset step for x position
        print("G1 X0 Y0 F{}".format(movingFeed), file=open('cube.tap','a')) # move back to origin

    # do a contour pass around the tracks that were just hatched
    print("m08", file=open('cube.tap','a'))
    print("G1 X-{} F{}".format(x_distance,printingFeed), file=open('cube.tap','a'))
    print("G1 Y-{}".format(y_distance), file=open('cube.tap','a'))
    print("G1 X0", file=open('cube.tap','a'))
    print("G1 Y0", file=open('cube.tap','a'))
    print("m09", file=open('cube.tap','a'))
    z_position+=z_step
    print("G1 Z{}".format(z_position), file=open('cube.tap','a'))
    layer_number+=1
