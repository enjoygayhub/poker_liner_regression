import pandas as pd

data = pd.read_csv('file0.csv')
features = data[:]

x=features.values.T


m=400 #训练样本为前400个
alpha = 0.01#学习率0.01
theta0 = 1
theta1 = 1
theta2 = 1
theta3 = 1
theta4 = 1
theta5 = 1
for i in range (100000):
    sum0=0
    sum1=0
    sum2=0
    sum3=0
    sum4=0
    sum5=0
    for j in range(400):
        number=theta0+theta1*x[0][j]+theta2*x[1][j]+theta3*x[2][j]+theta4*x[3][j]+theta5*x[4][j]-x[5][j]
        sum0+=number
        sum1+=number*x[0][j]
        sum2+=number*x[1][j]
        sum3+=number*x[2][j]
        sum4+=number*x[3][j]
        sum5+=number*x[4][j]
    temp0=theta0-alpha*(1/m)*sum0
    temp1=theta1-alpha*(1/m)*sum1
    temp2=theta2-alpha*(1/m)*sum2
    temp3=theta3-alpha*(1/m)*sum3
    temp4=theta4-alpha*(1/m)*sum4
    temp5=theta5-alpha*(1/m)*sum5
    judge = 0
    if theta0==temp0:judge+=1
    if theta1==temp1:judge+=1
    if theta2==temp2:judge+=1
    if theta3==temp3:judge+=1
    if theta4==temp4:judge+=1
    if theta5==temp5:judge+=1
    if judge==6:break
    theta0=temp0
    theta1=temp1
    theta2=temp2
    theta3=temp3
    theta4=temp4
    theta5=temp5
print(theta0 ,theta1 ,theta2, theta3, theta4, theta5 )
res=[]
totol=0
for k in range (300,501):
    predict= theta0+theta1*x[0][k]+theta2*x[1][k]+theta3*x[2][k]+theta4*x[3][k]+theta5*x[4][k]
    print("预测:{0:.3f}  实际： {1:.3f}".format(predict, x[5][k]))
    totol+=abs(predict-x[5][k])
    if abs(predict-x[5][k])<0.05:
        res.append(1)
    else:
        res.append(0)
print("误差小于5%的准确率为： {:.3f}".format(sum(res)/len(res)))
print(totol/201)