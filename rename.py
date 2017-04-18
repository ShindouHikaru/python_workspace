import os
import sys

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("please input dir, before, after")
        # return
    else:
        d = sys.argv[1];
        before = sys.argv[2];
        after = sys.argv[3];
        for file in os.listdir(d):
            file_name = str(file)
            new_name = file_name.replace(before, after)
            v1 = d + "/" + file_name
            v2 = d + "/" + new_name
            print(v1 + " -> " + v2)
            os.rename(v1, v2);
