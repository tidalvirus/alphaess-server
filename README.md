# This is a WIP.

# Fake www.alphaess.com Server
Personal project to run a fake www.alphaess.com server at home, so that my battery isn't talking in cleartext with a server across the Internet

See protocoldescription.md for my attempt at understanding the packet formats.

Fake battery and fake server setup - the fake server can listen to a real battery, but it won't do a whole lot with the data - just output it to the terminal, and respond to /everything/ with a 'Status: Success'.

## Testing with fake battery / server

Make sure that 'fakeserver.py' is listening on localhost '''host = '127.0.0.1''' and port 7778 in the code. Fake battery should be setup to connect to 127.0.0.1:7778 already.
Generate a few json files from the sample files. The battery is setup for a few files that are numbered N-N-N.direct.json. The 3 digit prefix on the filename is important, as they will be converted to binary integers that get sent out in the header before the actual json data. I don't have sample files for all the types of json, I just did a few for the things I wanted based on packet captures, and so I could make sure the checksums matched (they did). They have my serial number, hence why they're not checked in.

## Basic running with fake server

My setup at home is a pihole as DHCP server, so everything on the network gets the Pi as the DNS server. I have added an entry for www.alphaess.com to point to a local server (in my instance, that's 10.1.1.35).

I won't know all commands yet, so will need to make sure I dump any unknown traffic for later analysis.

Initially, will be logging everything, just because.

Will not be uploading dumps (pcaps or hex dumps), as they include serial numbers and passwords, and PII. Will save sanitised json or csv data instead.

Some Credits:
https://jhalon.github.io/reverse-engineering-protocols/ - Helped me realise that there was a checksum (and I also used the code in there as a base for my own decoding).
https://www.scadacore.com/tools/programming-calculators/online-checksum-calculator/ - Helped me work out the checksum type for the data.