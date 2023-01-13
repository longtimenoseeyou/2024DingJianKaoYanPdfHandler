import fitz
import re
import os
import shutil
import img2pdf
import tkinter as tk
from tkinter import filedialog


class PdfHandler(object):
    def pdf_to_img(self, pdf_path, img_path):
        os.makedirs(img_path)
        checkIM = r"/Subtype(?= */Image)"
        doc = fitz.open(pdf_path)
        imgcount = 0
        lenXREF = doc.xref_length()
        for i in range(lenXREF):
            text = doc.xref_object(i)
            isImage = re.search(checkIM, text)
            if not isImage:
                continue
            imgcount += 1
            pix = fitz.Pixmap(doc, i)
            if imgcount < 10:
                save_imgcount = '00' + str(imgcount)
            elif imgcount < 100:
                save_imgcount = '0' + str(imgcount)
            else:
                save_imgcount = str(imgcount)
            img_name = img_path + save_imgcount + '.png'
            pix.save(img_name)
            if imgcount == len(doc):
                break

    def img_to_pdf(self, img_path, pdf_path):
        with open(pdf_path, 'wb') as f:
            imgs = []
            for i in os.listdir(img_path):
                if not i.endswith('.png'):
                    continue
                path = os.path.join(img_path, i)
                imgs.append(path)
            f.write(img2pdf.convert(imgs))
        shutil.rmtree(img_path)


class PdfDeleteWatermark(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("2024顶尖考研PDF书籍取水印By RongRongStudioV1.0")
        self.root.geometry("700x300")
        self.select_texts = tk.StringVar()
        self.delete_water_mark_files = []
        self.del_flag = tk.StringVar()

    def select_files(self):
        selected_files_path = filedialog.askopenfilenames()
        err = 0
        for i in selected_files_path:
            if i[-4:] != ".pdf":
                err += 1
        if not err:
            self.delete_water_mark_files = selected_files_path
            files_length = len(self.delete_water_mark_files)
            self.select_texts.set(f'您选择了{files_length}个PDF文件')

    def start_del(self):
        pdf_del = PdfHandler()
        for i in self.delete_water_mark_files:
            cur_path = os.path.dirname(i)
            pdf_del.pdf_to_img(i, cur_path + '/del/')
            pdf_del.img_to_pdf(cur_path + '/del/', i[:-4] + '_delByRongRongStudio.pdf')
        self.del_flag.set('去除水印已完成')

    def del_ui(self):
        tk.Label(self.root, text="本程序由RongRongStudio提供，仅用于学习用途，请勿用于商业用途").grid(column=0, row=0)
        tk.Label(self.root, text="若有侵权请联系rongrongstudio@qq.com").grid(column=0, row=1)
        tk.Label(self.root, text="删除水印后的PDF文件保存在原始文件位置，文件名为xxx_delByRongRongStudio.pdf").grid(
            column=0, row=2)
        tk.Label(self.root, text="请选择带有水印的PDF网盘原始文件").grid(column=0, row=3)
        tk.Entry(self.root, textvariable=self.select_texts).grid(column=1, row=3)
        tk.Button(self.root, text="选择单个或多个文件", command=self.select_files).grid(row=3, column=2)
        tk.Label(self.root, text="去除水印耗时较长，请耐心等待").grid(row=4, column=0)
        tk.Button(self.root, text="开始去除水印", command=self.start_del).grid(row=5, column=0)
        tk.Label(self.root, textvariable=self.del_flag).grid(row=6, column=0)
        tk.Label(self.root, text="去除水印完成后请务必核对PDF总页数和内容").grid(row=7, column=0)
        tk.Label(self.root, text="关注微信公众号:ArtistcProgramming获取最新支持").grid(row=8, column=0)

    def run(self):
        self.del_ui()
        self.root.mainloop()


if __name__ == '__main__':
    PdfDeleteWatermark().run()
