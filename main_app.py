from multiprocessing import dummy
from kivy.core.window import Window
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivymd.app import MDApp

import random
import time
random.seed(time.process_time())


#Designate .kv design file
Builder.load_file('attentionapp.kv')

class AttentionGame(FloatLayout):
    clickCount = NumericProperty(0)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    

class StartScreen(Screen):
    def on_enter(self):
        brainLabel = Label(text="Find the " + attentionApp.brainColor + " brain!", pos=(15,100))
        self.add_widget(brainLabel)
    pass
     
class GameScreen(Screen):

    def on_enter(self):
        attentionApp.start = time.time()
        for x in range(6):
            dummy = DummyBrain()
            self.add_widget(dummy)

    def on_touch_up(self, touch):
        attentionApp.clickCount += 1
    pass

class EndScreen(Screen):

    def on_enter(self):
        timeElapsed = Label(text="Time elapsed: " + attentionApp.timeDiff + " seconds") 
        timeElapsed.pos = (20, 150)
        self.add_widget(timeElapsed)
        numOfClicks = Label(text = "Number of clicks: " + str(attentionApp.clickCount + 1))
        attentionApp.totalClicks += attentionApp.clickCount + 1
        numOfClicks.pos = (20, 100)
        self.add_widget(numOfClicks)
        accuracy = Label(text = "Accuracy: " + str(attentionApp.rounds / attentionApp.totalClicks) + " (" + str(attentionApp.rounds) + " correct clicks / " + str(attentionApp.totalClicks) + " total clicks)")
        accuracy.pos = (20, 50)
        attentionApp.accuracy = attentionApp.rounds / attentionApp.totalClicks
        self.add_widget(accuracy)

    def restart(self):
        attentionApp.restart(self)
    pass



class Brain(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(Brain, self).__init__(**kwargs)
        self.source = attentionApp.brainColor + "brain.png"
        
        random_x = random.uniform(0, Window.width)
        random_y = random.uniform(0, Window.height)

        self.pos = (random_x, random_y)

    def on_press(self):
        self.source = 'Brain.png'
        attentionApp.end = time.time()
        attentionApp.timeDiff = str(attentionApp.end - attentionApp.start)
        
class DummyBrain(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(DummyBrain, self).__init__(**kwargs)
        otherColor = random.choice(attentionApp.colorOptions)
        self.source = otherColor + "brain.png"
        
        random_x = random.uniform(0, Window.width)
        random_y = random.uniform(0, Window.height)

        self.pos = (random_x, random_y)
        self.size_hint = .09, .09

class attentionApp(MDApp, App):
    start = 0
    end = 0 
    rounds = 1
    timeDiff = ""
    clickCount = 0
    totalClicks = 0
    colorOptions = ["yellow", "blue", "green"]
    brainColor = random.choice(colorOptions)
    colorOptions.remove(brainColor)
    accuracy = 0
    global sm
    sm = ScreenManager()

    def restart(self, v):
        attentionApp.clickCount = 0
        attentionApp.start = 0
        attentionApp.end = 0
        attentionApp.timeDiff = "" 
        attentionApp.colorOptions = ["yellow", "blue", "green"]
        attentionApp.brainColor = random.choice(attentionApp.colorOptions)
        attentionApp.colorOptions.remove(attentionApp.brainColor)
        attentionApp.rounds += 1
        sm.clear_widgets()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(EndScreen(name='end'))
        sm.current = 'start'

    def build(self):
    
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(EndScreen(name='end'))        
        return sm
    
if __name__ == '__main__':
    attentionApp = attentionApp()
    attentionApp.run()





