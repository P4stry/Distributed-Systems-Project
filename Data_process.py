def serialize(data):
    # Considering four main data structures: list, tuple, set, dictionary
    # input: data structure
    # return: string
    serialized_data = ""
    
    #Only consider legal data structure

    # Dictionary type
    # before: {key, value}
    # after: length:type{length:<type>key:length:<type>value}
    # input: dictionary
    # return :string
    if(type(data) == dict):
        for key, value in data.items():
            key_type = type(key)
            value_type = type(value)

            # Only data structure tuple can be the key of a dictionary
            # Process different key type
            if key_type == tuple:
                element_key = serialize(key)
            else:
                key = str(key)
                key_length = len(str(key_type) + key)
                element_key = str(key_length) + ':' + str(key_type) + key
            # Process different value type
            if value_type == dict:
                element_value = serialize(value)
            elif value_type == tuple:
                element_value = serialize(value)
            elif value_type == set:
                element_value = serialize(value)
            elif value_type == list:
                element_value = serialize(value)
            else:
                value = str(value)
                value_length = len(str(value_type) + value)
                element_value = str(value_length) + ':' + str(value_type) + value
            element = element_key + ':' + element_value
            serialized_data += element
        # Process whole dictionary structure
        serialized_data = str(dict) + '{' + serialized_data + '}'
        serialized_data = str(len(serialized_data)) + ':' + serialized_data
        return serialized_data

    # List type
    # before: [a,b,c]
    # after: length:type[length:<type>alength:<type>blength:<type>c]
    # input :list
    # output: string
    elif(type(data) == list):
        for element in data:
            element_type = type(element)
            # Process different element type
            if element_type == dict:
                element_value = serialize(element)
            elif element_type == tuple:
                element_value = serialize(element)
            elif element_type == set:
                element_value = serialize(element)
            elif element_type == list:
                element_value = serialize(element)
            else:
                element = str(element)
                element_length = len(str(element_type) + element)
                element_value = str(element_length) + ':' + str(element_type) + element
            serialized_data += element_value
        # Process whole tuple structure
        serialized_data = str(list) + '[' + serialized_data + ']'
        serialized_data = str(len(serialized_data)) + ':' + serialized_data
        return serialized_data

    # Tuple type (can have any data structure as its element)
    # before: (a,b,c)
    # after: length:type(length:<type>alength:<type>blength:<type>c)
    # input: tuple
    # return: string
    elif(type(data) == tuple):
        for element in data:
            element_type = type(element)
            # Process different element type
            if element_type == dict:
                element_value = serialize(element)
            elif element_type == tuple:
                element_value = serialize(element)
            elif element_type == set:
                element_value = serialize(element)
            elif element_type == list:
                element_value = serialize(element)
            else:
                element = str(element)
                element_length = len(str(element_type) + element)
                element_value = str(element_length) + ':' + str(element_type) + element
            serialized_data += element_value
        # Process whole tuple structure
        serialized_data = str(tuple) + '(' + serialized_data + ')'
        serialized_data = str(len(serialized_data)) + ':' + serialized_data
        return serialized_data

    # Set type
    # before: {a,b,c}
    # afer: length:type{length:<type>alength:<type>blength:<type>c}
    # input: set
    # output string
    elif(type(data) == set):
        for element in data:
            element_type = type(element)
            # Process different element type
            if element_type == dict:
                element_value = serialize(element)
            elif element_type == tuple:
                element_value = serialize(element)
            elif element_type == set:
                element_value = serialize(element)
            elif element_type == list:
                element_value = serialize(element)
            else:
                element = str(element)
                element_length = len(str(element_type) + element)
                element_value = str(element_length) + ':' + str(element_type) + element
            serialized_data += element_value
        # Process whole tuple structure
        serialized_data = str(set) + '{' + serialized_data + '}'
        serialized_data = str(len(serialized_data)) + ':' + serialized_data
        return serialized_data



def deserialize(data):
    # Only consider legal input
    # input: string
    # output: data structure

    data_type_start = data.find('<')
    data_type_end = data.find('>')
    
    # Deserialize dictionary data
    # before: length:type{length:<type>key:length:<type>value}
    # after: {key, value}
    # input string
    # return dictionary
    if 'dict' in data[data_type_start : data_type_end + 1]:
        # 14:<class 'int'>1:14:<class 'int'>214:<class 'int'>3:14:<class 'int'>4
        deserialized_data = dict()
        dict_elements = data[data_type_end + 2:-1]
        keys = []
        values = []
        flag = 0
        while flag != len(dict_elements):
            key_start = flag # start of key string
            key_length_flag = dict_elements[key_start:].find(':') # locate the offset(relative) of key length string
            key_length = int(dict_elements[key_start:key_start + key_length_flag]) # key length 
            key_end = key_start + key_length_flag + key_length # end of key string
            keys.append(dict_elements[key_start:key_end + 1]) # 
            flag = key_end # move flag
            
            value_start = key_end + 2 # start of value string
            value_length_flag = dict_elements[value_start:].find(':') # locate the offset(relative) of value length string
            value_length = int(dict_elements[value_start:value_start + value_length_flag]) # value length
            value_end = value_start + value_length_flag + value_length # end of value string
            values.append(dict_elements[value_start:value_end + 1])
            flag = value_end + 1 # move flag
        # deserialized key and value
        for i in range(len(keys)):
            element_key = deserialize(keys[i])
            element_value = deserialize(values[i])
            deserialized_data[element_key] = element_value #construct data structure
        return deserialized_data
    
    # Deserialize tuple data
    # before: length:type(length:<type>alength:<type>blength:<type>c)
    # after: (a,b,c)
    # input: string
    # return: tuple
    elif 'tuple' in data[data_type_start : data_type_end + 1]:
        deserialized_data = tuple()
        tuple_elements = data[data_type_end + 2: -1]
        elements = []
        flag = 0
        while flag != len(tuple_elements):
            element_start = flag # start of element string
            element_length_flag = tuple_elements[element_start:].find(':') # locate the offset(relative) of element length string
            element_length = int(tuple_elements[element_start:element_start + element_length_flag]) # element length
            element_end = element_start + element_length_flag + element_length # end of element string
            elements.append(tuple_elements[element_start:element_end + 1])
            flag = element_end + 1
        # deserialized each element
        for i in elements:
            element = deserialize(i)
            deserialized_data += (element,) # construct data struture
        return deserialized_data

    # Deserialize set data
    # before: length:type{length:<type>alength:<type>blength:<type>c}
    # afer: {a,b,c}
    # input: string
    # output set
    elif 'set' in data[data_type_start : data_type_end + 1]:
        deserialized_data = set()
        set_elements = data[data_type_end + 2: -1]
        elements = []
        flag = 0
        while flag != len(set_elements):
            element_start = flag # start of element string
            element_length_flag = set_elements[element_start:].find(':')
            element_length = int(set_elements[element_start:element_start + element_length_flag]) # locate the offset(relative) of element length string
            element_end = element_start + element_length_flag + element_length # element length
            elements.append(set_elements[element_start:element_end + 1]) # end of element string
            flag = element_end + 1
        # deserialized each element
        for i in elements:
            element = deserialize(i)
            deserialized_data.add(element) # construct data struture
        return deserialized_data
    
    # Deserialize list data
    # before: length:type[length:<type>alength:<type>blength:<type>c]
    # after: [a,b,c] 
    # input : string
    # output: list
    elif 'list' in data[data_type_start : data_type_end + 1]:
        deserialized_data = list()
        list_elements = data[data_type_end + 2: -1]
        elements = []
        flag = 0
        while flag != len(list_elements):
            element_start = flag # start of element string
            element_length_flag = list_elements[element_start:].find(':')
            element_length = int(list_elements[element_start:element_start + element_length_flag]) # locate the offset(relative) of element length string
            element_end = element_start + element_length_flag + element_length # element length
            elements.append(list_elements[element_start:element_end + 1]) # end of element string
            flag = element_end + 1
        for i in elements:
            element = deserialize(i)
            deserialized_data.append(element) # construct data struture
        return deserialized_data

    # Deserialize int and string data
    else:
        if 'int' in data[data_type_start : data_type_end + 1]:
            deserialized_data = int(data[data_type_end + 1:]) # deserialize int data
        elif 'str' in data[data_type_start : data_type_end + 1]:
            deserialized_data = data[data_type_end + 1:] # deserialize string data
        elif 'bool' in data[data_type_start : data_type_end + 1]:
            deserialized_data = bool(data[data_type_end + 1:])
        return deserialized_data

# test data
# test_tuple = ((1,2,({1:'K',9:(3,'7',{(1,2): 6})},(3,4,'H'),'1')), {1,10,11})
# # test_dict = {1:{2:(6,{'1':'2'}), (8,17):9, 10:11},'12':'13', 4:5, 7:{1,2,3}}
# test_dict = {"isSuccess":True, "content":"abcd"}
# test_set = {1,2,(1,2,'1'),'3'}
# test_list = [1,2,{1:2, 3:{4,5,(7,8,9)}}]
# test_data = [test_tuple, test_dict, test_set, test_list]

# # Serialize & Deserialize the data
# serialized_data = serialize(test_dict)
# print("Serialized Data:", serialized_data)
# print("Type of Serialized Data:", type(serialized_data))
# deserialized_data = deserialize(serialized_data)
# print("Deserialized Data:", deserialized_data)
# print("Type of Deserialized Data:", type(deserialized_data))
