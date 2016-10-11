
class TimeSeries:
    
    def __init__(self,values,times=None):
        """Create a TimeSeries instance.
        
        :param values: Mandatory data used to populate time series instance.
        :type values: Sequence object
        :param times: Optional time data.
        :type times: Sequence object
        :rtype: None
        """
        if times == None:
            self.__times = range(0,len(values))
        else:
            self.__times = [x for x in times]
            
        self.__values = [x for x in values]
        
        
    def __len__(self):
        return len(self.__values)
    
    
    def __getitem__(self, time):
        try:
            return self.__values[self.__times.index(time)]
        except IndexError:
            raise("Index out of bounds")
        
    
    def __setitem__(self, time, value):
        try:
            self.__values[self.__times.index(time)] = value
        except IndexError:
            raise("Index out of bounds")
        
    def __repr__(self):
        """For TimeSeries with greater than 10 elements, returns a string with name of the class, length of the data, and list containing the first element and the last element separated by an ellipsis. Otherwise, returns a string with the name of the class, length of the data, and the full list representation of the data.
                
        :rtype: String 
        """              
        class_name = type(self).__name__
        print(type(self))
        if len(self.__values) > 10:
            return '{}(Length: {}, Contents:[({},{}), ... ,({},{})])'.format(class_name, len(self.__values), self.__times[0], self.__values[0], self.__times[-1],self.__values[-1]) 
        else:
            
            return '{}(Length: {}, Contents:[{}])'.format(class_name, len(self.__values), ','.join([str(z) for z in zip(self.__times, self.__values)]))      
        
    def __str__(self):
        """For TimeSeries with greater than 10 elements, returns a string with a list containing the first element and the last element separated by an ellipsis. Otherwise, prints out string of list of all the data.
                
        :rtype: String 
        """        
        class_name = type(self).__name__
        if len(self.__values) > 10:
            return 'Length: {} [({},{}), ... ,({},{})]'.format(len(self.__values), self.__times[0], self.__values[0], self.__times[-1],self.__values[-1]) 
        else:
            
            return 'Length: {} [{}]'.format(len(self.__values), ','.join([str(z) for z in zip(self.__times, self.__values)]))      
        
    def __iter__(self):
        for i in self.__values:
            yield i
            
    def __itertimes__(self):
        for i in self.__times:
            yield i    
            
    def __iteritems__(self):
        for i,j in zip(self.__times,self.__values):
            yield i,j  
            
      