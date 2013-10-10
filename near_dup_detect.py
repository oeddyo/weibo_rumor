__author__ = 'eddiexie'


def ratio_similar(doc_A, doc_B):
    doc_A = set(doc_A)
    doc_B = set(doc_B)
    n_sim = 0.0
    for word in doc_A:
        if word in doc_B:
            n_sim += 1
    set_u = set.union(doc_A, doc_B)
    return n_sim * 1.0/(len(set_u))


def clean_dup(docs, ratio):
    cleaned_docs = []
    mark_dup = [0]*len(docs)
    #print len(docs)
    #docs = [set(doc) for doc in docs]
    cluster_number = 0
    for i in range(len(docs)):
        #if i % 100 == 0:
        #    print i
        if mark_dup[i] != 0:continue

        for j in range(i, len(docs)):
            if ratio_similar(docs[i]['seg_text'], docs[j]['seg_text']) >= ratio:
                mark_dup[j] = cluster_number
        cluster_number += 1


    for i in range(len(docs)):
        if mark_dup[i] == 0:
            cleaned_docs.append(docs[i])
    return mark_dup


def test_clean_dup():
    docs = [['a', 'b', 'c', 'd'], ['a', 'b', 'c'], ['a', 'b'], ['d']]
    print clean_dup(docs, 0.5)
    print clean_dup(docs, 0.8)



#test_clean_dup()
