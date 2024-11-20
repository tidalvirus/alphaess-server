# archived, as apparently the firmware now has encrypyted connections, and I have allowed a third party to have control of the battery.

# This is a WIP.

# Fake www.alphaess.com Server
Personal project to run a fake www.alphaess.com server at home, so that my battery isn't talking in cleartext with a server across the Internet. Unencrypted battery control over the Internet seems like a recipe for disaster. Especially with authentication that appears to have been extremely naively designed.

See protocoldescription.md for my attempt at understanding the packet formats.

Fake battery and fake server setup - the fake server can listen to a real battery, but it won't do a whole lot with the data - just output it to the terminal, and respond to /everything/ with a 'Status: Success'.

## Alternatives ?
I'm aware since I started this that there are some other smarter people doing some awesome work, here's a few I have found - note, I have not tested any of them, but I will likely be looking at their code for ideas :)

* https://github.com/230delphi/alphaess-to-mqtt - for a similar thing written in Go! This one can either be considered a proxy (man in the middle type), or an interceptor - traffic still goes to the insecure Alpha ESS system, but you have way more control, and local access to boot. I was considering stopping development on my Python version and learning Go to modify this to be standalone, but I think I'll stick with my Python for now - it's a learning experience for me, writing my own TCP server. I do feel like this developer actually understands how this protocol works a lot better than I do. :)
* https://github.com/CharlesGillanders/alphaess - from the page: "This Python library logs in to cloud.alphaess.com and retrieves data on your Alpha ESS inverter, photovoltaic panels, and battery if you have one." - upside, easy-ish to use, great way to get access to the data of your own battery. Downside, it still needs the battery to talk to the Internet, and all your queries are reliant on Alpha ESS's servers being up.
* https://github.com/SorX14/alphaess_modbus - A way to access the data directly via Modbus! I've no idea how this really works, and I'm a bit scared that I'll break something, so I haven't seriously considered this.

If any of the others had existed when I got my battery, I would probably never have started what I did :)

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

### Calculating accurate time
On the first data packet with current time from the battery (1,1,16 packets), calculate the clock drift/skew with UTC time, and store it, so that for all future data packets, we can just read the time from the battery and calculate for all future data captures. This way if the battery dumps more than one reading at a time, it can just be converted, and we can still get the data with no missing bits.

### Some Credits
* https://jhalon.github.io/reverse-engineering-protocols/ - Helped me realise that there was a checksum (and I also used the code in there as a base for my own decoding).
* https://www.scadacore.com/tools/programming-calculators/online-checksum-calculator/ - Helped me work out the checksum type for the data.
