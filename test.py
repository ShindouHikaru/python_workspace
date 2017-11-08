def test():
    # new code hiakru added : rename ------------------------
    # sample: GameCenter-release-android-1-2.0.0-2.apk
    src_apk_name = "GameCenter-release-android-dashen-1-2.1.0.apk"
    target_channel = "android-dashen-6"

    mark = "android-dashen-"
    target_start = src_apk_name.find(mark)
    assert(target_start != -1)
    target_end = target_start + len(mark)
    final_name = src_apk_name[:target_start] + target_channel + src_apk_name[target_end+1:]
    print(final_name)
    # target_apk = output_dir + final_name + src_apk_extension  
    # print(target_apk)

if __name__ == '__main__':
    test()
    # print("abc")
