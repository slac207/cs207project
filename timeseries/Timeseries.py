class TimeSeries:
    
    def __init__(self, values, times=None):
        """
        Stores a single, ordered set of numerical data.
        
        Parameters
        ----------
        values : a sequence 
           data used to populate time series instance.
        times  : a sequence (optional)
           time associated with each observation in `values`.

        Returns
        -------
        Nothing (for now).
        
        Notes
        -----
        PRE: 
           - 
           -
        POST: 
           - 
           -
        INVARIANTS: 
           -
           -
        WARNINGS:
           -
           -
        """
        if times == None:
            self.__times = range(0,len(values))
        else:
            self.__times = [x for x in times]
            
        self.__values = [x for x in values]
        
        
    def __len__(self):
        """
        Reports the length of a TimeSeries instance.
        
        Parameters
        ----------
        self : a TimeSeries instance.

        Returns
        -------
        An integer representing the length of the instance.
        
        Notes
        -----
        PRE: 
           - 
           -
        POST: 
           - 
           -
        INVARIANTS: 
           -
           -
        WARNINGS:
           -
           -
        """        
        return len(self.__values)
    
    
    def __getitem__(self, time):
        """
        Reports the data value located at `self[time]`, where
           `self` is a TimeSeries instance.
        
        Parameters
        ----------
        self  : a TimeSeries instance.
        time  : time associated with the desired data value.

        Returns
        -------
        The data value associated with `self[time]`.
        
        Notes
        -----
        PRE: 
           - 
           -
        POST: 
           - 
           -
        INVARIANTS: 
           -
           -
        WARNINGS:
           - Assumes the user knows the appropriate type of `time`.
           -
        """        
        try:
            return self.__values[self.__times.index(time)]
        except IndexError:
            raise("Index out of bounds.")
        
    
    def __setitem__(self, time, value):
        """
        Assigns the data value `value` to `self[time]`, where
           `self` is a TimeSeries instance.
        
        Parameters
        ----------
        self  : a TimeSeries instance.
        time  : time associated with the desired data value.
        value : the data value being associated with `time`.

        Returns
        -------
        Nothing (for now).
        
        Notes
        -----
        PRE: 
           - 
           -
        POST: 
           - 
           -
        INVARIANTS: 
           -
           -
        WARNINGS:
           - Assumes the user knows the appropriate type of `time`
                and `value`.
           -
        """         
        try:
            self.__values[self.__times.index(time)] = value
        except IndexError:
            raise("Index out of bounds.")
        
    def __repr__(self):
        """
        Prints a string representation of a TimeSeries instance.
        - For a TimeSeries instance with > 10 elements:
             returns a string with name of the class, length of the instance, 
             and list containing the first element and the last element 
             separated by an ellipsis. 
        - For a TimeSeries instance with <= 10 elements: 
             returns a string with name of the class, length of the instance, 
             and the full list representation of the data.        
        
        Parameters
        ----------
        self  : a TimeSeries instance.
        time  : time associated with the desired data value.
        value : the data value being associated with `time`.

        Returns
        -------
        Nothing (for now).
        
        Notes
        -----
        PRE: 
           - 
           -
        POST: 
           - 
           -
        INVARIANTS: 
           -
           -
        WARNINGS:
           - 
           -
        """           
        class_name = type(self).__name__
        print(type(self))
        if len(self.__values) > 10:
            return '{}(Length: {}, Contents:[({},{}), ... ,({},{})])'.format(class_name, len(self.__values), self.__times[0], self.__values[0], self.__times[-1],self.__values[-1]) 
        else:
            return '{}(Length: {}, Contents:[{}])'.format(class_name, len(self.__values), ','.join([str(z) for z in zip(self.__times, self.__values)]))      
        
    def __str__(self):
        """
        Prints a string representation of a TimeSeries instance.
        - For a TimeSeries instance with > 10 elements:
             prints a string with a list containing the first element 
             and the last element separated by an ellipsis. 
        - For a TimeSeries instance with <= 10 elements: 
             prints the full list representation of the data.        
        
        Parameters
        ----------
        self  : a TimeSeries instance.
        time  : time associated with the desired data value.
        value : the data value being associated with `time`.

        Returns
        -------
        Nothing (for now).
        
        Notes
        -----
        PRE: 
           - 
           -
        POST: 
           - 
           -
        INVARIANTS: 
           -
           -
        WARNINGS:
           - 
           -
        """           
        class_name = type(self).__name__
        if len(self.__values) > 10:
            return 'Length: {} [({},{}), ... ,({},{})]'.format(len(self.__values), self.__times[0], self.__values[0], self.__times[-1],self.__values[-1]) 
        else:
            return 'Length: {} [{}]'.format(len(self.__values), ','.join([str(z) for z in zip(self.__times, self.__values)]))      
        
    def __iter__(self):
        """
        Called when an iterator is required for a container. 
        
        Parameters
        ----------
        self  : a TimeSeries instance.

        Returns
        -------
        A new iterator object that can iterate over all the objects in the
           container. For mappings, it should iterate over the keys of the 
           container.
        
        Notes
        -----
        PRE: 
           - 
           -
        POST: 
           - 
           -
        INVARIANTS: 
           -
           -
        WARNINGS:
           - 
           -
        """            
        for i in self.__values:
            yield i
            
    def __itertimes__(self):
        """
        Description.
        
        Parameters
        ----------
        self  : a TimeSeries instance.

        Returns
        -------
        Nothing (for now).
        
        Notes
        -----
        PRE: 
           - 
           -
        POST: 
           - 
           -
        INVARIANTS: 
           -
           -
        WARNINGS:
           - 
           -
        """           
        for i in self.__times:
            yield i    
            
    def __iteritems__(self):
        """
        Description.
        
        Parameters
        ----------
        self  : a TimeSeries instance.

        Returns
        -------
        Nothing (for now).
        
        Notes
        -----
        PRE: 
           - 
           -
        POST: 
           - 
           -
        INVARIANTS: 
           -
           -
        WARNINGS:
           - 
           -
        """           
        for i,j in zip(self.__times,self.__values):
            yield i,j