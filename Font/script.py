import fontforge
import sys
import os




source_path = "D:/University_Work/y2/sem2/AI/code/Project/Font/source"
for file in os.listdir(source_path):
    if file.endswith(".ttf"):
        print(file)
        font = fontforge.open(source_path + "/" +file)
        output_path = "D:/University_Work/y2/sem2/AI/code/Project/Font/output/"
        if not os.path.exists(output_path):
            os.makedirs(output_path)

        # print(font)

        for glyph in font:
            if "." in glyph:
                continue
            if "uni" in glyph:
                if (int(glyph[3:],16)) in range(0xE01, 0xE4F):
                    # char = chr(int(glyph[3:],16))
                    # print(char)
                    save_path = output_path + glyph + "/"
                    print(save_path)
                    if not os.path.exists(save_path):
                        os.makedirs(save_path)
                    # filename = save_path + file[:-4] + ".png"
                    filename = save_path + file[:-4] + ".png"
                    print(filename)
                    font[glyph].export(filename,500)
    else:
        print("No .ttf file found")






# # change folder name 
# folder_path=r"D:\University_Work\y2\sem2\AI\code\Project\Font\output"
# for folder in os.listdir(folder_path):
#     print(folder)
#     #change folder name from unicode to string
#     os.rename(folder_path+"\\"+folder, folder_path+"\\"+chr(int(folder[3:], 16)))