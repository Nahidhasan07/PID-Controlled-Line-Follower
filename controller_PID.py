"""LFR controller."""
#controller_PID
# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
##color funtion
def color_identification(ar):
    res=[1,0,1]
    for i in range(len(ar)):
        x=ar[i]
        if (x<350):
             ##white=1
             res[i]=1
        elif (x>350):
             ##black=0
             res[i]=0
                     
    return res
##error number
def error_function(ar):
    err=-1
    if (ar[0]==0 and ar[1]==0 and ar[2]==1):
          err=1 ##mid & left in black
    elif (ar[0]==0 and ar[1]==1 and ar[2]==1):
         err=2  ## only left in black
    elif (ar[0]==1 and ar[1]==0 and ar[2]==0):
         err=3  ## mid & right in black
    elif (ar[0]==1 and ar[1]==1 and ar[2]==0):
         err=4  ## only right in black  
            
    return err
#error correction_left
def error_correction_Left(err,speed,ar):
    per=0.60
    newL=speed
    if err==1:
       newL=speed-((per*speed)/(ar[0]+ar[1]+ar[2]))
    elif err==2:
       newL=speed-((per*speed)/(ar[0]+ar[1]+ar[2]))
    elif err==3:
       newL=speed+((per*speed)/(ar[0]+ar[1]+ar[2]))
    elif err==4:
       newL=speed+((per*speed)/(ar[0]+ar[1]+ar[2]))
       
    return newL
    
#error correction_right
def error_correction_Right(err,speed,ar):
    per=0.60
    newR=speed
    if err==1:
       newR=speed+((per*speed)/(ar[0]+ar[1]+ar[2]))
    elif err==2:
       newR=speed+((per*speed)/(ar[0]+ar[1]+ar[2]))
    elif err==3:
       newR=speed-((per*speed)/(ar[0]+ar[1]+ar[2]))
    elif err==4:
       newR=speed-((per*speed)/(ar[0]+ar[1]+ar[2]))
       
    return newR    

#kind of main funtion
def main_function(robot):
    # You should insert a getDevice-like function in order to get the
    # instance of a device of the robot. Something like:
    #  motor = robot.getMotor('motorname')
    #  ds = robot.getDistanceSensor('dsname')
    #  ds.enable(timestep)
    
    time_step = 32
    speed = 5 #(3.50 to 6)
    
    blm=robot.getDevice('wheel_4')
    brm=robot.getDevice('wheel_3')
    flm=robot.getDevice('wheel_2')
    frm=robot.getDevice('wheel_1')
    
    blm.setPosition(float('inf'))
    brm.setPosition(float('inf'))
    flm.setPosition(float('inf'))
    frm.setPosition(float('inf'))
    
    blm.setVelocity(0)
    brm.setVelocity(0)
    flm.setVelocity(0)
    frm.setVelocity(0)
    
    lir=robot.getDevice('left')
    lir.enable(time_step)
    rir=robot.getDevice('right')
    rir.enable(time_step)
    mid=robot.getDevice('mid')
    mid.enable(time_step)
    ##array
    ar=[0,1,0] ##white black white
    n=1 #count
    # Main loop:
    # - perform simulation steps until Webots is stopping the controller
    while robot.step(time_step) != -1:
            # Read the sensors:
            # Enter here functions to read sensor data, like:
            #  val = ds.getValue()
            # print("n=", n)
            lir_val=lir.getValue()
            rir_val=rir.getValue()
            mid_val=mid.getValue()
            print("left: {} mid: {} right: {}".format(lir_val,mid_val,rir_val))

            #Process sensor data here.
            ar=[lir_val,mid_val,rir_val]
            ar=color_identification(ar)
            print("array ", ar)
            ##
            err=error_function(ar)
            print("error number ", err)
            ##
            ls=error_correction_Left(err,speed,ar)
            rs=error_correction_Right(err,speed,ar)
            print("left speed ", ls)
            print("right speed", rs)
            # #motor.setPosition(10.0)
            blm.setVelocity(ls)
            brm.setVelocity(rs)
            flm.setVelocity(ls)
            frm.setVelocity(rs)
            print("count ", n)
            n=n+1
    
# Enter here exit cleanup code.

if __name__ == "__main__":
 # create the Robot instance.
    robot = Robot()
    main_function(robot)