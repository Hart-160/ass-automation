---
--- Generated by EmmyLua(https://github.com/EmmyLua)
--- Created by Jeunette.
--- DateTime: 2020/10/14 10:43
---

local tr = aegisub.gettext

script_name = tr"[D4DJ] 打字机特效"
script_description = tr"\\t+ based typewriter effect automation"
script_author = "Jeunette"
script_version = "1.1"

--- GUI

dialog_config=
{
    [1]={class="label",x=0,y=1,label="字间间隔 (ms):"},
    [2]={class="edit",name="Single Character Duration (ms):",x=1,y=1,width=1,height=1,items={},value="80"},
    [3]={class="label",x=0,y=2,label="渐变时长 (ms):"},
    [4]={class="edit",name="Animation Duration (ms):",x=1,y=2,width=1,height=1,items={},value="10"},

    [5]={class="label",x=0,y=3,label=""},
    [6]={class="label",x=0,y=4,width=1,height=1,label="空格间隔 :"},
    [7]={class="dropdown",name="Count Space :",x=1,y=4,width=1,height=1,items={},value=""},
    [8]={class="label",x=0,y=5,width=1,height=1,label="是否保留特效 :"},
    [9]={class="dropdown",name="Bypass Effects :",x=1,y=5,width=1,height=1,items={},value=""},
    [10]={class="label",x=0,y=6,width=1,height=1,label="是否保留换行符\\N :"},
    [11]={class="dropdown",name="Bypass e.g \\N :",x=1,y=6,width=1,height=1,items={},value=""},
    [12]={class="label",x=0,y=7,width=1,height=1,label="换行间隔 :"},
    [13]={class="dropdown",name="Count e.g \\N :",x=1,y=7,width=1,height=1,items={},value=""},
    [14]={class="label",x=0,y=8,label="换行等待时长 ："},
    [15]={class="edit",name="e.g \\N Duration (ms):",x=1,y=8,width=1,height=1,items={},value="300"},

}

countSpaceIdx = 7;
bypassEffectIdx = 9;
bypassNewLineIdx = 11;
countNewLineIdx = 13;

function setGUI()

    dialog_config[ countSpaceIdx ].items={};
    table.insert(dialog_config[ countSpaceIdx ].items,"Yes");
    table.insert(dialog_config[ countSpaceIdx ].items,"No");
    dialog_config[ countSpaceIdx ].value = "Yes";

    dialog_config[ bypassEffectIdx ].items={};
    table.insert(dialog_config[ bypassEffectIdx ].items,"Yes");
    table.insert(dialog_config[ bypassEffectIdx ].items,"No");
    dialog_config[ bypassEffectIdx ].value = "Yes";

    dialog_config[ bypassNewLineIdx ].items={};
    table.insert(dialog_config[ bypassNewLineIdx ].items,"Yes");
    table.insert(dialog_config[ bypassNewLineIdx ].items,"No");
    dialog_config[ bypassNewLineIdx ].value = "Yes";

    dialog_config[ countNewLineIdx ].items={};
    table.insert(dialog_config[ countNewLineIdx ].items,"Yes");
    table.insert(dialog_config[ countNewLineIdx ].items,"No");
    dialog_config[ countNewLineIdx ].value = "Yes";

end

function typewriter(subtitles, selected_lines)
    setGUI()
    buttons,results =aegisub.dialog.display(dialog_config,{"OK","Cancel"});

    if buttons == "OK" then
        local duration = results["Single Character Duration (ms):"]
        local durationAnimation = results["Animation Duration (ms):"]
        local countSpace = results["Count Space :"]
        local bypassEffect = results["Bypass Effects :"]
        local bypassNewLine = results["Bypass e.g \\N :"]
        local countNewLine = results["Count e.g \\N :"]
        local durationNewLine = results["e.g \\N Duration (ms):"]

        for z, i in ipairs(selected_lines) do
            local line = subtitles[i]
            if line.class == "dialogue" then
                local character = {}
                local text = ""
                local bracketBypass = false
                local newlineBypass = false
                local durationLabel = 50
                for currentChar in line.text:gmatch("[%z\1-\127\194-\244][\128-\191]*") do
                    if bypassEffect == "Yes" and currentChar == "{" or bracketBypass then
                        bracketBypass = true
                        character[#character + 1] = currentChar
                        text=text..character[#character]
                        if currentChar == "}" then
                            bracketBypass=false
                        end
                    elseif bypassNewLine == "Yes" and currentChar == "\\" or newlineBypass then
                        character[#character + 1] = currentChar
                        text = text..character[#character]
                        if newlineBypass then
                            newlineBypass = false
                        else
                            newlineBypass = true
                            if countNewLine == "Yes" then
                                durationLabel = durationLabel + tonumber(durationNewLine)
                            end
                        end
                    elseif countSpace == "No" and currentChar == " " or currentChar == "　" then
                        character[#character + 1] = currentChar
                        text = text..character[#character]
                    else
                        character[#character + 1] = "{\\alphaFF\\t("..(durationLabel)..","..(durationLabel+durationAnimation)..",1,\\alpha0}"..currentChar
                        durationLabel = durationLabel + tonumber(duration)
                        text = text..character[#character]
                    end
                end
                line.text = text
                subtitles[i] = line
            end
        end
    end
end

function script_main(subs,sel)
    typewriter(subs,sel)
    aegisub.set_undo_point(script_name)
end

aegisub.register_macro(script_name, script_description, script_main)