import sys  # for sys.argv
import os
import os.path
import re
import shutil

old_dir = "./"
root_dir = "d:/"

def processSong(song_tuple, new_dir):
    """parse song_tuple, cp the song to the new_dir"""
    song_path, song_name = song_tuple
    song_new_path = new_dir+'/'+song_name
    print("Copying {} ------> {}".format(song_path,song_new_path))
    # shutil.copy(song_path, song_new_path)
    print("Done!")


def processNewList(old_PL_path, new_PL_path, song_list):
    """input songlist of tuples, old_PL_path, new_PL_path
       cp playlist to new path, and change each song's relative path in the list"""
    print("Processing new play list file {} -----> {}".format(old_PL_path, new_PL_path))
    if os.path.exists(new_PL_path):
        os.remove(new_PL_path)
    shutil.copy(old_PL_path, new_PL_path)

    new_PL_descriptor = open(new_PL_path, mode='r+')
    PL_lines = new_PL_descriptor.readlines()
    new_PL_content = ""
    old_path, new_path = song_list[0]
    #print(song_list)
    index =1
    for line in PL_lines:
        if index > len(song_list):
            new_PL_content+=line
            continue
        if line==old_path+'\n':
            new_PL_content+=new_path+'\n'
            try:
                old_path, new_path = song_list[index]
                index+=1
            except:
                index+=1
        else:
            new_PL_content+=line
    #print(new_PL_content)
    new_PL_descriptor.seek(0)
    new_PL_descriptor.truncate()
    new_PL_descriptor.write(new_PL_content)
    print("Done!")


def processSongList(song_list_path):
    """input a song list, each element with path
       return a list with tuples (song_with_path, song_name)"""
    result_list=[]
    #song_name_pattern = re.compile(r"/.*?\.(flac)|(m4a)|(mp3)|(ape)")
    song_name_pattern = re.compile(r"/([^/]*?((\.flac)|(\.m4a)|(\.mp3)|(\.ape)))")
    for path in song_list_path:
        song_name = song_name_pattern.search(path).group(1)
        #print(path)
        #print(song_name)
        result_list.append((path,song_name))
    return result_list


def processPlayListFile(file_name):
    """open playlist file, return a list of songs to be copied with relative paths"""
    song_pattern = re.compile(r".+\.((flac)|(m4a)|(mp3)|(ape))")
    result_list = []
    try:
        PL_descriptor = open(file_name, mode='r')
        line_lists = PL_descriptor.readlines()
    finally:
        PL_descriptor.close()
    for line in line_lists:
        search_result = song_pattern.search(line)
        if search_result:
            song_with_path = search_result.group()
            # print(song_with_path)
            result_list.append(song_with_path)
    return result_list


if __name__=="__main__":
    pl_pattern = re.compile(".+\.M3U8")
    root_file_list = os.listdir(old_dir)
    
    for file_name in root_file_list:
        if pl_pattern.match(file_name):
            song_list_path = processPlayListFile(file_name)
            dir_name = file_name[:-5]
            print("PROCESSING {}\n".format(dir_name))
            if os.path.exists(root_dir+'/'+dir_name):
                print("Folder exists!\n")
            else:
                os.mkdir(root_dir+'/'+dir_name)
                print("Created folder {}\n".format(root_dir+'/'+dir_name))

            song_list = processSongList(song_list_path)
            #print(song_list)
            for song_tuple in song_list:
                processSong(song_tuple, root_dir+'/'+dir_name)
            processNewList(old_dir+file_name, root_dir+'/'+dir_name+'/'+file_name, song_list)

