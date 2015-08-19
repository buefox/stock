# coding=utf-8
import matplotlib.pyplot as plt
import datetime

def calMini(the_li):
    local_min = -1
    local_min_time = ""
    local_max = -1
    local_max_time = ""
    for li in the_li:
        li = li.split('\t')
        # print li[2]
        if local_min == -1:
            local_min = int(li[2])
            local_max = int(li[2])
        else:
            point = int(li[2])
            if local_min > point:
                local_min = point
                local_min_time = li[0] + li[1]
            elif local_max < point:
                local_max = point
                local_max_time = li[0] + li[1]

    # print "Local High:" + local_max_time + ", Point:" + str(local_max)
    # print "Local Min:" + local_min_time + ", Point:" + str(local_min)
    tmp_max.append(local_max_time + "=" + str(local_max))
    tmp_min.append(local_min_time + "=" + str(local_min))

with open("data") as f:
    data = f.read()

data_list = data.split('\n')
tmp_list = list()
# 2001/01/02	08:46:00	4702	4719	4700	4710	67
tmp_max = list()
tmp_min = list()
for row in data_list:
    if len(tmp_list) < 50:
        tmp_list.append(row)
    else:
        tmp_list.pop(0)
        tmp_list.append(row)
    calMini(tmp_list)

time = [datetime.datetime.strptime(row.split('\t')[0] + " " + row.split('\t')[1],  '%Y/%m/%d %H:%M:%S') for row in data_list]
p_open = [row.split('\t')[2] for row in data_list]
p_high = [row.split('\t')[3] for row in data_list]
p_low = [row.split('\t')[4] for row in data_list]
p_close = [row.split('\t')[5] for row in data_list]

fig = plt.figure()

ax1 = fig.add_subplot(111)

ax1.set_title("Plot title...")
ax1.set_xlabel('your x label..')
ax1.set_ylabel('your y label...')

ax1.plot(time,p_open)
leg = ax1.legend()


plt.show()