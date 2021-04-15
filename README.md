# This is a WIP.

# Fake www.alphaess.com Server
Personal project to run a fake www.alphaess.com server at home, so that my battery isn't talking in cleartext with a server across the Internet. Unencrypted battery control over the Internet seems like a recipe for disaster. Especially with authentication that appears to have been extremely naively designed.

See protocoldescription.md for my attempt at understanding the packet formats.

Fake battery and fake server setup - the fake server can listen to a real battery, but it won't do a whole lot with the data - just output it to the terminal, and respond to /everything/ with a 'Status: Success'.

## Testing with fake battery / server

Make sure that 'fakeserver.py' is listening on localhost '''host = '127.0.0.1''' and port 7778 in the code. Fake battery should be setup to connect to 127.0.0.1:7778 already.
Generate a few json files from the sample files. fake-battery.py is setup for a few files that are numbered N-N-N.direct.json. The 3 digit prefix on the filename is important, as they will be converted to binary integers that get sent out in the header before the actual json data. I don't have sample files for all the types of json, I just did a few for the things I wanted based on packet captures, and so I could make sure the checksums matched (they did). They have my serial number, hence why they're not checked in.

## Basic running with fake server

My setup at home is a pihole as DHCP server, so everything on the network gets the Pi as the DNS server. I have added an entry for www.alphaess.com to point to a local server (in my instance, that's 10.1.1.35).

Run fake-server.py, and then hopefully that's all you will need to start dumping data locally.

To be clear, this TOTALLY breaks the connection with the actual www.alphaess.com server. Considering how insecure that setup is, I'm taking this minimal approach for now as a win. Though I'd rather they work out some way of securing that system. 

## Other

I don't know all commands yet, so will need to make sure I dump any unknown traffic for later analysis. I think I will never know how to set the time on the battery now, unless someone shares some packet captures or information on what commands are used from www.alphaess.com to set time.
Check protocoldescription.md for my rough working out of what commands exist (check in raw mode, because I haven't fixed up the formatting yet)

Will not be uploading dumps (pcaps or hex dumps), as they include serial numbers and passwords, and PII. Will save sanitised json or csv data instead.

### Some Credits
https://jhalon.github.io/reverse-engineering-protocols/ - Helped me realise that there was a checksum (and I also used the code in there as a base for my own decoding).
https://www.scadacore.com/tools/programming-calculators/online-checksum-calculator/ - Helped me work out the checksum type for the data.