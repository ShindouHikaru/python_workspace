import random;
KEYS = ["C", "D", "E", "F", "G", "A", "B"];
# PITCH_NAMES = []
KEY_PITCH = {
    "C":["C", "D", "E", "F", "G", "A", "B"],
    "G":["G", "A", "B", "C", "D", "E", "#F"],       # #F
    "D":["D", "E", "#F", "G", "A", "B", "#C"],      # #F #C
    "A":["A", "B", "#C", "D", "E", "#F", "#G"],     # #F #C #G
    "E":["E", "#F", "#G", "A", "B", "#C", "#D"],    # #F #C #G #D
    "B":["B", "#C", "#D", "E", "#F", "#G", "#A"],   # #F #C #G #D #A
    "#F":["#F", "#G", "#A", "B", "#C", "#D", "#E"], # #F #C #G #D #A #E
    # 这里是下行四度，因为是五度圈逆着走，从降号开始
    "F":["F", "G", "A", "bB", "C", "D", "E"],       # bB
    "bB":["bB", "C", "D", "bE", "F", "G", "A"],     # bB bE
    "bE":["bE", "F", "G", "bA", "bB", "C", "D"],    # bB bE bA
    "bA":["bA", "bB", "C", "bD", "bE", "F", "G"],   # bB bE bA bD
    "bD":["bD", "bE", "F", "bG", "bA", "bB", "C"],  # bB bE bA bD bG
    "bG":["bG", "bA", "bB", "bC", "bD", "bE", "F"], # bB bE bA bD bG bC

}

SYLLABLE = [1, 2, 3, 4, 5, 6, 7];

# let fishCount = CommonTools.queryInterface(GameStage).fishLayer.m_vcSprite.length;
# let tweenCount = egret.Tween._tweens.length;
# console.log("fuck fish count " + fishCount +  " tween count " + tweenCount + " ratio " + tweenCount/fishCount + " diff " + (tweenCount - fishCount)); 

def test(test_type, times):
    key_index = random.randint(0, len(KEYS) - 1);
    if test_type != 1:
        key_index = 6;
    sy_index = random.randint(0, len(SYLLABLE) - 1);
    if key_index == 0 or sy_index == 0: # filtet C F and do
        # test(test_type);
        return False;
        # pass

    sy = SYLLABLE[sy_index];
    key = KEYS[key_index];
    input_tip = "key: " + key + "\n"
    pitches = KEY_PITCH.get(key);
    right_answer = ' '.join(pitches);
    if test_type != 1 and times > 0:
        key = ""

    if test_type == 2:
        input_tip = "key: " + key + " " + str(sy) + "\n"
        right_answer = pitches[sy - 1];
    elif test_type == 3:
        input_tip = "key: " + key + " " + pitches[sy_index] + "\n"
        right_answer = sy;

    input_answer = input(input_tip).upper().strip();
    input_answer = input_answer.replace("BB", "bB");
    if(input_answer == str(right_answer)):
        # print("CORRECT!");
        # print(input_answer);
        pass
    else:
        print("error answer: " + input_answer);
        print("right answer: " + str(right_answer));

    return True;
    # test(test_type, False); 

if __name__ == '__main__':
    i = 0
    while True:
        if test(2, i):
            i += 1;















