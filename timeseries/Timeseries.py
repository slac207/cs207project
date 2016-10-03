
class TimeSeries:
    
    def __init__(self,initial_data):
        """Create a TimeSeries instance.
        
        :param initial_data: Data used to populate time series instance.
        :type initial_data: Sequence object
        :rtype: None
        """
        self.data = [x for x in initial_data]
        
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, position):
        return self.data[position]
    
    def __setitem__(self, position, item):
        self.data[position] = item
        
    def __repr__(self):
        """For TimeSeries with greater than 10 elements, returns a string with name of the class, length of the data, and list containing the first two elements and the last two elements separated by an ellipsis. Otherwise, returns a string with the name of the class, length of the data, and the full list representation of the data.
                
        :rtype: String 
        """              
        class_name = type(self).__name__
        if len(self.data) > 10:
            abridged_data = "["+str(self.data[0])+","+str(self.data[1])+",...,"+str(self.data[-2])+","+ str(self.data[-1])+"]"
            return '{}(Length: {}, {})'.format(class_name, len(self.data), abridged_data) 
        else:
            return '{}(Length: {}, {})'.format(class_name, len(self.data), self.data)      
        
    def __str__(self):
        """For TimeSeries with greater than 10 elements, returns a string with a list containing the first two elements and the last two elements separated by an ellipsis. Otherwise, prints out string of list of all the data.
                
        :rtype: String 
        """        
        if len(self.data) > 10:
            abridged_data = "["+str(self.data[0])+","+str(self.data[1])+",...,"+str(self.data[-2])+","+ str(self.data[-1])+"]"
            return abridged_data 
        else:
            return self.data       
        
      
