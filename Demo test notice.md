# Demo test notice

## Normal test

### Server setting:

Timeout: n

Message loss: n

### Client A setting:

Mode: none

Freshness interval: 20

### Client B setting:

Mode: none

Freshness interval: 5

### Test read:

read

test.txt

0

100

Test

### Test write insert:

write insert

test.txt

0

U

### Test write append: (non-idempotent)

write append

test.txt

U

### Test caching:

#### Test t_mclient on Client B:

Read on B

Wait 5 seconds

Read on B

It shows that still read from cache since t_mclient = t_mserver

#### Test expired cache:

Read on A

Write on B

Read on A

It shows that A still read from cache since T_c < freshness interval

### Test register monitor:

register monitor on A

test.txt

20

write append on B

It shows that A is informed of the update

### Test get file attribute:(idempotent)

get file attribute

test.txt



## Timeout test(At most once)

### Server setting:

Timeout: y

Sleep interval: 1

Message loss: n

### Client setting:

Mode: at-most-once

Timeout: 1

Freshness interval: 1

### Test idempotent operation:

read

test.txt

0

100

It shows that the same request is sent to the server repeatedly, but for the requests with same request id, the server will send the reply stored in history

### Test non-idempotent operation:

write append

test.txt

P

It shows that the same request is sent to the server repeatedly, but for the requests with same request id, the server will send the reply stored in history, and the operation is only executed once



## Timeout test(At least once)

### Server setting:

Timeout: y

Sleep interval: 1

Message loss: n

### Client setting:

Mode: at-least-once

Timeout: 1

Freshness interval: 1

### Test idempotent operation:

read

test.txt

0

100

It shows that the same request is sent to the server repeatedly, and the operation is executed repeatedly, but for idempotent operations, it makes no harm, the result is still correct

### Test non-idempotent operation:

write append

test.txt

K

It shows that the same request is sent to the server repeatedly, and the operation is executed repeatedly, for the non-idempotent operation, repeatedly executing leads to wrong result



## Message loss test (reply lost)

### In Normal mode:

There would be a deadlock, since no time out, client would wait the reply forever

### In timeout mode(take at-most-once as an example):

### Server setting:

Timeout: n

Message loss: y

Possibility of loss: 70

### Client setting:

Mode: at-most-once

Timeout: 1

Freshness interval: 1

### Test idempotent operation:

read

test.txt

0

100

It shows that the some replies will be lost during the communication, and the client would repeatedly send request to the server, but the operation would be only executed once.

### Test non-idempotent operation:

write append

test.txt

F

It shows that the some replies will be lost during the communication, and the client would repeatedly send request to the server, but the operation would be only executed once.



## Message loss test (request lost)

Similar to reply loss

### In Normal mode:

There would be a deadlock, since no time out, client would wait the reply forever

### In timeout mode(take at-most-once as an example):

### Server setting:

Timeout: n

Message loss: n

### Client setting:

Mode: at-most-once

Timeout: 1

Freshness interval: 1

Message loss: y

Possibility of loss: 90

### Test idempotent operation:

read

test.txt

0

100

It shows that the some replies will be lost during the communication, and the client would repeatedly send request to the server, but the operation would be only executed once since the server only receive one request.

### Test non-idempotent operation:

write append

test.txt

F

It shows that the some replies will be lost during the communication, and the client would repeatedly send request to the server, but the operation would be only executed once since the server only receive one request.