
import json, sys, os, csv, datetime, argparse
#from print_progress import print_progress
#print('Opening file ' + sys.argv[1])

def setupArgparse():
    parser = argparse.ArgumentParser(description = 'python script to filter out posts with specified tags')
    parser.add_argument('posts_file', help = 'file containing analyzed posts in JSON format')
    parser.add_argument('tags_filter_file', help = 'file containing tags to filter out, seperated by whitespace')
    return parser.parse_args()

def getCurrTime():
    return datetime.datetime.now().strftime('%y%m%d_%H%M%S')

def dumpJsonAry(jsons, filename):
    with open(filename, "w", encoding='utf-8') as file:
         json.dump(jsons, file, indent=4, sort_keys=True, ensure_ascii=False)
    print("jsons dumped to {}".format(filename))

args = setupArgparse()
with open(args.posts_file, 'r', encoding='utf-8') as f:
    posts = json.load(f)
    print('Reading from file {}'.format(args.posts_file))
    assert (len(posts) != 0), 'posts cannot be empty'
    if('metadata' in posts[0]):
        print("Post contains metadata tag. First element in list removed. Not a problem")
        posts.pop(0)

with open(args.tags_filter_file, 'r', encoding='utf-8') as f:
    tags = f.read().split()
    print('filtering tags: {}'.format(tags))

exit()


data = []
for x in posts:
    isMatch = False
    if(x["analysis"]["sentiment_score"] == "Error"):
        continue

    tags_set = set(x["tags"])

    # I've created new keys for entries
    x["filtering"] = {}
    x["filtering"]["matched_tags"] = []
    x["filtering"]["matched_entities"] = [];

    if(tags_set & target_tags):
        x["filtering"]["matched_tags"] += list(tags_set.intersection(target_tags));
        isMatch = True

    # for filtering entities I have to use a set first since there may be duplicate
    # entities in each post (one with caps and the other without)
    entities_set = set()
    for entity in x["analysis"]["entitiy_sentiments"]:
        if(entity["name"].lower() in target_strings):
            entities_set.add(entity["name"].lower())
            isMatch = True
    x['filtering']['matched_entities'] = list(entities_set)

    if(isMatch == True):
        data.append(x)

# dumpJsonAry(data, "dataRequest_Thesis_AsAmer{}.json".format(len(data)))
dumpJsonAry(data, os.path.expanduser( "~/Desktop/enigmadailydata/requestResultsThesis/json/dataRequest_Thesis_AsAmer{}.json".format(len(data))))

# with open('ThesisAsAmer{}.csv'.format(len(data)), 'w', encoding='utf-8', newline='') as csvfile:
with open(os.path.expanduser('~/Desktop/enigmadailydata/requestResultsThesis/csv/ThesisAsAmer{}.csv'.format(len(data))), 'w', encoding='utf-8', newline='') as csvfile:
    fieldnames = ['post_id', 'date', 'title', 'author', 'sentiment_score', 'sentiment_magnitude', 'link', 'matched_tags', 'matched_entities']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    csvRow = {}
    for x in data:
        csvRow['post_id'] = x['id']
        csvRow['date'] = x['date']
        csvRow['title'] = x['title_text']
        csvRow['author'] = x['author']
        csvRow['sentiment_score'] = x['analysis']['sentiment_score']
        csvRow['sentiment_magnitude'] = x['analysis']['sentiment_magnitude']
        csvRow['link'] = x['link']

        # I decided to print out the list for tags directly due to how excel
        # treats them as numbers, and does some weird formatting on them
        csvRow['matched_tags'] = x['filtering']['matched_tags']
        csvRow['matched_entities'] = ','.join(x['filtering']['matched_entities'])
        writer.writerow(csvRow)
