from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from PIL import Image, ImageStat
import numpy as np
import matplotlib.pyplot as plt


Builder.load_string("""
<MyWidget>:
    id: my_widget
    
    GridLayout:
        cols: 2
        
        GridLayout:
            cols: 1
            FileChooserListView:
                id: filechooser
                on_selection: my_widget.selected(filechooser.selection)
                
            Image:
                id: image_hist
                source: ""

            GridLayout:
                cols: 5
                size_hint_y: None
                height: 50
                
                Button:
                    text:"R"
                    on_press: root.btn_R()
                Button:
                    text:"G"
                    on_press: root.btn_G()
                Button:
                    text:"B"
                    on_press: root.btn_B()
                Button:
                    text:"RGB"
                    on_press: root.btn_RGB()
                Button:
                    text:"Gray"
                    on_press: root.btn_gray()

        GridLayout:
            cols: 1
            Image:
                id: image
                source: ""
        
            Image:
                id: image_gray
                source: ""            
""")


class MyWidget(BoxLayout):
    
    def selected(self, filename):
        try:
            # imaginea originala
            self.ids.image.source = filename[0]
            
            # imaginea alb negru
            img = Image.open(filename[0])
            img_stat = ImageStat.Stat(img)
            # img_stat.sum gives us a sum of all pixels in list view = [R, G, B]. For grayscale image all elements of list are equal.
            if sum(img_stat.sum)/3 != img_stat.sum[0]: # verific daca imaginea este color
                img_gray = Image.open(filename[0]).convert('L')
                img_gray.save('./gray_im.jpg')
                self.ids.image_gray.source = './gray_im.jpg'
                self.ids.image_gray.reload()
            else:
                img_gray = Image.open(filename[0]).convert('L')
                self.ids.image_gray.source = './eroare-alb-negru.jpg'
                self.ids.image_gray.reload()

            # histograma canale RGB
            global h_R, h_G, h_B, h_gray
            R, G, B = img.split()
            h_R = np.zeros(256)
            h_G = np.zeros(256)
            h_B = np.zeros(256)
            h_gray = np.zeros(256)
            for i, value in enumerate(R.histogram()):
                h_R[i] = value
            for i, value in enumerate(G.histogram()):
                h_G[i] = value
            for i, value in enumerate(B.histogram()):
                h_B[i] = value
            for i, value in enumerate(img_gray.histogram()):
                h_gray[i] = value
            
        except:
            pass
    
    def btn_R(self):
        try:
            plt.plot(h_R, 'r')
            plt.savefig('./hist_RGB.jpg')
            plt.clf()
            self.ids.image_hist.source = './hist_RGB.jpg'
            self.ids.image_hist.reload()
        except:
            print("Nu ati incarcat o imagine!")
    def btn_G(self):
        try:
            plt.plot(h_G, 'g')
            plt.savefig('./hist_RGB.jpg')
            plt.clf()
            self.ids.image_hist.source = './hist_RGB.jpg'
            self.ids.image_hist.reload()
        except:
            print("Nu ati incarcat o imagine!")
    def btn_B(self):
        try:
            plt.plot(h_B, 'b')
            plt.savefig('./hist_RGB.jpg')
            plt.clf()
            self.ids.image_hist.source = './hist_RGB.jpg'
            self.ids.image_hist.reload()
        except:
            print("Nu ati incarcat o imagine!")
    def btn_RGB(self):
        try:
            plt.plot(h_R, 'r')
            plt.plot(h_G, 'g')
            plt.plot(h_B, 'b')
            plt.savefig('./hist_RGB.jpg')
            plt.clf()
            self.ids.image_hist.source = './hist_RGB.jpg'
            self.ids.image_hist.reload()
        except:
            print("Nu ati incarcat o imagine!")
    def btn_gray(self):
        try:
            plt.plot(h_gray)   
            plt.savefig('./hist_RGB.jpg')
            plt.clf()
            self.ids.image_hist.source = './hist_RGB.jpg'
            self.ids.image_hist.reload()
        except:
            print("Nu ati incarcat o imagine!")
        
class MyApp(App):
    def build(self):
        return MyWidget()


if __name__ == '__main__':
    MyApp().run()