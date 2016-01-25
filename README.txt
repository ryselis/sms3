SMS
===

The sms package provides sms capabilities for enfora gsm modems, and
probably others.

The sms package provides Modem and Message classes for sending and
receiving sms message.

The sms.server module provides two servers that allow you to dispatch
incoming sms messages. The sms.echo module is an example that works
with the sms.server.subprocess_server.

Usage
-----

Create a modem object passing it the serial device ID. On windows this
would be something like 'COM1'. The example below is for mac and
linux:

    >>> import sms
    >>> m = sms.Modem('/dev/ttyS0')

You can have use several modem objects concurrently if you have more
than one modem attached to different serial ports.

For the purposes of this test we're going to replace the real serial
connection on the modem with a dummy one so that the test doesn't
actually send sms messages.

    >>> m.conn = DummyConnection()

The dummy connection will simply keep a list of AT commands sent
rather than actually sending them to a modem.

To send a sms message call the send method, passing a phone number
string and a message string.

    >>> m.send('14161234567', 'This is a message')

Let's see what AT commands were sent.

    >>> m.conn.sent()
    'AT+CMGS="14161234567"\r\nThis is a message\x1a'

The AT+CMGS command was send, followed by the sms message terminated
with ctrl-z.

Let's simulate an error in sending, by hardcoding the connection to
return an error string.

    >>> m.conn.response = ['ERROR']

Now let's try to send a message.

    >>> m.send('14161234567', 'This is a message')
    Traceback (most recent call last):
    ...
    ModemError: ['ERROR']

A ModemError is raised with the error message.

Let's restore the normal connection response.

    >>> m.conn.response = []

You can receive sms messages with the messages() method. It retuns a
list of all messages that have been received.

    >>> m.messages()
    []

So far no messages have been received. Let's see how the modem asks
for messages.

    >>> m.conn.reset()
    >>> m.messages()
    []
    >>> m.conn.sent()
    'AT+CMGL="ALL"\r\n'

The AT+CMGL message tells the modem to list stored messages. Let's
simulate a typical response to this command.

    >>> m.conn.response = ['\r\n', '+CMGL: 1,"REC UNREAD","+16476186676",,"08/07/11,11:02:11+00"\r\n', 'Activation code 63966 Go 2 www.ipipi.com and signin with  your username and pwd, enter 63966 to activate your mobile/account\r\n', '\r\n', '\r\n', 'Welcome 2 ipipi.com\r\n', 'OK\r\n']

Now we let's try again.

    >>> msgs = m.messages()
    >>> msgs
    [<sms.Message object at 0x...>]

Message objects have a couple attributes: number, date, and text.

    >>> msgs[0].number
    '+16476186676'

    >>> msgs[0].date
    datetime.datetime(2008, 7, 11, 11, 2, 11)

    >>> msgs[0].text
    'Activation code 63966 Go 2 www.ipipi.com and signin with  your username and pwd, enter 63966 to activate your mobile/account\n\nWelcome 2 ipipi.com'

Let's do a more complex example to make sure that we can deal with
different types of messages.

    >>> m.conn.response = ['\r\n', '+CMGL: 1,"REC READ","+16476186676",,"08/07/11,11:02:11+00"\r\n', 'Activation code 63966 Go 2 www.ipipi.com and signin with  your username and pwd, enter 63966 to activate your mobile/account\r\n', '\r\n', '\r\n', 'Welcome 2 ipipi.com\r\n', '+CMGL: 2,"STO UNSENT","14166243508",,\r\n', 'Out over the fields,\r\n', '\n', 'attached to nothing,\r\n', '\n', 'a skylark sings\r\n', '\r\n', '+CMGL: 3,"REC READ","+14161234567","Example Name","08/07/11,13:02:11+00"\r\n', 'Test message\r\n','OK\r\n']

    >>> msgs = m.messages()
    >>> len(msgs)
    3
    >>> msgs[0].number
    '+16476186676'
    >>> msgs[0].date
    datetime.datetime(2008, 7, 11, 11, 2, 11)
    >>> msgs[0].text
    'Activation code 63966 Go 2 www.ipipi.com and signin with  your username and pwd, enter 63966 to activate your mobile/account\n\nWelcome 2 ipipi.com'
    >>> msgs[2].number
    '+14161234567'
    >>> msgs[2].date
    datetime.datetime(2008, 7, 11, 13, 2, 11)
    >>> msgs[2].text
    'Test message'

After you receive messages you'll want to delete them from the SIM
card. This is done by calling the delete method on the messages.

    >>> msgs[0].delete()

Let's test this by taking a look at the AT commands sent to the modem
when a message is deleted.

    >>> m.conn.reset()
    >>> msgs[0].delete()
    >>> m.conn.sent()
    'AT+CMGD=1\r\n'

    >>> m.conn.reset()
    >>> msgs[1].delete()
    >>> m.conn.sent()
    'AT+CMGD=2\r\n'

Rather than polling the modem to find messages you can call the wait()
method, which blocks until a message is received. The wait method
takes an optional timeout argument.

For the purposes of this test rather than actually blocking, the
connection will print how many seconds it would block for.

    >>> m.wait(1)
    reading with 1 timeout

    >>> m.wait()
    reading with no timeout

The wait message doesn't return anything. You should call the
messages() method after it returns to receive the messages. Note that
it's possible that there may in fact be no messages available after
the wait method returns.


Message Decoding
----------------

Most of the time you can treat SMS messages as ASCII strings. However
they are supposedly in GMS 03.38 7bit encoding. I have never seen this
in practice.

I have seen unicode messages. They are encoded as a series of hex
numbers like so:

    >>> text = "004500200074006500730074002000E800E9002000C800C90020006100200074006500730074002000C000C1002000E000E1"

There is a function to decode these messages.

    >>> import sms.encoding
    >>> sms.encoding.decode_unicode(text)
    u'E test \xe8\xe9 \xc8\xc9 a test \xc0\xc1 \xe0\xe1'

It will fail if you try to feed it text that doesn't appear to be a unicode message.

    >>> sms.encoding.decode_unicode('not a unicode message')
    Traceback (most recent call last):
    ...
    ValueError: Message is not unicode

I have also observered accented characters mixed in with ascii
characters. The accented characters are values above 127. I don't know
what encoding they are in, but I've reverse engineered it and it works
for me.

Here's an example:

    >>> text = "Montr\x82al"

The decode_accents function will decode these messages into unicode as
best it can.

    >>> sms.encoding.decode_accents(text)
    u'Montr\xe9al'

The decode_accents function won't fail with unknown characters. It
will simply replace them with the unicode replacement character.

    >>> sms.encoding.decode_accents('what is this \xff')
    u'what is this \ufffd'

There's also a convenience to_ascii function to turn unicode into
ascii. It uses Fredrick Lundh's unaccent script.

    >>> sms.encoding.to_ascii(u'Montr\xe9al')
    'Montreal'

Characters that can't be easily turned into ascii are changed to ?.

    >>> sms.encoding.to_ascii(u'\ufffd')
    '?'
