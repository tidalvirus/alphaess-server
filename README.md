# This is a WIP.

# Fake www.alphaess.com Server
Personal project to run a fake www.alphaess.com server at home, so that my battery isn't talking in cleartext with a server across the Internet

See protocoldescription.md for my attempt at understanding the packet formats.

Working on faking battery, before I write a fake server, to test, before switching things on.

I won't know all commands yet, so will need to make sure I dump any unknown traffic for later analysis.

Initially, will be logging everything, just because.

Will not be uploading dumps (pcaps or hex dumps), as they include serial numbers and passwords, and PII. Will save sanitised json or csv data instead.

Some Credits:
https://jhalon.github.io/reverse-engineering-protocols/ - Helped me realise that there was a checksum (and I also used the code in there as a base for my own decoding).
https://www.scadacore.com/tools/programming-calculators/online-checksum-calculator/ - Helped me work out the checksum type for the data.