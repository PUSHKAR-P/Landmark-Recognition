#Landmark Recognition

import numpy as np
from normailze import normalize
import pandas as pd
import requests
import cv2
from sklearn import svm
from sklearn.metrics import classification_report,accuracy_score

def conv(mag,angle,b,a) :
	mat=np.zeros(9)
	for i in range(17*a,17*a+17):
		for j in range(17*b,17*b+17):
			m=0
			if(angle[i][j]>=180):
				m=angle[i][j]%180
			x=m%20
			y=m/20
			z=int(y)
			p=mag[i][j]*((20-x)/20)
			mat[z]+=p
			if(y>8):
				mat[1]+=mag[i][j]-p
			else:
				mat[z+1]+=mag[i][j]-p
	return mat
              

<<<<<<< HEAD
df=pd.read_csv(r"/home/kartikey/Desktop/Landmark/landmarks.csv")
df1=df["URL"]
df2=df["labels"]
print(type(df2[0]))
hog_features = []
for i in range(38,43):
=======
df=pd.read_csv(r"C:\Users\Aditya\Desktop\Landmark-Recognition\landmarks.csv")
df1=df["URL"]
hog_features = []
for i in range(0,81):
>>>>>>> d679c9cdfc79a73a0c4903ea81d5edfb6dcf64c9
	file_name='image.jpg'
	url = df1[i]
	r = requests.get(url, allow_redirects=True)
	try:
		open(file_name, 'wb').write(r.content)
		img = cv2.imread(file_name,0)
		newimg= cv2.resize(img,(102,255))
	except Exception as e:
		print(str(e))
<<<<<<< HEAD
		df2=df2.drop(df[i],axis=0,inplace=True)
=======
>>>>>>> d679c9cdfc79a73a0c4903ea81d5edfb6dcf64c9
		continue
	#cv2.imshow('image',newimg)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
	print(i)
	newimg = np.float32(newimg) / 255.0 
	gx = cv2.Sobel(newimg, cv2.CV_32F, 1, 0, ksize=1)
	gy = cv2.Sobel(newimg, cv2.CV_32F, 0, 1, ksize=1)
	mag, angle = cv2.cartToPolar(gx, gy, angleInDegrees=True)
	if(i==15):
		print(len(angle),len(angle[0]))
	bin_hist=np.zeros((15,6,9))
	for k in range(0,15):
		for j in range(0,6):
			bin_hist[k][j]=conv(mag,angle,j,k)


	hog_descriptor=np.zeros((0))
	for k in range(0,14):
		for j in range(0,5):
			temp=np.concatenate((bin_hist[k][j],bin_hist[k+1][j],bin_hist[k][j+1],bin_hist[k+1][j+1]))
			hog_descriptor=np.concatenate((hog_descriptor,normalize(temp)))
	hog_features.append(hog_descriptor)


<<<<<<< HEAD
labels =  np.array(df2).reshape(len(df2),1) 
=======
labels =  np.array(df['labels']).reshape(len(df['labels']),1) 
>>>>>>> d679c9cdfc79a73a0c4903ea81d5edfb6dcf64c9
clf = svm.SVC()
hog_features = np.array(hog_features)
print(len(hog_features), len(hog_features[0]))
print(len(labels), len(labels[0]))
data_frame = np.hstack((hog_features,labels))
np.random.shuffle(data_frame)


percentage = 80
partition = int(len(hog_features)*percentage/100)

x_train, x_test = data_frame[:partition,:-1],  data_frame[partition:,:-1]
y_train, y_test = data_frame[:partition,-1:].ravel() , data_frame[partition:,-1:].ravel()

clf.fit(x_train,y_train)

y_pred = clf.predict(x_test)

print("Accuracy: "+str(accuracy_score(y_test, y_pred)))
print('\n')
print(classification_report(y_test, y_pred))