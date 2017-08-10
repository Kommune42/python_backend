import os
import json

updates_buffer = {}
buffer_dir = "./src/server/hard_buffer/"
buffer_filenames = [filename for filename in os.listdir(buffer_dir) if os.path.isfile(buffer_dir + filename) and filename.endswith(".log")]
buffer_size = 1000


# def get_highest_file_buffered_update_id():
#     highet_update_id = 0
#     for filename in buffer_filenames:
#         highest_index_in_file = get_index_by_filename(filename) + buffer_size - 1
#         if highest_index_in_file > highet_update_id:
#             update_id = highest_index_in_file
#     return highet_update_id


def get_by_id(update_id):
    if update_id in updates_buffer.keys():
        return updates_buffer[update_id]
    else:
        for filename in buffer_filenames:
            file_starting_index = int(filename.replace(".log", ""))
            if file_starting_index < update_id and (file_starting_index + buffer_size) > update_id:
                with open(buffer_dir + filename, "r") as buffer_file:
                    return json.load(buffer_file)[str(update_id)]
    raise AttributeError("update_id not found")


def buffer_telegram_update(update):
    global updates_buffer
    global buffer_filenames
#    if update.update_id in updates_buffer:
#        raise IndexError("Update already in buffer")
    updates_buffer[update.update_id] = update.to_dict()
    print "updates_buffer"
    print len(updates_buffer.keys())
    print "update_id"
    print update.update_id
    print

    if len(updates_buffer.keys()) == buffer_size:
        lowest_update_id = min(updates_buffer.keys())
        if update.update_id < lowest_update_id:
            raise IndexError("The update is duplicated in hard buffer")

        new_filename = str(lowest_update_id) + ".log"

        with open(buffer_dir + new_filename, "w") as new_file:
            print type(updates_buffer.keys()[0])
            json.dump(updates_buffer, new_file, indent=4)

        buffer_filenames.append(new_filename)
        updates_buffer = {}
