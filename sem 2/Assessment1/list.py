''' Write a function merge_and_sort(list1, list2) that merges two lists and returns the sorted list 
in ascending order.'''
def merge_and_sort(list1, list2):
    merged_list = list1 + list2
    merged_list.sort()
    print(merged_list)

list=["Luffy","Zoro","Brook"]
list1=["Nami","Robin","Chopper","Sanji","Jinbe"," God Ussop"]

merge_and_sort(list,list1)