def binary_search(da_array, needle):
    """
    An algorithm that operates in O(lg(n)) to search for an element
    in an array sorted in ascending order.
    
    Parameters
    ----------
    da_array : list
        a list of "comparable" items sorted in non-descending order
    needle: an item to find in the array; it may or may not
        be in the array
        
    Returns
    -------
    index: int
        an integer representing the index of `needle` if found, and -1
        otherwise
        
    Notes
    -----
    PRE: `da_array` is a list that is sorted in non-decreasing order (thus items in
        `da_array` must be comparable: implement < and ==)
    POST: 
        - `da_array` is not changed by this function (immutable)
        - returns `index`=-1 if `needle` is not in `da_array`
        - returns an int `index ` in [0:len(da_array)] if
          `index` is in `da_array`
    INVARIANTS:
        - If `needle` in `da_array`, needle in `da_array[min_index:max_index]`
          is a loop invariant in the while loop below.
          
    Examples
    --------
    >>> binary_search([1,2,3,4,5], 2) #if needle in the array, return its index
    1
    >>> binary_search([1,2,3,4,5], 1.5) #if needle not in array, return surrounding indices
    (0, 1)

    """
    min_index = 0
    max_index=len(da_array) - 1

    while True:
        "needle in da_array => needle in da_array[min_index:max_index]"   
        if min_index > max_index: 
            return (max_index,min_index)
        
        midpoint = min_index + (max_index - min_index)//2
        if da_array[midpoint] > needle:#lower part
            max_index = midpoint - 1
        elif da_array[midpoint] < needle:
            min_index = midpoint + 1
        else:
            index = midpoint
            return index
        
        
