import re
from ..swf.swf import Swf, GetElementId
from ..worker.variables import CORE_VERSION
from ..worker.gameswf import GetGameFileClass
from ..worker.brawlhalla import BRAWLHALLA_VERSION
from ..ffdec.classes import PlaceObject2Tag, DefineEditTextTag, CSMTextSettingsTag, MATRIX

TEMPLATE = """
[
xmin -40
ymin -40
xmax {xmax}
ymax {ymax}
readonly 1
noselect 1
html 1
useoutlines 1
font 2
height 260
color #ff{color1}
align {align}
leftmargin 0
rightmargin 0
indent 0
leading 40
]<p align="{align}"><font face="Eras Demi ITC" size="{fontSize}" color="#{color2}" letterSpacing="0.00" kerning="1">{text}</font></p>
""".strip()

UI_SCREEN_SOCIAL_HUB_MOD_V1_ID = "init_ScreenSocialHubV1"
BH_VERSION_TEXT = f"Brawlhalla: {BRAWLHALLA_VERSION}"


def _addText(swf: Swf, content: str, xmax, ymax, align="right", fontSize=13, color="#f7f8f9"):
    textId = swf.getNextCharacterId()
    text = DefineEditTextTag(swf._swf)
    text.setFormattedText(None,
                          TEMPLATE.format(text=content, xmax=xmax, ymax=ymax, color1=color.strip("#"), align=align,
                                          fontSize=fontSize, color2=color.strip("#")),
                          None)
    swf.addElement(text, textId)

    CSM = CSMTextSettingsTag(swf._swf)
    CSM.textID = GetElementId(text)
    CSM.useFlashType = 1
    CSM.gridFit = 1 if align == "left" else 2
    CSM.setModified(True)
    swf.addElement(CSM)

    return textId


def _updateTextContent(textElem: DefineEditTextTag, newContent: str):
    newText = re.sub(r"(<font .+>).+(<\/font>)",
                     r"\1{}\2".format(newContent),
                     str(textElem.initialText))
    if newText != textElem.initialText:
        textElem.initialText = newText
        textElem.setModified(True)


def _addPlaceObjectTag(swf: Swf, sprite, setCharacterId, depth, name, index,
                       translateX=0, translateY=0, scaleX=None, scaleY=None):
    spriteMatrix = MATRIX(None)
    spriteMatrix.translateX = translateX
    spriteMatrix.translateY = translateY
    if scaleX is not None and scaleY is not None:
        spriteMatrix.hasScale = True
        spriteMatrix.scaleX = scaleX
        spriteMatrix.scaleY = scaleY

    spritePlace = PlaceObject2Tag(swf._swf)
    spritePlace.setCharacterId(setCharacterId)
    spritePlace.depth = depth
    spritePlace.placeFlagHasName = True
    spritePlace.name = name
    spritePlace.placeFlagHasMatrix = True
    spritePlace.matrix = spriteMatrix
    spritePlace.setModified(True)

    sprite.addTag(index, spritePlace)
    sprite.setModified(True)


def UninstallUIScreenSocialHubV1():
    pass



def InstallUIScreenSocialHubV1():

    print("Installing ModLoader...")





def InstallBaseMod(firstText=None):

    InstallUIScreenSocialHubV1()
