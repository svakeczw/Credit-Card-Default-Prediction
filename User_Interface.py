from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
import pandas as pd
import tensorflow as tf
from os import environ
environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 40)
pd.set_option('display.width', 1000)


class Main:

    def __init__(self):
        self.sfname = None
        self.modelname = None
        self.exportPath = None
        self.data = None
        self.raw_data = None
        self.root = Tk()
        self.processed = False

        self.root.title('Default Payment Prediction')

        self.root.geometry('500x300+570+200')

        label1 = Label(self.root, text='Select file:')
        label2 = Label(self.root, text='Select model:')

        self.text1 = Entry(self.root, bg='white', width=30)
        self.text2 = Entry(self.root, bg='white', width=30)
        self.text3 = Entry(self.root, bg='white', width=30)

        button1 = Button(self.root, text='Browse', width=8, command=self.selectExcelfile)
        # button2 = Button(self.root, text='Train Process', width=10, command=self.doProcess_train)
        button3 = Button(self.root, text='Exit', width=8, command=self.closeThisWindow)
        button4 = Button(self.root, text='Predict & Export CSV', width=15, command=self.load_model_predict)
        button5 = Button(self.root, text='Process Data', width=10, command=self.doProcess_predict)
        button6 = Button(self.root, text='Browse', width=8, command=self.selectModel)

        label1.pack()
        label2.pack()

        self.text1.pack()
        self.text2.pack()

        button1.pack()
        # button2.pack()
        button3.pack()
        button4.pack()
        button5.pack()
        button6.pack()

        label1.place(x=10, y=30)
        label2.place(x=10, y=59)

        self.text1.place(x=100, y=30)
        self.text2.place(x=100, y=57)

        button1.place(x=390, y=33)
        # button2.place(x=160, y=80)
        button3.place(x=210, y=200)
        button4.place(x=260, y=120)
        button5.place(x=120, y=120)
        button6.place(x=390, y=59)

        self.root.mainloop()

    def selectExcelfile(self):
        self.sfname = filedialog.askopenfilename(title='Select Csv File', filetypes=[('Excel', '*.csv'), ('All Files', '*')])
        self.text1.insert(INSERT, self.sfname)

    def selectModel(self):
        self.modelname = filedialog.askdirectory()
        self.text2.insert(INSERT, self.modelname)

    def closeThisWindow(self):
        self.root.destroy()

    def doProcess_train(self):
        if self.sfname == None:
            tkinter.messagebox.showinfo('Alert', 'Please select CSV file')
        self.data = pd.read_csv(self.sfname)
        self.data.drop(labels='ID', axis=1)
        self.data['LIMIT_BAL'] = self.process_norm(self.data['LIMIT_BAL'])

        for i in range(11, 23):
            self.data.iloc[:, i] = self.process_norm(self.data.iloc[:, i])

        self.data = self.process_age(self.data)
        self.data = self.onehot_pay(self.data['PAY_0'], self.data, 1)
        self.data = self.onehot_pay(self.data['PAY_2'], self.data, 2)
        self.data = self.onehot_pay(self.data['PAY_3'], self.data, 3)
        self.data = self.onehot_pay(self.data['PAY_4'], self.data, 4)
        self.data = self.onehot_pay(self.data['PAY_5'], self.data, 5)
        self.data = self.onehot_pay(self.data['PAY_6'], self.data, 6)
        self.data = self.data.drop(labels=['PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6'], axis=1)

        self.data = self.onehot_other(self.data)

        true_label = self.data['default.payment.next.month']
        self.data = self.data.drop(labels='default.payment.next.month', axis=1)
        self.data.insert(96, 'default.payment.next.month', true_label)
        # print(self.data.head((10)))
        # print(len(self.data))
        # print(self.data.columns)
        tkinter.messagebox.showinfo('Done', 'Finished')
        return self.data

    def doProcess_predict(self):

        if self.sfname == None:
            tkinter.messagebox.showinfo('Alert', 'Please select CSV file')
        self.data = pd.read_csv(self.sfname)
        self.raw_data = self.data
        self.data = self.data.drop(labels='ID', axis=1)
        self.data['LIMIT_BAL'] = self.process_norm(self.data['LIMIT_BAL'])

        for i in range(11, 23):
            self.data.iloc[:, i] = self.process_norm(self.data.iloc[:, i])

        self.data = self.process_age(self.data)

        self.data = self.onehot_pay(self.data['PAY_0'], self.data, 1)
        self.data = self.onehot_pay(self.data['PAY_2'], self.data, 2)
        self.data = self.onehot_pay(self.data['PAY_3'], self.data, 3)
        self.data = self.onehot_pay(self.data['PAY_4'], self.data, 4)
        self.data = self.onehot_pay(self.data['PAY_5'], self.data, 5)
        self.data = self.onehot_pay(self.data['PAY_6'], self.data, 6)
        self.data = self.data.drop(labels=['PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6'], axis=1)

        self.data = self.onehot_other(self.data)

        # true_label = self.data['default.payment.next.month']
        # self.data = self.data.drop(labels='default.payment.next.month', axis=1)
        # self.data.insert(96, 'default.payment.next.month', true_label)
        # print(self.data.head((10)))
        # print(len(self.data))
        # print(self.data.columns)
        tkinter.messagebox.showinfo('Done', 'Success!')

        self.processed = True
        return self.data
        # tkinter.messagebox.showinfo('提示', '处理Excel文件的示例程序。')

    @staticmethod
    def process_norm(data):
        data = (data - data.mean()) / (data.max() - data.min())
        return data

    @staticmethod
    def process_age(data):
        # data = (data - data.mean()) / (data.max() - data.min())
        data.loc[((data['AGE'] > 20) & (data['AGE'] < 30)), 'AgeBin'] = 1
        data.loc[((data['AGE'] >= 30) & (data['AGE'] < 40)), 'AgeBin'] = 2
        data.loc[((data['AGE'] >= 40) & (data['AGE'] < 50)), 'AgeBin'] = 3
        data.loc[((data['AGE'] >= 50) & (data['AGE'] < 60)), 'AgeBin'] = 4
        data.loc[((data['AGE'] >= 60) & (data['AGE'] < 70)), 'AgeBin'] = 5
        data.loc[(data['AGE'] >= 70) & (data['AGE']<80), 'AgeBin'] = 6
        data['AgeBin'] = pd.cut(data['AGE'], 6, labels=[1, 2, 3, 4, 5, 6])
        data = data.drop(labels='AGE', axis=1)
        return data

    @staticmethod
    def onehot_other(data):
        data = data.join(pd.get_dummies(data.SEX, prefix='Sex'))
        data = data.join(pd.get_dummies(data.EDUCATION, prefix='Education'))
        data = data.join(pd.get_dummies(data.MARRIAGE, prefix='Marriage'))
        data = data.join(pd.get_dummies(data.AgeBin, prefix='AgeBin'))
        data = data.drop(labels=['SEX', 'EDUCATION', 'MARRIAGE', 'AgeBin'], axis=1)
        # true_label = data['default.payment.next.month']
        # data = data.drop(labels='default.payment.next.month', axis=1)
        # data.insert(96, 'default.payment.next.month', true_label)
        return data

    @staticmethod
    def onehot_pay(data_col, data, i):
        data = data.join(pd.get_dummies(data_col, prefix='PAY_' + str(i)))
        return data

    def load_model_predict(self):
        if self.processed is False:
            tkinter.messagebox.showinfo('Alert', 'Please click process before predict')
        else:
            x_data = self.data
            # y_data = (self.data.iloc[:, -1].values)
            my_model = tf.keras.models.load_model(filepath=self.modelname)
            # predictions = models.predict(x_data)
            # predictions = tf.keras.Model.predict_on_batch(self=my_model, x=x_data)
            predictions = my_model.predict(x_data)
            for i in range(predictions.shape[0]):
                if predictions[i] > 0.5:  # Threshold value
                    predictions[i] = 1
                else:
                    predictions[i] = 0
            predictions = pd.DataFrame(predictions)
            self.raw_data['Prediction'] = predictions
            self.exportPath = filedialog.askdirectory()
            self.raw_data.to_csv(path_or_buf=self.exportPath + '/predictions.csv')
            tkinter.messagebox.showinfo('Done', 'Export Success!')


if __name__ == "__main__":
    main_app = Main()
