section_li = [{'Index': 1, 'WordCount': 10, 'Start': '0:00:02.26', 'End': '0:00:49.93', 'SectionLength': 47664.28333333333}, {'Index': 2, 'WordCount': 1, 'Start': '0:00:50.06', 'End': '0:00:50.08', 'SectionLength': 16.683333333334303}, {'Index': 3, 'WordCount': 1, 'Start': '0:00:50.16', 'End': '0:00:51.88', 'SectionLength': 1718.3833333333387}, {'Index': 4, 'WordCount': 10, 'Start': '0:00:52.05', 'End': '0:01:38.69', 'SectionLength': 46646.600000000006}, {'Index': 5, 'WordCount': 3, 'Start': '0:01:41.16', 'End': '0:01:52.21', 'SectionLength': 11044.366666666654}, {'Index': 6, 'WordCount': 1, 'Start': '0:01:52.24', 'End': '0:01:52.27', 'SectionLength': 33.36666666666861}, {'Index': 7, 'WordCount': 1, 'Start': '0:01:52.39', 'End': '0:01:52.41', 'SectionLength': 16.683333333334303}, {'Index': 8, 'WordCount': 2, 'Start': '0:01:52.42', 'End': '0:02:03.00', 'SectionLength': 10577.233333333337}, {'Index': 9, 'WordCount': 1, 'Start': '0:02:05.47', 'End': '0:02:16.11', 'SectionLength': 10643.966666666645}, {'Index': 10, 'WordCount': 0, 'Start': '0:02:24.24', 'End': '0:02:24.37', 'SectionLength': 133.46666666667443, 'Remove': True}, {'Index': 11, 'WordCount': 1, 'Start': '0:02:24.47', 'End': '0:02:24.49', 'SectionLength': 16.683333333348855}, {'Index': 12, 'WordCount': 1, 'Start': '0:02:24.56', 'End': '0:02:24.57', 'SectionLength': 16.68333333331975}, {'Index': 13, 'WordCount': 1, 'Start': '0:02:24.59', 'End': '0:02:26.24', 'SectionLength': 1651.6500000000233}, {'Index': 14, 'WordCount': 4, 'Start': '0:02:27.58', 'End': '0:02:46.58', 'SectionLength': 19002.31666666668}, {'Index': 15, 'WordCount': 1, 'Start': '0:02:47.56', 'End': '0:02:49.65', 'SectionLength': 2085.416666666657}, {'Index': 16, 'WordCount': 2, 'Start': '0:02:50.72', 'End': '0:03:01.96', 'SectionLength': 11244.56666666671}, {'Index': 17, 'WordCount': 1, 'Start': '0:03:04.51', 'End': '0:03:05.10', 'SectionLength': 583.916666666657}, {'Index': 18, 'WordCount': 2, 'Start': '0:03:05.23', 'End': '0:03:12.70', 'SectionLength': 7474.133333333331}, {'Index': 19, 'WordCount': 11, 'Start': '0:03:15.12', 'End': '0:03:53.76', 'SectionLength': 38638.600000000006}]

def jitter_clean(sections):
    jitter_li = []
    jitter_subli = []
    modify_li = []
    for i in range(len(sections)):
        sec = sections[i]
        if sec['SectionLength'] <= 1000.0:
            if sections[i-1]['SectionLength'] <= 1000.0:
                continue
            jitter_subli.append(sec)
            for j in range(1, 15):
                if i+j > len(sections):
                    break
                if sections[i+j]['SectionLength'] <= 1000.0:
                    jitter_subli.append(sections[i+j])
                else:
                    jitter_li.append(jitter_subli)
                    jitter_subli = []
                    break
        else:
            continue

    for sub in jitter_li:
        modify_li.append(sub[0])
        for s in sub:
            sections.remove(s)

    for m in modify_li:
        if 'Remove' in m:
            modify_li.remove(m)

    return sections, modify_li

section_li, modify = jitter_clean(section_li)
print('Sections')
for s in section_li:
    print(s)
print('Jitter Alert')
for m in modify:
    print(m)
