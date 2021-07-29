#! /usr/bin/env python2

import sys

PGM_NAME = "skywalker"
PGM_VERSION = "v0.0.2a"

PES_HEADER_PTS = ['\x00', '\x00', '\x01', '\xE0', '\x00', '\x00', '\x80', '\x80', '\x05', '\x21', '\x00', '\x01', '\x00', '\x01']
PES_HEADER = ['\x00', '\x00', '\x01', '\xE0', '\x00', '\x00', '\x80', '\x00', '\x00']
PACKET_SIZE = 65521 # 2^16 -1 - 14

def print_err(msg):
    print >> sys.stderr, 'Error: ' + msg

def usage():
    """
    Display the help message
    """
    print "Usage:"
    print "%s [ -h | -v ]" % PGM_NAME
    print "%s [ -r ] <input_file> <output_file>" % PGM_NAME
    print "Convert an ES into a PES"
    print
    print "<input_file>\tFile to convert"
    print "<output_file>\tFile output"
    print
    print "-h\t Print this help"
    print "-v\t Print the version"
    print "-r\t Reverse the conversion (PES to ES)"

def write_pes_packet(header, fin, fout):
    """
    Write a new PES packet from the stream fin to the stream fout
    """
    packet = fin.read(PACKET_SIZE)
    if not packet:
        # EOF
        return False
    pesSize = len(packet) + 3 + ord(header[8])
    header[4] = chr((pesSize >> 8) & 0xFF)
    header[5] = chr((pesSize) & 0xFF)
    fout.write(''.join(header) + packet)
    return True

def es_to_pes(inFilename, outFilename):
    """
    Convert an es file to a pes file
    """
    try:
        fin = open(inFilename, 'r')
    except:
        print_err('cannot open %s' % inFilename)
        return 2
    try:
        fout = open(outFilename, 'w')
    except:
        print_err('cannot open %s' % outFilename)
        return 3
    # Add first frame header with pts
    write_pes_packet(PES_HEADER_PTS, fin, fout)
    # Add next pes packet
    while write_pes_packet(PES_HEADER, fin, fout):
        pass
    # closes both fd
    fin.close()
    fout.close()
    return 0

def pes_to_es(inFilename, outFilename):
    """
    Convert an pes file to an es file
    """
    try:
        fin = open(inFilename, 'r')
    except:
        print_err('cannot open %s' % inFilename)
        return 2
    try:
        fout = open(outFilename, 'w')
    except:
        print_err('cannot open %s' % outFilename)
        return 3
    # Skip header
    fin.seek(len(PES_HEADER_PTS))
    while True:
        packet = fin.read(PACKET_SIZE)
        if not packet:
            break
        fout.write(packet)
        #fin.seek(len(PES_HEADER))

def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == '-h':
            usage()
            return 0
        elif sys.argv[1] == '-v':
            print PGM_VERSION
            return 0
    elif len(sys.argv) == 3:
        return es_to_pes(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 4 and sys.argv[1] == '-r':
        return pes_to_es(sys.argv[2], sys.argv[3])
    usage()
    return 1

if __name__ == '__main__':
    sys.exit(main())
