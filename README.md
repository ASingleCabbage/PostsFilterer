# PostsFilterer

Filter posts with specified tags
Run program using python 3, from the command line.
Program takes in 2 arguments, the JSON posts file, and the file with the tags to filter out.
Outputs a json and csv file.

An example:
        python post_extract_tags.py resultSegment_2017_1543.json filter_tags

        resultSegment_2017_1543 is our JSON posts file (not included in repository)
        filter_tags is our tags file, which has a bunch of tag ids separated with whitespace

You can edit the output file prefix name in the python script, by changing the values at the very top.
