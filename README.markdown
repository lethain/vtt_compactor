Script for turning VTT transcripts, e.g. those created by Zoom when you
record a meeting, into a denser format with less redundant information.
Specifically created to simplify manual editing of interview transcripts for a
project that I've been working on.

Usage:

    python3 compact.y yourfile.rtt

There are no 3rd party package dependencies.

The input into script will look like this:

    24
    00:03:46.020 --> 00:03:53.970
    Will Larson: That's amazing. I have so many questions that are off script that I want to ask on but like, how do you measure that a lot of people feel about it like that. I want to ask, there's

    25
    00:03:54.420 --> 00:03:58.560
    Will Larson: I think the fact that somebody's going to be using program. And I've actually never heard anything quite like it before.

And the output will look like this:

    24. Will Larson. 00:03:46.020 -> 00:03:58.560

    That's amazing. I have so many questions that are off script that I want to ask on but like, how do you measure that a lot of people feel about it like that. I want to ask, there's
    I think the fact that somebody's going to be using program. And I've actually never heard anything quite like it before.

Which is to say, it takes all the messages by a single speaker and compacts them into a block with a single
set of metadata.