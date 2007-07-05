import httplib, urllib, os, os.path, webbrowser
import glipper

def info():
   info = {"Name": "Nopaste", 
      "Description": "Paste the entry of your clipboard to a No-Paste service",
      "Preferences": True}
   return info

def rafbnet(lang, nick, desc, text):
   conn = httplib.HTTPConnection("rafb.net")
   params = urllib.urlencode({"lang": lang, "nick": nick, 
      "desc": desc, "text": text, "tabs": "no"})
   headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
   conn.request("POST", "/paste/paste.php", params, headers)
   url = conn.getresponse().getheader("location")
   conn.close()
   return url

def activated(menu):
   languageList = ("C89", "C", "C++", "C#", "Java", "Pascal", "Perl", "PHP", 
         "PL/I", "Python", "Ruby", "SQL", "VB", "Plain Text")
   cf = confFile("r")
   url = rafbnet(languageList[cf.getLang()], cf.getNick(), "pasted by glipper", glipper.get_history_item(0))
   webbrowser.open(url)
   cf.close()

def init():
   item = gtk.MenuItem("Nopaste")
   item.connect('activate', activated)
   glipper.add_menu_item(__name__, item)

def on_show_preferences(parent):
   preferences(parent).show()


#config file class:
class confFile:
   def __init__(self, mode):
      self.mode = mode

      dir = os.environ["HOME"] + "/.glipper/plugins"
      if (mode == "r") and (not os.path.exists(dir + "/nopaste.conf")):
         self.lang = 13
         self.nick = "Glipper user"
         return
      if not os.path.exists(dir):
         os.makedirs(dir)
      self.file = open(dir + "/nopaste.conf", mode)

      if mode == "r":
         self.lang = int(self.file.readline()[:-1])
         self.nick = self.file.readline()[:-1]

   def setLang(self, lang):
      self.lang = lang
   def getLang(self):
      return self.lang
   def setNick(self, nick):
      self.nick = nick
   def getNick(self):
      return self.nick
   def close(self):
      if not 'file' in dir(self):
         return
      try:
         if self.mode == "w":
            self.file.write(str(self.lang) + "\n")
            self.file.write(self.nick + "\n")
      finally:
         self.file.close()

#preferences dialog:
import gtk
import gtk.glade

class preferences:
   def __init__(self, parent):
      gladeFile = gtk.glade.XML(os.path.dirname(__file__) + "/nopaste.glade")
      self.prefWind = gladeFile.get_widget("preferences")
      self.prefWind.set_transient_for(parent)
      self.nickEntry = gladeFile.get_widget("nickEntry")
      self.langBox = gladeFile.get_widget("langBox")
      self.prefWind.connect('response', self.on_prefWind_response)

      #read configurations
      f = confFile("r")
      self.nickEntry.set_text(f.getNick())
      self.langBox.set_active(f.getLang())
      f.close()

   def destroy(self, window):
      window.destroy()

   def show(self):
      self.prefWind.show_all()

   #EVENTS:
   def on_prefWind_response(self, widget, response):
      if response == gtk.RESPONSE_DELETE_EVENT or response == gtk.RESPONSE_CLOSE:
         f = confFile("w")
         f.setNick(self.nickEntry.get_text())
         f.setLang(self.langBox.get_active())
         f.close()
         widget.destroy()   
      
