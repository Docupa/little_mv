#----------------------------------------------------------------------------------------------------
#2018.11.18 - 2018.11.22
#----------------------------------------------------------------------------------------------------
import sensor, image, time
import time
from pyb import Pin, Timer

sensor.reset() # Initialize the camera sensor.
sensor.set_pixformat(sensor.RGB565) # use RGB565.160x128
sensor.set_framesize(sensor.QQVGA) # use QQVGA for speed.
sensor.skip_frames(10) # Let new settings take affect.
sensor.set_auto_whitebal(False) # turn this off.
clock = time.clock() # Tracks FPS.
green_find_n=[0,0]
back_nn=[0,0]
cant_ball=[0,0]
# For color tracking to work really well you should ideally be in a very, very,
# very, controlled enviroment where the lighting is constant...
green_threshold   = (0, 100, -128, -26, -128, 127)
red_threshold = (0, 100, 34, 127, -128, 127)
blue_threshold= (0, 79, -128, 6, -128, -20)
size_threshold = 2000
# init pin
#---------------------------------------------------------
# to pin2 and pin3, the pin 2 is high bit, the pin 3 is low bit, so clamp is 01, loosen is 10
send_signal_1 = Pin('P2',mode=Pin.OUT)
send_signal_2 = Pin('P3',mode=Pin.OUT)
recv_signal_1 = Pin('P0',mode=Pin.IN)
recv_signal_2 = Pin('P1',mode=Pin.IN)
send_signal_1.low()
send_signal_2.low()
pwm_left1 = Pin('P4')
pwm_left2 = Pin('P5')
tim = Timer(2, freq=1000)
left1 = tim.channel(3, Timer.PWM, pin=pwm_left1)
left2 = tim.channel(4, Timer.PWM, pin=pwm_left2)
pwm_right1 = Pin('P7')
pwm_right2 = Pin('P8')
tim = Timer(4, freq=1000)
right1 = tim.channel(1, Timer.PWM, pin=pwm_right1)
right2 = tim.channel(2, Timer.PWM, pin=pwm_right2)
left1.pulse_width_percent(0)
left2.pulse_width_percent(0)
right1.pulse_width_percent(0)
right2.pulse_width_percent(0)
get_ball=Pin('P9',mode=Pin.IN,pull=Pin.PULL_DOWN)
get_green=Pin('P6',mode=Pin.IN,pull=Pin.PULL_DOWN)
#---------------------------------------------------------

def car_move(left,right):
	#print("car_move...")
	if left < 0 and right < 0:# car_back, direction not ensure
		left1.pulse_width_percent(0)
		left2.pulse_width_percent(abs(left))
		right1.pulse_width_percent(0)
		right2.pulse_width_percent(abs(right))
	elif left < 0 and right > 0: # only turn left
		left1.pulse_width_percent(abs(left))
		left2.pulse_width_percent(0)
		right1.pulse_width_percent(0)
		right2.pulse_width_percent(abs(right))
	elif left > 0 and right < 0: # only turn right
		left1.pulse_width_percent(0)
		left2.pulse_width_percent(abs(left))
		right1.pulse_width_percent(abs(right))
		right2.pulse_width_percent(0)
	else : # car_go or stop, direction not ensure
		left1.pulse_width_percent(abs(left))
		left2.pulse_width_percent(0)
		right1.pulse_width_percent(abs(right))
		right2.pulse_width_percent(0)

def run(circle_x,circle_y,flag=0,green_blob=0,back_n=0,can_ball=0):
	#print("run...")
	left_speed=0
	right_speed=0
	turn_flag=0
	can_clip=1
	move_back=0
	if flag == 0:
		#The target point is about x=90,y=104,wait to debug
		if circle_y  < 100:#should cloes to ball
			can_clip=0
			turn_flag=1
			left_speed=50
			right_speed=50
			back_n[0]=0
		elif circle_y > 104:
			back_n[0]=back_n[0]+1
			move_back=1
			can_clip=0
			turn_flag=1
			left_speed=-50
			right_speed=-50
			if back_n[0] > 200:
				car_move(100,100)
				time.sleep(800)
		if move_back==0:
			if get_green.value()==1:
				car_move(-100,-100)
				time.sleep(800)
				car_move(100,-100)
				time.sleep(800)
			'''
			clock.tick() # Track elapsed milliseconds between snapshots().
			img = sensor.snapshot() # Take a picture and return the image.
			green_blobs=img.find_blobs([green_threshold],roi=(0,65,160,95))
			if green_blobs:
				green_chunk=find_max(green_blobs)
				if green_chunk.h()> 30:
					#print("turn!!!green")
					#img.draw_rectangle(green_chunk[:4])
					if green_chunk.cx()<=90:
						right_speed=right_speed-40
					else :
						right_speed=right_speed-40
			'''
			if circle_x  < 86:#should turn right
				can_clip=0
				if turn_flag == 0:
					left_speed = -25
					right_speed = 25
				else :
					left_speed = left_speed + 40
			elif circle_x > 90:#should turn left
				can_clip=0
				if turn_flag == 0:
					left_speed = 25
					right_speed = -25
				else :
					right_speed = right_speed +40
		else:# other way to car_back
			if circle_x  < 86:#should turn right
				can_clip=0
				if turn_flag == 0:
					left_speed = -25
					right_speed = 25
				else :
					left_speed = left_speed - 40
			elif circle_x > 90:#should turn left
				can_clip=0
				if turn_flag == 0:
					left_speed = 25
					right_speed = -25
				else :
					right_speed = right_speed - 40
		if can_clip and can_ball[0] < 3:
			car_move(0,0)
			can_ball[0]=can_ball[0]+1
			loosen_signal()
			clamping_signal()
		elif can_ball[0] >= 3:
			car_move(-100,100)
			time.sleep(500)
			can_ball[0]=0
		else :
			car_move(left_speed,right_speed)
		return 0
	else :
		left_speed=60
		right_speed=60
		'''
		if w * h > 200 :#200 is not ensure
			if abs(circle_x-80) <= 2 :# emmmmm......
				car_move(0,0)
				loosen_signal()
				go_back()
				return 1
			else:
				turn_flag=0
		'''
		#print("rect=",green_blob.w()*green_blob.h())
		#print("rectxy=",green_blob.cx(),green_blob.cy())
		if green_blob.w() * green_blob.h()> 170:
			'''
			if green_blob.w() * green_blob.h() < 450:
				if green_blob.w() / green_blob.h() < 3:
					car_move(50,-50)
					return 0
			'''
			if get_green.value()==1 :#200 is not ensure
				time.sleep(10)
				if get_green.value()==1 :
					#print("green_blob!!!!!")
					car_move(0,0)
					loosen_signal()
					go_back()
				#print("green_turn_left")
					return 1
			if green_blob.cx()  < 79:#should turn right
				#print("green_turn_right")
				if green_blob.cx() < 62:
					left_speed = -80
					right_speed = 80
				else :
					left_speed = left_speed + 50
					#right_speed=right_speed-20
			elif green_blob.cx() > 81:#should turn left
				if green_blob.cx() > 96:
					left_speed = 80
					right_speed = -80
				else :
					right_speed = right_speed + 50
					#left_speed=left_speed-20
			car_move(left_speed,right_speed)
			return 0
		else :
			return 0
	
def find_max(blobs):
	max_size=0
	for blob in blobs:
		if blob[2]*blob[3] > max_size:
			max_blob=blob
			max_size = blob[2]*blob[3]
	return max_blob

def find_max_circle(blobs):
	max_size=0
	for blob in blobs:
		if blob.r() * blob.r() > max_size:
			max_blob=blob
			max_size=blob.r() * blob.r()
	return max_blob

def find_green_place_then_go(img,green_find_n):
	#print("find_green_place_then_go...")
	clock.tick() # Track elapsed milliseconds between snapshots().
	img = sensor.snapshot() # Take a picture and return the image.
	green_blobs=img.find_blobs([green_threshold],roi=(0,65,160,95))# can change roi parameter
	if green_blobs:
		green_blob=find_max(green_blobs)
		img.draw_rectangle(green_blob[:4])
		img.draw_cross(green_blob.cx(),green_blob.cy())
		print(green_blob.w() / green_blob.h())
		if green_blob.w() * green_blob.h()> 170:
			run(green_blob.cx(),green_blob.cy(),1,green_blob)
			green_find_n[0]=0
			return 0
	'''
	green_find_n[0]=green_find_n[0]+1
	if green_find_n[0] > 700:
		color_area_all=0
		green_blue_blob=img.find_blobs([blue_threshold],roi=(0,65,160,95))
		green_red_blob=img.find_blobs([red_threshold],roi=(0,65,160,95))
		color_area_all=color_area_all+len(green_blue_blob)+len(green_red_blob)
		if color_area_all > 8:
			car_move(100,100)
			time.sleep(3000)
			green_find_n[0]=0
			return 0
	'''
	car_move(-70,70)

def loosen_signal():
	#print("send_loosen_signal...")
	send_signal_1.high() # send_signal_1 --> pin2 --> 32 pin10 --> in
	while recv_signal_1.value()==0:# recv_signal_1 --> pin0 --> 32 pin13 --> out
		while recv_signal_1.value()==0:
			pass
		time.sleep(10)
	send_signal_1.low()

def clamping_signal():
	#print("send_clamping_signal...")
	send_signal_2.high() # send_signal_2 --> pin3 --> 32 pin11 --> in 
	while recv_signal_2.value()==0: # recv_signal_2 --> pin1 --> 32 pin12 --> out
		while recv_signal_2.value()==0:
			pass
		time.sleep(10)
	if recv_signal_1.value()==1 and recv_signal_2.value()==1:
		car_move(70,-70)
		send_signal_2.low()
		time.sleep(500)#not ensure
	send_signal_2.low()
	
def go_back():
	#print("go_back...")
	car_move(-100,-100)
	time.sleep(1000)
	car_move(100,-100)
	time.sleep(250)
	
	
	
	
while(True):
	flag=0
	clock.tick() # Track elapsed milliseconds between snapshots().
	img = sensor.snapshot() # Take a picture and return the image.
	if get_ball.value():
		cant_ball[0]=0
		'''
		isnt_ball=img.find_blobs([blue_threshold],roi=(65,15,45,45))
		isnt_ball=find_max(isnt_ball)
		if isnt_ball.area() > 250:
			loosen_signal()
			continue
		'''
		#print("have right up ball")
		find_green_place_then_go(img,green_find_n)
		flag=1
		continue
	# no ball in the mechanical claws
	if flag==0:
		blobs = img.find_blobs([blue_threshold],roi=(0,65,160,95))# roi is not ensure
		if blobs:
			max_blob = find_max(blobs)
			#img.draw_rectangle(max_blob[0:4])
			nice_area=(max_blob[0]-5,max_blob[1]-5,max_blob[2]+10,max_blob[3]+10)
			#nice_chunk = img.copy(roi=nice_area) #heap memory overflow,and fuck myself because I forget the roi parameter in find_circles
			#img.draw_image(nice_chunk,0,0)
			all_circle=img.find_circles(roi=nice_area,threshold = 2000, x_margin = 10, y_margin = 10, r_margin = 10,r_min = 2, r_max = 30, r_step = 2)
			if all_circle:
				max_circle=find_max_circle(all_circle)
				run(max_circle.x(),max_circle.y(),back_n=back_nn,can_ball=cant_ball)
			else :
				run(max_blob.x()+max_blob.w()/2,max_blob.y()+max_blob.h()/2,back_n=back_nn,can_ball=cant_ball)
			'''
			if all_circle:
				img.draw_circle(max_circle.x(), max_circle.y(), max_circle.r(), color = (0, 255, 0))
				img.draw_cross(max_circle.x(), max_circle.y())
			else :
				img.draw_rectangle(max_blob[0:4]) # rect
				img.draw_cross(max_blob[5], max_blob[6]) # cx, cy
			#print("fps:",clock.fps())
			'''
		else:
			car_move(60,-60)
			#print("not find\n")
			#print("nothing??")
