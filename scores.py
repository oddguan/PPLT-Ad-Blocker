import pandas as pd

# modify the source files here
original = pd.read_csv("data/unblocked_news.csv")
test = pd.read_csv("data/blocked_news.csv")

base_time = original['avg_load_time'].values.tolist()
base_memo = original['avg_memory_used'].values.tolist()
test_time = test['avg_load_time'].values.tolist()
test_memo = test['avg_memory_used'].values.tolist()

adg_time = test_time[0:20]
adp_time = test_time[20:40]
gos_time = test_time[40:60]
pb_time = test_time[60:80]
ubo_time = test_time[80:100]
adu_time = test_time[100:120]
tb_time = test_time[120:140]
adl_time = test_time[140:160]
vb_time = test_time[160:180]
aka_time = test_time[180:200]

adg_memo = test_memo[0:20]
adp_memo = test_memo[20:40]
gos_memo = test_memo[40:60]
pb_memo = test_memo[60:80]
ubo_memo = test_memo[80:100]
adu_memo = test_memo[100:120]
tb_memo = test_memo[120:140]
adl_memo = test_memo[140:160]
vb_memo = test_memo[160:180]
aka_memo = test_memo[180:200]

blocked_trackers = test['avg_num_blocked'].values.tolist()
adg_blocked = blocked_trackers[0:20]
adp_blocked = blocked_trackers[20:40]
gos_blocked = blocked_trackers[40:60]
pb_blocked = blocked_trackers[60:80]
ubo_blocked = blocked_trackers[80:100]
adu_blocked = blocked_trackers[100:120]
tb_blocked = blocked_trackers[120:140]
adl_blocked = blocked_trackers[140:160]
vb_blocked = blocked_trackers[160:180]
aka_blocked = blocked_trackers[180:200]

def time_scores(base_time, real_time):
    res = 0
    for i in range(len(base_time)):
        proportion = (base_time[i] - real_time[i]) / base_time[i]
        if proportion >= 0.5:
            res += 5
        elif 0.25 <= proportion < 0.5:
            res += 4
        elif 0 <= proportion < 0.25:
            res += 3
        elif -0.25 <= proportion < 0:
            res += 2
        elif proportion < -0.25:
            res += 1
    return res / 20

# modify the target blockers here
print(time_scores(base_time, adg_time))

def memo_scores(base_memo, real_memo):
    res = 0
    for i in range(len(base_memo)):
        proportion = (base_memo[i] - real_memo[i]) / base_memo[i]
        if proportion >= 0.2:
            res += 5
        elif 0.1 <= proportion < 0.2:
            res += 4
        elif -0.1 < proportion < 0.1:
            res += 3
        elif -0.2 < proportion <= -0.1:
            res += 2
        elif proportion <= -0.2:
            res += 1
    return res / 20

# modify the target blockers here
print(memo_scores(base_memo, adg_memo))

def get_max(a, b, c, d, e, f, g, h, i, j):
    list = []
    list.append(a)
    list.append(b)
    list.append(c)
    list.append(d)
    list.append(e)
    list.append(f)
    list.append(g)
    list.append(h)
    list.append(i)
    list.append(j)
    res = max(list)
    return res


def block_num_scores(l1, l2, l3, l4, l5, l6, l7, l8, l9, la):
    res = [0 for _ in range(10)]
    for i in range(len(l1)):
        base_scores = get_max(l1[i], l2[i], l3[i], l4[i], l5[i], l6[i], l7[i], l8[i], l9[i], la[i])
        if base_scores == 0:
            res[0] += 5
            res[1] += 5
            res[2] += 5
            res[3] += 5
            res[4] += 5
            res[5] += 5
            res[6] += 5
            res[7] += 5
            res[8] += 5
            res[9] += 5
        else:
            res[0] += (l1[i] / base_scores) * 5
            res[1] += (l2[i] / base_scores) * 5
            res[2] += (l3[i] / base_scores) * 5
            res[3] += (l4[i] / base_scores) * 5
            res[4] += (l5[i] / base_scores) * 5
            res[5] += (l6[i] / base_scores) * 5
            res[6] += (l7[i] / base_scores) * 5
            res[7] += (l8[i] / base_scores) * 5
            res[8] += (l9[i] / base_scores) * 5
            res[9] += (la[i] / base_scores) * 5
    for i in range(10):
        res[i] = round(res[i]/20, 2)
    return res

print(block_num_scores(adg_blocked, adp_blocked, gos_blocked, pb_blocked, ubo_blocked,
                       adu_blocked, tb_blocked, adl_blocked, vb_blocked, aka_blocked))
