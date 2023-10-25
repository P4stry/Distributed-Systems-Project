# Manual of the System

## Introduction

In this project, I implement a system for remote file access based on client-server architecture. In the system, all shared files are stored on the local disk of the server. And the server side also implements a set of services for clients to remotely access the files, including read, write and get the attribute of file etc.. Meanwhile, the client side provides an interface for users to invoke these services. After receiving a request input from the user, the client would send the request to the server. The server would perform the requested service and returns the result to the client. The client then presents the result on the console to the user. All communication between the client and the server is through UDP. Besides, a client could also register a monitor to get the notification of file updates from the server. Moreover, I simulate the situation of message loss and transmission delay in the unstable UDP channel, and design some experiments to demonstrate the different effects of these failures or delays on idempotent operations and non-idempotent operations.

## Background

The server process and the client process use the system calls in UDP socket programming only. The server address and port number are known to the client. On the other hand, the server does not know the client address in advance. The client address is obtained by the server when it receives a request from a client.

**On the client**: It provides an interface that repeatedly asks the user to enter a request and sends the request to the server. Each reply or error message returned from the server would be printed on the screen, and the client also include an option for user to terminate the process

**On the server**: It repeatedly receives requests from the client, and performs the service and replies to the client who sends the corresponding request. All received request and the replies sent to the client would be printed on the screen

**On the communication channel**: Since the UDP channel is unstable, the message loss and transmission delays in the channel are also considered.

## The Structure of the Project

Following is the tree structure of the entire project

- ### Client

  - Global variable of client (Client_GLOBAL.py)
  - Interface of Client (Client.py)
  - Get shared file list (Client_Get_file_list.py)
  - Read file (Client_Read_file.py)
  - Write file (Client_Write_file.py)
    - Insert (function write_insert)
    - Append (function write_append)
  - Caching  (Client_Caching.py)
  - Get file attribute (Client_Get_file_attr.py)
  - Register monitor (Client_Register_Monitor.py)
  - Wait for notifications from the server (Client_Wait_notification.py)
  - Send request and receive response (Client_Send_and_Receive.py)

- ### Server

  - Global variable of client (Server_GLOBAL.py)
  - Interface of Server (Server.py)
  - Get shared file list (Server_Get_file_list.py)
  - Read file (Server_Read_file.py)
  - Write file (Server_Write_file.py)
    - Insert (function write_insert)
    - Append (function write_append)
  - Get file attribute (Server_Get_file_attr.py)
  - Register monitor and call back registered clients (Server_Monitor.py)

- ### Data processing (Data_process.py)

  - Marshaling (function serialize)
  - Unmarshaling (function deserialize)



## Message format, marshaling and unmarshaling

### Message format

In this project, all message would in the json format.

#### For the request message

The format is as following: 

{"operation": operation(String), "parameter_1": parameter_1(Any type), "parameter_2": parameter_2(Any type), ...}

The client would only accept any legal operation provided by it.

In the at-most-once mode, request id would be added into the request message before sending it out, and the format of request message is as following:

{"requestId":requestId(int), operation": operation(String), "parameter_1": parameter_1(Any type), "parameter_2": parameter_2(Any type), ...}

#### For the reply message

For the response to read or write operation, the format is as following:{"isSuccess":isSuccess(bool),"content":content(String)}

isSuccess denotes if the request is successfully performed by the server. If it is true, the content would be the data client needs to read or the file after updating. If it is false, the content would be the error message which would inform the client which type of error occurs on the server.

For the response to other operations, the format is different, I would take the response to the request "get file attribute" as an example:

{"T_mserver":t_mserver(int), "length":length(int)}

The variable t_mserver denotes the last modified time of a file on the server. It is a timestamp recorded in the server side. If its value is -1, this shows that the file exists and does not modified after the server is initialized. The variable length denotes the size of the specific files, which is calculated in bytes.

### Marshaling and Unmarshaling

The logic of marshaling and Unmarshaling is wrote in Data_process.py. The implementation of marshaling is function serialize and the implementation of unmarshaling is function deserialize. Since the project is wrote in Python, I mainly consider 4 types of data structure(set, dictionary, list and tuple) and 3 types of data(int, string and bool). And they also cover all data types and data structures I used in the project. Before marshaling, the data is in json format, and after marshaling, all data will be turned into string. After that, string would be turned into bytes so that it could be sent out. I design a protocol to marshal different data types data structures into different forms and unmarshal corresponding string back to different data types. The process would run recursively until all data types and data structures are handled.

#### Marshaling

##### For dictionary

Before marshaling, the format is as following, the data type is dictionary: {key, value}

After marshaling, the format is as following, the data type is string: "length:\<class 'dict'\>{length:\<data_type>key:length:\<data_type\>value}", and its

The value of length at the beginning denotes the length of string begins from ":" to the end which is "}" in dictionary. And \<class 'dict'\> denotes the origin type of data. The first "length" after "{" denotes the length of string begins form ":" to the end of the string of key, and the second "length after "{" denotes the length of string begins from ":" to the end of the string of value.

**Example**:

Before marshaling:

{"isSuccess":False, 1:2}

After marshaling:

"99:<class 'dict'>{22:<class 'str'>isSuccess:19:<class 'bool'>False14:<class 'int'>1:14:<class 'int'>2}"


##### For list

Before marshaling, the format is as following, the data type is list: [element_1,element_2]

After marshaling, the format is as following, the data type is string: "length:\<class 'list'\>[length:\<data_type\>element_1length:\<data_type\>element_2]"

The value of length at the beginning denotes the length of string begins from ":" to the end which is "]" in list. And \<class 'list'\> denotes the origin type of data. The first "length" after "[" denotes the length of string begins from ":" to the end of the string of element_1, and the second "length" after "[" denotes the length of string begins from ":" to the end of the string of element_2

**Example**:

Before marshaling:

[1,'2',False]

After marshaling:

"72:<class 'list'>[14:<class 'int'>114:<class 'str'>219:<class 'bool'>False]"


##### For set

Before marshaling, the format is as following, the data type is set: {element_1,element_2}

After marshaling, the format is as following, the data type is string: "length:<class 'set'>{length:\<data_type\>element_1length:\<data_type\>element_2}"

The basic marshaling logic is similar to the marshaling in list type

**Example**:

Before marshaling:

 {1,'A',False}

After marshaling(the order of elements is changed since the property of set):

"71:<class 'set'>{19:<class 'bool'>False14:<class 'int'>114:<class 'str'>A}"


##### For tuple

Before marshaling, the format is as following, the data type is tuple: (element_1, element_2)

After marshaling, the format is as following, the data type is string: "length:<class 'tuple'>(length:\<data_type>element_1length:\<data_type>element2)"

The basic marshaling logic is similar to the marshaling in list type

**Example**:

Before marshaling:

(1,'A',False)

After marshaling:

"73:<class 'tuple'>(14:<class 'int'>114:<class 'str'>A19:<class 'bool'>False)"


##### For basic date types(int, string, bool)

Before marshaling, the format is as following, the data type is int / string / bool

After marshaling, the format is as following, the data type is string: "length:\<class 'int'\>value" / "length:\<class 'str'\>value" "length:\<class 'bool'\>value" 

The value of length at the beginning denotes the length of string begins from ":" to the end of the string of value, the type behind "class" denotes the data type before marshaling

##### Nesting of different data structures

The input data structure would be marshaled recursively until all basic data types(int, string, bool) in it is marshaled. And the marshaling of different data structures would follow their corresponding rules as we mentioned above. The string which returns by the marshaling would place into the proper position of the whole string.

**Example**:

Before marshaling:

{"isSuccess":False, "test_data":[1,'A',(2,'B'),{3,'C'},{4:'D'}]}

After marshaling:

"304:<class 'dict'>{22:<class 'str'>isSuccess:19:<class 'bool'>False22:<class 'str'>test_data:210:<class 'list'>[14:<class 'int'>114:<class 'str'>A51:<class 'tuple'>(14:<class 'int'>214:<class 'str'>B)49:<class 'set'>{14:<class 'int'>314:<class 'str'>C}51:<class 'dict'>{14:<class 'int'>4:14:<class 'str'>D}]}"


#### Unmarshaling

For unmarshaling, function deserialize would process the string derived from function serialize recursively until it finds the basic data types(int, string, bool), and would unmarshal these basic data types first. After all basic data types in a data structure is processed, the function would unmarshal the entire data structure and place the element previously got into the proper position of the data structure.

**Example**:

Before unmarshaling:

"304:<class 'dict'>{22:<class 'str'>isSuccess:19:<class 'bool'>False22:<class 'str'>test_data:210:<class 'list'>[14:<class 'int'>114:<class 'str'>A51:<class 'tuple'>(14:<class 'int'>214:<class 'str'>B)49:<class 'set'>{14:<class 'int'>314:<class 'str'>C}51:<class 'dict'>{14:<class 'int'>4:14:<class 'str'>D}]}"

After unmarshaling:

{"isSuccess":False, "test_data":[1,'A',(2,'B'),{3,'C'},{4:'D'}]}


## Design and implementation of three scenarios

### On the client

#### At-least-once scenario

In the at-least-once scenario, a timeout needs to be set by the user, and request id will not be added to the request message. After sending requests to the server, the client would wait for the respond from the server, once no reply from the server within timeout, the client would resend the same request immediately, and wait for the reply until it get a reply from the server. 

The following is the code of implementation in client:

```python
# in Client_Send_and_Receive.py
if Client_GLOBAL.TIMEOUT > 0:
  # record receive reponse or not
      flag = False
      while not flag:
          # test message loss
          if Client_GLOBAL.TEST_LOSS:
              success = random.randint(1,100)
              if success > Client_GLOBAL.POSSIBILITY_OF_LOSS:
                 Client_GLOBAL.CLIENT_SOCKET.sendto(str.encode(request),Client_GLOBAL.SERVER_ADDRESS)
              else:
                  print("Message loss")
          # send request(str) to server
          else:
              Client_GLOBAL.CLIENT_SOCKET.sendto(str.encode(request),Client_GLOBAL.SERVER_ADDRESS)
          # receive response
          try:
              # receive response(str) from server
              response, _= Client_GLOBAL.CLIENT_SOCKET.recvfrom(10240)
              flag = True
          except timeout:
              print("Timeout, no response from server within %d seconds" % Client_GLOBAL.TIMEOUT)
              print("Resend request")
              print("\\"*50 + "Retrying" + "/"*50)
              continue
```

#### At-most-once scenario

In the at-most-once scenario, a timeout needs to be set by the user, and request id will be added to the request message. After sending requests to the server, the client would have a same logic as it in at-least-once mode. 

The following is the main different of implementation in at-least-once scenario and at-most-once scenario:

```python
# in Client_Send_and_Receive.py
# at-most-once
if Client_GLOBAL.REQUEST_ID != -1:
    request["requestId"] = Client_GLOBAL.REQUEST_ID
    Client_GLOBAL.REQUEST_ID += 1
```

#### None scenario

In the none scenario, timeout is not required, and request id will not be added to the request message. After sending requests to the server, the client would wait until it receives a reply from the server.

The following is the code of implementation in client:

```python
# in Client_Send_and_Receive.py
# No timeout senario
Client_GLOBAL.CLIENT_SOCKET.sendto(str.encode(request),Client_GLOBAL.SERVER_ADDRESS)
response, _= Client_GLOBAL.CLIENT_SOCKET.recvfrom(10240)
```

### On the server

After unmarshaling the request, it would firstly check if there is a key "requestId" in the request. If the "requestId" exists, it would check whether the client address and the request id have existed in the reply history or not (i.e.. check if it is a repeat request from the same client). If the record exists in the history, it would reply the reply recorded in the history directly. Otherwise would perform the operation in the request and record the client address, request id as well as the reply in the history. The implementation is in Server.py.

The history has following structure: {address(str):{requestId(int):reply(str)}}

The following is the code of implementation (take "list_files" operation as an example):

```python
# in Server.py
if operation == "list_files":
  flag = True
  if "requestId" in request:
      if address in Server_GLOBAL.HISTORY:
          if request["requestId"] in Server_GLOBAL.HISTORY[address]:
              # send the recoreded reply to client
              requestId = request["requestId"]
              flag = False
  if flag:
      return_value = Server_Get_file_list.get_file_list()
...
if operation == "list_files":
  if flag:
      response = {"file_list":return_value}
      # record the reply, if at-most-once
      if "requestId" in request:
          requestId = request["requestId"]
          Server_GLOBAL.HISTORY[address] = {requestId:response}
  else:
      print("Repeated request, send the recorded reply to client")
      response = Server_GLOBAL.HISTORY[address][requestId]
```

## Design and implementation of cache on the client

The file content read by the client is retained in a buffer of the client program. If the file content requested by the client is available in the cache, the client may read the cached content directly without contacting the server. On the other hand, the updates made by the client to file content are always sent to the server immediately. And the client would also update the information of the content in cache. The validation of content in the cache is checked by following rules:

$T_c$ : the time when the cache entry was last validated (is recorded in cache and would be updated by read and write operation)

$T_mclient$: the time when the cached file was last modified by the client (is recorded in cache and would be updated by write operation)

$T$: current time

$T_mserver$: the time when the cached file was last modified on the server (is recorded on the server and would be updated if any client updates the shared file)

$t$: freshness interval. User needs to set this value at the initialization of the client.

If $T - T_c < t$: no need to evaluate further, read data from cache

If $T - T_c ≥ t$, issue get file attribute request to server to obtain $T_mserver$

- $T_mclient = T_mserver$, the cache entry is valid (the data have not been modified by others at the server) and $T_c$ is updated to current time

- $T_mclient < T_mserver$, the cache entry is invalidated, and a new request is sent to server for updated data, $T_c$ is also updated

The cache on the client has following format: {pathname:{offset:int, end:int, T_c:int, T_mclient:int, content:string}}

Variable pathname is string type and denotes the name of cached file

Variable offset is int type and denotes the start offset of content cached as to the entire file on the server side. It would be updated by read operation, and write operation would set it to 0 since the response of write operation would contain the entire file

Variable end is int type and denotes the end offset of content cached as to the entire file on the server side. It would be updated by read operation since the read operation has parameter "length", and write operation would set it to -1, which denotes the entire file is cached

The main implementation is wrote in Client_Caching.py. 

The code of evaluating is as following:

```python
# in Client_Caching.py
def check_cache(pathname, offset, length):
    curr_dt = datetime.now()
    curr_t = int(round(curr_dt.timestamp()))
    if pathname in Client_GLOBAL.CACHE:
        # check if offset and length are valid
        # if end == -1, the whole file is cached (last cache is updated by write operation)
        if offset < Client_GLOBAL.CACHE[pathname]["offset"] or (offset + length - 1) > Client_GLOBAL.CACHE[pathname]["end"]:
            if Client_GLOBAL.CACHE[pathname]["end"] == -1:
                pass
            else:
                return False
        if curr_t - Client_GLOBAL.CACHE[pathname]["T_c"] < Client_GLOBAL.FRESHNESS_INTERVAL:
            return True
        else:
            # return format: (t_mserver(int), length(int)) (tuple)
            return_value = Client_Get_file_attr.get_file_attr(pathname)
            t_mserver = return_value[0]
            if Client_GLOBAL.CACHE[pathname]["T_mclient"] == t_mserver:
                Client_GLOBAL.CACHE[pathname]["T_c"] = curr_t
                return True
            else:
                return False
    else:
        return False
```

While updating the cache, the function uses whether `t_mclient` is equal to -1 or not to distinguish if the update is performed by write operation or read operation

The code of updating cache is as following:

```python
# in Client_Caching.py
def update_cache(pathname, data , t_c, t_mclient, offset, length):
    if pathname in Client_GLOBAL.CACHE:
        Client_GLOBAL.CACHE[pathname]["content"] = data
        Client_GLOBAL.CACHE[pathname]["T_c"] = t_c
        Client_GLOBAL.CACHE[pathname]["offset"] = offset
        if length == -1: # whole file is cached
            Client_GLOBAL.CACHE[pathname]["end"] = -1 # write operation updates
        else:
            Client_GLOBAL.CACHE[pathname]["end"] = offset + length - 1 # read operation updates
        if t_mclient != -1: # write operation updates
            Client_GLOBAL.CACHE[pathname]["T_mclient"] = t_mclient
    else:
        if length == -1: # write operation updates
            end = -1
        else:
            end = offset + length - 1 # read operation updates
        Client_GLOBAL.CACHE[pathname] = {"offset":offset, "end": end, "T_c":t_c, "T_mclient":t_mclient, "content":data}
        
# in Client_Read_file.py
...
curr_dt = datetime.now()
curr_t = int(round(curr_dt.timestamp()))
Client_Caching.update_cache(pathname, content, curr_t, -1, offset, length)
...
# in Client_Write_file.py
...
curr_dt = datetime.now()
curr_t = int(round(curr_dt.timestamp()))
Client_Caching.update_cache(pathname, content, curr_t, curr_t, 0, -1) # length == -1, entire file is cached
...
```

While reading content from cache, new offset would be calculated

The code of reading from cache is as following:

```python
# in Client_Read_file.py
...
isValid = Client_Caching.check_cache(pathname, offset, length)
if isValid:
    print("Read from cache")
    content = Client_Caching.read_from_cache(pathname,offset,length)
else:
...
# in Client_Caching.py
def read_from_cache(pathname,offset,length):
    # recaculate offset in cached content
    offset = offset - Client_GLOBAL.CACHE[pathname]["offset"]

    content = Client_GLOBAL.CACHE[pathname]["content"]
    return content[offset : offset + length]
```

## Initialized Setting

### On the client

#### Scenarios

Three different scenarios are given, and users could choose one of them

- At-least-once scenario: 

  In this scenario, a timeout needs to be set by the user, and request id will not be added to the request message. The design and implement of this scenario is elaborated above.

- At-most-once mode: 

  In this scenario, a timeout needs to be set by the user, and request id will be added to the request message. The design and implement of this scenario is elaborated above.

- None scenario: 

  In this scenario, timeout is not required, and request id will not be added to the request message. The design and implement of this scenario is elaborated above.

#### Freshness interval

Then user needs to input freshness interval to specify the validate time of data cached in the client. The usage of freshness interval is elaborated in the design and implement of caching

#### Message loss

At last, users need to choose whether there is a message loss in request sending or not. If users want to simulate message loss, they need to input an integer between 1 and 100 to set the possibility of message loss. The higher number users choose, the higher possibility of message loss in the channel. The implementation code is as following:

```python
# in Client_Send_and_Receive.py
if Client_GLOBAL.TEST_LOSS:
    success = random.randint(1,100)
    if success > Client_GLOBAL.POSSIBILITY_OF_LOSS:
        Client_GLOBAL.CLIENT_SOCKET.sendto(str.encode(request),Client_GLOBAL.SERVER_ADDRESS)
    else:
        print("Message loss")
```

### On the server

#### Sleep interval

Users need to choose whether to test timeout or not. If they need to test time out, they need to input a sleep interval which force the server to sleep for specific seconds before sending out the response  to simulate the transmission delays. The implementation code is as following:

```python
# in Server.py
if Server_GLOBAL.SLEEP_INTERVAL > 0:
    time.sleep(Server_GLOBAL.SLEEP_INTERVAL)
```

#### Message loss

Then, users need to choose whether to test message loss or not.  Users need to input an integer between 1 and 100 to set the possibility of reply message lost in the channel. The higher number users choose, the higher possibility of message loss in the channel. The implementation code is as following:

```python
# in Server.py
if Server_GLOBAL.TEST_LOSS:
    sucess = random.randint(1,100)
    if sucess > Server_GLOBAL.POSSIBILITY_OF_LOSS:
        Server_GLOBAL.SERVER_SOCKET.sendto(response,client_address)
    else:
        print("Message loss")
        continue
```

## Design and implementation of each service

### Send and receive messages

The project sends and receives messages by socket programming and using UDP. 

**For the client:**


**For the server:**


#### On the client

The main implementation code is in Client_Send_and_Receive.py. The implementation of timeout and resending is elaborated in the design and implementation of at-least-once and at-most-once scenarios. The implementation of message loss is elaborated in the initialized setting. The rest is implemented by following code:

```python
# in Client_Send_and_Receive.py
# marshalling
request = Data_process.serialize(request)
...
# convert string to bytes and send request
Client_GLOBAL.CLIENT_SOCKET.sendto(str.encode(request),Client_GLOBAL.SERVER_ADDRESS)
...
# receive response from the server
response, _= Client_GLOBAL.CLIENT_SOCKET.recvfrom(10240)
...
# convert bytes to string
response = bytes.decode(response)
# unmarshalling
response = Data_process.deserialize(response)
```

#### On the server

After server receive the request from the client, firstly it would check if there is key "requestId" in the request. If the key exists, it would check if it is a repeat request from the same client. If the request had been performed, the server would return the reply stored in the history. Otherwise, it would perform requested operation immediately and store the response in the history before sending out the response. If "requestId" does not exist in the request, it would directly extract parameters from the request and execute the operation. The implementation of this part is also elaborated in the design and implementation of at-least-once and at-most-once scenarios. The rest is implemented by following code:

```python
# in Server.py
# receive request from the client
request, client_address= Server_GLOBAL.SERVER_SOCKET.recvfrom(10240)
# convert (client_ip(str),client_port(int)) to the address(string), format: "ip:port"
address = client_address[0] + ":" + str(client_address[1])
# convert bytes to string
request = bytes.decode(request)
# unmashalling
request = Data_process.deserialize(request)
...
# marshaling
response = Data_process.serialize(response)
# convert string into bytes
response = str.encode(response)

# test timeout
if Server_GLOBAL.SLEEP_INTERVAL > 0:
    time.sleep(Server_GLOBAL.SLEEP_INTERVAL)

# test message loss
if Server_GLOBAL.TEST_LOSS:
    sucess = random.randint(1,100)
    if sucess > Server_GLOBAL.POSSIBILITY_OF_LOSS:
        Server_GLOBAL.SERVER_SOCKET.sendto(response,client_address)
    else:
        print("Message loss")
        continue

# send reponse to the client
Server_GLOBAL.SERVER_SOCKET.sendto(response,client_address)
```

### List files

This service allows users to get a list of shared files on the server. 

Users do not need to input any parameter on the client

The response of the server is consist of

- file_list: a list of shared files that client could access

The implementation of this service are in Client_Get_file_list.py and Server_Get_file_list.py

#### On the client

Client would construct request as following: 

- In at-most-once scenario: {"requestId":Id(int),"operation":"list_files"}
- In at-least-once and none scenario: {"operation":"list_files"}

After receiving the response from the server, it would extract information out from and print the result on the console. The implementation code is as following:

```python
# in Client_Get_file_list.py
response = Client_Send_and_Receive.send_and_receive(request)
file_list = response["file_list"]
if file_list:
    for file_name in file_list:
        print(file_name)
else:
    print("No file in the server")
```

#### On the server

Server would perform the operation and construct response as following:

```python
# in Server_Get_file_list.py
def get_file_list():
    file_list = os.listdir('Shared file')
    return file_list
# in Server.py
response = {"file_list":return_value}
```

#### The screenshot of execution

##### On the client


##### On the server


### Read

This service allows users to get the content of specific shared file. 

Users need to input 

- pathname: the name of shared file
- offset: the offset of the read start from
- length: the length of content they want to read on the client

on the client

Response of the server is consist of

- isSuccess: whether the operation executed correctly or not
- content: if the operation is performed successfully, the content is the specific part of the file. Otherwise, the content is the corresponding error message.

The implementation of this service are in Client_Read_file.py and Server_Read_file.py, and the read operation would also update the cache on the client.

#### On the client

Client would construct request as following: 

- In at-most-once scenario: {"requestId":Id(int), "operation":"read", "pathname":pathname, "offset":offset, "length":length}
- In at-least-once and none scenario: {"operation":"read", "pathname":pathname, "offset":offset, "length":length}

Main implementation is as following. and the cache updating is elaborated in the design and implementation of cache on the client.

```python
# in Client_Read_file.py
def read_file(pathname,offset,length):
    isValid = Client_Caching.check_cache(pathname, offset, length)
    if isValid:
        print("Read from cache")
        content = Client_Caching.read_from_cache(pathname,offset,length)
    else:
        # if isSuccess is false, content is error message
        # if isSuccess is true, content is file content
        # reponse format: {"isSuccess":isSuccess(bool), "content":content(str)}
        request = {"operation":"read", "pathname":pathname, "offset":offset, "length":length}
        response = Client_Send_and_Receive.send_and_receive(request)
        isSuccess = response["isSuccess"]
        content = response["content"]
        if isSuccess:
            curr_dt = datetime.now()
            curr_t = int(round(curr_dt.timestamp()))
            Client_Caching.update_cache(pathname, content, curr_t, -1, offset, length)
        else:
            print(content)
            return False
    print(content)
    return True
```

#### On the server

The server would return the requested content, and if any error including file does not exist, could not open the file and the offset is over range occurs, the server would return error message to the client.

Server would perform the operation and construct response as following:

```python
# in Server_Read_file.py
# return data or error message
def read_file(pathname,offset,length):
    check_exist = os.path.isfile(pathname)
    if not check_exist:
        return Server_GLOBAL.Error.FILE_NOT_EXIST
    try:
        f = open(pathname,'r')
    except OSError:
        return Server_GLOBAL.Error.FILE_OPEN_ERROR
    
    max_offset = os.path.getsize(pathname) - 1
    if offset > max_offset or offset < 0:
        return Server_GLOBAL.Error.FILE_SEEK_ERROR
    f.seek(offset)

    data = f.read(length)
    f.close()
    return data
# in Server.py
...
if return_value == Server_GLOBAL.Error.FILE_NOT_EXIST:
    isSuccess = False
    content = "File does not exist"
elif return_value == Server_GLOBAL.Error.FILE_OPEN_ERROR:
    isSuccess = False
    content = "Cannot open file, please check the pathname"
elif return_value == Server_GLOBAL.Error.FILE_SEEK_ERROR:
    isSuccess = False
    content = "Offset exceeds the file length"
else:
    isSuccess = True
    content = return_value
...
response = {"isSuccess":isSuccess, "content":content}
```

#### The screenshot of execution

##### On the client

- Read from server


- Read from cache


##### On the server

- Client read from server


- Client request for checking the validation of the cache

  The `T_mserver` is equal to  -1 which denotes that the file is never modified after the server is initialized


### Write (insert)

This service would allow users to insert new content into existed shared file. 

Users need to input

- pathname: the name of the shared file
- offset: the position they want to insert the content
- data: the content they want to insert

on the client

The response of the server is consist of

- isSuccess: whether the operation executed correctly or not
- content: if the operation is performed successfully, the content is the entire updated. Otherwise, the content is the corresponding error message.

The implementation of this service is in function write_insert in Client_Write_file.py and Server_Write_file.py, and the insert operation would also update the cache on the client.

#### On the client

Client would construct request as following: 

- In at-most-once scenario: {"requestId":Id(int),"operation":"write_insert", "pathname":pathname(str), "offset":offset(int), "data":data(str)}
- In at-least-once and none scenario: {"operation":"write_insert", "pathname":pathname(str), "offset":offset(int), "data":data(str)}

Main implementation is as following. And the cache updating is elaborated in the design and implementation of cache on the client.

```python
# in Client_Write_file.py
def write_insert(pathname,offset,data):
    # if isSuccess is false, content is error message
    # if isSuccess is true, content is new file content
    # reponse format: {"isSuccess":isSuccess(bool), "content":content(str)}
    request = {"operation":"write_insert", "pathname":pathname, "offset":offset, "data":data}
    response = Client_Send_and_Receive.send_and_receive(request)
    isSuccess = response["isSuccess"]
    content = response["content"]
    if isSuccess:
        curr_dt = datetime.now()
        curr_t = int(round(curr_dt.timestamp()))
        Client_Caching.update_cache(pathname, content, curr_t, curr_t, 0, -1) # length == -1, whole file is cached
        print(content)
        return True
    else:
        print(content) # Print error message
        return False
```

#### On the server

The server would return the entire updated file, and if any error including file does not exist, could not open the file and the offset is over range occurs, the server would return error message to the client.

Server would perform the operation and construct response as following. The operation update file attribute and call back registered clients would elaborate in following sections.

```python
# in Server_Write_file.py
# return an acknowledgement, clients to be notified, new content
def write_insert(pathname, offset, data):
    check_exist = os.path.isfile(pathname)
    if not check_exist:
        return Server_GLOBAL.Error.FILE_NOT_EXIST
    try:
        f = open(pathname, 'r')
    except OSError:
        return Server_GLOBAL.Error.FILE_OPEN_ERROR
    max_offset = os.path.getsize(pathname) - 1
    if offset > max_offset or offset < 0:
        return Server_GLOBAL.Error.FILE_SEEK_ERROR
    
    current_content = f.read()
    f.close()

    # write insert
    new_content = current_content[:offset] + data + current_content[offset:]
    f = open(pathname, 'w')
    f.write(new_content)
    f.close()

    # update file attribute
    curr_dt = datetime.now()
    timestamp = int(round(curr_dt.timestamp()))
    Server_Get_file_attr.update_file_attr(pathname, timestamp)

    # update clients to be notified
    clients = Server_Monitor.callback_clients(pathname)

    return True, clients, new_content
    # Server sends new content to the client requesting write operation anyway
# in Server.py
...
if return_value == Server_GLOBAL.Error.FILE_NOT_EXIST:
    isSuccess = False
    content = "File does not exist"
elif return_value == Server_GLOBAL.Error.FILE_OPEN_ERROR:
    isSuccess = False
    content = "Cannot open file, please check the pathname"
elif return_value == Server_GLOBAL.Error.FILE_SEEK_ERROR:
    isSuccess = False
    content = "Offset exceeds the file length"
else:
    isSuccess = True
    alive_clients = return_value[1]
    content = return_value[2]
...
response = {"isSuccess":isSuccess, "content":content}
```

#### The screenshot of execution

##### On the client


##### On the server


### Write (append) (Non-idempotent Operation)

This service allows users to write new content append to existed shared files.

Users need to input

- pathname: the name of the shared file
- data: new content that users want to write append to existed shared files

on the client

The response of the server is consist of

- isSuccess: whether the operation executed correctly or not
- content: if the operation is performed successfully, the content is entire updated file. Otherwise, the content is the corresponding error message.

The implementation of this service is in function write_append in Client_Write_file.py and Server_Write_file.py, and the append operation would also update the cache on the client.

#### On the client

Client would construct request as following: 

- In at-most-once scenario: {"requestId":Id(int),"operation":"write_append", "pathname":pathname(str), "data":data(str)}
- In at-least-once and none scenario: {"operation":"write_append", "pathname":pathname(str), "data":data(str)}

Main implementation is as following. And the cache updating is elaborated in the design and implementation of cache on the client.

```python
def write_append(pathname, data):
    # if isSuccess is false, content is error message
    # if isSuccess is true, content is new file content
    # reponse format: {"isSuccess":isSuccess(bool), "content":content(str)}
    request = {"operation":"write_append", "pathname":pathname, "data":data}
    response = Client_Send_and_Receive.send_and_receive(request)
    isSuccess = response["isSuccess"]
    content = response["content"]
    if isSuccess:
        curr_dt = datetime.now()
        curr_t = int(round(curr_dt.timestamp()))
        Client_Caching.update_cache(pathname, content, curr_t, curr_t, 0, -1) # length == -1, whole file is cached
        print(content)
        return True
    else:
        print(content) # Print error message
        return False
```

#### On the server

The server would return the entire updated file, and if any error including file does not exist, could not open the file and the offset is over range occurs, the server would return error message to the client.

Server would perform the operation and construct response as following. The operation update file attribute and call back registered clients would elaborate in following sections.

```python
def write_append(pathname, data):
    check_exist = os.path.isfile(pathname)
    if not check_exist:
        return Server_GLOBAL.Error.FILE_NOT_EXIST
    try:
        f = open(pathname, 'a')
    except OSError:
        return Server_GLOBAL.Error.FILE_OPEN_ERROR

    # write append
    f.write(data)
    f.close()

    # current content
    f = open(pathname, 'r')
    new_content = f.read()
    f.close()

    # update file attribute
    curr_dt = datetime.now()
    timestamp = int(round(curr_dt.timestamp()))
    Server_Get_file_attr.update_file_attr(pathname, timestamp)

    # update clients to be notified
    clients = Server_Monitor.callback_clients(pathname)

    return True, clients, new_content
```

#### The screenshot of execution

##### On the client


##### On the server


### Register monitor

This service allows clients to register a monitor on specific shared files. If any change is performed on the monitored file during the monitoring interval, all registered clients will be notified with the entire updated file. After the expiration of the monitor interval, the client record is removed from the server which will no longer deliver the file content to the client

Users need to input

- pathname: the name of the shared file
- interval: the monitoring interval

on the client

The response of the server is consist of

- isSuccess: the operation is executed successfully or not

The call back message of the server is consist of

- file name: name of the file which is updated
- file updated: the content is entire updated file

The implementation of this service is in Client_Register_Monitor.py, Client_Wait_notification.py, Server_Monitor.py and Server.py, and the call back would also updates the cache on the client

#### On the client

Client would construct request as following: 

- In at-most-once scenario: {"requestId":Id(int),"operation":"register_monitor", "pathname":pathname(str), "interval":t(int)}
- In at-least-once and none scenario: {"operation":"register_monitor", "pathname":pathname(str), "interval":t(int)}

Main implementation is as following. 

```python
# in Client_Register_Monitor.py
def register_monitor(pathname, t):
    # reponse format: {"isSuccess":isSuccess(bool)}
    request = {"operation":"register_monitor", "pathname":pathname, "interval":t}
    response = Client_Send_and_Receive.send_and_receive(request)
    isSuccess = response["isSuccess"]
    if isSuccess:
        print("Register monitor on "+ pathname + " successfully, expiration time is " + str(t) + " seconds")
        return True
    else:
        print("Register monitor fail")
        return False

# in Client_Wait_notification.py
def wait_for_notification(interval):
    curr_dt = datetime.now()
    curr_t = int(round(curr_dt.timestamp()))
    expiration = curr_t + interval
    Client_GLOBAL.CLIENT_SOCKET.settimeout(interval)
    while expiration > curr_t:
        # wait for update notification from the server
        print("#"*40 + "Waiting update notification from the Server" + "#"*40)
        try:
            notification, _= Client_GLOBAL.CLIENT_SOCKET.recvfrom(10240)
        except timeout:
            print("The monitoring interval expired, exit monitoring")
            break
        notification = bytes.decode(notification)
        notification = Data_process.deserialize(notification)
        file_name = notification["file name"]
        content = notification["file updated"]
        print("File %s has been updated" % file_name)
        print("New content is: %s" % content)
        
        #record the update
        curr_dt = datetime.now()
        curr_t = int(round(curr_dt.timestamp()))
        Client_Caching.update_cache(file_name, content, curr_t, -1, 0, -1) # cache the whole updated file, keep the t_mclient unchanged
        
        # update timeout
        Client_GLOBAL.CLIENT_SOCKET.settimeout(expiration - curr_t)
        
    if Client_GLOBAL.TIMEOUT > 0:
        Client_GLOBAL.CLIENT_SOCKET.settimeout(Client_GLOBAL.TIMEOUT)
    else:
        Client_GLOBAL.CLIENT_SOCKET.settimeout(None)
        
# in Client.py
isSuccess = Client_Register_Monitor.register_monitor(pathname,interval)
if isSuccess:
    # wait for update notification from the server
    Client_Wait_notification.wait_for_notification(interval)
```

In the function register_monitor, the client could register monitor on specific shared files. Then the client could repeatedly receive message from the server for a period of time which is specify as the monitoring interval. 

#### On the server

The server would firstly check if the file exists. If the file does not exist, the server would return error message to the client. Otherwise, the server would record the address and monitoring interval of the client into a list. Any operations that could change the file would invoke function callback_clients, which would return a list of clients whose monitoring interval is still valid and delete the expired record in the list at the same time. As long as the client's monitoring interval is valid, all updates on the monitored file would be sent to it in Server.py.

Main implementation is as following

```python
# in Server_Monitor.py
def register(pathname, address, t):
    if not os.path.isfile(pathname):
        return False
    curr_dt = datetime.now()
    timestamp = int(round(curr_dt.timestamp()))
    expiration = t + timestamp
    if pathname in Server_GLOBAL.MONITORING:
        Server_GLOBAL.MONITORING[pathname][address] = expiration
    else:
        Server_GLOBAL.MONITORING[pathname] = {address:expiration}
    return True

# return list of clients to be notified
def callback_clients(pathname):
    alive_clients = []
    expired_clients = []
    curr_dt = datetime.now()
    timestamp = int(round(curr_dt.timestamp()))
    if pathname in Server_GLOBAL.MONITORING:
        for address, expiration in Server_GLOBAL.MONITORING[pathname].items():
            if expiration < timestamp:
                expired_clients.append(address) # remove the expired record
            else:
                alive_clients.append(address) # record the client to be notified
    else:
        pass

    for address in expired_clients:
        del Server_GLOBAL.MONITORING[pathname][address]
    
    return alive_clients

# in Server.py
response = {"isSuccess":isSuccess}
...
# notify other clients
if alive_clients:
    notification = {"file name": request["pathname"], "file updated":content}
    # marshalling
    notification = Data_process.serialize(notification)
    notification = str.encode(notification)
    for alive_client in alive_clients:
        # do not notify the client who made the change
        if alive_client == address:
            continue
        # conver "ip:port" to (ip(str),port(int))(tuple)
        print("Send %s to %s" % (notification, alive_client))
        address_ip = alive_client.split(":")
        alive_client_address = (address_ip[0],int(address_ip[1]))
        # send notification to each client
        Server_GLOBAL.SERVER_SOCKET.sendto(notification,alive_client_address)
```

The notification of updates would not send to the client who requests the update. The client who requests the update would receive the response of that operation instead. And in at-most-once scenario, the update operation on file would only perform once, so the registered client would also receive the notification once.

#### The screenshot of execution

##### On the client

- Register monitor


- Receive updates


##### On the server

- Confirm of registry


- Send notification to all registered clients


### Get file attribute (Idempotent Operation)

This service allows users get attributes of specific files, including the size of the file and the last modified time of the file on the server.

Users need to input

- pathname: the name of the shared file

on the client

The response of the server is concise of

- T_mserver: the last modified time of the file on the server
- length: the size of the file

The implementation of this service is in Client_Get_file_attr.py and Server_Get_file_attr.py

#### On the client

Client would construct request as following: 

- In at-most-once scenario: {"requestId":Id(int),"operation":"get_file_attr", "pathname":pathname(str)}
- In at-least-once and none scenario: {"operation":"get_file_attr", "pathname":pathname(str)}

Main implementation is as following

```python
# in Client_Get_file_attr.py
def get_file_attr(pathname):
    # reponse format: {"T_mserver":t_mserver(int), "length":length(int)}
    # t_mserver: last modified time on the server
    # length: length of file
    request = {"operation":"get_file_attr", "pathname":pathname}
    response = Client_Send_and_Receive.send_and_receive(request)
    return response["T_mserver"], response["length"]
```

#### On the server

Server save attributes of files in a list "FILE_ATTR" as following format: {pathname(str):{"t_mserver":t(int), "length":length(int)}}

Server_Get_file_attr.py is consist of two function, one is update_file_attr and the other is get_file_attr.

Function update_file_attr is used to update FILE_ATTR while any updates are performed on the shared file

In function get_file_attr, the server would firstly check if the file exists or not. If the file does not exist, the server would return t_mserver = -1 and length = -1, which denotes the file is not found on the server. Otherwise, the server would check if the entry of the file exists in FILE_ATTR. If the entry does not exist, the server would create a new entry of this file and set its t_mserver as -1, since the server does not know its latest modified time.Otherwise, the server would return the record stored in FILE_ATTR.

Main implementation is as following

```python
# in Server_Get_file_attr.py
def update_file_attr(pathname,t):
    if pathname not in Server_GLOBAL.FILE_ATTR:
        Server_GLOBAL.FILE_ATTR[pathname] = {}
    Server_GLOBAL.FILE_ATTR[pathname]["t_mserver"] = t
    Server_GLOBAL.FILE_ATTR[pathname]["length"] = os.path.getsize(pathname)
def get_file_attr(pathname):
    check = os.path.isfile(pathname)
    # file not exist
    if not check:
        return -1, -1
    # file exist but not in FILE_ATTR
    if pathname not in Server_GLOBAL.FILE_ATTR:
        Server_GLOBAL.FILE_ATTR[pathname] = {}
        Server_GLOBAL.FILE_ATTR[pathname]["t_mserver"] = -1 # do not know the last modified time
        Server_GLOBAL.FILE_ATTR[pathname]["length"] = os.path.getsize(pathname)
    return Server_GLOBAL.FILE_ATTR[pathname]["t_mserver"], Server_GLOBAL.FILE_ATTR[pathname]["length"]
```

#### The screenshot of execution

##### On the client


##### On the server


