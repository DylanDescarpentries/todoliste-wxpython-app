import json
import wx

class Tache:
    def __init__(self, id, nom_tache, complete=False):
        self.id = id
        self.nom_tache = nom_tache
        self.complete = complete
    
    def __str__(self):
        etat = "terminee" if self.complete else "En cours"
        return f"la tâche {self.id} : {self.nom_tache} statut : ({etat})"
    

class ModifierTacheDialog(wx.Dialog):
    def __init__(self, parent, title, tache):
        super(ModifierTacheDialog, self).__init__(parent, title=title, size=(300, 200))

        self.tache = tache

        self.InitUI()
        self.Centre()
        self.ShowModal()
        self.Destroy()

    def InitUI(self):
        panel = wx.Panel(self)

        sizer = wx.GridBagSizer(5, 5)

        label_nom = wx.StaticText(panel, label="Nom de la tâche:")
        sizer.Add(label_nom, pos=(0, 0), flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        self.nom_input = wx.TextCtrl(panel, value=self.tache.nom_tache)
        sizer.Add(self.nom_input, pos=(0, 1), span=(1, 3), flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)

        label_etat = wx.StaticText(panel, label="État de la tâche:")
        sizer.Add(label_etat, pos=(1, 0), flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        etats = ['En cours', 'Terminée']
        self.etat_input = wx.Choice(panel, choices=etats)
        self.etat_input.SetSelection(0 if not self.tache.complete else 1)
        sizer.Add(self.etat_input, pos=(1, 1), span=(1, 3), flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM, border=10)

        btn_ok = wx.Button(panel, label='OK', size=(70, 30))
        btn_annuler = wx.Button(panel, label='Annuler', size=(70, 30))

        sizer.Add(btn_ok, pos=(2, 1), flag=wx.LEFT, border=10)
        sizer.Add(btn_annuler, pos=(2, 2), flag=wx.LEFT, border=5)

        btn_ok.Bind(wx.EVT_BUTTON, self.OnOK)
        btn_annuler.Bind(wx.EVT_BUTTON, self.OnAnnuler)

        panel.SetSizerAndFit(sizer)

    def OnOK(self, event):
        self.tache.nom_tache = self.nom_input.GetValue()
        self.tache.complete = (self.etat_input.GetSelection() == 1)
        self.EndModal(wx.ID_OK)

    def OnAnnuler(self, event):
        self.EndModal(wx.ID_CANCEL)