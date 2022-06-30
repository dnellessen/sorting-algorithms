from copy import deepcopy
import random
import sys


_self = sys.modules[__name__]

__all__ = (
    'bubble_sort',
    'cocktail_sort',
    'insertion_sort',
    'selection_sort',
    'counting_sort',
    'heap_sort',
    'merge_sort',
    'quick_sort',
)



def init():
    ''' Initialize varibales. '''

    all_dicts = []
    for fname in __all__:
        func = getattr(_self, fname)
        all_dicts.append({
            'fname': fname,
            'func': func,
            'name': func.name,
            'timecomplexity': func.timecomplexity,
        })

    new = {
        'all_dicts': all_dicts,
        'fnames': [hmap['fname'] for hmap in all_dicts],
        'funcs': [hmap['func'] for hmap in all_dicts],
        'names': [hmap['name'] for hmap in all_dicts],
        'timecomplexitys': [hmap['timecomplexity'] for hmap in all_dicts],
    }
    globals().update(new)


def get(name):
    ''' Get dot-accessible dictionary of algorithm name. '''

    class ddict(dict):
        __getattr__ = dict.get

    index = globals()['names'].index(name)
    dictionary = globals()['all_dicts'][index]

    return ddict(dictionary)



def name(name):
	''' Sets 'name' property of function. '''

	def inner(function):
		function.name = name
		return function
	return inner


def timecomplexity(big_o):
	''' Sets 'timecomplexity' property of function.'''

	def inner(function):
		function.timecomplexity = big_o
		return function
	return inner



@name('Bubble Sort')
@timecomplexity('O(n²)')
def bubble_sort(arr, bars):
    ''' O(n²), where n is the input size '''

    high = len(arr) - 1

    swapped = True
    while swapped:
        swapped = False
        for i in range(high):
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                swapped = True
            bars.update(arr, selected=i+1)
        high -= 1

        if not swapped:
            break


@name('Cocktail Sort')
@timecomplexity('O(n²)')
def cocktail_sort(arr, bars):
    ''' O(n²), where n is the input size '''

    low = 0
    high = len(arr) - 1

    swapped = False
    while not swapped:
        for i in range(low, high):
            bars.update(arr, selected=i+1)
            if arr[i] > arr[i+1]:
                arr[i], arr[i+1] = arr[i+1], arr[i]
                swapped = True
        high -= 1

        if not swapped:
            break

        swapped = False

        for i in range(high, low, -1):
            bars.update(arr, selected=i+1)
            if arr[i] < arr[i-1]:
                arr[i], arr[i-1] = arr[i-1], arr[i]
                swapped = True
        low += 1

        swapped = False


@name('Insertion Sort')
@timecomplexity('O(n²)')
def insertion_sort(arr, bars):
    ''' O(n²), where n is the size of the input '''

    i = 0
    while i < len(arr)-1:
        while arr[i] > arr[i+1] and i >= 0:
            arr[i], arr[i+1] = arr[i+1], arr[i]
            bars.update(arr, selected=i)
            i -= 1
        i += 1


@name('Selection Sort')
@timecomplexity('O(n²)')
def selection_sort(arr, bars):
    ''' O(n²), where n is the input size '''

    n = len(arr)
    for i in range(n):
        min_i = i
        for x in range(i+1, n):
            bars.update(arr, selected=x)
            if arr[x] < arr[min_i]:
                min_i = x

        arr[min_i], arr[i] = arr[i], arr[min_i]
        bars.update(arr, selected=i)


@name('Counting Sort')
@timecomplexity('O(n + k)')
def counting_sort(arr, bars):
    ''' O(n + k), where n is the size of the input and k is the input range '''

    min_value = int(min(arr))
    max_value = int(max(arr))
    value_range = max_value - min_value

    count_arr = [0] * (value_range + 1)
    output_arr = [0] * len(arr)
    output_arr = deepcopy(arr)

    for i in range(len(arr)):
        count_arr[arr[i] - min_value] += 1
        bars.update(output_arr, selected=i)

    for i in range(1, len(count_arr)):
        count_arr[i] += count_arr[i-1]
        bars.update(output_arr, selected=i)

    for i in range(len(arr)):
        output_arr[count_arr[arr[i] - min_value] - 1] = arr[i]
        count_arr[arr[i] - min_value] -= 1

    for i in range(len(arr)):
        arr[i] = output_arr[i]
        bars.update(arr, selected=i)


@name('Heap Sort')
@timecomplexity('O(nlog(n))')
def heap_sort(arr, bars):
    ''' O(nlog(n)), where n is the input size '''

    def heapify(arr, i, max):
        parent = i
        l = 2 * i + 1
        r = 2 * i + 2

        if l < max and arr[l] > arr[parent]:
            parent = l

        if r < max and arr[r] > arr[parent]:
            parent = r

        if parent != i:
            arr[i], arr[parent] = arr[parent], arr[i]
            bars.update(arr, selected=i)
            heapify(arr, parent, max)

    max = len(arr)

    # build heap
    for i in range(max, -1, -1):
        heapify(arr, i, max)
 
    for i in range(max-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        bars.update(arr, selected=i)
        heapify(arr, 0, i)


@name('Merge Sort')
@timecomplexity('O(nlog(n))')
def merge_sort(arr, bars, l=0, r=None):
    ''' O(nlog(n)), where n is the size of the input '''

    def merge(arr, l, m, r, bars):
        len1 = m - l + 1
        len2 = r - m

        L = [0] * (len1)
        R = [0] * (len2)

        for il in range(len1):
            L[il] = arr[l + il]

        for ir in range(len2):
            R[ir] = arr[m + 1 + ir]

        il = ir = 0
        i = l

        while il < len1 and ir < len2:
            if L[il] <= R[ir]:
                arr[i] = L[il]
                il += 1
            else:
                arr[i] = R[ir]
                ir += 1
            bars.update(arr, selected=i)
            i += 1

        while il < len1:
            arr[i] = L[il]
            bars.update(arr, selected=i)
            il += 1
            i += 1

        while ir < len2:
            arr[i] = R[ir]
            bars.update(arr, selected=i)
            ir += 1
            i += 1

    r = len(arr)-1 if r is None else r

    if l < r:
        m = l + (r - l) // 2
        merge_sort(arr, bars, l, m)
        merge_sort(arr, bars, m+1, r)
        merge(arr, l, m, r, bars)


@name('Quick Sort')
@timecomplexity('O(nlog(n))')
def quick_sort(arr, bars, low=0, high=None):
    '''
    Average case time complexity: O(nlog(n)), where n is the size of the input.
    Worst case time complexity: O(n²), where n is the size of the input.
    By using a random pivot, the worst case can be avoided in most cases.
    '''

    def partition(arr, bars, low, high):
        pivot_idx = random.randint(low, high)
        pivot = arr[pivot_idx]

        arr[high], arr[pivot_idx] = arr[pivot_idx], arr[high]
        bars.update(arr, selected=high)
        pivot_idx = high

        bigger = low
        for smaller in range(low, high):
            if arr[smaller] <= pivot:
                arr[smaller], arr[bigger] = arr[bigger], arr[smaller]
                bars.update(arr, selected=smaller)
                bigger += 1

        arr[high], arr[bigger] = arr[bigger], arr[high]
        bars.update(arr, selected=high)
        pivot_idx = bigger

        return pivot_idx

    high = len(arr)-1 if high is None else high
    if low < high:
        pivot_loc = partition(arr, bars, low, high)
        quick_sort(arr, bars, low, pivot_loc-1)
        quick_sort(arr, bars, pivot_loc+1, high)

