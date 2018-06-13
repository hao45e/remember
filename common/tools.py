# -*-coding:utf-8-*-
from . import final
import time
import base64
import qrcode
from PIL import Image
import datetime
import os


def b64en_today(user_id, tp):
    """
    分享链接:base64编码
    用户id > 今天(2018-06-07) : 类型(1)
    """
    day_time = time.strftime("%F")
    msg = str(user_id) + '>' + day_time + ':' + tp
    msg_base64 = base64.b64encode(msg.encode('utf-8')).decode('utf-8')
    return msg_base64


def b64de_today(share_link):
    """
    分享链接:base64解码
    """
    msg = base64.b64decode(share_link.encode('utf-8')).decode('utf-8')
    share_user_id = msg.split('>')[0]
    share_time = msg.split('>')[1].split(':')[0]
    share_type = msg.split(':')[-1]
    plaintext = {
        'share_user_id': share_user_id,
        'share_time': share_time,
        'share_type': share_type,
    }
    return plaintext


def returnVectorMapAddressCode(friends_list):
    """
    获取省区code及该省好友人数
    """
    address_code_map = {}
    for friend in friends_list:
        new_address = str(friend.new_address).split('-')[0]
        old_address = str(friend.old_address).split('-')[0]
        if new_address != '':
            try:
                address_code = final.FinalMap.VECTOR_MAP_ADDRESS_CODE_MAP[new_address]
                if address_code in address_code_map.keys():
                    address_code_map[address_code] += 1
                else:
                    address_code_map[address_code] = 1
            except KeyError:
                pass
            continue
        elif old_address != '':
            try:
                address_code = final.FinalMap.VECTOR_MAP_ADDRESS_CODE_MAP[old_address]
                if address_code in address_code_map.keys():
                    address_code_map[address_code] += 1
                else:
                    address_code_map[address_code] = 1
            except KeyError:
                pass
            continue
    return address_code_map


def makeQRcodeInURL(url, username, logo_file):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    date = datetime.datetime.now()
    filename = username + '.png'
    upload_url = 'media/user/qrcode/{}/{}/{}/'.format(date.year, date.month, date.day)
    file_url = upload_url + filename
    if not os.path.exists(upload_url):
        os.makedirs(upload_url)

    # 初步生成二维码图像
    qr = qrcode.QRCode(version=5, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=8, border=4)
    qr.add_data(url)
    qr.make(fit=True)

    # 获得Image实例并把颜色模式转换为RGBA
    img = qr.make_image()
    img = img.convert("RGBA")

    # 打开logo文件
    # logo_file = ''
    icon = Image.open(logo_file)

    # 计算logo的尺寸
    img_w, img_h = img.size
    factor = 4
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)

    # 比较并重新设置logo文件的尺寸
    icon_w, icon_h = icon.size
    if icon_w > size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h
    icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)

    # 计算logo的位置，并复制到二维码图像中
    w = int((img_w - icon_w) / 2)
    h = int((img_h - icon_h) / 2)
    icon = icon.convert("RGBA")
    img.paste(icon, (w, h), icon)

    # 保存二维码
    img.save(file_url)

    return file_url
