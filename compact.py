"""
Script for turning VTT transcripts, e.g. those created by Zoom when you
record a meeting, into a denser format with less redundant information.
Specifically created to simplify manual editing of interview transcripts for a
project that I've been working on.

Usage:

    python3 compact.y yourfile.rtt

There are no 3rd party package dependencies.
"""
import argparse


class Segment:
    def __init__(self):
        self.num = 0
        self.speaker = None
        self.start = ""
        self.end = ""
        self.text = ""
        

    def time(self, txt):
        self.start, self.end = txt.split(' --> ')
        
    def is_complete(self):
        return self.num and self.speaker and  self.text

    def __repr__(self):
        return "Segment(%s, %s, %s, text: %s)" % (self.num, self.speaker, self.start, len(self.text))


def segments(fd):
    segments = []
    seg = Segment()
    for line in fd:
        try:
            if seg.is_complete():
                segments.append(seg)
                seg = Segment()
            line = line.strip()
            if line and line != "WEBVTT":
                if not seg.num:
                    seg.num = int(line)
                elif not seg.start:
                    seg.time(line)
                elif seg.speaker is None:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        seg.speaker, seg.text =  parts
                    elif len(parts) == 1:
                        # this happens sometimes for unclear reasons
                        seg.speaker = "OMITTED"
                        seg.text = parts[0]
                    seg.text = seg.text.strip()
        except Exception as e:
            print("couldn't parse: %s" % (line,))
            raise(e)
    return segments


def compact(segs):
    chunks = []
    if len(segs) == 0:
        return chunks

    chunk = segs[0]
    for seg in segs[1:]:
        if seg.speaker == chunk.speaker:
            chunk.text += "\n" + seg.text
            chunk.end = seg.end
        else:
            chunks.append(chunk)
            chunk = seg
    chunks.append(chunk)
    return chunks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath")
    args = parser.parse_args()

    with open(args.filepath, 'r') as fin:
        segs = segments(fin)
        chunks = compact(segs)
        for chunk in chunks:
            print("%s. %s. %s -> %s\n\n%s\n" % (chunk.num, chunk.speaker, chunk.start, chunk.end, chunk.text))


if __name__ == "__main__":
    main()
